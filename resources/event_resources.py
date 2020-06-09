#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from builtins import super
import falcon
from falcon.media.validators import jsonschema
from falcon_pagination.offset_pagination_hook import OffsetPaginationHook
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

import messages
from db.models import User, GenereEnum, Favour, EventTypeEnum, FavourTypeEnum
from hooks import requires_auth
from resources.base_resources import DAMCoreResource
from resources.schemas import SchemaRegisterUser, SchemaUpdateFavour


mylogger = logging.getLogger(__name__)


#@falcon.before(OffsetPaginationHook())
@falcon.before(requires_auth)
class ResourceGetEvents(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceGetEvents, self).on_get(req, resp, *args, **kwargs)

        #offset = req.context['pagination']['offset']
        #limit = req.context['pagination']['limit']

        #print("-----")
        #print(offset)
        #print(limit)
        #print("-----")

        request_favour_userid = req.get_param("user_id", False)
        current_user = req.context["auth_user"]
        request_category = req.get_param("category", False)
        request_type = req.get_param("type", False)
        response_events = list()




        #Agafem tots els valors del usuari
        if request_favour_userid is not None:
            aux_events = self.db_session.query(Favour).filter(Favour.owner_id == request_favour_userid)
        else:
            aux_events = self.db_session.query(Favour).filter(Favour.owner_id != current_user.id)

        if request_category is not None:
            aux_events = \
            aux_events.filter(
            Favour.category == EventTypeEnum(request_category))

        if request_type is not None:
            if (request_type not in [i.value for i in FavourTypeEnum.__members__.values()]):
                raise falcon.HTTPInvalidParam(messages.parameters_invalid, "type")
            else:
                aux_events = aux_events.filter(Favour.type == FavourTypeEnum(request_type))

        # For pagination
        #aux_events = aux_events.offset(offset).limit(limit)

        if aux_events is not None:
            for current_event in aux_events:
                response_events.append(current_event.json_model)

        print(len(response_events))

        resp.media = response_events
        resp.status = falcon.HTTP_200


@falcon.before(requires_auth)
class UpdateFavour(DAMCoreResource):
    @jsonschema.validate(SchemaUpdateFavour)
    def on_post(self, req, resp, *args, **kwargs):
        super(UpdateFavour, self).on_post(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]
        #Assegurar que el id del favor correspon al id del usuari

        print(kwargs)
        if "id" in kwargs:
            try:
                favour = self.db_session.query(Favour).filter(Favour.id == kwargs["id"], Favour.owner_id == current_user.id).one()
                print(req.media)
                if (req.media["name"]) is not None:
                    favour.name = req.media["name"]
                if (req.media["desc"]) is not None:
                    favour.desc = req.media["desc"]
                if (req.media["category"]) is not None:
                    favour.category = req.media["category"]
                if (req.media["amount"]) is not None:
                    favour.amount = req.media["amount"]
                # El username no té sentit modificar-ho:
                # if (req.media["username"]) is not None:
                #    favour.user = req.media["username"]
                self.db_session.add(favour)
                self.db_session.commit()

                resp.status = falcon.HTTP_200

            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.user_not_found) #TODO



@falcon.before(requires_auth)
class DeleteFavour(DAMCoreResource):
    #@jsonschema.validate(SchemaUpdateFavour)
    def on_get(self, req, resp, *args, **kwargs):
        super(DeleteFavour, self).on_get(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]
        print(current_user.id , "CURRENTUSER ID")
        fav = self.db_session.query(Favour).filter(Favour.id == kwargs["id"], Favour.owner_id == current_user.id).delete()
        self.db_session.commit()
        resp.status = falcon.HTTP_200

@falcon.before(requires_auth)
class ResourcePostFavour(DAMCoreResource):
    #@jsonschema.validate(SchemaRegisterUser)
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourcePostFavour, self).on_post(req, resp, *args, **kwargs)

        favour = Favour()
        current_user = req.context["auth_user"]
        try:
            # Que representa la columna user? Per que ho necessiteu?
            favour.user = current_user.username
            favour.name = req.media["name"]
            # Si no es posa en blanc
            favour.desc = req.media["desc"]
            favour.category = req.media["category"]
            favour.amount = req.media["amount"]
            # Primer heu d'obtenir i passar per Android si no us falla
            # favour.longitud = req.media["longitud"]
            # favour.latitud = req.media["latitud"]
            favour.owner_id = current_user.id
            #favour.registered = [current_user]
            self.db_session.add(favour)

            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest(IntegrityError)

        except KeyError:
            raise falcon.HTTPBadRequest(description=messages.parameters_invalid)

        resp.status = falcon.HTTP_200
