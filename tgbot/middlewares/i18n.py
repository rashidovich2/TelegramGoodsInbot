# - *- coding: utf- 8 - *-
import os
from pathlib import Path
import gettext
from contextvars import ContextVar
from typing import Any, Dict, Tuple
from babel import Locale

from aiogram.types import Message, User
from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from tgbot.services.api_sqlite import get_user_lang, get_userx
#from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseMiddleware

#from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR

class I18nMiddleware(BaseMiddleware):
    """
    I18n middleware based on gettext util

    >>> dp = Dispatcher(bot)
    >>> i18n = I18nMiddleware(DOMAIN, LOCALES_DIR)
    >>> dp.middleware.setup(i18n)
    and then
    >>> _ = i18n.gettext
    or
    >>> _ = i18n = I18nMiddleware(DOMAIN_NAME, LOCALES_DIR)
    """

    ctx_locale = ContextVar('ctx_user_locale', default=None)

    def __init__(self, domain='mybot', path=None, default='ru'):
        """
        :param domain: domain
        :param path: path where located all *.mo files
        :param default: default locale name
        """
        super(I18nMiddleware, self).__init__()

        if path is None:
            rd = Path(__file__).parents
            base_dir = rd[1]
            path = str(f"{base_dir}{os.sep}locales")
            #path = os.path.join(os.getcwd(), 'locales')

        self.domain = domain
        self.path = path
        self.default = default
        #self.locale = locale

        self.locales = self.find_locales()

    def find_locales(self) -> Dict[str, gettext.GNUTranslations]:
        """
        Load all compiled locales from path

        :return: dict with locales
        """
        translations = {}

        for name in os.listdir(self.path):
            if not os.path.isdir(self.path):
                continue
            mo_path = os.path.join(self.path, name, 'LC_MESSAGES', f'{self.domain}.mo')

            if os.path.exists(mo_path):
                with open(mo_path, 'rb') as fp:
                    translations[name] = gettext.GNUTranslations(fp)

        return translations

    def reload(self):
        """
        Hot reload locles
        """
        self.locales = self.find_locales()

    @property
    def available_locales(self) -> Tuple[str]:
        """
        list of loaded locales

        :return:
        """
        return tuple(self.locales.keys())

    def __call__(self, singular, plural=None, n=1, locale=None) -> str:
        return self.gettext(singular, plural, n, locale)

    def gettext(self, singular, plural=None, n=1, locale=None) -> str:
        """
        Get text

        :param singular:
        :param plural:
        :param n:
        :param locale:
        :return:
        """
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in self.locales:
            return singular if n == 1 else plural
        translator = self.locales[locale]

        if plural is None:
            return translator.gettext(singular)
        else:
            return translator.ngettext(singular, plural, n)

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        """
        User locale getter
        You can override the method if you want to use different way of getting user language.

        :param action: event name
        :param args: event arguments
        :return: locale name
        """
        user: types.User = types.User.get_current()
        if locale := user.locale:
            *_, data = args
            language = data['locale'] = locale.language
            return language

    async def get_user_locale2(self, user_id) -> str:
        """
        User locale getter
        You can override the method if you want to use different way of getting user language.

        :param action: event name
        :param args: event arguments
        :return: locale name
        """
        user_lang = get_userx(user_id=user_id)['user_lang']
        if len(user_lang) == 0: user_lang = "ru"
        return user_lang

    async def set_user_locale(self, locale: str) -> None:
        if user := types.User.get_current():
            state = Dispatcher.get_current().current_state(user=user.id)

            async with state.proxy() as data:
                data["locale"] = locale
                i18n.ctx_locale.set(locale)

    async def trigger(self, action, args):
        """
        Event trigger

        :param action: event name
        :param args: event arguments
        :return:
        """
        if 'update' not in action \
                and 'error' not in action \
                and action.startswith('pre_process'):
            locale = await self.get_user_locale(action, args)
            self.ctx_locale.set(locale)
            return True

        if action == 'pre_process_error':
            self.ctx_locale.reset()
            return True

    '''async def process_message(self, message: types.Message) -> None:
        """
        Process message

        :param message:
        :return:
        """
        await self.set_user_locale(self.default)
        self.ctx_locale.set(self.default)'''
