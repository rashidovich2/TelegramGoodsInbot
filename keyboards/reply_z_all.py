# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from tgbot.data.config import get_admins, get_shopadmins
from tgbot.services.api_sqlite import get_userx, check_user_shop_exist, get_user_lang
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
#from tgbot.middlewares.i18n import I18nMiddleware
#i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
#I18nMiddleware.setup_middlewares(i18n)
#print(i18n)
# Alias for gettext method
#_ = i18n.gettext


# Кнопки главного меню
def menu_frep(user_id, lang):
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = "User" if user_role is None else user_role

    if lang == 'en':
        buybtn = "🎁 Buy"
        sellbtn = "🌐 Sell"
        shopbtn = "🎁 Shops"
        enbtn = "🏫 Cources"
        entbtn = "Events"
        vacancies = "💼 Create Vacancy"
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

    elif lang == 'ru':
        buybtn = "🎁 Купить"
        sellbtn = "🌐 Продать"
        shopbtn = "🎁 Магазины"
        enbtn = "🏫 Кружки"
        entbtn = "Афиша"
        vacancies = "💼 Создать вакансию"
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

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(buybtn, tubtn)
    #keyboard.row(buybtn, sellbtn)
    #keyboard.row(vacancies)
    #keyboard.row(shopbtn, stbtn, entbtn)
    #keyboard.row(ptfbtn)

    if user_role is None or user_role == "User":
        keyboard.row(ptfbtn, supbtn)
        #keyboard.row(vacancies)

    if user_role == "Admin":
        keyboard.row(pmbtn, ptfbtn, stabtn)
        #keyboard.row(vacancies, enbtn)
        keyboard.row(stbtn, psbtn, ufbtn)
        keyboard.row(srbtn)

    elif user_role == "ShopAdmin":
        #keyboard.row(supbtn)
        keyboard.row(pmbtn, psbtn)

    return keyboard

# Кнопки продавца
def lang_menu_frep(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🇷🇺 Русский","🇬🇧 English")

    return keyboard

# Кнопки продавца
def shop_admin_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'en':
        sabtn = "Send Request"
        mmbtn = "⬅ Main Menu"

    elif lang == 'ru':
        sabtn = "Отправить заявку"
        mmbtn = "⬅ Главное меню"
    keyboard.row(sabtn)
    keyboard.row(mmbtn)

    return keyboard


# Кнопки платежных систем
def payments_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'en':
        chqbtn = "₮ Tether Address"
        chtrbtn = "TRX, Tron(Trc20) Address"
        chkqbtn = "₿, Bitcoin(Bep-20) Address"
        bqbtn = "Change Card Number"
        mmbtn = "⬅ Main Menu"
        chybtn = "💳 Change Yoo 🖍"
        pmbtn = "🖲 Payment Methods"

    elif lang == 'ru':
        chqbtn = "₮ Tether адрес"
        chtrbtn = "TRX, Tron(Trc20) адрес"
        chkqbtn = "₿, Bitcoin(Bep-20) адрес"
        bqbtn = "Изменить номер карты"
        mmbtn = "⬅ Главное меню"
        chybtn = "💳 Изменить Yoo 🖍"
        pmbtn = "🖲 Способы пополнения"
    #keyboard.row(chqbtn, chkqbtn)
    keyboard.row(chqbtn, bqbtn)
    #keyboard.row(chtrbtn, bqbtn)
    keyboard.row(mmbtn, pmbtn)

    return keyboard


# Кнопки общих функций
def functions_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'en':
        fpbtn = "🔍 Find Profile"
        mslbtn = "📢 MassSendlite"
        msbtn = "📢 Mass Send"
        fabtn = "🧾 Fund Adds"
        fcbtn = "🧾 Find Checks 🔍"
        vabtn = "🧾 Vacancies Approval"
        сhgrbtn = "🧾 Groups and Channels for Posting"
        mmbtn = "⬅ Main Menu"

    elif lang == 'ru':
        fpbtn = "🔍 Поиск профиля"
        msbtn = "📢 Рассылка"
        mslbtn = "📢 Рассылка_lite"
        fabtn = "🧾 Пополнения"
        fcbtn = "🧾 Поиск чеков 🔍"
        vabtn = "🧾 Cогласование вакансий"
        сhgrbtn = "🧾 Каналы и группы для постинга"
        mmbtn = "⬅ Главное меню"
    keyboard.row(fpbtn)
    #keyboard.row(vabtn, сhgrbtn)
    keyboard.row(mslbtn, fabtn)
    keyboard.row(mmbtn)

    return keyboard


# Кнопки запросов в продавцы
def fund_adds_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        keyboard.row("🧾 Ожидают подтверждения", "🧾 Успешные")
        keyboard.row("⬅ Главное меню")
    if lang == 'en':
        keyboard.row("🧾 Wait Confirmation", "🧾 Success")
        keyboard.row("⬅ Main Menu")

    return keyboard


# Кнопки запросов в продавцы
def vacposition_post_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        #keyboard.row("🖍 Посмотреть запросы")
        keyboard.row("🖍 Вакансии Созданные", "🖍 Вакансии Согласованные", "🖍 Вакансии Опубликованные", "🖍 Вакансии в Вещании")
        keyboard.row("⬅ Главное меню")
    if lang == 'en':
        #keyboard.row("🖍 Show list requests")
        keyboard.row("🖍 Positions Created", "🖍 Positions Approved", "🖍 Positions Posted", "🖍 Positions in Broadcasting")
        keyboard.row("⬅ Main Menu")

    return keyboard

# Кнопки запросов в продавцы
def seller_requests_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == 'ru':
        #keyboard.row("🖍 Посмотреть запросы")
        keyboard.row("🖍 запросы Created", "🖍 запросы Approved")
        keyboard.row("⬅ Главное меню")
    if lang == 'en':
        #keyboard.row("🖍 Show list requests")
        keyboard.row("🖍 requests Created", "🖍 requests Approved")
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

    elif lang == 'ru':
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

    keyboard.row(cebtn, chbtn, dabtn)
    keyboard.row(cpbtn, chpbtn, dapbtn)
    keyboard.row(cabtn, chabtn, daabtn)
    keyboard.row(mmbtn)

    return keyboard


# Кнопки изменения товаров
def items_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    print(lang)
    if lang == 'en':
        apbtn = "🎁 Add Goods➕"
        dpbtn = "🎁 Delete Goods 🖍"
        dapbtn = "🎁 Delete All Goods ❌"
        cpbtn = "📁 Create Position ➕"
        chpbtn = "📁 Edit Position 🖍"
        dagbtn = "📁 Delete all Positions ❌"
        ccbtn = "🗃 Create Category ➕"
        chcbtn = "🗃 Edit Category 🖍"
        dacbtn = "🗃 Delete all Categories ❌"
        cshbtn = "🏪 Create Shop ➕"
        chbtn = "🏪 Edit Shop 🖍"
        dashbtn = "🏪 Delete all Shops ❌"
        mmbtn = "⬅ Main Menu"

    elif lang == 'ru':
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
    keyboard.row(apbtn, dpbtn, dapbtn)
    keyboard.row(cpbtn, chpbtn, dagbtn)
    keyboard.row(ccbtn, chcbtn, dacbtn)
    keyboard.row(cshbtn, chbtn, dashbtn)
    keyboard.row(mmbtn)

    return keyboard

# Кнопки изменения товаров
def items_sh_frep(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
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

    elif lang == 'ru':
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
