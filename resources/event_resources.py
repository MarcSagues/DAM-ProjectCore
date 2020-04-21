#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from builtins import super
import falcon
from falcon.media.validators import jsonschema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

import messages
from db.models import User, GenereEnum, Favour
from hooks import requires_auth
from resources.base_resources import DAMCoreResource
from resources.schemas import SchemaRegisterUser, SchemaUpdateFavour

mylogger = logging.getLogger(__name__)


@falcon.before(requires_auth)
class ResourceGetEvents(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceGetEvents, self).on_get(req, resp, *args, **kwargs)

        request_favour_userid = req.get_param("user_id", False)
        current_user = req.context["auth_user"]
        response_events = list()

        #Agafem tots els valors del usuari
        if request_favour_userid is not None:
            aux_events = self.db_session.query(Favour).filter(Favour.owner_id == current_user.id)
        else:
            aux_events = self.db_session.query(Favour).filter(Favour.owner_id != current_user.id)

        if aux_events is not None:
            for current_event in aux_events:
                response_events.append(current_event.json_model)

        resp.media = response_events
        resp.status = falcon.HTTP_200


@falcon.before(requires_auth)
class UpdateFavour(DAMCoreResource):
    @jsonschema.validate(SchemaUpdateFavour)
    def on_post(self, req, resp, *args, **kwargs):
        super(UpdateFavour, self).on_post(req, resp, *args, **kwargs)

        current_user = req.context["auth_user"]
        #Assegurar que el id del favor correspon al id del usuari

        if "id" in kwargs:
            try:
                favour = self.db_session.query(Favour).filter(Favour.id == kwargs["id"], Favour.owner_id == current_user.id).one()
                if (req.media["name"]) is not None:
                    favour.name = req.media["name"]
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
        #Assegurar que el id del favor correspon al id del usuari

        if "id" in kwargs:
            try:
                favour = self.db_session.query(Favour).delete(Favour.id == kwargs["id"], Favour.owner_id == current_user.id)
                self.db_session.commit()

                resp.status = falcon.HTTP_200

            except NoResultFound:
                raise falcon.HTTPBadRequest(description=messages.user_not_found) #TODO

@falcon.before(requires_auth)
class ResourcePostFavour(DAMCoreResource):
    #@jsonschema.validate(SchemaRegisterUser)
    def on_post(self, req, resp, *args, **kwargs):
        super(ResourcePostFavour, self).on_post(req, resp, *args, **kwargs)

        favour = Favour()
        current_user = req.context["auth_user"]
        try:
            favour.user = req.media["username"]
            favour.name = req.media["name"]
            favour.desc = req.media["desc"]
            favour.category = req.media["category"]
            favour.amount = req.media["amount"]
            favour.owner_id = current_user.id
            favour.registered = [current_user]
            self.db_session.add(favour)

            try:
                self.db_session.commit()
            except IntegrityError:
                raise falcon.HTTPBadRequest(IntegrityError)

        except KeyError:
            raise falcon.HTTPBadRequest(description=messages.parameters_invalid)

        resp.status = falcon.HTTP_200
