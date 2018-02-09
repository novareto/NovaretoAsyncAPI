# -*- coding: utf-8 -*-

from asyncio import sleep, Future
from sanic import response
from .api import Action

### TESTING PURPOSE ONLY
from random import randint
###


requested_keys = {

}


async def long_API_call(request, key):
    future = requested_keys.get(key)
    if future is None:
        future = requested_keys[key] = Future()
        print('long call for ')
        await sleep(15)
        future.set_result(randint(1, 41))
    return future


class Dummy(Action):

    async def get(self, request):
        key = request.raw_args.get('key', None)
        if key is None:
            return response.raw(b'Gimme key !', status=400)

        cache = request.app.cache
        if key in cache:
            result = cache.get(key)
        else:
            future = await long_API_call(request, key)
            result = cache[key] = await future
            
        return response.json(
            {'result': result}, status=200)
