# - *- coding: utf- 8 - *-
import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.services.api_sqlite import get_all_categoriesx, get_itemsx, get_positionsx, get_all_shopx, get_city_user\
    , get_position_on_city, get_category_in_city, get_shopsxx, get_paramposition_on_city, get_shopposition_on_city, get_all_shopx

cpage = 10


# fp - flip page
# cpage - count page

################################################################################################
################################# СТРАНИЦЫ ИЗМЕНЕНИЯ КАТЕГОРИЙ #################################
# Стартовые страницы выбора категории для изменения
def category_edit_open_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"category_edit_here:{get_categories[a]['category_id']}:{remover}"))
        count += 1

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_nextp:{remover + cpage}")
        )
    elif remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_nextp:{remover + cpage}"),
        )

    return keyboard


# Следующая страница выбора категории для изменения
def category_edit_next_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"category_edit_here:{get_categories[a]['category_id']}:{remover}"))
        count += 1
    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_nextp:{remover + cpage}"),
        )

    return keyboard


# Предыдующая страница выбора категории для изменения
def category_edit_back_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"category_edit_here:{get_categories[a]['category_id']}:{remover}"))
        count += 1

    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"catategory_edit_nextp:{remover + cpage}"),
        )

    return keyboard


################################################################################################
################################### СТРАНИЦЫ СОЗДАНИЯ ПОЗИЦИЙ ##################################
# Стартовые страницы выбора категории для добавления позиции
def position_create_open_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_create_here:{get_categories[a]['category_id']}"))
        count += 1

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_create_nextp:{remover + cpage}")
        )

    return keyboard

# Стартовые страницы выбора категории для добавления позиции
def position_select_shop_fp(user_id):
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    count = 0
    remover = 0

    for a in range(remover, len(get_shops)):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['name']}",
                             callback_data=f"here_position_addtoshop:{get_shops[a]['shop_id']}"))
        count += 1

    if len(get_shops) <= 10:
        pass
    elif len(get_shops) > cpage:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_addtoshop_nextp:{remover + cpage}")
        )

    return keyboard


# Следующая страница выбора категории для добавления позиции
def position_create_next_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_create_here:{get_categories[a]['category_id']}"))
        count += 1

    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_create_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_create_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_create_nextp:{remover + cpage}"),
        )

    return keyboard

# Предыдующая страница выбора категории для добавления позиции
def position_create_back_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_create_here:{get_categories[a]['category_id']}"))
        count += 1

    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_create_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_create_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_create_nextp:{remover + cpage}")
        )

    return keyboard

################################################################################################
################################## СТРАНИЦЫ ИЗМЕНЕНИЯ ПОЗИЦИЙ ##################################
########################################### Категории ##########################################
# Стартовые страницы категорий при изменении позиции
def position_edit_category_open_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_edit_category:{get_categories[a]['category_id']}"))
        count += 1

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_nextp:{remover + cpage}")
        )
    elif remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Следующая страница категорий при изменении позиции
def position_edit_category_next_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_edit_category:{get_categories[a]['category_id']}"))
        count += 1

    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Предыдующая страница категорий при изменении позиции
def position_edit_category_back_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_edit_category:{get_categories[a]['category_id']}"))
        count += 1

    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_category_nextp:{remover + cpage}"),
        )

    return keyboard

########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для их изменения
def position_edit_open_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_positions)):
        if count < cpage:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"position_edit:{get_positions[a]['position_id']}:{remover}:{category_id}"))
        count += 1

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}")
        )
    elif remover + cpage >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data="position_edit_category_return"))

    return keyboard

# Следующая страница позиций для их изменения
def position_edit_next_page_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_positions)):
        if count < cpage:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"position_edit:{get_positions[a]['position_id']}:{remover}:{category_id}"))
        count += 1

    if remover + cpage >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data="position_edit_category_return"))

    return keyboard

# Предыдующая страница позиций для их изменения
def position_edit_back_page_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_positions)):
        if count < cpage:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"position_edit:{get_positions[a]['position_id']}:{remover}:{category_id}"))
        count += 1

    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data="position_edit_category_return"))

    return keyboard

################################################################################################
################################## СТРАНИЦЫ ДОБАВЛЕНИЯ ТОВАРОВ #################################
# Стартовые страницы категорий при добавлении товара
def products_add_category_open_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"products_add_category:{get_categories[a]['category_id']}"))
        count += 1

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_nextp:{remover + cpage}")
        )
    elif remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Следующая страница категорий при добавлении товара
def products_add_category_next_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"products_add_category:{get_categories[a]['category_id']}"))
        count += 1

    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Предыдующая страница категорий при добавлении товара
def products_add_category_back_page_fp(remover):
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"products_add_category:{get_categories[a]['category_id']}"))
        count += 1

    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_category_nextp:{remover + cpage}"),
        )

    return keyboard

########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для добавления товаров
def products_add_position_open_fp(remover, category_id):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_positions)):
        if count < cpage:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"products_add_position:{get_positions[a]['position_id']}:{category_id}"))
        count += 1

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_position_nextp:{remover + cpage}:{category_id}")
        )
    elif remover + cpage >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_position_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"products_add_position_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"products_add_position_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data="back_add_products_to_category"))

    return keyboard

################################################################################
##################### Страница подтверждения запроса на продавца ###############
################################################################################

def request_seller_role(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
            ikb("🔸 Запросить права продавца 🔸", callback_data="create_seller_request"))

    return keyboard

#keyboard.add(ikb(f"Психологическая поддержка PsyБОР", url="https://t.me/psyborbot"))

#############################################################################################
####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def products_item_category_swipe_fp(remover, city_id):
    #get_categories = get_category_in_city(city_id)
    get_categories = get_all_categoriesx()
    print(len(get_categories))
    #keyboard = InlineKeyboardMarkup()
    count = 0
    if city_id is None: city_id = 0

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"buy_category_open:{get_categories[a]['category_id']}:{city_id}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}:{city_id}"),
        )

    return keyboard

# Страницы категорий при покупке товара
def products_item_shop_swipe_fp(remover, city_id):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    get_shops = get_all_shopx()
    #get_shops = get_shopsxx()
    print(len(get_shops))
    #keyboard = InlineKeyboardMarkup()
    count = 0
    if city_id is None: city_id = 0

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_shops): remover -= 10

    for count, a in enumerate(range(remover, len(get_shops))):
        if count < 10:
            keyboard.add(ikb(get_shops[a]['name'],
                             callback_data=f"buy_shop_open:{get_shops[a]['shop_id']}:{city_id}"))

    if len(get_shops) <= 10:
        pass
    elif len(get_shops) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_shops) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_shop_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_shops):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_shop_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_shops) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_shop_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_shops) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_shop_swipe:{remover + 10}:{city_id}"),
        )

    return keyboard

# Страницы позиций для покупки товаров
def products_item_position_swipe_fp(remover, category_id, city_id):
    get_positions = get_positionsx(category_id=category_id)
    #get_positions = get_position_on_city(category_id, city_id)
    keyboard = InlineKeyboardMarkup()

    if city_id is None: city_id = 0
    if category_id is None: category_id = 0

    if remover >= len(get_positions): remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"buy_position_open:{get_positions[a]['position_id']}:{category_id}:{remover}:{city_id}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}:{city_id}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_category_swipe:{0}:{city_id}"))

    return keyboard

# Страницы позиций для покупки товаров
def products_shopitem_position_swipe_fp(remover, shop_id, city_id):
    #get_positions = get_positionsx(store_id=shop_id, position_city_id=city_id)
    get_positions = get_positionsx(store_id=shop_id)
    #get_positions = get_position_on_city(category_id, city_id)
    #get_positions = get_shopposition_on_city(shop_id, city_id)
    keyboard = InlineKeyboardMarkup()
    print(remover, shop_id, city_id)
    if city_id is None: city_id = 0

    if remover >= len(get_positions): remover -= 10
    print("||||")

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽", # | {len(get_items)} шт",
                callback_data=f"buy_parposition_open:{get_positions[a]['position_id']}:{shop_id}:{remover}:{city_id}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_parposition_swipe:{shop_id}:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_parposition_swipe:{shop_id}:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_parposition_swipe:{shop_id}:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_parposition_swipe:{shop_id}:{remover + 10}:{city_id}"),
        )
    keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))

    return keyboard
