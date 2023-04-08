# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from tgbot.data.config import get_admins, get_shopadmins
from tgbot.services.api_sqlite import get_userx, check_user_shop_exist, get_user_lang
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
from tgbot.middlewares.i18n import I18nMiddleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
#I18nMiddleware.setup_middlewares(i18n)
#print(i18n)
# Alias for gettext method
#_ = i18n.gettext


# Кнопки главного меню
def menu_frep(user_id, lang):
    user_role=get_userx(user_id=user_id)
    lang = get_user_lang(user_id)['user_lang']
    print(lang)
    user_role = "User" if user_role is None else user_role['user_role']
    print(user_role)

    if lang == 'ru':
        buybtn = "🎁 Купить"
        sellbtn = "🌐 Продать"
        shopbtn = "🎁 Магазины"
        enbtn = "🏫 Кружки"
        entbtn = "Афиша"
        ptfbtn = "👤 Профиль"
        tubtn = "💰 Пополнить"
        crtbtn = "🧮 Корзина"
        supbtn = "☎ Поддержка"
        isbtn = "Я продавец"
        esbtn = "Админ Афиши"
        stabtn = "📊 Статистика"
        prtbtn = "Партнеры"
        pmbtn = "🎁 Управление товарами 🖍"
        stbtn = "⚙ Настройки"
        embtn = "🎫 Управление событиями 🖍"
        ufbtn = "🔆 Общие функции"
        psbtn = "🔑 Платежные системы"
        rsbtn = "Запросы продавцов"
        obtn = "🚛 Заказы"
        srbtn = "📊 Отчет о продажах"

    if lang == 'en':
        buybtn = "🎁 Buy"
        sellbtn = "🌐 Sell"
        shopbtn = "🎁 Shops"
        enbtn = "🏫 Cources"
        entbtn = "Events"
        ptfbtn = "👤 Profile"
        tubtn = "💰 Top Up"
        crtbtn = "🧮 Cart"
        supbtn = "☎ Support"
        isbtn = "I'm seller"
        esbtn = "Events Admin"
        stabtn = "📊 Statistic"
        prtbtn = "Partners"
        pmbtn = "🎁 Products Management 🖍"
        stbtn = "⚙ Settings"
        embtn = "🎫 Events Management 🖍"
        ufbtn = "🔆 General Functions"
        psbtn = "🔑 Payment Systems"
        rsbtn = "Sellers Request"
        obtn = "🚛 Orders"
        srbtn = "📊 Sales Report"

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(buybtn, sellbtn) # enbtn
    keyboard.row(shopbtn, entbtn)
    keyboard.row(ptfbtn, tubtn, crtbtn)

    if user_role is None or user_role == "":
        keyboard.row(supbtn, isbtn, esbtn, prtbtn)

    if user_role == "Admin": #in get_admins():
        keyboard.row(pmbtn, stabtn, prtbtn)
        keyboard.row(stbtn, embtn, ufbtn, psbtn)
        keyboard.row(rsbtn, obtn, srbtn)

    if user_role == "ShopAdmin":
        #print(f'вывод меню reply_z_all.py 28')
        keyboard.row(supbtn, prtbtn)
        keyboard.row(pmbtn, psbtn) #, "🧮 Корзина") #, "🔑 Платежные системы") #, "📊 Статистика")
        #keyboard.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
        #keyboard.row("Запросы продавцов", "Управление магазинами")

    return keyboard

# Кнопки продавца
def lang_menu_frep(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🇷🇺 Русский","🇬🇧 English")

    return keyboard

# Кнопки продавца
def shop_admin_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        sabtn = "Отправить заявку"
        mmbtn = "⬅ Главное меню"
    if lang == 'en':
        sabtn = "Send Request"
        mmbtn = "⬅ Main Menu"

    keyboard.row(sabtn) #"Отправить заявку"
    keyboard.row(mmbtn)

    return keyboard


# Кнопки платежных систем
def payments_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        chqbtn = "🥝 Изменить QIWI 🖍"
        chkqbtn = "🥝 Проверить QIWI ♻"
        bqbtn = "🥝 Баланс QIWI 👁"
        mmbtn = "⬅ Главное меню"
        chybtn = "💳 Изменить Yoo 🖍"
        pmbtn = "🖲 Способы пополнения"
    if lang == 'en':
        chqbtn = "🥝 Change QIWI 🖍"
        chkqbtn = "🥝 Check QIWI ♻"
        bqbtn = "🥝 Balance QIWI 👁"
        mmbtn = "⬅ Main Menu"
        chybtn = "💳 Change Yoo 🖍"
        pmbtn = "🖲 Payment Methods"

    keyboard.row(chqbtn, chkqbtn, bqbtn)
    keyboard.row(mmbtn, chybtn, pmbtn)

    return keyboard


# Кнопки общих функций
def functions_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        fpbtn = "👤 Поиск профиля 🔍"
        msbtn = "📢 Рассылка"
        fcbtn = "🧾 Поиск чеков 🔍"
        mmbtn = "⬅ Главное меню"
    if lang == 'en':
        fpbtn = "👤 Find Profile 🔍"
        msbtn = "📢 Mass Send"
        fcbtn = "🧾 Find Checks 🔍"
        mmbtn = "⬅ Main Menu"

    keyboard.row(fpbtn, fcbtn)
    keyboard.row(msbtn)
    keyboard.row(mmbtn)

    return keyboard

# Кнопки запросов в продавцы
def seller_requests_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        keyboard.row("🖍 Посмотреть запросы")
        keyboard.row("⬅ Главное меню")
    if lang == 'en':
        keyboard.row("🖍 Show list requests")
        keyboard.row("⬅ Main Menu")

    return keyboard

# Кнопки настроек
def settings_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    print(lang)
    if lang == 'ru':
        keyboard.row("🖍 Изменить данные", "🕹 Выключатели")
        keyboard.row("⬅ Главное меню")
    if lang == 'en':
        keyboard.row("🖍 Edit data", "🕹 Switches")
        keyboard.row("⬅ Main Menu")

    return keyboard

# Кнопки изменения товаров
def events_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    print(lang)
    if lang == 'ru':
        cebtn = "📁 Создать событие ➕"
        chbtn = "📁 Изменить событие 🖍"
        dabtn = "📁 Удалить все события ❌"
        cpbtn = "🗃 Создать место ➕"
        chpbtn = "🗃 Изменить место 🖍"
        dapbtn = "🗃 Удалить все места ❌"
        cabtn = "🏪 Создать артиста ➕"
        chabtn = "🏪 Изменить артиста 🖍"
        daabtn = "🏪 Удалить всех артистов ❌"
        mmbtn = "⬅ Главное меню"

    if lang == 'en':
        cebtn = "📁 Create Event ➕"
        chbtn = "📁 Edit Event 🖍"
        dabtn = "📁 Delete all Events ❌"
        cpbtn = "🗃 Create Place ➕"
        chpbtn = "🗃 Edit Place 🖍"
        dapbtn = "🗃 Delete all Places ❌"
        cabtn = "🏪 Create Artist ➕"
        chabtn = "🏪 Edit Artist 🖍"
        daabtn = "🏪 Delete all Artists ❌"
        mmbtn = "⬅ Main Menu"

    keyboard.row(cebtn, chbtn, dabtn)
    keyboard.row(cpbtn, chpbtn, dapbtn)
    keyboard.row(cabtn, chabtn, daabtn)
    keyboard.row(mmbtn)

    return keyboard


# Кнопки изменения товаров
def items_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    print(lang)
    if lang == 'ru':
        apbtn = "🎁 Добавить товары ➕"
        dpbtn = "🎁 Удалить товары 🖍"
        dapbtn = "🎁 Удалить все товары ❌"
        cpbtn = "📁 Создать позицию ➕"
        chpbtn = "📁 Изменить позицию 🖍"
        dagbtn = "📁 Удалить все позиции ❌"
        ccbtn = "🗃 Создать категорию ➕"
        chcbtn = "🗃 Изменить категорию 🖍"
        dacbtn = "🗃 Удалить все категории ❌"
        cshbtn = "🏪 Создать магазин ➕"
        chbtn = "🏪 Изменить магазин 🖍"
        dashbtn = "🏪 Удалить все магазины ❌"
        mmbtn = "⬅ Главное меню"
    if lang == 'en':
        apbtn = "🎁 Add Goods➕"
        dpbtn = "🎁 Delete Goods 🖍"
        dapbtn = "🎁 Delete All Goods ❌"
        cpbtn = "📁 Create position ➕"
        chpbtn = "📁 Edit position 🖍"
        dagbtn = "📁 Delete all positions ❌"
        ccbtn = "🗃 Create category ➕"
        chcbtn = "🗃 Edit category 🖍"
        dacbtn = "🗃 Delete all categories ❌"
        cshbtn = "🏪 Create shop ➕"
        chbtn = "🏪 Edit shop 🖍"
        dashbtn = "🏪 Delete all shops ❌"
        mmbtn = "⬅ Main Menu"

    keyboard.row(apbtn, dpbtn, dapbtn)
    keyboard.row(cpbtn, chpbtn, dagbtn)
    keyboard.row(ccbtn, chcbtn, dacbtn)
    keyboard.row(cshbtn, chbtn, dashbtn)
    keyboard.row(mmbtn)

    return keyboard

# Кнопки изменения товаров
def items_sh_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        apbtn = "🎁 Добавить товары ➕"
        dpbtn = "🎁 Удалить товары 🖍"
        dapbtn = "🎁 Удалить все товары ❌"
        cpbtn = "📁 Создать позицию ➕"
        chpbtn = "📁 Изменить позицию 🖍"
        dagbtn = "📁 Удалить все позиции ❌"
        ccbtn = "🗃 Создать категорию ➕"
        chcbtn = "🗃 Изменить категорию 🖍"
        dacbtn = "🗃 Удалить все категории ❌"
        cshbtn = "🏪 Создать магазин ➕"
        chbtn = "🏪 Изменить магазин 🖍"
        dashbtn = "🏪 Удалить все магазины ❌"
        mmbtn = "⬅ Главное меню"
    if lang == 'en':
        apbtn = "🎁 Add Goods➕"
        dpbtn = "🎁 Delete Goods 🖍"
        dapbtn = "🎁 Delete All Goods ❌"
        cpbtn = "📁 Create position ➕"
        chpbtn = "📁 Edit position 🖍"
        dagbtn = "📁 Delete all positions ❌"
        ccbtn = "🗃 Create category ➕"
        chcbtn = "🗃 Edit category 🖍"
        dacbtn = "🗃 Delete all categories ❌"
        cshbtn = "🏪 Create shop ➕"
        chbtn = "🏪 Edit shop 🖍"
        dashbtn = "🏪 Delete all shops ❌"
        mmbtn = "⬅ Main Menu"

    keyboard.row(apbtn, dpbtn, dapbtn)
    keyboard.row(cpbtn, chpbtn, dagbtn)
    #keyboard.row("🗃 Создать категорию ➕", "🗃 Изменить категорию 🖍") #, "🗃 Удалить все категории ❌")
    #user_id = message.from_user.id
    #if check_user_shop_exist(message.from_user.id) == 'True':
    #keyboard.row("🏪 Изменить магазин 🖍") #, "🏪 Удалить все магазины ❌")
    #if check_user_shop_exist(message.from_user.id) == 'False':
    keyboard.row(cshbtn, chbtn)  # , "🏪 Удалить все магазины ❌")
    keyboard.row(mmbtn)

    return keyboard

# Завершение загрузки товаров
finish_load_rep = ReplyKeyboardMarkup(resize_keyboard=True)
finish_load_rep.row("📥 Закончить загрузку товаров")
