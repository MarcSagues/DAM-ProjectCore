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
from resources.schemas import SchemaRegisterUser

mylogger = logging.getLogger(__name__)


#@falcon.before(requires_auth)
class ResourceGetEvents(DAMCoreResource):
    def on_get(self, req, resp, *args, **kwargs):
        super(ResourceGetEvents, self).on_get(req, resp, *args, **kwargs)

        response_events = list()
        aux_events = self.db_session.query(Favour)

        if aux_events is not None:
            for current_event in aux_events:
                response_events.append(current_event.json_model)

        resp.media = response_events
        resp.status = falcon.HTTP_200

