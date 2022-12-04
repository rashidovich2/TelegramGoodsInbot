# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.services.api_sqlite_shop import get_all_shopx

cpage = 10


# fp - flip page
# cpage - count page


################################################################################################
################################# СТРАНИЦЫ ИЗМЕНЕНИЯ МАГАЗИНА #################################
# Стартовые страницы выбора магазина для изменения
def shop_edit_open_fp(remover, shops):
    kb = InlineKeyboardMarkup()
    count = 0
    if len(shops) < 10:
        for shop in shops:
            kb.add(ikb(f"{shop[1]}",
                                callback_data=f"shop_edit_here:{shop[0]}:{remover}"))



    else:
        pg_cnt = len(shops) // 10
        print(f'pg_cnt {pg_cnt}')
        print(f'page {remover}')

        if remover > 0:
            bt3 = ikb('Предыдущая страница', callback_data=f'change_shop_edit_pg:{remover - 1}')
            kb.add(bt3)

        pg_end = (int(remover) + 1) * 10
        print(f'pg_end {pg_end}')
        for shop in shops[pg_end - 10:pg_end]:
            bt2 = ikb(f'+{shop[1]}', callback_data=f'shop_edit_here:{shop[0]}')
            kb.add(bt2)

        if remover < pg_cnt:
            bt4 = ikb('Следующая страница', callback_data=f'change_shop_edit_pg:{remover + 1}')
            kb.add(bt4)
    return kb


# Стартовые страницы выбора категории для добавления позиции
def position_create_shop_fp(remover):
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_shops)):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['shop_name']}",
                             callback_data=f"position_shop_create_here:{get_shops[a]['shop_id']}"))
        count += 1

    if len(get_shops) <= 10:
        pass
    elif len(get_shops) > cpage:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_shop_create_nextp:{remover + cpage}")
        )

    return keyboard
