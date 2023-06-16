# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.data.config import get_admins, get_shopadmins, is_shopadmin
from tgbot.services.api_sqlite import get_settingsx, get_user_lang

# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in get_admins()

# Проверка на админа
class IsShopAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in get_shopadmins()

#Проверка на любого админа
class IsAdminorShopAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return (
            message.from_user.id in get_admins()
            or message.from_user.id in get_shopadmins()
        )

# Проверка на принадлежность товара для админа магазина
class IsProductShopAdmin(BoundFilter):
    async def check(self, message: types.Message):
        #print message.from_user.id 
        # if message.from_user.id in get_admins():
        #     return True
        # else:
        #     return False
        return True

# Проверка на возможность покупки товара
class IsBuy(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        return (
            get_settings['status_buy'] != "True"
            and message.from_user.id not in get_admins()
        )


# Проверка на возможность пополнения
class IsRefill(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        return (
            get_settings['status_refill'] != "True"
            and message.from_user.id not in get_admins()
        )


# Проверка на технические работы
class IsWork(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        return (
            get_settings['status_work'] != "False"
            and message.from_user.id not in get_admins()
        )

class IsShopExist(BoundFilter):
    async def check(self, message: types.Message):
        return check_user_shop_exist(message.from_user.id) == 'True'
