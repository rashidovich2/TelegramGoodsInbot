# - *- coding: utf- 8 - *-
import os
import gettext
from contextvars import ContextVar
from typing import Any, Dict, Tuple
from babel import Locale

from aiogram.types import Message, User
from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
#from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware


#from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR


class I18nMiddleware(BaseMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        if user := types.User.get_current():
            locale: Locale = user.locale

            state = Dispatcher.get_current().current_state(user=user.id)
            try:
                async with state.proxy() as data:
                    return data["lang"]
            except KeyError:

                if locale:
                    *_, data = args
                    language = data['locale'] = locale.language
                    return language

    async def set_user_locale(self, locale: str) -> None:
        if user := types.User.get_current():
            state = Dispatcher.get_current().current_state(user=user.id)

            async with state.proxy() as data:
                data["lang"] = locale
                i18n.ctx_locale.set(locale)

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)