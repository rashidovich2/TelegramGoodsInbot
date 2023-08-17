# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.data.config import BOT_VERSION, PATH_LOGS, PATH_DATABASE
from tgbot.keyboards.reply_z_all import payments_frep, settings_frep, functions_frep, items_frep, seller_requests_frep
from tgbot.loader import dp
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
from tgbot.middlewares.i18n import I18nMiddleware
from tgbot.services.api_sqlite import get_all_usersx, get_top_sellersx, get_userx
from tgbot.utils.const_functions import get_date
from tgbot.utils.misc.bot_filters import IsAdmin, IsAdminorShopAdmin
from tgbot.utils.misc_functions import get_statisctics

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext

# Платежные системы
@dp.message_handler(text=["🔑 Платежные системы", "🔑 Payment Systems"], state="*")
async def admin_payment(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        await message.answer(_("<b>🔑 Настройка платежных систем.</b>", locale=lang), reply_markup=payments_frep(lang))


# Настройки бота
@dp.message_handler(IsAdmin(), text=["⚙ Настройки", "⚙ Settings"], state="*")
async def admin_settings(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        await message.answer(_("<b>⚙ Основные настройки бота.</b>", locale=lang), reply_markup=settings_frep(lang))


# Запросы продавцов
@dp.message_handler(text=["Запросы продавцов", "Sellers Request"],state="*")
async def admin_requests(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin']:
        await message.answer(_("<b>⚙ Запросы продавцов.</b>", locale=lang), reply_markup=seller_requests_frep(lang))


# Общие функции
@dp.message_handler(text=["🔆 Общие функции", "🔆 General Functions"], state="*") #, "🔆 General Functions"
async def admin_functions(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        print(lang)
        await state.finish()
        await message.answer(_("<b>🔆 Выберите нужную функцию.</b>", locale=lang), reply_markup=functions_frep(lang))


# Управление товарами
@dp.message_handler(text=["🎁 Управление товарами 🖍", "🎁 Products Management 🖍"], state="*")
async def admin_products(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(user_role)
    if user_role in ['Admin', 'ShopAdmin']:
        print(lang)
        await state.finish()
        await message.answer("<b>🎁 Редактирование товаров.</b>", reply_markup=items_frep(lang))


# Cтатистики бота
@dp.message_handler(text=["📊 Статистика", "📊 Statistic"], state="*")
async def admin_statistics(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        lang = get_userx(user_id=user_id)['user_lang']
        print(lang)
        await state.finish()
        await message.answer(get_statisctics(lang))


# Получение БД
@dp.message_handler(IsAdmin(), commands=['db', 'database'], state="*")
async def admin_database(message: Message, state: FSMContext):
    await state.finish()

    with open(PATH_DATABASE, "rb") as document:
        await message.answer_document(document,
                                      caption=f"<b>📦 BACKUP\n"
                                              f"🕰 <code>{get_date()}</code></b>")


# Получение Логов
@dp.message_handler(IsAdmin(), commands=['log', 'logs'], state="*")
async def admin_log(message: Message, state: FSMContext):
    await state.finish()

    with open(PATH_LOGS, "rb") as document:
        await message.answer_document(document,
                                      caption=f"<b>🖨 LOGS\n"
                                              f"🕰 <code>{get_date()}</code></b>")


# Получение версии бота
@dp.message_handler(commands=['version', 'log'], state="*")
async def admin_version(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(f"<b>❇ Текущая версия бота: <code>{BOT_VERSION}</code></b>")
