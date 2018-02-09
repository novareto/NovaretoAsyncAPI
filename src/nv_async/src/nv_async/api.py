# -*- coding: utf-8 -*-

import json
import inspect
import asyncio

from concurrent.futures import ProcessPoolExecutor
from sanic import response
from sanic.views import HTTPMethodView
from cromlech.jwt.components import TokenException


executor = ProcessPoolExecutor(max_workers=4)

ALLOWABLE_METHODS = frozenset(('PUT', 'DELETE', 'POST', 'GET', 'PATCH'))
cors_headers = {
    "Access-Control-Allow-Origin": '*'
}

def is_allowable_method(member):
    return inspect.ismethod(member) and (
        member.__name__.upper() in ALLOWABLE_METHODS)


class Action(HTTPMethodView):

    async def options(self, request):
        methods = dict(inspect.getmembers(self, predicate=is_allowable_method))
        headers = {
            "Access-Control-Allow-Origin": request.headers.get('Origin'),
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": ",".join(methods.keys()),
            "Access-Control-Allow-Headers": (
                "Authorization, Content-Type, X-Requested-With"),
        }
        return response.raw(
            b'', status=200, headers=headers, content_type="text/plain")


def protected(action):

    async def check_token(request):
        token = request.token
        if token:
            try:
                loop = asyncio.get_event_loop()
                payload = await loop.run_in_executor(
                    executor, request.app.jwt_service.check_token, token)
                if payload is not None:
                    return payload
            except (TokenException, ValueError) as err:
                pass
        return None

    async def jwt_protection(inst, request):
        payload = await check_token(request)
        if payload is None:
            return response.text('Unauthorized', status=401)
        request.app.auth_payload = payload
        return await action(inst, request)

    return jwt_protection
