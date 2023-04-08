from typing import Any, Dict, Optional

from aiogram import Dispatcher
from aiogram.types import User
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n import I18nMiddleware as BaseI18nMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from babel import Locale, UnknownLocaleError

from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR #I18N_DEFAULT_LOCALE,
from tgbot.services.api_sqlite import *
#from src.models.user import UserModel


class I18nMiddleware(BaseI18nMiddleware):
    def get_internal_locale(self, language_code: str):
        if language_code and language_code in self.i18n.available_locales:
            return language_code

    def get_external_locale(self, user_id: str):
        user: UserModel = get_userx(user_id)

        if user and user.settings.language_code and user.settings.language_code in self.i18n.available_locales:
            return user.settings.language_code

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user: Optional[User] = data.get("event_from_user")

        if user is None:
            return self.i18n.default_locale

        internal_locale = self.get_internal_locale(user.language_code)
        print("internal_locale:", internal_locale)  # ! en
        external_locale = self.get_external_locale(user.id)
        print("external_locale:", external_locale)  # ! None

        locale = external_locale or internal_locale

        try:
            locale = Locale.parse(locale, sep="-")
            print("locale:", locale)  # ! en
        except UnknownLocaleError:
            return self.i18n.default_locale


def setup(dispatcher: Dispatcher):
    i18n = I18n(path=I18N_LOCALES_PATH,
                default_locale=I18N_DEFAULT_LOCALE, domain=I18N_DOMAIN)
    i18nMiddleware = I18nMiddleware(i18n=i18n)

    return dispatcher.message.middleware(i18nMiddleware)