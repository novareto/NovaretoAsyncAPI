# -*- coding: utf-8 -*-

from asyncio import sleep, Future
from sanic import response
from zeep import Client
from zeep.asyncio import AsyncTransport

from .api import Action


requested_keys = {

}


async def soap_request(request, key):
    year, mnr, c_number = key
    future = requested_keys.get(key)
    if future is None:
        future = requested_keys[key] = Future()
        transport = AsyncTransport(request.app.loop, cache=None)
        client = Client(request.app.config.soap_service, transport=transport)
        result = await client.service.getLNRecherche(c_number, mnr, year)
        future.set_result(result)
    return future


class Recherche(Action):

    async def get(self, request):

        key = []
        for arg in ('year', 'mnr', 'c_number'):
            param = request.raw_args.get(arg, None)
            if param is None:
                return response.text(
                    'Missing {0}'.format(arg), status=400)
            key.append(arg)

        key = tuple(key)
        cache = request.app.cache
        if key in cache:
            result = cache.get(key)
        else:
            future = await soap_request(request, key)
            result = cache[key] = await future

        return response.json(
            {'result': result}, status=200)
