# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.types import Message, User, CallbackQuery
from aiogram.utils.deep_linking import get_start_link, decode_payload

import gettext
from pathlib import Path
from contextvars import ContextVar
from tgbot.data.config import I18N_DOMAIN, LOCALES_DIR, DEFAULT_LANGUAGE

from tgbot.keyboards.inline_user import user_support_finl, open_deep_link_object_finl, lang_menu_finl, lang_menu_ext_finl
from tgbot.keyboards.reply_z_all import menu_frep
from aiogram import Dispatcher
from tgbot.loader import dp
from tgbot.services.api_sqlite import get_settingsx, get_userx, get_positionx, update_userx, get_user_lang
from tgbot.utils.misc.bot_filters import IsBuy, IsRefill, IsWork
from tgbot.utils.misc_functions import get_position_of_day
from tgbot.services.location_function import is_location, add_city
from tgbot.services.lang_function import is_lang
from tgbot.services.location_stat import geo_choice
from tgbot.keyboards.location_keyboards import geo_11_kb
from babel import Locale
from tgbot.middlewares.i18n import I18nMiddleware

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
print(i18n)
_ = i18n.gettext

# Игнор-колбэки покупок
prohibit_buy = ['buy_category_open', 'buy_category_return', 'buy_category_nextp', 'buy_category_backp',
                'buy_shop_open', 'buy_shop_return', 'buy_shop_nextp', 'buy_shop_backp',
                'buy_position_open', 'buy_position_open', 'buy_position_return', 'buy_position_nextp', 'buy_position_backp',
                'buy_purchase_select', 'here_purchase_count', 'xpurchase_item', 'add_item_cart', 'user_cart',
                'enter_address_manualy', 'enter_address_manualy_fin', 'checkout_finally',
                'here_itemsadd_cart', 'xaddcart_item', 'geo_first_letter', 'cart_checkout_start',
                'enter_message_manualy', 'conf_order_addr_saved']
# Игнор-колбэки пополнений
prohibit_refill = ['user_refill', 'refill_choice', 'Pay:', 'Pay:Form', 'Pay:ForYm', 'Pay:Number', 'Pay:Nickname']


####################################################################################################
######################################## ТЕХНИЧЕСКИЕ РАБОТЫ ########################################
# Фильтр на технические работы - сообщение
@dp.message_handler(IsWork(), state="*")
async def filter_work_message(message: Message, state: FSMContext):
    await state.finish()

    user_support = get_settingsx()['misc_support']
    if str(user_support).isdigit():
        get_user = get_userx(user_id=user_support)

        if len(get_user['user_login']) >= 1:
            await message.answer(_("<b>⛔ Бот находится на технических работах.</b>", locale=lang),
                                 reply_markup=user_support_finl(get_user['user_login']))
            return

    await message.answer(_("<b>⛔ Бот находится на технических работах.</b>", locale=lang))


# Фильтр на технические работы - колбэк
@dp.callback_query_handler(IsWork(), state="*")
async def filter_work_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(_("⛔ Бот находится на технических работах.", locale=lang), True)

####################################################################################################
########################################### СТАТУС ПОКУПОК #########################################
# Фильтр на доступность покупок - сообщение
@dp.message_handler(IsBuy(), text="🎁 Купить", state="*")
@dp.message_handler(IsBuy(), state="here_purchase_count")
async def filter_buy_message(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(_("<b>⛔ Покупки временно отключены.</b>", locale=lang))

# Фильтр на доступность покупок - колбэк
@dp.callback_query_handler(IsBuy(), text_startswith=prohibit_buy, state="*")
async def filter_buy_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(_("⛔ Покупки временно отключены.", locale=lang), True)


####################################################################################################
######################################### СТАТУС ПОПОЛНЕНИЙ ########################################
# Фильтр на доступность пополнения - сообщение
@dp.message_handler(IsRefill(), state="here_pay_amount")
async def filter_refill_message(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(_("<b>⛔ Пополнение временно отключено.</b>", locale=lang))


# Фильтр на доступность пополнения - колбэк
@dp.callback_query_handler(IsRefill(), text_startswith=prohibit_refill, state="*")
async def filter_refill_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer(_("⛔ Пополнение временно отключено.", locale=lang), True)


####################################################################################################
############################################## ПРОЧЕЕ ##############################################
# В случае - если посетитель идет по deeplink'у или просто стартует
@dp.message_handler(filters.CommandStart())
@dp.message_handler(text=['⬅ Main Menu', '⬅ Главное меню', '/start', '⬆️ Выбрать город позже', 'start'], state="*")
async def main_start(message: Message, state: FSMContext):
    print(message.text)
    if args := message.get_args():
        payload = decode_payload(args)
        list = payload.split("&")
        print(list)
        category_id = 0
        object_id = 0
        print(list[0])
        object_id = list[2]
        position = get_positionx(position_id=object_id)
        user = get_userx(user_id=message.from_user.id)
        print(position)
        print(user)
        remover= 0
        city_id = 34
        category_id = position['category_id']
        await message.answer("🔸 Открываем объект по внешней ссылке.\n"
                             "▶ Добро пожаловать в TelegramGoodsinbot!",
                             reply_markup=open_deep_link_object_finl(object_id, category_id, remover, city_id))

    get_settings = get_settingsx()
    type_trade = get_settings['type_trade']

    if is_lang(message.from_user.id) == False:
        lang = DEFAULT_LANGUAGE
        await message.answer("Выберите язык", reply_markup=lang_menu_finl(lang))
    else:
        lang = get_userx(user_id=message.from_user.id)['user_lang']
        await message.answer(f"Ваш язык: {lang}", reply_markup=menu_frep(message.from_user.id, lang)) #lang_menu_finl()

    if type_trade in ['hybrid', 'real']:
        print("loco is not present")
        print("hybrid|real")
        if message.text == '⬆️ Выбрать город позже':
            add_city(1, "Москва", message.from_user.id)
            await message.answer("🔸 Город не определен. Вам показываются позиции в городе Москва.\n"
                                 "🔸 Бот готов к использованию.\n"
                                 "🔸 Если не появились вспомогательные кнопки.\n"
                                 "▶ Введите /start",
                                 reply_markup=menu_frep(message.from_user.id, lang))

        elif is_location(message.from_user.id) == True:
            print("loco is present")
            await message.answer(f"🔸 Город определен. Бот готов к использованию.\n"
                                 "🔸 Выберите один из разделов[Купить, Продать, Магазины, Афиша].\n"
                                 "🔸 Если не появились вспомогательные кнопки.\n"
                                 "▶ Введите /start",
                                 reply_markup=menu_frep(message.from_user.id, lang))
        else:
            await geo_choice.location.set()
            await message.answer('Отправьте локацию или выберите город из списка', reply_markup=geo_11_kb())

    elif type_trade == 'digital':
        await message.answer("🔸 Режим Digital. Бот готов к использованию.\n"
                             "🔸 Если не появились вспомогательные кнопки.\n"
                             "▶ Введите /start",
                             reply_markup=menu_frep(message.from_user.id, lang))

@dp.message_handler(commands='lang')
async def cmd_lang(message: Message):
    lang = get_userx(user_id=message.from_user.id)['user_lang']
    await message.answer("Выберите язык: ", reply_markup=lang_menu_finl(lang))

@dp.message_handler(commands='edit_location')
async def cmd_location(message: Message):
    await geo_choice.location.set()
    #lang = get_userx(user_id=message.from_user.id)['user_lang']
    await message.answer("Выберите Ваш город: ", reply_markup=geo_11_kb())

@dp.callback_query_handler(text_startswith="lang", state="*")
async def language_was_selected(call: CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[1]
    if lang in ('ru', 'en'):
        if lang == 'ru':
            locale = Locale('ru', 'RU')
            yourl = "Ваш язык "
        if lang == 'en':
            locale = Locale('en', 'US')
            yourl = "Your Language "

        print(call.from_user.id, lang)
        update_userx(call.from_user.id, user_lang = lang)

        state = Dispatcher.get_current().current_state()
        await state.update_data(locale=locale)

        print(locale.language, locale.language_name)
        lang = get_userx(user_id=call.from_user.id)['user_lang']

        await call.answer(f"{lang}")
        await call.message.answer(f"{yourl} : {lang}", reply_markup=menu_frep(call.from_user.id, lang))
    else: print("Такого языка нет.-*")
