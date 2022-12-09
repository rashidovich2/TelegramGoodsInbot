# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup

from tgbot.data.config import get_admins, get_shopadmins
from tgbot.services.api_sqlite import get_userx, check_user_shop_exist

# Кнопки главного меню
def menu_frep(user_id):
    user_role=get_userx(user_id=user_id)
    if user_role is None:
        user_role = "User"
    else:
        user_role=user_role['user_role']

    print(user_role)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🎁 Купить", "🎁 Магазины", "👤 Профиль", "🧮 Корзина")

    if user_role is None or user_role == "":
        keyboard.row("☎ Поддержка", "Я продавец", "💰 Пополнить")

    if user_id in get_admins():
        keyboard.row("🎁 Управление товарами 🖍", "📊 Статистика")
        keyboard.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
        keyboard.row("Запросы продавцов", "📊 Отчет о продажах")

    if user_id in get_shopadmins():
        #print(f'вывод меню reply_z_all.py 28')
        keyboard.row("☎ Поддержка", "💰 Пополнить")
        keyboard.row("🎁 Управление товарами дмаг.🖍", "🔑 Платежные системы") #, "🧮 Корзина") #, "🔑 Платежные системы") #, "📊 Статистика")
        #keyboard.row("⚙ Настройки", "🔆 Общие функции", "🔑 Платежные системы")
        #keyboard.row("Запросы продавцов", "Управление магазинами")

    return keyboard


# Кнопки продавца
def shop_admin_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отправить заявку")
    keyboard.row("⬅ Главное меню")

    return keyboard

# Кнопки платежных систем
def payments_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🥝 Изменить QIWI 🖍", "🥝 Проверить QIWI ♻", "🥝 Баланс QIWI 👁")
    keyboard.row("⬅ Главное меню", "💳 Изменить Yoo 🖍", "🖲 Способы пополнения")

    return keyboard


# Кнопки общих функций
def functions_frep(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("👤 Поиск профиля 🔍", "📢 Рассылка", "🧾 Поиск чеков 🔍")
    keyboard.row("⬅ Главное меню")

    return keyboard


# Кнопки запросов в продавцы
def seller_requests_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🖍 Посмотреть запросы")
    keyboard.row("⬅ Главное меню")

    return keyboard

# Кнопки настроек
def settings_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🖍 Изменить данные", "🕹 Выключатели")
    keyboard.row("⬅ Главное меню")

    return keyboard

# Кнопки изменения товаров
def items_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🎁 Добавить товары ➕", "🎁 Удалить товары 🖍", "🎁 Удалить все товары ❌")
    keyboard.row("📁 Создать позицию ➕", "📁 Изменить позицию 🖍", "📁 Удалить все позиции ❌")
    keyboard.row("🗃 Создать категорию ➕", "🗃 Изменить категорию 🖍", "🗃 Удалить все категории ❌")
    keyboard.row("🏪 Создать магазин ➕", "🏪 Изменить магазин 🖍", "🏪 Удалить все магазины ❌")
    keyboard.row("⬅ Главное меню")

    return keyboard

# Кнопки изменения товаров
def items_sh_frep():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🎁 Добавить товары ➕", "🎁 Удалить товары 🖍", "🎁 Удалить все товары ❌")
    keyboard.row("📁 Создать позицию ➕", "📁 Изменить позицию 🖍", "📁 Удалить все позиции ❌")
    #keyboard.row("🗃 Создать категорию ➕", "🗃 Изменить категорию 🖍") #, "🗃 Удалить все категории ❌")
    #user_id = message.from_user.id
    #if check_user_shop_exist(message.from_user.id) == 'True':
    #keyboard.row("🏪 Изменить магазин 🖍") #, "🏪 Удалить все магазины ❌")
    #if check_user_shop_exist(message.from_user.id) == 'False':
    keyboard.row("🏪 Создать магазин ➕", "🏪 Изменить магазин 🖍")  # , "🏪 Удалить все магазины ❌")
    keyboard.row("⬅ Главное меню")

    return keyboard

# Завершение загрузки товаров
finish_load_rep = ReplyKeyboardMarkup(resize_keyboard=True)
finish_load_rep.row("📥 Закончить загрузку товаров")
