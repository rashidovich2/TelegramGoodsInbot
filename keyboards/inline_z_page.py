# - *- coding: utf- 8 - *-
import math
import gettext
from pathlib import Path
from contextvars import ContextVar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
from tgbot.middlewares.i18n import I18nMiddleware

from tgbot.services.api_sqlite import get_all_categoriesx, get_itemsx, get_positionsx, get_all_shopx, get_city_user\
    , get_position_on_city, get_category_in_city, get_shopsxx, get_paramposition_on_city, get_shopposition_on_city,\
    get_all_shopx, get_my_shopx, get_events_in_city, get_all_events, get_all_places, get_eventxx, get_events_in_place, \
    get_eventsxx,  get_artistsxx, get_category_in_cityx, get_shop_in_cityx, get_events_in_cityx, get_places_in_cityx, \
    get_category_in_citypx, get_positionsorder, get_parent_cat, get_category_count, get_parent_catc, get_categories_in_cityx, get_positionsax

cpage = 10

'''i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
#I18nMiddleware.setup_middlewares(i18n)
print(i18n)
# Alias for gettext method
_ = i18n.gettext
#_ = i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
#lang1 = gettext.translation('mybot', languages=['ru'])
#lang1.install()
print(i18n.find_locales())
#current_user_id_ctx = ContextVar('current_user_id_ctx')
ctx_user_locale = ContextVar('ctx_user_locale')'''

# fp - flip page
# cpage - count page
##############################################################################################
################################################################################################
###################################### ИЗМЕНЕНИЕ КАТЕГОРИИ #####################################
# Стартовые страницы выбора категории для изменения
def shop_edit_swipe_fp(user_id, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_shops = get_my_shopx(user_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_shops): remover -= 10

    for count, a in enumerate(range(remover, len(get_shops))):
        if count < 10:
            keyboard.add(ikb(get_shops[a]['name'],
                             callback_data=f"shop_edit_open:{get_categories[a]['category_id']}:{remover}"))

    if len(get_categories) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_swipe:{remover + 10}")
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_swipe:{remover - 10}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_swipe:{remover + 10}"),
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
def category_edit_open_fp(remover, lang):
    print(lang)
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"category_edit_here:{get_categories[a]['category_id']}:{remover}"))
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_nextp:{remover + cpage}")
        )
    elif remover + cpage >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_nextp:{remover + cpage}"),
        )

    return keyboard


# Следующая страница выбора категории для изменения
def category_edit_next_page_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"category_edit_here:{get_categories[a]['category_id']}:{remover}"))
    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_nextp:{remover + cpage}"),
        )

    return keyboard

################################################################################################
################################# СТРАНИЦЫ ИЗМЕНЕНИЯ МАГАЗИНА #################################
# Стартовые страницы выбора магазина для изменения
def artist_edit_open_fp(remover, user_id):
    get_my_artists = get_artistsxx(admin=user_id)
    keyboard = InlineKeyboardMarkup()
    print(len(get_my_artists))

    for count, a in enumerate(range(remover, len(get_my_artists))):
        if count < cpage:
            keyboard.add(ikb(f"{get_my_artists[a]['name']}",
                             callback_data=f"artist_edit:{get_my_artists[a]['artist_id']}:{user_id}:{remover}"))
    if len(get_my_artists) <= 10:
        pass
    elif len(get_my_artists) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(_("Далее ➡", locale=lang), callback_data=f"artist_edit_swipe:{remover + cpage}:{user_id}")
        )
    elif remover + cpage >= len(get_my_artists):
        keyboard.add(
            ikb(_("⬅ Назад", locale=lang), callback_data=f"artist_edit_swipe:{remover - cpage}:{user_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(_("⬅ Назад", locale=lang), callback_data=f"artist_edit_swipe:{remover - cpage}:{user_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(_("Далее ➡", locale=lang), callback_data=f"artist_edit_swipe:{remover + cpage}:{user_id}"),
        )
    return keyboard


# Предыдующая страница выбора категории для изменения
def category_edit_back_page_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"category_edit_here:{get_categories[a]['category_id']}:{remover}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"catategory_edit_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"catategory_edit_nextp:{remover + cpage}"),
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
                keyboard.add(
                    ikb(
                        get_categories[a]['category'],
                        callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:0:0:{get_categories[a]['category_id']}:{city_id}",
                    )
                )
            elif level == 2:
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"position_people_create_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}"))

    if len(get_categories) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(
                f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
            ikb(
                _("Далее ➡", locale=lang),
                callback_data=f"buy_people_category_swipe:0:{remover + 10}:0:0:{city_id}",
            ),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb(
                _("⬅ Назад", locale=lang),
                callback_data=f"buy_people_category_swipe:0:{remover - 10}:0:0:{city_id}",
            ),
            ikb(
                f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
        )
    else:
        keyboard.add(
            ikb(
                _("⬅ Назад", locale=lang),
                callback_data=f"buy_people_category_swipe:0:{remover - 10}:0:0:{city_id}",
            ),
            ikb(
                f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
            ikb(
                _("Далее ➡", locale=lang),
                callback_data=f"buy_people_category_swipe:0:{remover + 10}:0:0:{city_id}",
            ),
        )

    keyboard.add(
        ikb(
            _("⬅ Вернуться ↩", locale=lang),
            callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:0:{level - 1}:0:{city_id}",
        )
    )

    return keyboard

#############################################################################################
####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def position_people_create_open_fp(category_id, remover, level, parent, city_id, action, lang): #+ action = create / open
    print(city_id, action)
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    #if parent == "" or parent is None: parent = 0
    #lang = ctx_user_locale.get()
    #print(lang)
    #user_id = message.from_user.id
    #lang = get_user_lang(user_id)
    '''if category_id != 0:
        get_categories = get_category_in_citypx(parent_id=category_id)
    elif level == 1:
        get_categories = get_category_in_citypx(level=1)
    else:'''

    if action == "open":
        get_categories = get_pm_category_count()
    elif action == "create":
        get_categories = get_category_in_citypx(parent_id=parent)


    print(len(get_categories))
    print(category_id, remover, level, parent, city_id, action, lang)

    count = 0
    if city_id is None: city_id = 0

    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        level = get_categories[a]['level']
        if count < 10:
            position_count_category = get_category_count(get_categories[a]['category_id'])
            if get_categories[a]['level'] == 1 and action == "open":
                keyboard.add(
                    ikb(
                        get_categories[a]['category'],
                        callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:0:0:{get_categories[a]['category_id']}:{city_id}:{action}",
                    )
                )
            elif get_categories[a]['level'] == 2 and action == "create":
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"position_people_create_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}:{lang}"))
            elif get_categories[a]['level'] == 2 and action == "open":
                keyboard.add(ikb(get_categories[a]['category'],
                             callback_data=f"position_people_open_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}:{lang}"))

    if len(get_categories) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(
                f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
            ikb(
                fwdbutton,
                callback_data=f"buy_people_category_swipe:0:{remover + 10}:0:0:{city_id}:{action}",
            ),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb(
                bwdbutton,
                callback_data=f"buy_people_category_swipe:0:{remover - 10}:0:0:{city_id}:{action}",
            ),
            ikb(
                f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
        )
    else:
        keyboard.add(
            ikb(
                bwdbutton,
                callback_data=f"buy_people_category_swipe:0:{remover - 10}:0:0:{city_id}:{action}",
            ),
            ikb(
                f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
            ikb(
                fwdbutton,
                callback_data=f"buy_people_category_swipe:0:{remover + 10}:0:0:{city_id}:{action}",
            ),
        )

    keyboard.add(
        ikb(
            bbutton,
            callback_data=f"buy_people_category_swipe:{get_categories[a]['parent_id']}:0:{level - 1}:0:{city_id}:{action}",
        )
    )

    return keyboard

####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def cources_opcr_fp(category_id, remover, level, parent, city_id, action, lang): #+ action = create / open
    print(category_id, remover, level, parent, city_id, action, lang)
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"

    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_curcategory_in_citypx(parent_id=parent)

    print(len(get_categories))

    count = 0
    if city_id is None: city_id = 0

    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        level = get_categories[a]['level']
        if count < 10:
            if get_categories[a]['level'] == 1:
                keyboard.add(
                    ikb(
                        get_categories[a]['category'],
                        callback_data=f"cources_category_swipe:{get_categories[a]['parent_id']}:0:0:{get_categories[a]['category_id']}:{city_id}:{action}",
                    )
                )
            elif get_categories[a]['level'] == 2 and action == "create":
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"cources_create_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}:{lang}"))
            elif get_categories[a]['level'] == 2 and action == "open":
                keyboard.add(ikb(get_categories[a]['category'],
                                 callback_data=f"cources_open_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}:{lang}"))

    if len(get_categories) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(
                f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
            ikb(
                fwdbutton,
                callback_data=f"cources_category_swipe:0:{remover + 10}:0:0:{city_id}:{action}",
            ),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            ikb(
                bwdbutton,
                callback_data=f"cources_category_swipe:0:{remover - 10}:0:0:{city_id}:{action}",
            ),
            ikb(
                f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
        )
    else:
        keyboard.add(
            ikb(
                bwdbutton,
                callback_data=f"cources_category_swipe:0:{remover - 10}:0:0:{city_id}:{action}",
            ),
            ikb(
                f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸",
                callback_data="...",
            ),
            ikb(
                fwdbutton,
                callback_data=f"cources_category_swipe:0:{remover + 10}:0:0:{city_id}:{action}",
            ),
        )

    keyboard.add(
        ikb(
            bbutton,
            callback_data=f"cources_category_swipe:{get_categories[a]['parent_id']}:0:{level - 1}:0:{city_id}:{action}",
        )
    )

    return keyboard

################################################################################################
################################### СТРАНИЦЫ СОЗДАНИЯ ПОЗИЦИЙ ##################################
# Стартовые страницы выбора категории для добавления позиции
def position_create_open_fp(remover, lang):
    get_categories = get_all_categoriesx()
    if lang == 'en':
        fwdbutton = "Next ➡"

    elif lang == 'ru':
        fwdbutton = "Далее ➡"
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_create_here:{get_categories[a]['category_id']}"))
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_create_nextp:{remover + cpage}:{lang}")
        )

    return keyboard

# Стартовые страницы выбора категории для добавления позиции
def position_select_shop_fp(user_id, lang):
    get_shops = get_all_shopx()
    if lang == 'en':
        fwdbutton = "Next ➡"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
    #get_shops = get_my_shopx(user_id)
    keyboard = InlineKeyboardMarkup()
    remover = 0
    cpage = 10

    for a in range(remover, len(get_shops)):
        keyboard.add(ikb(f"{get_shops[a]['name']}",
                             callback_data=f"here_position_addtoshop:{get_shops[a]['shop_id']}"))
    if len(get_shops) <= 10:
        pass
    elif len(get_shops) > cpage:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_addtoshop_nextp:{remover + cpage}:{lang}")
        )

    return keyboard

# Следующая страница выбора категории для добавления позиции
def position_addtoshop_nextp(remover, lang):
    #get_categories = get_all_categoriesx()
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"

    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_shops))):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['name']}",
                             callback_data=f"here_position_addtoshop:{get_shops[a]['shop_id']}"))
    if remover + cpage >= len(get_shops):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_addtoshop_backp:{remover - cpage}:{lang}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_addtoshop_backp:{remover - cpage}:{lang}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_addtoshop_nextp:{remover + cpage}:{lang}"),
        )

    return keyboard

# Предыдующая страница выбора категории для добавления позиции
def position_addtoshop_backp(remover, lang):
    #get_categories = get_all_categoriesx()
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_shops))):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['category_name']}",
                             callback_data=f"position_create_here:{get_shops[a]['category_id']}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_addtoshop_nextp:{remover + cpage}:{lang}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_addtoshop_backp:{remover - cpage}:{lang}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_addtoshop_nextp:{remover + cpage}:{lang}")
        )

    return keyboard

# Следующая страница выбора категории для добавления позиции
def position_create_next_page_fp2(remover, lang):
    #get_categories = get_all_categoriesx()
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_shops = get_all_shopx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_shops[a]['name']}",
                             callback_data=f"position_create_here:{get_shops[a]['shop_id']}"))
    if remover + cpage >= len(get_shops):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_create_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_create_backp:{remover - cpage}:{lang}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_create_nextp:{remover + cpage}:{lang}"),
        )

    return keyboard

# Следующая страница выбора категории для добавления позиции
def position_create_next_page_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_create_here:{get_categories[a]['category_id']}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_create_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_create_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            #ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸"),
            ikb(fwdbutton, callback_data=f"position_create_nextp:{remover + cpage}")
        )

    return keyboard



# Предыдующая страница выбора категории для добавления позиции
def position_create_back_page_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_create_here:{get_categories[a]['category_id']}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_create_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_create_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_create_nextp:{remover + cpage}")
        )

    return keyboard

################################################################################################
################################## СТРАНИЦЫ ИЗМЕНЕНИЯ ПОЗИЦИЙ ##################################
########################################### Категории ##########################################
# Стартовые страницы категорий при изменении позиции
def position_edit_category_open_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_edit_category:{get_categories[a]['category_id']}"))
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_category_nextp:{remover + cpage}")
        )
    elif remover + cpage >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Следующая страница категорий при изменении позиции
def position_edit_category_next_page_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_edit_category:{get_categories[a]['category_id']}"))
    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Предыдующая страница категорий при изменении позиции
def position_edit_category_back_page_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"position_edit_category:{get_categories[a]['category_id']}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_category_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_category_nextp:{remover + cpage}"),
        )

    return keyboard

########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для их изменения
def position_edit_open_fp(remover, category_id, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"

    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    print(remover, category_id, lang)
    #order
    get_positions = get_positionsx(category_id=category_id)
    #get_positions = get_positionsorder(category_id)
    keyboard = InlineKeyboardMarkup()
    print(get_positions)

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < cpage:
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽", # {len(get_items)} шт",
                callback_data=f"position_edit:{get_positions[a]['position_id']}:{remover}:{category_id}"))
    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}")
        )
    elif remover + cpage >= len(get_positions):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb(bbutton, callback_data="position_edit_category_return"))

    return keyboard

# Следующая страница позиций для их изменения
def position_edit_next_page_fp(remover, category_id, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_positions))):
        if count < cpage:
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ |", # {len(get_items)} шт",
                callback_data=f"position_edit:{get_positions[a]['position_id']}:{remover}:{category_id}"))
    if remover + cpage >= len(get_positions):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb(bbutton, callback_data="position_edit_category_return"))

    return keyboard

# Предыдующая страница позиций для их изменения
def position_edit_back_page_fp(remover, category_id, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_positions))):
        if count < cpage:
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽", # | {len(get_items)} шт",
                callback_data=f"position_edit:{get_positions[a]['position_id']}:{remover}:{category_id}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"position_edit_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"position_edit_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb(bbutton, callback_data="position_edit_category_return"))

    return keyboard

################################################################################################
################################## СТРАНИЦЫ ДОБАВЛЕНИЯ ТОВАРОВ #################################
# Стартовые страницы категорий при добавлении товара
def products_add_category_open_fp(remover, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"products_add_category:{get_categories[a]['category_id']}"))
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_category_nextp:{remover + cpage}")
        )
    elif remover + cpage >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Следующая страница категорий при добавлении товара
def products_add_category_next_page_fp(remover):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"products_add_category:{get_categories[a]['category_id']}"))
    if remover + cpage >= len(get_categories):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_category_nextp:{remover + cpage}"),
        )

    return keyboard

# Предыдующая страница категорий при добавлении товара
def products_add_category_back_page_fp(remover):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_categories))):
        if count < cpage:
            keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                             callback_data=f"products_add_category:{get_categories[a]['category_id']}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_category_nextp:{remover + cpage}")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_category_backp:{remover - cpage}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_category_nextp:{remover + cpage}"),
        )

    return keyboard

########################################### ПОЗИЦИИ ##########################################
# Стартовые страницы позиций для добавления товаров
def products_add_position_open_fp(remover, category_id, lang):
    if lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"
    elif lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_positions))):
        if count < cpage:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"products_add_position:{get_positions[a]['position_id']}:{category_id}"))
    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > cpage and remover < 10:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_position_nextp:{remover + cpage}:{category_id}")
        )
    elif remover + cpage >= len(get_positions):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_position_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_position_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_position_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb(bbutton, callback_data="back_add_products_to_category"))

    return keyboard

################################################################################
##################### Страница подтверждения запроса на продавца ###############
################################################################################

def request_seller_role(user_id, lang):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
            ikb(_("🔸 Запросить права продавца 🔸", locale=lang), callback_data="create_seller_request"))

    return keyboard


#############################################################################################
####################################### ПОКУПКИ ТОВАРОВ #####################################
# Страницы категорий при покупке товара
def products_item_category_swipe_fp(remover, parent_id, city_id, action, lang):
    print(remover, parent_id, city_id, action, lang)
    #get_categories = get_category_in_city(city_id)
    #if parent_id == 0:
    #    get_categories = get_category_in_cityx(level=1)
    #else:
    #category_precount = get_category_count(category_id)['countp']
    #if category_precount == 0:

    '''get_settings = get_settingsx()
    print(get_settings)
    trade_type = get_settings['type_trade']
    if trade_type == "digital":
        city_id = 0
    get_categories = get_categories_in_cityx(parent_id, city_id)''' #, position_city_id=city_id position_type=1, flagallc=1

    get_categories = get_all_categoriesx()
    #lang = get_user_lang(user_id)['user_lang']
    #print(get_categories, len(get_categories))
    #keyboard = InlineKeyboardMarkup()
    #count = 0

    print("LLLLLL9999999")

    if lang == "ru":
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbbutton = "Вверх"
    elif lang == "en":
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbbutton = "Level Up"

    if city_id is None: city_id = 0
    bbtntext = ""

    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories): remover -= 10

    #keyboard.add(ikb(" Барахолка Вашего города ", callback_data="privateMarket"))

    for count, a in enumerate(range(remover, len(get_categories))):
        category_count = get_category_count(get_categories[a]['category_id'])['countp']
        print(count, category_count, action, get_categories[a]['category_name'], get_categories[a]['level'], get_categories[a]['category_id'], city_id, lang)

        if count < 10:
            if get_categories[a]['level'] == 1 and action == "edit" and category_count == 0:
                print("CAT EDIT 2 LEVEL")
                keyboard.add(ikb(f"{get_categories[a]['category_name']}",
                                 callback_data=f"position_edit_category_swipe:{get_categories[a]['category_id']}:{city_id}:{lang}"))

            elif get_categories[a]['level'] == 2 and action == "edit" and category_count > 0 or get_categories[a]['level'] == 1 and category_count > 0 and action == "edit":
                print("CAT EDIT 1 LEVEL")
                keyboard.add(ikb(get_categories[a]['category_name'],
                             callback_data=f"position_edit_category_open:{get_categories[a]['category_id']}:{city_id}:{lang}"))
                bbtntext = ikb(
                    bbbutton,
                    callback_data=f"buy_category_swipe:0:0:{city_id}:{action}",
                )

            elif get_categories[a]['level'] == 1 and category_count == 0 and action in ["open", "edit"]:
                print("way3")
                keyboard.add(ikb(get_categories[a]['category_name'],
                                 callback_data=f"buy_category_swipe:{remover}:{get_categories[a]['category_id']}:{city_id}:{action}"))
                #bbtntext = ikb(bbbutton, callback_data="start")

            elif get_categories[a]['level'] == 2 and action == "create":
                keyboard.add(ikb(get_categories[a]['category_name'],
                                 callback_data=f"position_create_here:{get_categories[a]['category_id']}:{get_categories[a]['parent_id']}:{city_id}:{lang}"))
                #bbtntext = ikb(bbbutton, callback_data=f"buy_category_swipe:{0}:{0}:{city_id}:{action}")

            elif get_categories[a]['level'] == 2 and action == "open" or get_categories[a]['level'] == 1 and action == "open" and category_count > 0:
                print("way5")
                keyboard.add(ikb(get_categories[a]['category_name'],
                                 callback_data=f"buy_category_open:{get_categories[a]['category_id']}:{city_id}"))
                bbtntext = ikb(
                    bbbutton,
                    callback_data=f"buy_category_swipe:0:0:{city_id}:{action}",
                )


    if len(get_categories) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_category_swipe:{remover + 10}:{get_categories[a]['parent_id']}:{city_id}:{action}"),
        )
    elif remover + 10 >= len(get_categories):
        print(len(get_categories))
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_category_swipe:{remover - 10}:{get_categories[a]['parent_id']}:{city_id}:{action}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_category_swipe:{remover - 10}:{get_categories[a]['parent_id']}:{city_id}:{action}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_category_swipe:{remover + 10}:{get_categories[a]['parent_id']}:{city_id}:{action}"),
        )
    keyboard.add(bbtntext)

    return keyboard

# Страницы магазин при покупке товара
def select_place_in_city_swipe_fp(city_id, lang):
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

    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"

    if remover >= len(get_places): remover -= 10
    keyboard.add(
        ikb(
            "🔸 События в Вашем городе🔸",
            callback_data=f"events_city_swipe:0:{city_id}",
        )
    )

    for count, a in enumerate(range(remover, len(get_places))):
        print(get_places[a]['place_id'])
        if count < 10:
            keyboard.add(ikb(get_places[a]['name'], # + " | " + get_places[a]['city_id'],
                             callback_data=f"here_event_place:{get_places[a]['place_id']}"))

    if len(get_places) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_places):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def places_in_city_swipe_fp(remover, city_id, lang):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    #get_events = get_events_in_city(city_id)
    #get_places = get_all_places()
    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"

    print(remover, city_id)
    get_places = get_places_in_cityx(city_id, flagallc=1, position_type=1)
    #get_shops = get_shopsxx()
    print(len(get_places))
    count = 0
    if city_id is None: city_id = 0
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_places): remover -= 10
    keyboard.add(
        ikb(
            "🔸 События в Вашем городе🔸",
            callback_data=f"events_city_swipe:0:{city_id}",
        )
    )

    for count, a in enumerate(range(remover, len(get_places))):
        if count < 10:
            keyboard.add(ikb(get_places[a]['name'], # + " | " + get_places[a]['city'],
                             callback_data=f"book_place_open:{get_places[a]['place_id']}"))

    if len(get_places) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_places):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"places_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_places) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"places_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def events_in_city_swipe_fp(remover, city_id, lang):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    #get_events = get_events_in_city(city_id)
    get_events = get_events_in_cityx(city_id, flagallc=1, position_type=1)
    #get_shops = get_shopsxx()
    print(len(get_events))
    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    #keyboard = InlineKeyboardMarkup()
    count = 0
    #if place_id is None: place_id = 0
    if city_id is None: city_id = 0

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_events): remover -= 10
    keyboard.add(
        ikb(
            "Добавить место или событие, нажмите 🔸",
            callback_data="open_inline_support",
        )
    )
    keyboard.add(
        ikb(
            "🔸 Места в Вашем городе🔸",
            callback_data=f"places_city_swipe:0:{city_id}",
        )
    )

    for count, a in enumerate(range(remover, len(get_events))):
        if count < 10:
            #edate = get_events[a]['event_date'] if get_events[a]['event_date'] else ""
            keyboard.add(
                ikb(
                    get_events[a]['event_name'] + " | ",
                    callback_data=f"book_event_open:{get_events[a]['event_id']}:0:{city_id}",
                )
            )

    if len(get_events) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_events):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def events_in_place_swipe_fp(remover, place_id, city_id, lang):
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
    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
    #keyboard = InlineKeyboardMarkup()
    count = 0
    print(city_id)
    if place_id is None: place_id = 0
    if city_id is None: city_id = 0
    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_events[0]): remover -= 10
    keyboard.add(
        ikb(
            "🔸 Места в Вашем городе🔸",
            callback_data=f"places_city_swipe:0:{city_id}",
        )
    )

    for count, a in enumerate(range(remover, len(get_events))):
        if count < 10:
            keyboard.add(ikb(get_events[a]['event_name'] + " | " + get_events[a]['event_date'],
                             callback_data=f"book_event_open:{get_events[a]['event_id']}:{place_id}:{city_id}"))

    if len(get_events) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_events):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"events_city_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_events) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"events_city_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы магазин при покупке товара
def products_item_shop_swipe_fp(remover, city_id, lang):
    #get_categories = get_category_in_city(city_id)
    #get_categories = get_all_categoriesx()
    get_shops = get_all_shopx()
    get_shops = get_shop_in_cityx(city_id=city_id, position_type=1, flagallc=1)
    #get_shops = get_shopsxx()
    print(len(get_shops))
    #keyboard = InlineKeyboardMarkup()
    count = 0
    if city_id is None: city_id = 0

    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"

    #get_categories = get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_shops): remover -= 10

    for count, a in enumerate(range(remover, len(get_shops))):
        if count < 10:
            keyboard.add(ikb(get_shops[a]['name'],
                             callback_data=f"buy_shop_open:{get_shops[a]['shop_id']}:{city_id}:{lang}"))

    if len(get_shops) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_shops) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_shop_swipe:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_shops):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_shop_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_shops) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_shop_swipe:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_shops) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_shop_swipe:{remover + 10}:{city_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data=f"buy_shop_swipe:0:{city_id}"))
    return keyboard

# Страницы позиций для покупки товаров
def products_item_position_swipe_fp(remover, action, category_id, city_id, source, lang): # + source = people / commercial
    source = str(source)
    if source == "commercial":
        parent_category = get_parent_catc(category_id)[0]
    elif source == "people":
        parent_category = get_parent_cat(category_id)[0]
    print(parent_category)

    #get_positions = get_positionsx(category_id=category_id, position_city_id=city_id)
    get_positions = get_positionsax(category_id, city_id)
    print(remover, category_id, city_id, source, lang)
    print(get_positions)
    position_rest = 0

    keyboard = InlineKeyboardMarkup()
    if lang == "en":
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"

    elif lang == "ru":
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"

    #city_id = сity_id if city_id else 0
    #category_id = category_id if category_id else 0
    #if category_id is None: category_id = 0

    if remover >= len(get_positions): remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            #get_items = len(get_itemsx(position_id=get_positions[a]['position_id']))
            if get_positions[a]['position_type'] == 1: position_rest = get_positions[a]['position_rest']
            if get_positions[a]['position_type'] == 2: position_rest = len(get_itemsx(position_id=get_positions[a]['position_id']))

            if action == "open":
                keyboard.add(ikb(
                    f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽| {position_rest} шт",
                    callback_data=f"buy_position_open:{get_positions[a]['position_id']}:{category_id}:{remover}:{city_id}:{lang}"))
            if action == "edit":
                keyboard.add(ikb(
                    f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽| {position_rest} шт",
                    callback_data=f"position_edit:{get_positions[a]['position_id']}:{category_id}:{remover}:{city_id}:{lang}"))

    if len(get_positions) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_position_swipe:{category_id}:{remover + 10}:{city_id}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_position_swipe:{category_id}:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_position_swipe:{category_id}:{remover - 10}:{city_id}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_position_swipe:{category_id}:{remover + 10}:{city_id}"),
        )
    keyboard.add(
        ikb(
            bbutton,
            callback_data=f"buy_category_swipe:0:{parent_category}:{city_id}:{action}",
        )
    )

    return keyboard

# Следующая страница позиций для добавления товаров
def products_add_position_next_page_fp(remover, category_id, lang):
    get_positions = get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()
    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"

    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < cpage:
            get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"products_add_position:{get_positions[a]['position_id']}:{category_id}"))
    if remover + cpage >= len(get_positions):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_position_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"products_add_position_backp:{remover - cpage}:{category_id}"),
            ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"products_add_position_nextp:{remover + cpage}:{category_id}"),
        )
    keyboard.add(ikb(bbutton, callback_data="back_add_products_to_category"))

    return keyboard

# Страницы позиций для покупки товаров
def products_shopitem_position_swipe_fp(remover, shop_id, city_id, source, lang):
    get_positions = get_positionsx(store_id=shop_id)
    keyboard = InlineKeyboardMarkup()
    print(remover, shop_id, city_id, lang)
    if city_id is None: city_id = 0
    position_rest = 0
    print(lang)
    source = "commercial"
    if lang == 'ru':
        fwdbutton = "Далее ➡"
        bwdbutton = "⬅ Назад"
        bbutton = "⬅ Вернуться ↩"

    elif lang == 'en':
        fwdbutton = "Next ➡"
        bwdbutton = "⬅ Back"
        bbutton = "⬅ Back to UP ↩"

    if remover >= len(get_positions): remover -= 10
    print("||||")

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            if get_positions[a]['position_type'] == 1: position_rest = get_positions[a]['position_rest']
            if get_positions[a]['position_type'] == 2: position_rest = len(get_itemsx(position_id=get_positions[a]['position_id']))

            keyboard.add(ikb(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {position_rest} шт",
                callback_data=f"buy_parposition_open:{get_positions[a]['position_id']}:{shop_id}:{remover}:{city_id}:{lang}"))

    if len(get_positions) <= 10:
        pass
    elif remover < 10:
        keyboard.add(
            ikb(f"🔸 1/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_parposition_swipe:{shop_id}:{remover + 10}:{city_id}:{source}:{lang}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_parposition_swipe:{shop_id}:{remover - 10}:{city_id}:{source}:{lang}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            ikb(bwdbutton, callback_data=f"buy_parposition_swipe:{shop_id}:{remover - 10}:{city_id}:{source}:{lang}"),
            ikb(f"🔸 {str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            ikb(fwdbutton, callback_data=f"buy_parposition_swipe:{shop_id}:{remover + 10}:{city_id}:{source}:{lang}"),
        )
    keyboard.add(ikb(bbutton, callback_data=f"buy_shop_swipe:0:{city_id}:{lang}"))

    return keyboard
