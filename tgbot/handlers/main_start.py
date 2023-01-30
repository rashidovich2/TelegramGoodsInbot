# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import get_start_link, decode_payload

from tgbot.keyboards.inline_user import user_support_finl, open_deep_link_object_finl
from tgbot.keyboards.reply_z_all import menu_frep
from tgbot.loader import dp
from tgbot.services.api_sqlite import get_settingsx, get_userx, get_positionx
from tgbot.utils.misc.bot_filters import IsBuy, IsRefill, IsWork
from tgbot.utils.misc_functions import get_position_of_day
from tgbot.services.location_function import is_location
from tgbot.services.location_stat import geo_choice
from tgbot.keyboards.location_keyboards import geo_11_kb

#from tgbot.services.user_seller_function import is_seller
#from tgbot.keyboards.user_seller_keyboards import geo_1_kb

# Игнор-колбэки покупок
prohibit_buy = ['buy_category_open', 'buy_category_return', 'buy_category_nextp', 'buy_category_backp',
                'buy_shop_open', 'buy_shop_return', 'buy_shop_nextp', 'buy_shop_backp',
                'buy_position_open', 'buy_position_open', 'buy_position_return', 'buy_position_nextp', 'buy_position_backp',
                'buy_purchase_select', 'here_purchase_count', 'xpurchase_item', 'add_item_cart', 'user_cart',
                'enter_address_manualy', 'enter_address_manualy_fin', 'checkout_finally',
                'here_itemsadd_cart', 'xaddcart_item', 'geo_first_letter', 'cart_checkout_start',
                'enter_message_manualy', 'conf_order_addr_saved']
#'add_item_cart', 'enter_address_manualy', 'enter_address_manualy_fin',
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
            await message.answer("<b>⛔ Бот находится на технических работах.</b>",
                                 reply_markup=user_support_finl(get_user['user_login']))
            return

    await message.answer("<b>⛔ Бот находится на технических работах.</b>")


# Фильтр на технические работы - колбэк
@dp.callback_query_handler(IsWork(), state="*")
async def filter_work_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer("⛔ Бот находится на технических работах.", True)

####################################################################################################
########################################### СТАТУС ПОКУПОК #########################################
# Фильтр на доступность покупок - сообщение
@dp.message_handler(IsBuy(), text="🎁 Купить", state="*")
@dp.message_handler(IsBuy(), state="here_purchase_count")
async def filter_buy_message(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>⛔ Покупки временно отключены.</b>")

# Фильтр на доступность покупок - колбэк
@dp.callback_query_handler(IsBuy(), text_startswith=prohibit_buy, state="*")
async def filter_buy_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer("⛔ Покупки временно отключены.", True)


####################################################################################################
######################################### СТАТУС ПОПОЛНЕНИЙ ########################################
# Фильтр на доступность пополнения - сообщение
@dp.message_handler(IsRefill(), state="here_pay_amount")
async def filter_refill_message(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>⛔ Пополнение временно отключено.</b>")


# Фильтр на доступность пополнения - колбэк
@dp.callback_query_handler(IsRefill(), text_startswith=prohibit_refill, state="*")
async def filter_refill_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.answer("⛔ Пополнение временно отключено.", True)


####################################################################################################
############################################## ПРОЧЕЕ ##############################################
# В случае - если посетитель идет по deeplink'у
'''@dp.message_handler(filters.CommandStart(deep_link='deep_link'))
async def deep_link(message: Message):
    await message.answer('Да, знаем мы такое:' + message.text)
    args = message.get_args()
    reference = decode_payload(args)
    if reference : print(reference)

@dp.message_handler(filters.CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f'Ну привет, хотел чего?')'''

''''@dp.message.register(main_start, CommandStart(deep_link=True, command_magic=filters.args.regexp(r"u(\d+)")))
async def deep_link(message: Message):
    await message.answer('Да, знаем мы такое:' + message.text)
    args = message.get_args()
    reference = decode_payload(args)
    if reference : print(reference)'''

# Открытие главного меню
#@dp.message_handler(text=['start'], state="*")
''''@dp.message_handler(filters.CommandStart())
async def deep_link(message: Message):
    args = message.get_args()
    payload = decode_payload(args)
    print(payload.split("&"))

    await message.answer(f"Your payload: {payload}")'''

# Открытие главного меню
@dp.message_handler(filters.CommandStart())
async def main_start(message: Message, state: FSMContext):
    #await state.finish()
    args = message.get_args()
    payload = decode_payload(args)
    #print(payload)
    list = payload.split("&")
    print(list)
    #print(payload[1].split('='))
    #if payload[1] != "":
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

#@dp.message_handler(filters.CommandStart())
@dp.message_handler(text=['⬅ Главное меню', '/start', '⬆️ Выбрать город позже', 'start'], state="*")
async def main_start(message: Message, state: FSMContext):
    #await state.finish()
    '''args = message.get_args()
    payload = decode_payload(args)
    print(payload.split("&"))
    #print(payload[1].split('='))
    #if payload[1] != "":
    category_id=0
    object_id = 0
    if payload:
        for arg in payload:
            x =+ 1
            if x == 1: object = arg
            if x == 2:
                object_id = arg
                position = get_positionx(position_id=object_id)
                user = get_userx(user_id=message.from_user.id)
                print(position)
                print(user['city_id'])
                remover= 0
                city_id = 34
                category_id = position['category_id']
        await message.answer("🔸 Открываем объект по внешней ссылке.\n"
                             "▶ Добро пожаловать в TelegramGoodsinbot!",
                             reply_markup=open_deep_link_object_finl(object_id, category_id, remover, city_id))'''

    #await message.answer(f"Your payload: {payload}")
    get_settings = get_settingsx()
    type_trade = get_settings['type_trade']

    if type_trade == 'hybrid' or type_trade == 'real':
        if message.text == '⬆️ Выбрать город позже':
            await message.answer("🔸 Город не определен. Бот готов к использованию.\n"
                                 "🔸 Если не появились вспомогательные кнопки.\n"
                                 "▶ Введите /start",
                                 reply_markup=menu_frep(message.from_user.id))

        else:
            if is_location(message.from_user.id) == True:

                await message.answer(f"🔸 Город определен. Бот готов к использованию.\n"
                                     "🔸 Если не появились вспомогательные кнопки.\n"
                                     "▶ Введите /start",
                                     reply_markup=menu_frep(message.from_user.id))
            else:
                await geo_choice.location.set()
                await message.answer('Отправьте локацию или выберите город из списка', reply_markup=geo_11_kb())

    elif type_trade == 'digital':
        await message.answer("🔸 Режим Digital. Бот готов к использованию.\n"
                             "🔸 Если не появились вспомогательные кнопки.\n"
                             "▶ Введите /start",
                             reply_markup=menu_frep(message.from_user.id))
