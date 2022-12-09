# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.data.config import get_admins, get_shopadmins, is_shopadmin
from tgbot.services.api_sqlite import get_settingsx


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
         if message.from_user.id in get_admins():
             return True
         else:
             return False
        #return True

# Проверка на админа
class IsShopAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in get_shopadmins(): #== is_shopadmin(message.from_user.id):
        #if message.from_user.id == is_shopadmin(message.from_user.id):
            return True
        else:
            return False

#Проверка на любого админа
class IsAdminorShopAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in get_admins() or message.from_user.id in get_shopadmins():
            return True
        else:
            return False

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

        if get_settings['status_buy'] == "True" or message.from_user.id in get_admins():
            return False
        else:
            return True


# Проверка на возможность пополнения
class IsRefill(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        if get_settings['status_refill'] == "True" or message.from_user.id in get_admins():
            return False
        else:
            return True


# Проверка на технические работы
class IsWork(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        if get_settings['status_work'] == "False" or message.from_user.id in get_admins():
            return False
        else:
            return True

class IsShopExist(BoundFilter):
    async def check(self, message: types.Message):
        if check_user_shop_exist(message.from_user.id) == 'True':
            return True
        else:
            return False
