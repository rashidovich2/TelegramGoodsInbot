# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.data.config import get_admins
from tgbot.services.api_sqlite_shop import get_all_shopx, get_shopx
from tgbot.services.api_sqlite import get_shopsxx, get_shopsxy

cpage = 10


# fp - flip page
# cpage - count page

################################################################################################
################################# СТРАНИЦЫ ИЗМЕНЕНИЯ МАГАЗИНА #################################
# Стартовые страницы выбора магазина для изменения
def shop_edit_open_fp(remover, user_id):
    if user_id in get_admins():
        get_my_shops = get_shopsxy()
    else:
        get_my_shops = get_shopsxx(admin=user_id)
    #get_my_shops = get_shopsxx(admin=user_id)
    keyboard = InlineKeyboardMarkup()
    count = 0
    print(len(get_my_shops))

    for a in range(remover, len(get_my_shops)):
        if count < cpage:
            keyboard.add(ikb(f"{get_my_shops[a]['name']}",
                             callback_data=f"shop_edit_open:{get_my_shops[a]['shop_id']}:{remover}:{user_id}"))
        count += 1

    if len(get_my_shops) <= 10:
        pass
    elif len(get_my_shops) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"shop_edit_nextp:{remover + cpage}:{user_id}")
        )
    elif remover + cpage >= len(get_my_shops):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"F:{remover - cpage}:{user_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"shop_edit_backp:{remover - cpage}:{user_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"shop_edit_nextp:{remover + cpage}:{user_id}"),
        )
    return keyboard


# Стартовые страницы выбора категории для добавления позиции
def position_create_shop_fp(remover):
    #get_shops = get_all_shopx()
    if user_id in get_admins():
        get_my_shops = get_shopsxy()
    else:
        get_my_shops = get_shopsxx(admin=user_id)
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_shops)):
        if count < cpage:
            keyboard.add(ikb(f"{get_my_shops[a]['shop_name']}",
                             callback_data=f"position_shop_create_here:{get_my_shops[a]['shop_id']}"))
        count += 1

    if len(get_my_shops) <= 10:
        pass
    elif len(get_my_shops) > cpage:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_shop_create_nextp:{remover + cpage}")
        )

    return keyboard

