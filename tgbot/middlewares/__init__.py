# - *- coding: utf- 8 - *-
from aiogram import Dispatcher


from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR
from tgbot.middlewares.exists_user import ExistsUserMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.middlewares.i18n import I18nMiddleware


# Подключение милдварей
def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(ExistsUserMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(I18nMiddleware())

def setup_middleware(dp: Dispatcher):
    i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
