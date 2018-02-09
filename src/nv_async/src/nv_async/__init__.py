# -*- coding: utf-8 -*-

import logging
from zope.i18nmessageid import MessageFactory
from .actions import Recherche


i18n = MessageFactory("novareto_async")
logger = logging.getLogger("novareto_async")


def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)


endpoints = {
    '/recherche': Recherche.as_view(),
}
