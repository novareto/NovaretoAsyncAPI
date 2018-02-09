# -*- coding: utf-8 -*-

import os
import asyncio
import logging

from json import loads
from loader import Configuration
from collections import namedtuple


def get_key(path):
    if not os.path.isfile(path):
        with open(path, 'w+', encoding="utf-8") as keyfile:
            from cromlech.jwt.components import JWTHandler
            key = JWTHandler.generate_key()
            export = key.export()
            keyfile.write(export)
    else:
        with open(path, 'r', encoding="utf-8") as keyfile:
            from jwcrypto import jwk
            data = loads(keyfile.read())
            key = jwk.JWK(**data)

    return key


with Configuration('config.json') as config:

    from sanic import Sanic
    from nv_async import endpoints
    from cromlech.jwt.components import JWTHandler, JWTService

    app = Sanic(__name__)
    
    @app.listener('before_server_start')
    def prepare_crypto(app, loop):
        key = get_key(config['crypto']['keypath'])
        app.jwt_service = JWTService(key, JWTHandler, lifetime=600)

    for path, action in endpoints.items():
        app.add_route(action, path)

    app.run(host="0.0.0.0", port=8080)
