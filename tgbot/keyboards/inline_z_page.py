# - *- coding: utf- 8 - *-
import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.services.api_sqlite import get_all_categoriesx, get_itemsx, get_positionsx, get_all_shopx, get_city_user\
    , get_position_on_city, get_category_in_city, get_shopsxx, get_paramposition_on_city, get_shopposition_on_city,\
    get_all_shopx, get_my_shopx, get_events_in_city, get_all_events, get_all_places, get_eventxx, get_events_in_place, \
    get_eventsxx,  get_artistsxx, get_category_in_cityx, get_shop_in_cityx, get_events_in_cityx, get_places_in_cityx, \
    get_category_in_citypx

cpage = 10


# fp - flip page
# cpage - count page
##############################################################################################
################################################################################################
###################################### ИЗМЕНЕНИЕ КАТЕГОРИИ #####################################
# Стартовые страницы выбора категории для изменения
def shop_edit_swipe_fp(user_id):
    get_shops = get_my_shopx(user_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_shops): remover -= 10

    for count, a in enumerate(range(remover, len(get_shops))):
        if count < 10:
            keyboard.add(ikb(get_shops[a]['name'],
                             callback_data=f"shop_edit_open:{get_categories[a]['category_id']}:{remover}"))

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

def open_partners_list():
    get_partners = get_all_partnersx()
    keyboard = InlineKeyboardMarkup()

    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for partner in get_partners:
        buttons_to_add = append([InlineKeyboardButton(text=partner['name'], url=partner['link'])])

    keyboard.add(*buttons_to_add)

    return keyboard

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

################################################################################################
################################# СТРАНИЦЫ ИЗМЕНЕНИЯ МАГАЗИНА #################################
# Стартовые страницы выбора магазина для изменения
def artist_edit_open_fp(remover, user_id):
    get_my_artists = get_artistsxx(admin=user_id)
    keyboard = InlineKeyboardMarkup()
    count = 0
    print(len(get_my_artists))

    for a in range(remover, len(get_my_artists)):
        if count < cpage:
            keyboard.add(ikb(f"{get_my_artists[a]['name']}",
                             callback_data=f"artist_edit:{get_my_artists[a]['artist_id']}:{user_id}:{remover}"))
        count += 1

    if len(get_my_artists) <= 10:
        pass
    elif len(get_my_artists) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"artist_edit_swipe:{remover + cpage}:{user_id}")
        )
    elif remover + cpage >= len(get_my_artists):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"artist_edit_swipe:{remover - cpage}:{user_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"artist_edit_swipe:{remover - cpage}:{user_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"artist_edit_swipe:{remover + cpage}:{user_id}"),
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



#############################################################################################
####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def position_2people_create_open_fp(category_id, remover, level, parent, city_id): # + action = create / open
    print(city_id)
    #if parent == "" or parent is None: parent = 0

    '''if category_id != 0:
        get_categories = get_category_in_citypx(parent_id=category_id)
    elif level == 1:
        get_categories = get_category_in_citypx(level=1)
    else:'''
    get_categories = get_category_in_citypx(parent_id=parent)
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_category_in_cityx(position_city_id=city_id, position_type=1, flagallc=1)

    #get_categories = get_all_categoriesx()
    print(len(get_categories))
    #keyboard = InlineKeyboardMarkup()
    count = 0
    if city_id is None: city_id = 0

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        level = get_categories[a]['level']
        if count < 10:
            if level == 1:
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:{0}:{0}:{get_categories[a]['category_id']}:{city_id}"))
            elif level == 2:
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"position_people_create_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_people_category_swipe:{0}:{remover + 10}:{0}:{0}:{city_id}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_people_category_swipe:{0}:{remover - 10}:{0}:{0}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_people_category_swipe:{0}:{remover - 10}:{0}:{0}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_people_category_swipe:{0}:{remover + 10}:{0}:{0}:{city_id}"),
        )

    keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:{0}:{level-1}:{0}:{city_id}"))

    return keyboard

#############################################################################################
####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def position_people_create_open_fp(category_id, remover, level, parent, city_id, action): #+ action = create / open
    print(city_id, action)
    #if parent == "" or parent is None: parent = 0

    '''if category_id != 0:
        get_categories = get_category_in_citypx(parent_id=category_id)
    elif level == 1:
        get_categories = get_category_in_citypx(level=1)
    else:'''
    get_categories = get_category_in_citypx(parent_id=parent)

    print(len(get_categories))

    count = 0
    if city_id is None: city_id = 0

    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        level = get_categories[a]['level']
        if count < 10:
            if get_categories[a]['level'] == 1:
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:{0}:{0}:{get_categories[a]['category_id']}:{city_id}:{action}"))
            elif get_categories[a]['level'] == 2 and action == "create":
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"position_people_create_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}"))
            elif get_categories[a]['level'] == 2 and action == "open":
                keyboard.add(ikb(get_categories[a]['category'],
                             callback_data=f"position_people_open_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_people_category_swipe:{0}:{remover + 10}:{0}:{0}:{city_id}:{action}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_people_category_swipe:{0}:{remover - 10}:{0}:{0}:{city_id}:{action}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"buy_people_category_swipe:{0}:{remover - 10}:{0}:{0}:{city_id}:{action}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"buy_people_category_swipe:{0}:{remover + 10}:{0}:{0}:{city_id}:{action}"),
        )

    keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:{0}:{level-1}:{0}:{city_id}:{action}"))

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
    #get_shops = get_my_shopx(user_id)
    keyboard = InlineKeyboardMarkup()
    count = 0
    remover = 0
    cpage = 10

    for a in range(remover, len(get_shops)):
        #if count < cpage:
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
def position_addtoshop_nextp(remover):
    #get_categories = get_all_categoriesx()
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_shops)):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['name']}",
                             callback_data=f"here_position_addtoshop:{get_shops[a]['shop_id']}"))
        count += 1

    if remover + cpage >= len(get_shops):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_addtoshop_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_addtoshop_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_addtoshop_nextp:{remover + cpage}"),
        )

    return keyboard

# Предыдующая страница выбора категории для добавления позиции
def position_addtoshop_backp(remover):
    #get_categories = get_all_categoriesx()
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_shops)):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['category_name']}",
                             callback_data=f"position_create_here:{get_shops[a]['category_id']}"))
        count += 1

    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_addtoshop_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"position_addtoshop_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"position_addtoshop_nextp:{remover + cpage}")
        )

    return keyboard

# Следующая страница выбора категории для добавления позиции
def position_create_next_page_fp(remover):
    #get_categories = get_all_categoriesx()
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    count = 0

    for a in range(remover, len(get_categories)):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['name']}",
                             callback_data=f"position_create_here:{get_shops[a]['shop_id']}"))
        count += 1

    if remover + cpage >= len(get_shops):
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
    print(get_positions)

    for a in range(remover, len(get_positions)):
        if count < cpage:
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            #print(get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ |",  #{len(get_items)} шт",
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
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ |", # {len(get_items)} шт",
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
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽", # | {len(get_items)} шт",
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
    print(city_id)
    #get_categories = get_category_in_city(city_id)
    get_categories = get_category_in_cityx(position_city_id=city_id, position_type=1, flagallc=1)

    #get_categories = get_all_categoriesx()
    print(len(get_categories))
    #keyboard = InlineKeyboardMarkup()
    count = 0
    if city_id is None: city_id = 0

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    keyboard.add(ikb(" Барахолка Вашего города ",
                     callback_data=f"privateMarket"))

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

# Страницы магазин при покупке товара
def select_place_in_city_swipe_fp(city_id):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    #get_events = get_events_in_city(city_id)
    get_places = get_places_in_cityx(city_id)
    #get_shops = get_shopsxx()
    print(get_places)
    print(len(get_places))
    remover = 0
    count = 0
    if city_id is None: city_id = 0
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_places): remover -= 10
    keyboard.add(ikb(f"🔸 События в Вашем городе🔸", callback_data=f"events_city_swipe:{0}:{city_id}"))

    for count, a in enumerate(range(remover, len(get_places))):
        print(get_places[a]['place_id'])
        if count < 10:
            keyboard.add(ikb(get_places[a]['name'], # + " | " + get_places[a]['city_id'],
                             callback_data=f"here_event_place:{get_places[a]['place_id']}"))

    if len(get_places) <= 10:
        pass
    elif len(get_places) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_places):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def places_in_city_swipe_fp(remover, city_id):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    #get_events = get_events_in_city(city_id)
    #get_places = get_all_places()
    print(remover, city_id)
    get_places = get_places_in_cityx(city_id, flagallc=1, position_type=1)
    #get_shops = get_shopsxx()
    print(len(get_places))
    count = 0
    if city_id is None: city_id = 0
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_places): remover -= 10
    keyboard.add(ikb(f"🔸 События в Вашем городе🔸", callback_data=f"events_city_swipe:{0}:{city_id}"))

    for count, a in enumerate(range(remover, len(get_places))):
        if count < 10:
            keyboard.add(ikb(get_places[a]['name'], # + " | " + get_places[a]['city'],
                             callback_data=f"book_place_open:{get_places[a]['place_id']}"))

    if len(get_places) <= 10:
        pass
    elif len(get_places) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_places):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def events_in_city_swipe_fp(remover, city_id):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    #get_events = get_events_in_city(city_id)
    get_events = get_events_in_cityx(city_id, flagallc=1, position_type=1)
    #get_shops = get_shopsxx()
    print(len(get_events))
    #keyboard = InlineKeyboardMarkup()
    count = 0
    #if place_id is None: place_id = 0
    if city_id is None: city_id = 0

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_events): remover -= 10
    keyboard.add(ikb(f"Добавить место или событие, нажмите 🔸", callback_data=f"open_inline_support"))
    keyboard.add(ikb(f"🔸 Места в Вашем городе🔸", callback_data=f"places_city_swipe:{0}:{city_id}"))

    for count, a in enumerate(range(remover, len(get_events))):
        if count < 10:
            #edate = get_events[a]['event_date'] if get_events[a]['event_date'] else ""
            keyboard.add(ikb(get_events[a]['event_name'] + " | ", # + edate,
                             callback_data=f"book_event_open:{get_events[a]['event_id']}:{0}:{city_id}"))

    if len(get_events) <= 10:
        pass
    elif len(get_events) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_events):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def events_in_place_swipe_fp(remover, place_id, city_id):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    #get_events = get_events_in_city(city_id)
    #get_events = get_all_events()
    print("||||")
    #get_events = get_events_in_place(place_id)
    get_events = get_eventsxx(place_id=place_id)
    #get_shops = get_shopsxx()
    print(get_events)
    print(get_events[0])
    print(remover, place_id)
    #keyboard = InlineKeyboardMarkup()
    count = 0
    print(city_id)
    if place_id is None: place_id = 0
    if city_id is None: city_id = 0
    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_events[0]): remover -= 10
    keyboard.add(ikb(f"🔸 Места в Вашем городе🔸", callback_data=f"places_city_swipe:{0}:{city_id}"))

    for count, a in enumerate(range(remover, len(get_events))):
        if count < 10:
            keyboard.add(ikb(get_events[a]['event_name'] + " | " + get_events[a]['event_date'],
                             callback_data=f"book_event_open:{get_events[a]['event_id']}:{place_id}:{city_id}"))

    if len(get_events) <= 10:
        pass
    elif len(get_events) > 10 and remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_events):
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb("⬅ Назад", callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def products_item_shop_swipe_fp(remover, city_id):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    get_shops = get_all_shopx()
    get_shops = get_shop_in_cityx(city_id=city_id, position_type=1, flagallc=1)
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
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы позиций для покупки товаров
def products_item_position_swipe_fp(remover, category_id, city_id, source): # + source = people / commercial
    source = str(source)
    get_positions = get_positionsx(category_id=category_id) #, source=source)
    print(remover, category_id, city_id, source)
    print(get_positions)

    keyboard = InlineKeyboardMarkup()

    #city_id = сity_id if city_id else 0
    #category_id = category_id if category_id else 0
    #if category_id is None: category_id = 0

    if remover >= len(get_positions): remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽", # | {len(get_items)} шт",
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

# Следующая страница позиций для добавления товаров
def products_add_position_next_page_fp(remover, category_id):
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

    if remover + cpage >= len(get_positions):
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
