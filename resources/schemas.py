#!/usr/bin/python
# -*- coding: utf-8 -*-

SchemaUserToken = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
    },
    "required": ["token"]
}

SchemaRegisterUser = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["username", "password", "email"]
}

SchemaUpdateFavour = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "amount": {"type": "number"},
    },
    "required": []
}

SchemaUpdateUser = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": "string"},
    },
    "required": ["username", "password", "email", "phone"]
}
