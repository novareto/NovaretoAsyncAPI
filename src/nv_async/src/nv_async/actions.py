# -*- coding: utf-8 -*-

from sanic import response
from .api import Action


class Dummy(Action):

    async def get(self, request):
        return response.json('OK !!', status=200)
