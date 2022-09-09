# - *- coding: utf- 8 - *-
import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.services.api_sqlite import get_all_categoriesx, get_itemsx, get_positionsx


# fp - flip page

################################################################################################
###################################### ИЗМЕНЕНИЕ КАТЕГОРИИ #####################################
# Стартовые страницы выбора категории для изменения
def category_edit_swipe_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"category_edit_open:{get_categories[a]['category_id']}:{remover}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}")
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"),
        )

    return keyboard


################################################################################################
######################################## СОЗДАНИЕ ПОЗИЦИИ ######################################
# Страницы выбора категории для добавления позиции
def position_create_swipe_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"position_create_open:{get_categories[a]['category_id']}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_create_swipe:{remover + 10}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_create_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_create_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_create_swipe:{remover + 10}"),
        )

    return keyboard


################################################################################################
####################################### ИЗМЕНЕНИЕ ПОЗИЦИИ ######################################
# Стартовые страницы категорий при изменении позиции
def position_edit_category_swipe_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"position_edit_category_open:{get_categories[a]['category_id']}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_swipe:{remover + 10}")
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_swipe:{remover + 10}"),
        )

    return keyboard


# Стартовые страницы позиций для их изменения
def position_edit_swipe_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_positions): remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"position_edit_open:{get_positions[a]['position_id']}:{category_id}:{remover}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_swipe:{category_id}:{remover + 10}")
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data="position_edit_category_swipe:0"))

    return keyboard


################################################################################################
####################################### ДОБАВЛЕНИЕ ТОВАРОВ #####################################
# Страницы категорий при добавлении товара
def products_add_category_swipe_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"products_add_category_open:{get_categories[a]['category_id']}:{remover}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_swipe:{remover + 10}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_swipe:{remover + 10}"),
        )

    return keyboard


# Страницы позиций для добавления товаров
def products_add_position_swipe_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_positions): remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"products_add_position_open:{get_positions[a]['position_id']}:{category_id}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_position_swipe:{category_id}:{remover + 10}")
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_position_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_position_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_position_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data="products_add_category_swipe:0"))

    return keyboard


#############################################################################################
####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def products_item_category_swipe_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"buy_category_open:{get_categories[a]['category_id']}:0"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
        )

    return keyboard


# Страницы позиций для покупки товаров
def products_item_position_swipe_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_positions): remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"buy_position_open:{get_positions[a]['position_id']}:{category_id}:{remover}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_category_swipe:0"))

    return keyboard
