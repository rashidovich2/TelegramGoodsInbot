# - *- coding: utf- 8 - *-
import asyncio
import json
from aiogram.dispatcher import FSMContext
#from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from tgbot.data.config import BOT_DESCRIPTION
from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl, payment_choice_finl, artist_edit_open_finl
from tgbot.keyboards.inline_user import user_support_finl, products_open_finl, products_confirm_finl, \
    products_addcart_confirm_finl, payment_as_choice_finl, accept_saved_adr, accept_saved_phone, \
    cart_enter_message_finl, give_number_inl, reply_order_message_finl, refill_choice_finl, charge_button_add, switch_category_shop_finl, shop_creation_request_finl, event_open_finl
from tgbot.keyboards.inline_z_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl, confirm_delete_user_cart_inl
from tgbot.keyboards.inline_z_all import refill_open_inl, profile_open_inl, cart_open_created_inl, cart_open_delivery_inl, checkout_step2_accept, order_user_refill, partners_list_inl
from tgbot.keyboards.inline_z_page import *
from tgbot.keyboards.reply_z_all import finish_load_rep
from tgbot.keyboards.reply_z_all import menu_frep, items_sh_frep, events_frep
from tgbot.keyboards.shop_keyboards import shop_edit_open_fp
from tgbot.loader import dp
from tgbot.loader import bot
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_sqlite_shop import *
from tgbot.services.api_sqlite import *
from tgbot.utils.const_functions import get_date, split_messages, get_unix, clear_list
from tgbot.utils.misc.bot_filters import IsShopAdmin, IsAdminorShopAdmin, IsAdmin
from tgbot.utils.misc_functions import user_refill_my, calc_cart_summ, open_cart_my, open_profile_my, upload_text, get_faq, send_admins
from tgbot.utils.misc_functions import get_position_admin, upload_text, get_artist_admin
from tgbot.keyboards.location_keyboards import geo_1_kb
from tgbot.services.location_function import update_position_city, get_city_info, is_location, update_artist_city
from tgbot.services.location_stat import geo_choice
from tgbot.keyboards.location_keyboards import geo_11_kb


async def notify(dp: Dispatcher, msg):
    print('Уведомление!')
    await send_admins(msg, markup="default")
################################################################################################
# Заявка на продавца магазина
# Открытие товаров
@dp.message_handler(text="Я продавец", state="*")
async def user_seller_request(message: Message, state: FSMContext):
    # await state.finish()
    await state.set_state("here_seller_request_direction")
    await message.answer("<b>📁 Введите вид товаров или услуг, которые Вы предлагаете:</b>")


# Открытие товаров
@dp.message_handler(text="Админ Афиши", state="*")
async def user_seller_request(message: Message, state: FSMContext):
    # await state.finish()
    await state.set_state("here_afisha_admin_request_direction")
    await message.answer("<b>📁 Опишите пожалуйста события или среду, которые Вы создаете:</b>")


# Управление событиями
@dp.message_handler(IsAdminorShopAdmin(), text="🎫 Управление событиями 🖍", state="*")
async def admin_products(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>🎫 Редактирование событий.</b>", reply_markup=events_frep())


# Управление товарами
@dp.message_handler(IsShopAdmin(), text="🎁 Управление товарами дмаг.🖍", state="*")
async def shopadmin_products(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>🎁 Редактирование товаров дмаг.</b>", reply_markup=items_sh_frep())


@dp.message_handler(text="🗃 Создать категорию ➕", state="*")
async def product_category_create(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state("here_category_name")
    await message.answer("<b>🗃 Введите название для категории 🏷</b>")


# Начальные категории для изменения позиции
@dp.message_handler(IsShopAdmin(), text="📁 Изменить позицию 🖍", state="*")  # !!!!!!!   Изменить позицию
async def product_position_edit(message: Message, state: FSMContext):
    print(f'📁 Изменить позицию 🖍  user_menu.py 56')
    await state.finish()

    await message.answer("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                         reply_markup=position_edit_category_open_fp(0))


# Открытие товаров
@dp.message_handler(text="🎁 Купить", state="*")
async def user_shop(message: Message, state: FSMContext):
    print(f'Открытие категорий товаров  user_menu.py 65')
    await state.finish()

    get_settings = get_settingsx()
    if(get_settings['type_trade'] != 'digital'):
        city_id = get_city_user(message.from_user.id)[0]
        #get_categories = get_category_in_city(city_id)
        if len(get_category_in_city(city_id)) >= 1:
            await message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_swipe_fp(0, city_id))
        else:
            await message.answer("<b>🎁 В вашем городе товаров нет, выберите другой город</b>\n\n"
                                 "🏙 Изменить город вы можете в личном кабинете")
    else: #if len(get_all_categoriesx()) >= 1
        await message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                             reply_markup=products_item_category_swipe_fp(0,0))

# Открытие товаров
@dp.message_handler(text="🎁 Магазины", state="*")
async def user_shop(message: Message, state: FSMContext):
    print(f'Открытие магазинов товаров  user_menu.py 65')
    await state.finish()

    get_settings = get_settingsx()
    if(get_settings['type_trade'] != 'digital'):
        city_id = get_city_user(message.from_user.id)[0]
        #get_categories = get_category_in_city(city_id)
        if len(get_shops_on_city(city=city_id)) >= 1:
            await message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_shop_swipe_fp(0, city_id))
        else:
            await message.answer("<b>🎁 В вашем городе товаров нет, выберите другой город</b>\n\n"
                                 "🏙 Изменить город вы можете в личном кабинете")
    else: #if len(get_all_categoriesx()) >= 1
        await message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                             reply_markup=products_item_shop_swipe_fp(0, 0))


# Открытие товаров
@dp.message_handler(text="Афиша", state="*")
async def user_afisha(message: Message, state: FSMContext):
    print(f'Открытие афишы  user_menu.py 115')
    await state.finish()

    if is_location(message.from_user.id) == True:
        #await message.answer("🔸 Афиша работает только в случае, если у Вас выбран город.\n"
        #                 "🔸 Если не появились вспомогательные кнопки\n"
        #                 "▶ Введите /start",
        #                 reply_markup=menu_frep(message.from_user.id))
        city_id = get_city_user(message.from_user.id)[0]
        print(city_id)
        if len(get_events_in_city(city_id)) >= 1:
            await message.answer("<b>Выберите интересное для Вас:</b>",
                                 reply_markup=events_in_city_swipe_fp(0, city_id))

    else:
        await geo_choice.location.set()
        await message.answer('Отправьте локацию или выберите город из списка', reply_markup=geo_11_kb())

# события в заведении
# заведения в городе
# события в городе
'''
    get_settings = get_settingsx()
    if(get_settings['type_trade'] != 'digital'):
        city_id = get_city_user(message.from_user.id)[0]
        #get_categories = get_category_in_city(city_id)
        if len(get_events_in_city(city_id=city_id)) >= 1:
            await message.answer("<b>Выберите интересное для Вас:</b>",
                                 reply_markup=events_in_city_swipe_fp(0, city_id))
        else:
            await message.answer("<b>🎁 В вашем городе товаров нет, выберите другой город</b>\n\n"
                                 "🏙 Изменить город вы можете в личном кабинете")
    else: #if len(get_all_categoriesx()) >= 1
        await message.answer("<b>Выберите интересное для Вас:</b>",
                             reply_markup=events_in_city_swipe_fp(0, 0))'''


# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="events_city_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    if remover == 0:
        await call.message.answer("<b>События в городе, выберите что-нибудь интересное:</b>",
                                  reply_markup=events_in_city_swipe_fp(remover, city_id))
    else:
        await call.message.edit_text("<b>События в городе, выберите что-нибудь интересное:</b>",
                                     reply_markup=events_in_city_swipe_fp(remover, city_id))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="events_place_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    place_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    if remover == 0:
        await call.message.answer("<b>События в месте, выберите что-нибудь интересное:</b>",
                                reply_markup=events_in_place_swipe_fp(remover, place_id, city_id))
    else:
        await call.message.edit_text("<b>События в месте, выберите что-нибудь интересное:</b>",
                                  reply_markup=events_in_place_swipe_fp(remover, place_id, city_id))


# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="places_city_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>События в городе, выберите что-нибудь интересное:</b>",
                                 reply_markup=places_in_city_swipe_fp(remover, city_id))


# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="open_inline_support", state="*")
async def open_inline_support(call: CallbackQuery, state: FSMContext):
    user_support = get_settingsx()['misc_support']
    if str(user_support).isdigit():
        get_user = get_userx(user_id=user_support)
        await call.message.answer("<b>Напишите, что Вы хотите добавить, мы добавим.:</b>",
                                 reply_markup=user_support_finl(get_user['user_login']))
        return
    else:
        update_settingsx(misc_support="None")
        await message.answer(f"☎ Поддержка. Измените их в настройках бота.\n➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}",
                            disable_web_page_preview=True)

# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="book_event_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print(f'Карточка товара: user_menu.py  152')
    event_id = int(call.data.split(":")[1])
    place_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    #category_id = int(call.data.split(":")[2])
    #remover = int(call.data.split(":")[3])
    #city_id = int(call.data.split(":")[4])
    #print(position_id, category_id, remover, city_id)

    city_id = get_city_user(call.from_user.id)[0]
    get_event = get_eventxx(event_id=event_id)
    #get_category = get_categoryx(category_id=category_id)
    #get_items = get_itemsx(position_id=position_id)
    get_settings = get_settingsx()
    print(get_event)

    if get_event['event_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_event['event_description']}"

    send_msg = f"<b>Мероприятие:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_event['event_name']}</code>\n" \
               f"🏙 Город: <code>{get_event['event_city']}</code>\n" \
               f"{text_description}"

    #f"📦 Остаток: <code>{len(get_items)}шт</code>" \
    print(get_settings['type_trade'])
    tt = get_settings['type_trade']

    if tt != "digital":
        #    product_markup = products_open_finl(position_id, remover, category_id)
        # product_markup = products_open_cart_finl(position_id, remover, category_id)
        if len(get_event['event_photo']) >= 5:
            print("\|")
            await call.message.delete()
            await call.message.answer_photo(get_event['event_photo'],
                                            send_msg, reply_markup=event_open_finl(event_id, 0, place_id, city_id))
        else:
            print("\||")
            await call.message.edit_text(send_msg,
                                         reply_markup=event_open_finl(event_id, 0, place_id, city_id))
    elif tt == "digital":
        if len(get_position['event_photo']) >= 5:
            print("\|")
            await call.message.delete()
            await call.message.answer_photo(get_event['event_photo'],
                                            send_msg, reply_markup=event_open_finl(event_id, 0, place_id, city_id))
        else:
            print("\||")
            await call.message.edit_text(send_msg,
                                         reply_markup=event_open_finl(event_id, 0, place_id, city_id))

# Открытие пополнения счета
@dp.message_handler(text="💰 Пополнить", state="*")
async def user_refill_b(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(user_refill_my(message.from_user.id), reply_markup=refill_open_inl)

#refiil_way(message.from_user.id)

# Открытие профиля
@dp.message_handler(text="👤 Профиль", state="*")
async def user_profile(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(open_profile_my(message.from_user.id), reply_markup=profile_open_inl)

# Открытие профиля
@dp.message_handler(text="Партнеры", state="*")
async def open_partners_list(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Наши славные партнеры:", reply_markup=partners_list_inl)

# Открытие корзины
@dp.message_handler(text="🧮 Корзина", state="*")
async def user_cart(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    orderdata = get_params_orderx(user_id=user_id)
    print(orderdata)
    for order in orderdata:
        print(order['order_state'])
        if order['order_state'] == 'delivery':
            await message.answer(open_cart_my(message.from_user.id), reply_markup=cart_open_delivery_inl)
        if order['order_state'] == 'created':
            await message.answer(open_cart_my(message.from_user.id), reply_markup=cart_open_created_inl)
        if order['order_state'] == 'submited':
            await message.answer(f"<b>Активных заказов нет.</b>\n")

# Открытие FAQ
@dp.message_handler(text=["ℹ FAQ", "/faq"], state="*")
async def user_faq(message: Message, state: FSMContext):
    await state.finish()

    send_message = get_settingsx()['misc_faq']
    if send_message == "None":
        send_message = f"ℹ Информация. Измените её в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}"

    await message.answer(get_faq(message.from_user.id, send_message), disable_web_page_preview=True)

###############################################################################################
##### ***** ###### *****         СОЗДАНИЕ АРТИСТА
###############################################################################################
# -----------------------------------------------------------------------------------------------------------
# Создание нового магазина
@dp.message_handler(IsAdminorShopAdmin(), text="🏪 Создать артиста ➕", state="*")
async def product_shop_create(message: Message, state: FSMContext):
    await state.finish()
    print("user_menu - создание артиста")
    print("-")
    user_id = message.from_user.id
    print(user_id)
    my_artist = check_user_artist_exist(user_id)
    print(my_artist)
    if my_artist == True:
        print("|")
        await message.answer(f"<b>🏪 Артист уже существует 🏷 Выбирайте его в каталоге при создании позиций: {my_artist} </b>", parse_mode='HTML')
    else:
        print("||")
        await state.set_state("here_artist_name")
        await message.answer("<b>🏪 Введите название артиста или коллектива 🏷</b>", parse_mode='HTML')


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdminorShopAdmin(), state="here_artist_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        print("admin_products_shop - создание артиста")
        await state.update_data(data={'name': message.text})
        await state.set_state('here_artist_description')
        await message.answer("<b>🏪 Введите Bio артиста 📜</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для артиста 🏷", parse_mode='HTML')

# принятие описания магазина, запрос адреса
@dp.message_handler(IsAdminorShopAdmin(), state="here_artist_description")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_artist_webadress')
        await message.answer("<b>🏪 Отправьте веб-сайт артиста 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


    else:
        await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите новое Bio для артиста 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdminorShopAdmin(), state="here_artist_webadress")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.text == '0':
        await state.update_data(data={'webaddress': 'None'})
    else:
        await state.update_data(data={'webaddress': message.text})
    await state.set_state('here_artist_logo')
    await message.answer("<b>🏪 Отправьте лого артиста 📷</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')

# принятие лого магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), content_types=['photo','text'], state="here_artist_logo")
async def product_category_create_logo(message: Message, state: FSMContext):
    if message.content_type == 'photo':
        logo = message.photo[0].file_id
    else:
        logo = None

    async with state.proxy() as data:
        print(data)
        name = data['name']
        description = data['description']
        webaddress = data['webaddress']

    await state.finish()

    type_trade = get_settingsx()
    if type_trade['type_trade'] != "digital":
        city = get_city_user3(message.from_user.id)
        print(city)
        city_id = city[0]
        geocode = city[1]
        city_name = city[2]
    else:
        city_id = 0
        geocode = ''
        city_name = ''
    add_artistx(name, description, webaddress, message.from_user.id, logo, city_id, geocode, city_name)
    await message.answer("<b>🏪 Карточка артиста была успешно создана ✅</b>", parse_mode='HTML')


# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsAdminorShopAdmin(), text="🏪 Изменить артиста 🖍", state="*")
async def artist_list_edit(message: Message, state: FSMContext):
    await state.finish()
    user_id=message.from_user.id
    #if get_my_shopx(user_id):
    artists = get_artistsxx(admin=user_id)
    #shops = get_all_shopx()
    #shops = get_all_shopx()
    #print(f'shops {shops}')
    print(artists)

    if len(artists) >= 1:
        await message.answer("<b>🏪 Выберите артиста для изменения 🖍</b>",
                             reply_markup=artist_edit_open_fp(0, user_id))
    else:
        await message.answer("<b>🏪 Ваши артисты отсутствуют 🖍</b>")


# Смена страницы выбора магазина
@dp.message_handler(IsAdminorShopAdmin(), text_startswith="change_artist_edit_pg:", state="*")
async def artist_list_edit_pg(call: CallbackQuery, state: FSMContext):
    await state.finish()
    remover = int(str(call.data).split(':')[1])
    #user_id = message.from_user.id
    user_id = int(str(call.data).split(':')[2])
    artists = get_artistsxx(admin=user_id)

    if len(artists) >= 1:
        await call.message.answer("<b>🏪 Выберите артиста для изменения 🖍</b>",
                                  reply_markup=artist_edit_open_fp(remover, user_id))
    else:
        await call.message.answer("<b>🏪 Артисты отсутствуют 🖍</b>")


# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit:", state="*")
async def artist_edit_open(call: CallbackQuery, state: FSMContext):
    print(f'Выбор артиста для редактирования api_sqlite.py 496')
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    print(artist_id, user_id, remover)

    get_message, get_photo = get_artist_admin(artist_id)

    if get_photo is not None and get_photo != '':
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message,
                                        reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await call.message.edit_text(get_message,
                                     reply_markup=artist_edit_open_finl(artist_id, user_id, remover))


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_return", state="*")
async def artist_edit_return(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    print(user_id)
    artists = get_artistsxx(admin=user_id)
    #shops = get_all_shopx()
    #shops = get_all_shopx()
    #print(f'shops {shops}')
    print(artists)

    if len(artists) >= 1:
        await call.message.delete()
        await call.message.answer("<b>📁 Выберите нужного Вам артиста 🖍</b>",
                                  reply_markup=artist_edit_open_fp(0, user_id))
    else:
        await call.answer("<b>❗ У Вас отсутствуют Артисты</b>")

# -----------------------------------------------------------------------------------------------------------
# Создание нового магазина
@dp.message_handler(IsAdminorShopAdmin(), text="🏪 Создать магазин ➕", state="*")
async def product_shop_create(message: Message, state: FSMContext):
    await state.finish()
    print("user_menu - создание магазина")
    print("-")
    user_id = message.from_user.id
    print(user_id)
    my_shop = check_user_shop_exist(user_id)
    print(my_shop)
    if my_shop == True:
        print("|")
        await message.answer(f"<b>🏪 Магазин уже существует 🏷 Выбирайте его в каталоге при создании позиций: {my_shop} </b>", parse_mode='HTML')
    else:
        print("||")
        await state.set_state("here_shop_name")
        await message.answer("<b>🏪 Введите название для магазина 🏷</b>", parse_mode='HTML')


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        print("admin_products_shop - создание магазина")
        await state.update_data(data={'name': message.text})
        await state.set_state('here_shop_description')
        await message.answer("<b>🏪 Введите описание для магазина 📜</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для магазина 🏷", parse_mode='HTML')


# принятие описания магазина, запрос адреса
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_description")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_shop_adress')
        await message.answer("<b>🏪 Отправьте адресс магазина 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


    else:
        await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите новое описание для магазина 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_adress")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.text == '0':
        await state.update_data(data={'address': 'None'})
    else:
        await state.update_data(data={'address': message.text})
    await state.set_state('here_shop_phone')
    await message.answer("<b>🏪 Отправьте телефон магазина ☎️</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие номера магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_phone")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.text == '0':
        await state.update_data(data={'phone': 'None'})
    else:
        await state.update_data(data={'phone': message.text})
    await state.set_state('here_shop_logo')
    await message.answer("<b>🏪 Отправьте лого магазина 📷</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие лого магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), content_types=['photo','text'], state="here_shop_logo")
async def product_category_create_logo(message: Message, state: FSMContext):
    if message.content_type == 'photo':
        logo = message.photo[0].file_id
    else:
        logo = None

    async with state.proxy() as data:
        print(data)
        name = data['name']
        description = data['description']
        address = data['address']
        phone = data['phone']

    await state.finish()

    type_trade = get_settingsx()
    if type_trade['type_trade'] != "digital":
        city = get_city_user3(message.from_user.id)
        print(city)
        city_id = city[0]
        geocode = city[1]
        city_name = city[2]
    else:
        city_id = 0
        geocode = ''
        city_name = ''
    add_shopx(name, description, address, phone, message.from_user.id, logo, city_id, geocode, city_name)
    await message.answer("<b>🏪 Магазин был успешно создан ✅</b>", parse_mode='HTML')

# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsAdminorShopAdmin(), text="🏪 Изменить магазин 🖍112", state="*")
async def product_category_edit(message: Message, state: FSMContext):
    await state.finish()

    shops = get_all_shopx()
    print(f'shops {shops}')

    if len(shops) >= 1:
        await message.answer("<b>🏪 Выберите магазин для изменения 🖍</b>",
                             reply_markup=shop_edit_open_fp(0, shops))
    else:
        await message.answer("<b>🏪 Магазины отсутствуют 🖍</b>")


# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsAdminorShopAdmin(), text="🏪 Изменить магазин 🖍", state="*")
async def shop_list_edit(message: Message, state: FSMContext):
    await state.finish()
    user_id=message.from_user.id
    #if get_my_shopx(user_id):
    shops = get_shopsxx(admin=user_id)
    #shops = get_all_shopx()
    #shops = get_all_shopx()
    #print(f'shops {shops}')
    print(shops)

    if len(shops) >= 1:
        await message.answer("<b>🏪 Выберите магазин для изменения 🖍</b>",
                             reply_markup=shop_edit_open_fp(0, user_id))
    else:
        await message.answer("<b>🏪 Ваши магазины отсутствуют 🖍</b>")


# Смена страницы выбора магазина
@dp.message_handler(IsAdminorShopAdmin(), text_startswith="change_shop_edit_pg:", state="*")
async def shop_list_edit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    page = int(str(call.data).split(':')[1])


    if len(shops) >= 1:
        await call.message.answer("<b>🏪 Выберите магазин для изменения 🖍</b>",
                                  reply_markup=shop_edit_open_fp(page, 0))
    else:
        await call.message.answer("<b>🏪 Магазины отсутствуют 🖍</b>")


# Открытие сообщения с ссылкой на поддержку
@dp.message_handler(text=["☎ Поддержка", "/support"], state="*")
async def user_support(message: Message, state: FSMContext):
    await state.finish()

    user_support = get_settingsx()['misc_support']
    if str(user_support).isdigit():
        get_user = get_userx(user_id=user_support)

        if len(get_user['user_login']) >= 1:
            await message.answer("<b>☎ Нажмите кнопку ниже для связи с Администратором.</b>",
                                 reply_markup=user_support_finl(get_user['user_login']))
            return
        else:
            update_settingsx(misc_support="None")

    await message.answer(f"☎ Поддержка. Измените их в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}",
                         disable_web_page_preview=True)

# Создание запроса на продавца
@dp.message_handler(state="here_seller_request_direction")
async def user_seller(message: Message, state: FSMContext):
    await state.finish()
    # message.answer(message.text)
    seller_request = create_seller_request(message.from_user.id, message.text)
    await message.answer("👌 Ваш запрос успешно отправлен.")

# Просмотр истории покупок
@dp.callback_query_handler(text="create_seller_request5", state="*")
async def user_seller(call: CallbackQuery, state: FSMContext):
    seller_request = create_seller_request(call.from_user.id)
    await call.answer("🎁 Запрос успешно создан")
    await notify(dp, f"Поступил новый запрос продавца!")
    # await bot.send_message(get_admins(), "ntcnnnnnn")

# Подтверждение удаления всех позиций
@dp.message_handler(IsShopAdmin(), text="📁 Удалить все позиции ❌", state="*")
async def product_position_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>📁 Вы действительно хотите удалить все позиции? ❌</b>\n"
                         "❗ Так же будут удалены все товары",
                         reply_markup=position_remove_confirm_inl)

# Удаление позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_delete", state="*")
async def product_position_edit_delete(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await call.message.delete()
    await call.message.answer("<b>📁 Вы действительно хотите удалить позицию? ❌</b>",
                              reply_markup=position_edit_delete_finl(position_id, category_id, remover))


# Подтверждение удаления позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_delete", state="*")
async def product_position_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    remover = int(call.data.split(":")[4])

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        remove_positionx(position_id=position_id)

        await call.answer("📁 Вы успешно удалили позицию и её товары ✅")

        if len(get_positionsx(category_id=category_id)) >= 1:
            await call.message.edit_text("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                         reply_markup=position_edit_open_fp(remover, category_id))
        else:
            await call.message.delete()
    else:
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Согласие очистики позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_clear", state="*")
async def product_position_edit_clear_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    remover = int(call.data.split(":")[4])

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        await call.answer("📁 Вы успешно удалили все товары позиции ✅")

    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message,
                                        reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await call.message.edit_text(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Открытие способов пополнения
@dp.message_handler(IsShopAdmin(), text="🖲 Способы пополнения", state="*")
async def payment_systems(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    await message.answer("<b>🖲 Выберите способ пополнения</b>", reply_markup=payment_as_choice_finl(user_id))


# Включение/выключение самих способов пополнения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="change_payment7:")
async def payment_systems_edit7(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]
    user_id = json.dumos(call.data.split(":")[3])
    print("Админ магазина")
    # print(call.data.split(":")[0])
    print(call.from_user.id)
    user_id = call.from_user.id

    count = get_upaycount(user_id)
    print(count['paycount'])
    if count['paycount'] == 0:
        cur = create_upayments_row(user_id)
    else:
        get_payment = get_upaymentx(user_id)

    if get_payment['qiwi_login'] != "None" and get_payment['qiwi_token'] != "None" or way_status == "False":
        if way_pay == "Form":
            if get_payment['qiwi_secret'] != "None" or way_status == "False":
                update_upaymentx(user_id, way_form=way_status)
            else:
                await call.answer(
                    "❗ Приватный ключ отсутствует. Измените киви и добавьте приватный ключ для включения оплаты по Форме",
                    True)
        elif way_pay == "ForYm":
            if get_payment['yoo_token'] != "None" or way_status == "False":
                update_upaymentx(user_id, way_formy=way_status)
            else:
                await call.answer(
                    "❗ Номер счета отсутствует. Измените YooMoney и добавьте токен для включения оплаты по Форме YooMoney",
                    True)
        elif way_pay == "Number":
            update_update_upaymentx(user_id, way_number=way_status)
        elif way_pay == "Nickname":
            status, response = await (await QiwiAPI(call)).get_nickname()
            if status:
                update_upaymentx(user_id, way_nickname=way_status, qiwi_nickname=response)
            else:
                await call.answer(response, True)
    else:
        await call.answer("❗ Добавьте киви кошелёк перед включением Способов пополнений.", True)

    try:
        await call.message.edit_text("<b>🖲 Выберите способ пополнения</b>", reply_markup=payment_as_choice_finl())
    except:
        pass


####################################### QIWI ######################################
# Изменение QIWI кошелька
@dp.message_handler(IsShopAdmin(), text="🥝 Изменить QIWI 🖍", state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_qiwi_login")
    await message.answer("<b>🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍</b>")


# Проверка работоспособности QIWI
@dp.message_handler(IsAdminorShopAdmin(), text="🥝 Проверить QIWI ♻", state="*")
async def payment_qiwi_check(message: Message, state: FSMContext):
    print("||| Проверка КИВИ админом площадки. |||")
    await state.finish()
    user_id = message.from_user.id
    print(user_id)

    await (await QiwiAPI(message, suser_id=user_id, check_pass=True)).pre_checker()


# Баланс QIWI
@dp.message_handler(IsAdminorShopAdmin(), text="🥝 Баланс QIWI 👁", state="*")
async def payment_qiwi_balance(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    await (await QiwiAPI(message, suser_id=user_id)).get_balance()


######################################## ПРИНЯТИЕ QIWI ########################################
# Принятие логина для QIWI
@dp.message_handler(IsShopAdmin(), state="here_qiwi_login")
async def payment_qiwi_edit_login(message: Message, state: FSMContext):
    if message.text.startswith("+"):
        await state.update_data(here_qiwi_login=message.text)

        await state.set_state("here_qiwi_token")
        await message.answer(
            "<b>🥝 Введите <code>токен API</code> QIWI кошелька 🖍</b>\n"
            "❕ Получить можно тут 👉 <a href='https://qiwi.com/api'><b>Нажми на меня</b></a>\n"
            "❕ При получении токена, ставьте только первые 3 галочки.",
            disable_web_page_preview=True
        )
    else:
        await message.answer("<b>❌ Номер должен начинаться с + <code>(+7..., +380...)</code></b>\n"
                             "🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍")


# Принятие токена для QIWI
@dp.message_handler(IsShopAdmin(), state="here_qiwi_token")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_qiwi_token=message.text)

    await state.set_state("here_qiwi_secret")
    await message.answer(
        "<b>🥝 Введите <code>Секретный ключ 🖍</code></b>\n"
        "❕ Получить можно тут 👉 <a href='https://qiwi.com/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
        "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
        disable_web_page_preview=True
    )


# Принятие приватного ключа для QIWI
@dp.message_handler(IsAdminorShopAdmin(), state="here_qiwi_secret")
async def payment_qiwi_edit_secret(message: Message, state: FSMContext):
    async with state.proxy() as data:
        qiwi_login = data['here_qiwi_login']
        qiwi_token = data['here_qiwi_token']
        if message.text == "0": qiwi_secret = "None"
        if message.text != "0": qiwi_secret = message.text
        user_id = message.from_user.id

    await state.finish()

    cache_message = await message.answer("<b>🥝 Проверка введённых QIWI данных... 🔄</b>")
    await asyncio.sleep(0.5)

    await (await QiwiAPI(cache_message, qiwi_login, qiwi_token, qiwi_secret, add_pass=True, suser_id=user_id)).pre_checker()


################################################################################################
###################################### УДАЛЕНИЕ ВСЕХ ПОЗИЦИЙ ###################################
# Согласие на удаление всех позиций и товаров
@dp.callback_query_handler(IsShopAdmin(), text_startswith="confirm_remove_position:", state="*")
async def product_position_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    print("SA DEL POSITIONS")
    user_id = call.from_user.id
    print(user_id)

    if get_action == "yes":

        get_positions = len(get_all_my_positionsnx(position_user_id=user_id))
        print(get_positions)
        get_items = len(get_all_my_itemsnx(creator_id=user_id))
        print(get_items)

        remove_positionx(position_user_id=user_id)
        remove_itemx(creator_id=user_id)

        await call.message.edit_text(
            f"<b>📁 Вы удалили все позиции<code>({get_positions}шт)</code> и товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>📁 Вы отменили удаление всех позиций ✅</b>")

#################### УДАЛЕНИЕ ТОВАРОВ ###################
# Кнопки с подтверждением удаления всех категорий
@dp.message_handler(IsShopAdmin(), text="🎁 Удалить все товары ❌", state="*")
async def product_item_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🎁 Вы действительно хотите удалить все товары? ❌</b>\n",
                         reply_markup=item_remove_confirm_inl)

##################################### УДАЛЕНИЕ ВСЕХ ТОВАРОВ ####################################
# Согласие на удаление всех товаров
@dp.callback_query_handler(IsShopAdmin(), text_startswith="confirm_remove_item:", state="*")
async def product_item_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    user_id = call.from_user.id

    if get_action == "yes":
        get_items = len(get_all_my_itemsnx(creator_id=user_id))
        remove_itemx(creator_id=user_id)

        await call.message.edit_text(f"<b>🎁 Вы удалили все товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>🎁 Вы отменили удаление всех товаров ✅</b>")


# Удаление определённых товаров
@dp.message_handler(IsShopAdmin(), text="🎁 Удалить товары 🖍", state="*")
async def product_item_delete(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_items_delete")
    await message.answer("<b>🖍 Вводите айди товаров, которые нужно удалить</b>\n"
                         "❕ Получить айди товаров можно при изменении позиции\n"
                         "❕ Если хотите удалить несколько товаров, отправьте ID товаров через запятую или пробел. Пример:\n"
                         "<code>▶ 123456,123456,123456</code>\n"
                         "<code>▶ 123456 123456 123456</code>")

################################################################################################
####################################### УДАЛЕНИЕ ТОВАРОВ ######################################
# Принятие айди товаров для их удаления
@dp.message_handler(IsAdminorShopAdmin(), state="here_items_delete")
async def product_item_delete_get(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    remove_ids, cancel_ids = [], []  # Айди удалённых и ненайденных товаров
    get_item_ids_one, get_item_ids_two = [], [[]]
    save_ids = []

    if "," in message.text:
        get_item_ids_one = clear_list(message.text.split(","))
    else:
        get_item_ids_one = clear_list([message.text])

    for item in get_item_ids_one:
        if " " in item:
            get_item_ids_two.append(item.split(" "))

    if len(get_item_ids_two) == 1:
        get_item_ids_two.append(get_item_ids_one)

    for check_item in get_item_ids_two:
        for item in clear_list(check_item):
            save_ids.append(item)

    save_ids = clear_list(save_ids)

    for item_id in save_ids:
        #check_item = get_itemx(item_id=item_id)
        check_item = get_itemx(item_id=item_id, creator_id=user_id)
        if check_item is not None:
            remove_itemx(item_id=item_id)
            remove_ids.append(item_id)
        else:
            cancel_ids.append(item_id)

    remove_ids = ", ".join(remove_ids)
    cancel_ids = ", ".join(cancel_ids)

    await message.answer(f"<b>✅ Успешно удалённые товары:\n"
                         f"▶ <code>{remove_ids}</code>\n"
                         f"➖➖➖➖➖➖➖➖➖➖\n"
                         f"❌ Ненайденные товары:\n"
                         f"▶ <code>{cancel_ids}</code></b>")
###############################################################################################
################################################################################################
####################################### ДОБАВЛЕНИЕ ПОЗИЦИЙ #####################################
# Следующая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_create_nextp:", state="*")
async def product_position_create_next(call: CallbackQuery, state: FSMContext):
    print(f'выбора категорий для создания позиций  user_menu.py 126')
    remover = int(call.data.split(":")[1])
    print(remover)

    await call.message.edit_text("<b>📁 Выберите категорию для позиции ➕</b>",
                                 reply_markup=position_create_next_page_fp(remover))

# Предыдущая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_create_backp:", state="*")
async def product_position_create_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию для позиции ➕</b>",
                                 reply_markup=position_create_back_page_fp(remover))


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_create_here:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_create_here - user_menu 160')
    category_id = int(call.data.split(":")[1])
    await state.update_data(here_cache_change_category_id=category_id)

    print('position_addtoshop - user_menu 555')
    user_id = call.from_user.id
    get_user_shops = get_shopsxx(admin=user_id)
    if len(get_user_shops) >= 1:
        await call.message.edit_text("<b>Выберите магазин для добавления позиции.</b>",
                                     reply_markup=position_select_shop_fp(0))
    else:
        await call.message.edit_text("<b>У Вас еще нет магазина на площадке, но Вы можете его создать.</b>",
                                     reply_markup=shop_creation_request_finl())
        await state.set_state("here_position_addtoshop")


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="here_position_addtoshop:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('here_position_addtoshop: - user_menu 566')
    key = call.data.split(":")[1]
    if key != "NoCreate":
        shop_id = int(call.data.split(":")[1])
        await state.update_data(here_cache_change_shop_id=shop_id)

        await state.set_state("here_position_name")
        await call.message.edit_text("<b>📁 Введите название для позиции 🏷</b>")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Заготовка под принятие города магазином
# Принятие города для создания позиции
# @dp.message_handler(IsShopAdmin(), state="here_position_city")
# async def product_position_create_name(message: Message, state: FSMContext):
#     print(f'Принятие города для создания позиции  admin_products_shop.py 344')
#     city_user = get_city_user(message.from_user.id)
# Принятие имени для создания позиции


@dp.message_handler(IsAdminorShopAdmin(), state="here_position_name")
async def product_position_create_name(message: Message, state: FSMContext):
    print(f'Принятие имени для создания позиции  user_menu.py 355')
    if len(message.text) <= 100:
        await state.update_data(here_position_name=clear_html(message.text),
                                here_position_city=get_citytext_user(message.from_user.id)[0]
                                , position_city_id=get_city_user(message.from_user.id)[0])

        await state.set_state("here_position_price")
        await message.answer("<b>📁 Введите цену для позиции 💰</b>")
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")


# Принятие цены позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), state="here_position_price")
async def product_position_create_price(message: Message, state: FSMContext):
    print(f'Принятие цены позиции  admin_products.py 366')
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.update_data(here_position_price=message.text)

            await state.set_state("here_position_description")
            await message.answer("<b>📁 Введите описание для позиции 📜</b>\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
        else:
            await message.answer("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰")


# Принятие описания позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), state="here_position_description")
async def product_position_create_description(message: Message, state: FSMContext):
    print(f'Принятие описания позиции  admin_products.py 386')

    try:
        if len(message.text) <= 600:
            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            await state.update_data(here_position_description=message.text)

            await state.set_state("here_position_photo")
            await message.answer("<b>📁 Отправьте изображение для позиции 📸</b>\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
        else:
            await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для позиции 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие изображения позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), content_types="photo", state="here_position_photo")
@dp.message_handler(IsAdminorShopAdmin(), text="0", state="here_position_photo")
async def product_position_create_photo(message: Message, state: FSMContext):
    print(f'Принятие изображения позиции  admin_products.py 418')
    async with state.proxy() as data:
        position_user_id = message.from_user.id
        position_city = data['here_position_city']
        position_city_id = data['position_city_id']
        position_name = clear_html(data['here_position_name'])
        position_price = data['here_position_price']
        catategory_id = data['here_cache_change_category_id']
        position_shop_id = data['here_cache_change_shop_id']
        position_description = data['here_position_description']
    await state.finish()

    if "text" in message:
        position_photo = ""
    else:
        position_photo = message.photo[-1].file_id


    add_positionx(position_city, position_city_id, position_name, position_price, position_description, position_photo,
                  catategory_id, position_shop_id, position_user_id)

    #async def on_notify(dp: Dispatcher, msg, markup):
    #    await send_admins(msg, markup="default")
    await notify(dp, f"Создана позиция: {position_name}, пользователем ID: {position_user_id}")

    await message.answer("<b>📁 Позиция была успешно создана ✅</b>")


################################################################################################
####################################### ИЗМЕНЕНИЕ ПОЗИЦИЙ #####################################
# Возвращение к начальным категориям для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_open_fp(0))


# Следующая страница категорий для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_nextp:", state="*")
async def product_position_edit_category_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_next_page_fp(remover))


# Предыдущая страница категорий для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_backp:", state="*")
async def product_position_edit_category_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_back_page_fp(remover))


# Выбор категории с нужной позицией
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category:", state="*")
async def product_position_edit_category_open(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.edit_text("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                     reply_markup=position_edit_open_fp(0, category_id))
    else:
        await call.answer("📁 Позиции в данной категории отсутствуют")


# Следующая страница позиций для их изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_nextp:", state="*")
async def product_position_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_next_page_fp(remover, category_id))


# Предыдущая страница позиций для их изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_backp:", state="*")
async def product_position_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_back_page_fp(remover, category_id))


# Выбор позиции для редактирования
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    print(f'Выбор позиции для редактирования api_sqlite.py 496')
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    user_id = call.from_user.id

    # IsProductShopAdmin()
    adminspos = check_position_owner(user_id, position_id)
    if adminspos is True:

        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await call.answer("<b>❗ У Вас нет прав редактировать данную позицию.</b>")


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.delete()
        await call.message.answer("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                  reply_markup=position_edit_open_fp(remover, category_id))
    else:
        await call.answer("<b>❗ Позиции в данной категории отсутствуют</b>")


######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_name", state="*")
async def product_position_edit_name(call: CallbackQuery, state: FSMContext):
    print(f'Изменение имени позиции api_sqlite.py 529')
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_name")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое название для позиции 🏷</b>")


# Принятие имени позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_name")
async def product_position_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            position_id = data['here_cache_position_id']
            category_id = data['here_cache_category_id']
            remover = data['here_cache_position_remover']
        await state.finish()

        update_positionx(position_id, position_name=clear_html(message.text))
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message,
                                       reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите новое название для позиции 🏷")

# Изменение цены позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_price", state="*")
async def product_position_edit_price(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_price")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новую цену для позиции 💰</b>")


# Принятие цены позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_price")
async def product_position_edit_price_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            async with state.proxy() as data:
                position_id = data['here_cache_category_id']
                category_id = data['here_cache_position_id']
                remover = data['here_cache_position_remover']
            await state.finish()

            update_positionx(position_id, position_price=message.text)
            get_message, get_photo = get_position_admin(position_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message,
                                           reply_markup=position_edit_open_finl(position_id, category_id, remover))
            else:
                await message.answer(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰")


# Изменение описания позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_description", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_description")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое описание для позиции 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие описания позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_description")
async def product_position_edit_description_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_category_id']
        category_id = data['here_cache_position_id']
        remover = data['here_cache_position_remover']

    try:
        if len(message.text) <= 600:
            await state.finish()

            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            update_positionx(position_id, position_description=message.text)
            get_message, get_photo = get_position_admin(position_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message,
                                           reply_markup=position_edit_open_finl(position_id, category_id, remover))
            else:
                await message.answer(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для позиции 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.")


# Изменение изображения позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_photo", state="*")
async def product_position_edit_photo(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_photo")
    await call.message.delete()
    await call.message.answer("<b>📁 Отправьте новое изображение для позиции 📸</b>\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие нового фото для позиции
@dp.message_handler(IsShopAdmin(), content_types="photo", state="here_change_position_photo")
@dp.message_handler(IsShopAdmin(), text="0", state="here_change_position_photo")
async def product_position_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_category_id']
        category_id = data['here_cache_position_id']
        remover = data['here_cache_position_remover']
    await state.finish()

    position = get_positionx(position_id=position_id)
    print(position['position_name'])

    if "text" in message:
        position_photo = ""
    else:
        position_photo = message.photo[-1].file_id


    update_positionx(position_id, position_photo=position_photo)
    get_message, get_photo = get_position_admin(position_id)
    await notify(dp, f"Была отредактирована позиция: {position['position_name']}")

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message,
                                   reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover))

# Изменение города продукта
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_city", state="*")
async def product_position_edit_description2(call: CallbackQuery, state: FSMContext):
    print(f'Изменение города продукта  admin_products.py 715')
    print(call.data)
    category_id = int(call.data.split(":")[2])
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[3])

    current_city = get_city_user(call.from_user.id)[0]
    get_user_shops = get_shopsxx(admin=user_id)
    if len(get_user_shops) >= 1:
        await call.message.edit_text("<b>Выберите магазин для добавления позиции.</b>",
                                 reply_markup=position_select_shop_fp(0))

    await state.set_state("here_change_shop")

    # await state.update_data(here_cache_category_id=category_id)
    # await state.update_data(here_cache_position_id=position_id)
    # await state.update_data(here_cache_position_remover=remover)


    #await state.update_data({'position_id': position_id, 'category_id': category_id, 'remover': remover})
    #await call.message.delete()
    #await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
    #                          "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
    #                          f"❕  Город товара: <code>{current_city}</code>", reply_markup=geo_1_kb())


# ---------------------------  Добавлено 12.08.22 ------------------------------------------

# Изменение города продукта
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_edit_city", state="*")
async def product_position_edit_city(call: CallbackQuery, state: FSMContext):
    print(f'Изменение города продукта  admin_products.py 715')
    print(call.data)
    category_id = int(call.data.split(":")[2])
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[3])

    current_city = get_city_user(call.from_user.id)[0]

    # await state.update_data(here_cache_category_id=category_id)
    # await state.update_data(here_cache_position_id=position_id)
    # await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_city")
    await state.update_data({'position_id': position_id, 'category_id': category_id, 'remover': remover})
    await call.message.delete()
    await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
                              "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
                              f"❕ Город товара: <code>{current_city}</code>", reply_markup=geo_1_kb())


# принятие новой геопозиции для позиции
@dp.callback_query_handler(text_startswith='geo_chosen_cities', state='here_change_city')
async def geo_5(cb: CallbackQuery, state: FSMContext):
    info = int(str(cb.data).split('#')[1])
    if info == 0:
        async with state.proxy() as data:
            city = data['city']
            position_id = int(data['position_id'])
            category_id = data['category_id']
            remover = data['remover']
            city_id = data['city_id']

    else:
        async with state.proxy() as data:
            position_id = int(data['position_id'])
            category_id = data['category_id']
            remover = data['remover']

        city_id = info
        city = get_city_info(info)

    await state.finish()
    update_position_city(city, city_id, position_id)

    # update_positionx(position_id)
    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await cb.message.answer_photo(get_photo, get_message,
                                      reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await cb.message.answer(get_message,
                                reply_markup=position_edit_open_finl(position_id, category_id, remover))

######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_name", state="*")
async def tgartist_edit_name(call: CallbackQuery, state: FSMContext):
    print(f'Изменение имени артиста api_sqlite.py 529')
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await state.set_state("here_change_artist_name")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое название для артиста 🏷</b>")


# Принятие имени артиста для его изменения
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_artist_name")
async def artist_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            artist_id = data['here_cache_artist_id']
            user_id = data['here_cache_user_id']
            remover = data['here_cache_artist_remover']
        await state.finish()

        update_artistx(artist_id, name=clear_html(message.text))
        get_message, get_photo = get_artist_admin(artist_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message,
                                       reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
        else:
            await message.answer(get_message, reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите новое название для артиста 🏷")
################################################################################################
# РЕДАКТИРОВАНИЕ ОПИСАНИЯ АРТИСТА
###################################
# Изменение описания артиста
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_description", state="*")
async def artist_edit_description(call: CallbackQuery, state: FSMContext):
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await state.set_state("here_change_artist_description")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое описание для артиста 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие описания позиции для её изменения
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_artist_description")
async def product_artist_edit_description_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        artist_id = data['here_cache_artist_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_artist_remover']

    try:
        if len(message.text) <= 600:
            await state.finish()

            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            update_artistx(artist_id, description=clear_html(message.text))
            get_message, get_photo = get_artist_admin(artist_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message,
                                           reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
            else:
                await message.answer(get_message,
                                     reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
        else:
            await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для артиста 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для артиста 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.")
##############################################################################################
########################## ARTIST _____ EDIT ________ PHOTO
##############################################################################################
# Изменение изображения позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_photo", state="*")
async def artist_edit_photo(call: CallbackQuery, state: FSMContext):
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await state.set_state("here_change_artist_photo")
    await call.message.delete()
    await call.message.answer("<b>📁 Отправьте новое изображение для артиста 📸</b>\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие нового фото для позиции
@dp.message_handler(IsAdminorShopAdmin(), content_types="photo", state="here_change_artist_photo")
@dp.message_handler(IsAdminorShopAdmin(), text="0", state="here_change_artist_photo")
async def product_artist_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        artist_id = data['here_cache_artist_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_artist_remover']
    await state.finish()

    artist = get_artistx(artist_id = artist_id)
    print(artist['name'])

    if "text" in message:
        artist_photo = ""
    else:
        artist_photo = message.photo[-1].file_id


    update_artistx(artist_id, logo=artist_photo)
    get_message, get_photo = get_artist_admin(artist_id)
    await notify(dp, f"Был отредактирован артист: {artist['name']}")

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message,
                                   reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await message.answer(get_message, reply_markup=artist_edit_open_finl(artist_id, user_id, remover))


# Изменение города продукта
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_city", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    print(f'Изменение города артиста  admin_products.py 715')
    print(call.data)
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    current_city = get_city_artist(artist_id=artist_id)[0]

    # await state.update_data(here_cache_category_id=category_id)
    # await state.update_data(here_cache_position_id=position_id)
    # await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_city_artist")
    await state.update_data({'artist_id': artist_id, 'user_id': user_id, 'remover': remover})
    await call.message.delete()
    await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
                              "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
                              f"❕ Город артиста: <code>{current_city}</code>", reply_markup=geo_1_kb())


# принятие новой геопозиции для позиции
@dp.callback_query_handler(text_startswith='geo_chosen_cities', state='here_change_city_artist')
async def geo_5(cb: CallbackQuery, state: FSMContext):
    info = int(str(cb.data).split('#')[1])
    if info == 0:
        async with state.proxy() as data:
            city = data['city']
            artist_id = int(data['artist_id'])
            user_id = data['user_id']
            remover = data['remover']
            city_id = data['city_id']

    else:
        async with state.proxy() as data:
            artist_id = int(data['artist_id'])
            user_id = data['user_id']
            remover = data['remover']

        city_id = info
        city = get_city_info(info)

    await state.finish()
    update_artist_city(city, city_id, artist_id)

    # update_positionx(position_id)
    get_message, get_photo = get_artist_admin(artist_id)

    if get_photo is not None:
        await cb.message.answer_photo(get_photo, get_message,
                                      reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await cb.message.answer(get_message,
                                reply_markup=artist_edit_open_finl(artist_id, user_id, remover))

# Удаление позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_delete", state="*")
async def artist_edit_delete(call: CallbackQuery, state: FSMContext):
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await call.message.delete()
    await call.message.answer("<b>📁 Вы действительно хотите удалить позицию? ❌</b>",
                              reply_markup=artist_edit_delete_finl())


# Подтверждение удаления позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_delete", state="*")
async def artist_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    async with state.proxy() as data:
        artist_id = data['here_cache_artist_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_artist_remover']
    await state.finish()

    if get_action == "yes":
        #remove_itemx(position_id=position_id)
        remove_artistx(artist_id=artist_id)

        await call.answer("📁 Вы успешно удалили артиста ✅")

        if len(get_artistx(admin=user_id)) >= 1:
            await call.message.edit_text("<b>📁 Выберите нужного Вам артиста 🖍</b>",
                                         reply_markup=artist_edit_open_fp(remover, user_id))
        else:
            await call.message.delete()
    else:
        get_message, get_photo = get_artist_admin(artist_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=artist_edit_open_finl(artist_id, user_id, remover))

# Просмотр истории покупок
@dp.callback_query_handler(text="user_history", state="*")
async def user_history(call: CallbackQuery, state: FSMContext):
    last_purchases = last_purchasesx(call.from_user.id, 5)

    if len(last_purchases) >= 1:
        await call.answer("🎁 Последние 5 покупок")
        await call.message.delete()

        for purchases in last_purchases:
            link_items = await upload_text(call, purchases['purchase_item'])

            await call.message.answer(f"<b>🧾 Чек: <code>#{purchases['purchase_receipt']}</code></b>\n"
                                      f"🎁 Товар: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}шт | {purchases['purchase_price']}₽</code>\n"
                                      f"🕰 Дата покупки: <code>{purchases['purchase_date']}</code>\n"
                                      f"🔗 Товары: <a href='{link_items}'>кликабельно</a>")

        await call.message.answer(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)
    else:
        await call.answer("❗ У вас отсутствуют покупки", True)


# Возвращение к профилю
@dp.callback_query_handler(text="user_profile", state="*")
async def user_profile_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)


# Возвращение к корзине
@dp.callback_query_handler(text="user_cart", state="*")
async def user_cart_return(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    orderdata = get_params_orderx(user_id=user_id)
    #cart_state = orderdata['order_state']
    for order in orderdata:
        #await call.message.edit_text(open_cart_my(call.from_user.id), reply_markup=cart_open_+{'cart_state'}+_inl)
        if order['order_state'] == 'created':
            await call.message.answer(open_cart_my(user_id), reply_markup=cart_open_created_inl)
        if order['order_state'] == 'delivery':
            await call.message.answer(open_cart_my(user_id), reply_markup=cart_open_delivery_inl)
        if order['order_state'] == 'submited':
            await call.message.answer(f"<b>🎁 Активных заказов нет.</b>\n")

################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
########################################### КАТЕГОРИИ ##########################################
# Открытие категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_open:", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print(f'Открытие категорий для покупки user_menu.py 133')
    category_id = int(call.data.split(":")[1])

    get_category = get_categoryx(category_id=category_id)
    city_id = get_city_user(call.from_user.id)[0]
    get_positions = get_position_on_city(category_id, city_id)  # get_positionsx(category_id=category_id)
    print(category_id, city_id)
    if len(get_positions) >= 1:
        await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=products_item_position_swipe_fp(0, category_id, city_id))
    else:
        await call.answer(f"❕ Товары в категории {get_category['category_name']} отсутствуют")


# Вернуться к категориям для покупки
@dp.callback_query_handler(text_startswith="buy_category_return", state="*")
async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
    get_categories = get_all_categoriesx()
    get_settings = get_settingsx()
    city_id = 0
    if get_settings['type_trade'] != 'digital':
        city_id = get_city_user(call.from_user.id)[0]

    if len(get_categories) >= 1:
        await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=products_item_category_swipe_fp(0, city_id))
    else:
        await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
        await call.answer("❗ Категории были изменены или удалены")


# Следующая страница категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_next_page_fp(remover))


# Предыдущая страница категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_backp", state="*")
async def user_purchase_category_prev_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_back_page_fp(remover))

############################################ МАГАЗИН => КАТЕГОРИИ #############################

########################################### МАГАЗИНЫ ##########################################
# Открытие магазина для покупки
@dp.callback_query_handler(text_startswith="buy_shop_open", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print(f'Открытие магазина для покупки user_menu.py 133')
    shop_id = int(call.data.split(":")[1])
    #get_shop = get_shopx(shop_id=shop_id)
    get_shop = get_shopsxx(shop_id=shop_id)
    print(get_shop)
    #if get_shop[8] != None: logo = get_shop[8]
    user_id = call.from_user.id
    city_id = get_city_user(user_id)[0]
    get_positions = get_shopposition_on_city(shop_id, city_id)  # get_positionsx(category_id=category_id)

    if len(get_positions) >= 1:
        #if get_shop['logo'] != None or get_place['logo'] != '':
        logo = get_shop[0]['logo']
        await call.message.answer_photo(logo, f"<b>Магазин : {get_shop[0]['name']}</b>\n" \
                                        f"Адрес : {get_shop[0]['address']}\n" \
                                        f"Телефон : {get_shop[0]['phone']}")
        #await call.message.answer_photo(logo, "<b>🎁 Выберите нужный вам товар:</b>",
        #                                    reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id))
        #else:
        #media = types.MediaGroup()
        #media.attach_photo(types.InputFile('media/Starbucks_Logo.jpg'), 'Превосходная фотография')
        #media.attach_photo(types.InputFile('media/Starbucks_Logo_2.jpg'), 'Превосходная фотография 2')
        #await bot.send_media_group(call.message.chat.id, media=media)

        await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id))
    else:
        await call.answer(f"❕ Товары в магазине {get_shop[2]} отсутствуют")


# Открытие магазина для покупки
@dp.callback_query_handler(text_startswith="book_place_open", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print(f'Открытие магазина для покупки user_menu.py 133')
    place_id = int(call.data.split(":")[1])
    #get_shop = get_shopx(shop_id=shop_id)
    get_place = get_placesx(place_id=place_id)
    print(get_place)
    #if get_shop[8] != None: logo = get_shop[8]
    user_id = call.from_user.id
    city_id = get_city_user(user_id)[0]
    print("|||")
    print(city_id, get_place['place_id'])
    #print(remover, place_id, city_id)
    #get_events = get_events_in_place(place_id)  # get_positionsx(category_id=category_id)

    if get_place['place_id'] != "":
        print("|||->")
        if get_place['logo'] != None or get_place['logo'] != '':
            logo = get_place['logo']
            await call.message.answer_photo(logo, f"<b>Место : {get_place['name']}</b>\n" \
                                              f"Адрес : {get_place['address']}\n" \
                                              f"Телефон : {get_place['phone']}")

            await call.message.answer("<b>Выберите что-нибудь интересное:</b>",
                                      reply_markup=events_in_place_swipe_fp(0, place_id, city_id))
        else:
        #media = types.MediaGroup()
        #media.attach_photo(types.InputFile('media/Starbucks_Logo.jpg'), 'Превосходная фотография')
        #media.attach_photo(types.InputFile('media/Starbucks_Logo_2.jpg'), 'Превосходная фотография 2')
        #await bot.send_media_group(call.message.chat.id, media=media)

            await call.message.answer("<b>Выберите что-нибудь интересное:</b>",
                                    reply_markup=events_in_place_swipe_fp(0, place_id, city_id))
    else:
        await call.answer(f"❕Cобытия места не загружены: {get_place['name']}, уточнить можно по телефону: {get_place['phone']}")


# Открытие магазина для покупки
@dp.callback_query_handler(text_startswith="book_event_open", state="*")
async def user_evebt_in_city_open(call: CallbackQuery, state: FSMContext):
    print(f'Открытие городских событий user_menu.py 1368')
    event_id = int(call.data.split(":")[1])
    get_event = get_eventxx(event_id=event_id)
    #city_id = int(call.data.split(":")[1])
    #get_shop = get_shopx(shop_id=shop_id)
    #get_events_in_city
    #get_shop = get_shopsxx(place_id=place_id)
    print(get_event)
    #if get_shop[8] != None: logo = get_shop[8]
    user_id = call.from_user.id
    #city_id = get_city_user(user_id)[0]
    get_positions = get_shopposition_on_city(shop_id, city_id)  # get_positionsx(category_id=category_id)

    if len(get_positions) >= 1:
        #if get_shop['logo'] != None:
        logo = get_shop[0]['logo']
        await call.message.answer_photo(logo, f"<b>Магазин : {get_shop[0]['name']}</b>\n" \
                                              f"Адрес : {get_shop[0]['address']}\n" \
                                              f"Телефон : {get_shop[0]['phone']}")
        #await call.message.answer_photo(logo, "<b>🎁 Выберите нужный вам товар:</b>",
        #                                    reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id))
        #else:
        #media = types.MediaGroup()
        #media.attach_photo(types.InputFile('media/Starbucks_Logo.jpg'), 'Превосходная фотография')
        #media.attach_photo(types.InputFile('media/Starbucks_Logo_2.jpg'), 'Превосходная фотография 2')
        #await bot.send_media_group(call.message.chat.id, media=media)

        await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                  reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id))
    else:
        await call.answer(f"❕ Товары в магазине {get_shop[2]} отсутствуют")

########################################### ПОЗИЦИИ ##########################################
# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="book_event_open2:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print(f'Карточка товара: user_menu.py  1194')
    event_id = int(call.data.split(":")[1])

    print(event_id)
    get_event = get_eventx(event_id=event_id)
    #if category_id != 0: get_category = get_categoryx(category_id=category_id)
    #else: get_category['category_name'] = 0
    #get_items = get_itemsx(position_id=position_id)
    get_settings = get_settingsx()
    #get_shop = get_shopx(shop_id=shop_id)
    print("|")

    if get_event['event_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_event['event_description']}"
    #get_shop['name']
    send_msg = f"<b>Карточка:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_position['position_name']}</code>\n" \
               f"🏙 Магазин: <code>{get_shop['name']}</code>\n" \
               f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
               f"🗃 Категория: <code></code>\n" \
               f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
               f"{text_description}"
    #{get_category['category_name']}
    #f"📦 Остаток: <code>{len(get_items)}шт</code>" \
    print(get_settings['type_trade'])
    tt = get_settings['type_trade']
    print("||")

    if tt != "digital":
        print("|||-")
        #    product_markup = products_open_finl(position_id, remover, category_id)
        # product_markup = products_open_cart_finl(position_id, remover, category_id)
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(1, position_id, remover, 0, shop_id))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(1, position_id, remover, 0, shop_id))
    elif tt == "digital":
        print("|||--")
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, 0, shop_id))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(0, position_id, remover, 0, shop_id))

# Вернуться к категориям для покупки
@dp.callback_query_handler(text_startswith="buy_parcategory_return", state="*")
async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
    get_categories = get_all_categoriesx()
    get_settings = get_settingsx()
    city_id = 0
    if get_settings['type_trade'] != 'digital':
        city_id = get_city_user(call.from_user.id)[0]

    if len(get_categories) >= 1:
        await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=products_item_shop_open_fp(0, shop_id, city_id))
    else:
        await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
        await call.answer("❗ Категории были изменены или удалены")

########################################### ПОЗИЦИИ ##########################################
# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_parposition_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print(f'Карточка товара: user_menu.py  um2082')
    if call.data.split(":")[4]: city_id = 0
    position_id = int(call.data.split(":")[1])
    #category_id = int(call.data.split(":")[2])
    shop_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    #city_id = int(call.data.split(":")[4])

    print(position_id, shop_id, remover, city_id)

    get_position = get_positionx(position_id=position_id)
    #if category_id != 0: get_category = get_categoryx(category_id=category_id)
    #else: get_category['category_name'] = 0
    get_items = get_itemsx(position_id=position_id)
    get_settings = get_settingsx()
    get_shop = get_shopx(shop_id=shop_id)
    print("|")

    if get_position['position_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_position['position_description']}"
    #get_shop['name']
    send_msg = f"<b>Карточка:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_position['position_name']}</code>\n" \
               f"🏙 Магазин: <code>{get_shop['name']}</code>\n" \
               f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
               f"🗃 Категория: <code></code>\n" \
               f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
               f"{text_description}"
    #{get_category['category_name']}
    #f"📦 Остаток: <code>{len(get_items)}шт</code>" \
    print(get_settings['type_trade'])
    tt = get_settings['type_trade']
    print("||")

    if tt != "digital":
        print("|||-")
        #    product_markup = products_open_finl(position_id, remover, category_id)
        # product_markup = products_open_cart_finl(position_id, remover, category_id)
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(1, position_id, remover, 0, shop_id))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(1, position_id, remover, 0, shop_id))
    elif tt == "digital":
        print("|||--")
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, 0, shop_id))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(0, position_id, remover, 0, shop_id))

# Вернуться к позициям для покупки
@dp.callback_query_handler(text_startswith="buy_parposition_return", state="*")
async def user_purchase_position_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    #category_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])
    shop_id = int(call.data.split(":")[2])
    print("buy_parposition_return")

    get_positions = get_all_positionsx()
    city_id = get_city_user(call.from_user.id)[0]

    if len(get_positions) >= 1:
        await call.message.delete()
        await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                  reply_markup=products_shopitem_position_open_fp(remover, shop_id, city_id))
    else:
        await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
        await call.answer("❗ Позиции были изменены или удалены")

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_parcategory_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_swipe_fp(remover))

# Переключение страницы позиций для покупки
@dp.callback_query_handler(text_startswith="buy_parposition_swipe:", state="*")
async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
    shop_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    get_shop = get_shopx(shop_id=shop_id)

    await call.message.edit_text(f"<b>🎁 Текущий магазин: <code>{get_shop['name']}</code></b>",
                                 reply_markup=products_shopitem_position_swipe_fp(remover, shop_id, city_id))

# Переключение страницы позиций для покупки
@dp.callback_query_handler(text_startswith="buy_position_swipe:", state="*")
async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    get_category = get_categoryx(category_id=category_id)

    await call.message.edit_text(f"<b>🎁 Текущая категория: <code>{get_category['category_name']}</code></b>",
                                 reply_markup=products_item_position_swipe_fp(remover, category_id, city_id))

# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_position_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print(f'Карточка товара: user_menu.py  152')
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    city_id = int(call.data.split(":")[4])
    print(position_id, category_id, remover, city_id)
    #link = await get_start_link(str(f"buy_position_open:{position_id}:0:0:0"), encode=True)
    link = await get_start_link(str(f"deep_link&position_id&{position_id}"), encode=True)

    get_position = get_positionx(position_id=position_id)
    get_category = get_categoryx(category_id=category_id)
    get_items = get_itemsx(position_id=position_id)
    get_settings = get_settingsx()

    if get_position['position_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_position['position_description']}"

    send_msg = f"<b>Карточка:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_position['position_name']}</code>\n" \
               f"🏷 Ссылка: <code>{link}</code>\n" \
               f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
               f"🗃 Категория: <code>{get_category['category_name']}</code>\n" \
               f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
               f"{text_description}"

    #f"📦 Остаток: <code>{len(get_items)}шт</code>" \
    print(get_settings['type_trade'])
    tt = get_settings['type_trade']

    if tt != "digital":
    #    product_markup = products_open_finl(position_id, remover, category_id)
    # product_markup = products_open_cart_finl(position_id, remover, category_id)
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(1, position_id, remover, category_id, 0))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(1, position_id, remover, category_id, 0))
    elif tt == "digital":
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, category_id, 0))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(0, position_id, remover, category_id, 0))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="artist_edit_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужного артиста:</b>",
                                 reply_markup=artist_edit_open_fp(remover, user_id))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_swipe_fp(remover, city_id))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_shop_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_shop_swipe_fp(remover, city_id))

# Вернуться к позициям для покупки
@dp.callback_query_handler(text_startswith="buy_position_return", state="*")
async def user_purchase_position_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    shop_id = int(call.data.split(":")[3])

    #get_positions = get_all_positionsx()
    city_id = get_city_user(call.from_user.id)[0]
    print(remover, category_id, shop_id, city_id)
    print("buy_position_return")

    #if len(get_positions) >= 1:
    await call.message.delete()
    if shop_id == 0:
        print("||||--=")
        await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                  reply_markup=products_item_position_swipe_fp(remover, category_id, city_id))
    elif category_id == 0:
        print("||||--==---")
        await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                  reply_markup=products_shopitem_position_swipe_fp(remover, shop_id, city_id))
    #else:
    #    await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
    #    await call.answer("❗ Позиции были изменены или удалены")


########################################### ПОКУПКА ##########################################
# Выбор количества товаров в корзине
@dp.callback_query_handler(text_startswith="add_item_cart", state="*")
async def user_purchase_addcart(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    print("Добавление в корзину")
    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    get_count = len(get_items)

    if get_count == 1:
        await state.update_data(here_cache_position_id=position_id)
        await state.finish()

        await call.message.delete()
        await call.message.answer(f"<b>1 шт. в наличии. Добавить товар(ы) в корзину?</b>\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                  f"📦 Остаток: <code>1шт</code>\n"
                                  f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                  reply_markup=products_addcart_confirm_finl(position_id, 1))
    elif get_count >= 1:
        await state.update_data(here_cache_position_id=position_id)
        await state.set_state("here_itemsadd_cart")

        await call.message.delete()
        await call.message.answer(f"<b>🎁 Введите количество товаров для покупки</b>\n"
                                  f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                  f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
    else:
        await call.answer("🎁 Товара нет в наличии")


# Принятие количества товаров в корзине
@dp.message_handler(state="here_itemsadd_cart")
async def user_purchase_select_count(message: Message, state: FSMContext):
    position_id = (await state.get_data())['here_cache_position_id']
    get_position = get_positionx(position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        if get_count > len(get_items): get_count = len(get_items)
    else:
        get_count = len(get_items)

    send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Введите количество товаров для покупки\n" \
                   f"▶ От <code>1</code> до <code>{get_count}</code>\n" \
                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n" \
                   f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>"
    print("test")
    if message.text:  # .isdigit()
        get_count = int(message.text)
        amount_pay = int(get_position['position_price']) * get_count

        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                # if int(get_user['user_balance']) >= amount_pay:
                await state.finish()
                await message.answer(f"<b>🎁 Вы действительно хотите добавить в корзину товар(ы)?</b>\n"
                                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                     f"📦 Остаток: <code>{get_count}шт</code>\n"
                                     f"💰 Сумма добавляемых товаров: <code>{amount_pay}₽</code>",
                                     reply_markup=products_addcart_confirm_finl(position_id, get_count))
                # else:
                needed_to_refill = amount_pay - int(get_user['user_balance'])
                await state.finish()
                await message.answer(f"<b>🎁 Вы действительно хотите добавить в корзину товар(ы)?</b>\n"
                                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                     f"📦 Остаток: <code>{get_count}шт</code>\n"
                                     f"💰 Сумма добавляемых товаров: <code>{amount_pay}₽</code>",
                                     f"💰 Сумма к пополнению: <code>{needed_to_refill}₽</code>",
                                     reply_markup=products_addcart_confirm_finl(position_id, get_count))

            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n" + send_message)
        else:
            await state.finish()
            await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>")
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n" + send_message)


# Подтверждение добавления товара в корзину
@dp.callback_query_handler(text_startswith="xaddcart_item", state="*")
async def user_addcart_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    get_count = int(call.data.split(":")[3])

    if get_action == "yes":
        await call.message.edit_text("<b>🔄 Ждите, товары подготавливаются</b>")

        get_position = get_positionx(position_id=position_id)
        get_items = get_itemsx(position_id=position_id)
        get_user = get_userx(user_id=call.from_user.id)

        amount_pay = int(get_position['position_price'] * get_count)

        if 1 <= int(get_count) <= len(get_items):
            save_items, send_count, split_len = buy_itemx(get_items, get_count)
            #await notify(dp, f"Позиция: {get_position['position_name']} добавлена в корзину пользователем: {call.from_user.id}.")


            # уточнение цены за количество в наличии
            if get_count != send_count:
                amount_pay = int(get_position['position_price'] * send_count)
                get_count = send_count

            receipt = get_unix()
            add_time = get_date()
            print(add_time)

            await call.message.delete()

            # if split_len == 0:
            #    await call.message.answer("\n\n".join(save_items), parse_mode="None")
            # else:
            #    for item in split_messages(save_items, split_len):
            #        await call.message.answer("\n\n".join(item), parse_mode="None")
            #        await asyncio.sleep(0.3)
            await asyncio.sleep(0.3)
            # update_userx(get_user['user_id'], user_balance=get_user['user_balance'] - amount_pay)
            i = 0
            #users_order = get_user_orderx(get_user['user_id'])
            users_order = get_params_orderx(user_id=get_user['user_id'], order_state='created')
            print(users_order)
            alength = len(users_order)
            for i in range(alength):
                print(users_order[i]['order_id'])

            print('test2')
            #print(users_order['order_id'])

            if not users_order:
                create_orderx(call.from_user.id, get_user['user_login'], get_user['user_name'], 'created', str(add_time),
                              receipt)
                users_order = get_params_orderx(user_id=get_user['user_id'], order_state='created')
                #print(users_order['order_id'])
            print('test3')
            for i in range(alength):
                print(users_order[i]['order_id'])
            order_id = users_order[i]['order_id']
            # price = int(get_position['position_price'])
            add_order_itemx(order_id, position_id, get_count, get_position['position_price'], receipt, get_position['position_user_id'])
            # add_order_itemx(1, 1, 1, 1, 1)
            if len(get_user['user_login']) >= 1: auser = get_user['user_login']
            else: auser = get_user['user_id']

            await notify(dp, f"Позиция: {get_position['position_name']} добавлена в корзину. Пользователь: @{auser}.")

            await call.message.answer(f"<b>✅ Вы успешно добавили товар(ы) в корзину</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🧾 Чек: <code>#{receipt}</code>\n"
                                      f"🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>\n"
                                      f"🕰 Дата покупки: <code>{add_time}</code>",
                                      reply_markup=menu_frep(call.from_user.id))
        else:
            await call.message.answer("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                                      reply_markup=menu_frep(call.from_user.id))
    else:
        if len(get_all_categoriesx()) >= 1:
            await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                         reply_markup=products_item_category_open_fp(0,0))
        else:
            await call.message.edit_text("<b>✅ Вы отменили покупку товаров.</b>")


# Удаление корзины
@dp.callback_query_handler(text_startswith="del_user_cart", state="*")
async def del_user_cart(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b> Удалить корзину и ее позиции?</b>",
                                 reply_markup=confirm_delete_user_cart_inl)

# Подтверждение удаления корзины
@dp.callback_query_handler(text_startswith="confirm_del_user_cart", state="*")
async def confirm_del_user_cart(call: CallbackQuery, state: FSMContext):

    user_id=call.from_user.id
    print(user_id)
    order=get_orderx(user_id=user_id)
    print(order)
    order_id=order['order_id']
    print(order_id)
    remove_ordersx(order_id=order_id)
    remove_orders_itemx(order_id=order_id)
    print("|||| -   - ||||")
    await call.message.edit_text("<b>✅ Вы удалили корзину.</b>")


#######################################################################################
# **************************  CHECK OUT CART ******************************************
#######################################################################################

# Оформление заказа по корзине - Адрес
@dp.callback_query_handler(text="checkout_start", state="*")
async def checkout_start(call: CallbackQuery, state: FSMContext):
    # user_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    get_user = get_userx(user_id=user_id)
    ub = get_user['user_balance']
    cart_sum = calc_cart_summ(user_id=user_id)
    delivery = 200
    order_total = cart_sum + delivery
    adr = geo = phone = 0
    users_order = get_user_orderx(user_id)
    order_id = users_order['order_id']
    touser_id = get_cart_sellersx(order_id)

    print(user_id)

    if get_user['user_address'] != "":
        print("Адрес есть")
        adr = 1
    if get_user['user_geocode'] != "":
        print("Геокод есть")
        geo = 1
    if get_user['user_phone'] != "":
        print("Телефон есть")
        phone = 1

    await call.message.answer(f"<b> Начинаем оформление заказа.</b>\n")

    if phone == 0:
        await state.set_state("enter_phone_auto")
        # await call.message.delete()
        # await call.message.answer(f"<b> Введите пожалуйста адрес доставки.</b>\n")

    if adr == 0:
        await state.set_state("enter_address_manualy")

    if ub < order_total:
        await state.set_state("user_balance_lower_than_cart")
        await call.message.delete()
        await call.message.answer(f"<b>Суммы на Вашем балансе не достаточно для оформления заказа.</b>\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f" Баланс: <code>{ub}</code>\n"
                                  f" Сумма заказа: <code>{order_total}</code>\n",
                                  reply_markup=order_user_refill)
    else:
        await state.set_state("checkout_finish")
        await call.message.answer(f"<b>Продолхить оформление заказа:.</b>\n",
                                  reply_markup=checkout_step2_accept)

    #await state.finish()


# Принятие адреса для доставки
#@dp.message_handler(state="checkout_finish")
#async def checkout_finish(message: Message, state: FSMContext):
@dp.callback_query_handler(text="checkout_finish", state="*")
async def checkout_finish(call: CallbackQuery, state: FSMContext):
    print('checkout_finish')
#проверка - есть вопросы без ответов
    touser_id = call.from_user.id
    cm = get_user_messagesx(to_uid=touser_id, state='created')
    if len(cm) > 0:
        print("Messages present:" + str(touser_id))
#статус заказа - delivery
    order_data = get_orderx(user_id=touser_id)
    order_id = order_data['order_id']
    os = update_orderx(order_id=order_id, order_state='delivery')
    await call.message.answer(f"<b>Начинаем доставку товара Вашей корзины.</b>")
    print('Сумма заказа на холде')
#холд суммы заказа
    validity = 5
    state = 'created'
    cart_sum = calc_cart_summ(user_id=touser_id)
    delivery = 200
    amount = cart_sum + delivery
    #amount = order_data['order_total']
    buyer = touser_id
    order_sellers = get_order_sellers(order_id)
    print(order_sellers)
    if(len(order_sellers)>1): print("продавцов более 1")
    #for seller in order_sellers:
    print(type(order_sellers))
    order_sellers = order_sellers.strip('[[')
    order_sellers = order_sellers.strip(']]')
    #seller=list(order_sellers)
    h = create_holdx(int(order_id), int(buyer), int(str(order_sellers)), int(amount), int(validity), state)
    i = update_userx(user_id = buyer, user_hold = amount)
    await call.message.answer(f"<b>Денежные средства в размере {amount}р. успешно заблокированы до \n"
                              f"подтверждения получения покупателем товара.</b>")

# Оформление заказа по корзине - Адрес
@dp.callback_query_handler(text="submit_order", state="*")
async def submit_order(call: CallbackQuery, state: FSMContext):
    #buyer
    user_id = call.from_user.id
    buyer_data = get_userx(user_id=user_id)
    print(buyer_data)
    order_data = get_orderx(user_id=user_id)
    order_id = order_data['order_id']
    print(order_id)
    order_sellers = get_order_sellers(order_id)
    print(order_sellers)
    if(len(order_sellers)>1): print("продавцов более 1")
    #for seller in order_sellers:
    print(type(order_sellers))
    order_sellers = order_sellers.strip('[[')
    order_sellers = order_sellers.strip(']]')
    print(order_sellers)
    hold_data = get_orders_holdsx(order_id)
    #hold_data = hold_data.strip('[')
    #hold_data = hold_data.strip(']')
    print(hold_data[0]['seller'])
    #seller
    seller_data = get_userx(user_id=hold_data[0]['seller'])
    print(seller_data)
    #hold_data['seller']
#изменение статуса заказа   submitted
    os = update_orderx(order_id=order_id, order_state='submitted', active=0)
#снятие холда с суммы заказа
    a = update_holdx(order_id = order_id, state = 'released')
#транзакция
    seller_rest = int(seller_data['user_balance'])+int(hold_data[0]['amount'])
    buyer_rest = int(buyer_data['user_balance'])-int(hold_data[0]['amount'])
    #списание у покупателя
    b = update_userx(user_id, user_balance=buyer_rest)
    #пополнение у продавца
    c = update_userx(order_sellers, user_balance=seller_rest)

    receipt = get_unix()
    buy_time = get_date()

    await call.message.answer(f"<b>Покупка завершена, возвращайтесь!</b>\n")

@dp.callback_query_handler(text="reply_toorder_message", state="*")
async def reply_toorder_message(call: CallbackQuery, state: FSMContext):
    print('reply_toorder_message')
    # order_id = int(call.data.split(":")[1])
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    print(user_id)
    get_user = get_userx(user_id=user_id)

    # get_user = get_userx(user_id=call.from_user.id)
    await state.set_state("reply_toorder_message_fin")

    # await call.message.delete()
    await call.message.answer(f"<b>Пожалуйста, введите сообщение для покупателя:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="reply_toorder_message_fin")
async def reply_toorder_message_fin(message: Message, state: FSMContext):
    print('reply_toorder_message_fin')
    # user_id = int(call.data.split(":")[1])
    # order_id = int(message.data.split(":")[1])
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    users_order = get_user_orderx(user_id)
    order_id = users_order['order_id']
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        messagetxt = str(message.text)
        print(str(user_id) + str(messagetxt))
        touser_id = get_cart_sellersx(order_id)
        print(touser_id)

        add_messagex(from_id=user_id, to_id=touser_id, order_id = order_id, txtmessage=messagetxt, photo='', state='responded')

    await message.delete()
    await message.answer(f"<b>✅ Было отправлено следующее сообщение покупателю:</b>\n"
                         + messagetxt, reply_markup=cart_enter_message_finl(user_id))

    cm = get_user_messagesx(to_uid=touser_id, state='responded')
    if len(cm) > 0:
        print("Messages present:" + str(touser_id))

    await dp.bot.send_message(chat_id=touser_id, text=f"Сообщение/вопрос по заказу от продавца:"+messagetxt, reply_markup=reply_order_message_finl(order_id))

@dp.callback_query_handler(text="enter_message_manualy", state="*")
async def enter_message_manualy(call: CallbackQuery, state: FSMContext):
    print('enter_message_manualy')
    # order_id = int(call.data.split(":")[1])
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    print(user_id)
    get_user = get_userx(user_id=user_id)

    # get_user = get_userx(user_id=call.from_user.id)
    await state.set_state("enter_message_manualy_fin")

    # await call.message.delete()
    await call.message.answer(f"<b>Пожалуйста, введите сообщение для продавца:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_message_manualy_fin")
async def enter_message_manualy_fin(message: Message, state: FSMContext):
    print('enter_message_manualy_fin')
    # user_id = int(call.data.split(":")[1])
    # order_id = int(message.data.split(":")[1])
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    users_order = get_user_orderx(user_id)
    order_id = users_order['order_id']
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        messagetxt = str(message.text)
        print(str(user_id) + str(messagetxt))
        touser_id = get_cart_sellersx(order_id)
        print(touser_id)

        add_messagex(from_id=user_id, to_id=touser_id, order_id = order_id, txtmessage=messagetxt, photo='', state='created')

    await message.delete()
    await message.answer(f"<b>✅ Было отправлено следующее сообщение продавцу:</b>\n"
                         + messagetxt, reply_markup=cart_enter_message_finl(user_id))

    cm = get_user_messagesx(to_uid=touser_id, state='created')
    if len(cm) > 0:
        print("Messages present:" + str(touser_id))

    await dp.bot.send_message(chat_id=touser_id, text=f"Сообщение/вопрос по заказу от покупателя:"+messagetxt, reply_markup=reply_order_message_finl(order_id))

@dp.callback_query_handler(text_startswith="enter_phone_auto", state="*")
async def enter_phone_man(call: CallbackQuery, state: FSMContext):
    print('enter_phone_auto')
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_phone_auto_fin")

    button_phone = KeyboardButton(text="Делись!", request_contact=True)
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button_phone)
    await call.message.answer(f"<b>✅ Вы можете поделиться своим номером телефона.</b>", reply_markup=menu_frep(message.from_user.id))

    # get_user = get_userx(user_id=call.from_user.id)

    # await state.finish()

    # await Person.contact.set()

    '''await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш номер телефона:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")'''

@dp.message_handler(content_types=['contact'], state="enter_phone_auto_fin")  # content_types=ContentType.CONTACT,
async def contacts(message: Message, state: FSMContext):
    phone = message.contact.phone_number

    print(phone)
    phone = str(message.text)
    phone = message.contact.phone_number
    update_userx(message.from_user.id, user_phone=phone)

    await message.answer(f"Ваш номер сохранен в Вашем личном кабинете: {message.contact.phone_number}",
                         reply_markup=ReplyKeyboardRemove())  # , reply_markup=types.ReplyKeyboardRemove()
    await state.finish()

    await message.answer(f"<b>✅ Номер телефон был успешно изменен на следующий:</b>\n"
                         + str(phone), reply_markup=accept_saved_phone(message.from_user.id))


'''
    await message.answer("🔸 Мы снова с Вами!.\n"
                     "🔸 Если не появились вспомогательные кнопки\n"
                     "▶ Введите /start",
                     reply_markup=menu_frep(message.from_user.id)) '''


# Принятие адреса для доставки
@dp.message_handler(state="enter_phone_auto_fin2")
async def user_get_phone(message: Message, state: FSMContext):
    print('enter_phone_auto_fin')
    # user_id = int(call.data.split(":")[1])
    phone = message.contact.phone_number
    # phone = int(message.data.split(":")[1])
    get_user = get_userx(user_id=message.from_user.id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    print(phone)

    # if message.text:
    #    phone = str(message.text)
    #    update_userx(message.from_user.id, user_phone=phone)

    await message.delete()
    await message.answer(f"<b>✅ Номер телефон был успешно изменен на следующий:</b>\n"
                         + phone, reply_markup=accept_saved_phone(message.from_user.id))

@dp.callback_query_handler(text_startswith="enter_phone_manualy", state="*")
async def enter_phone_man(call: CallbackQuery, state: FSMContext):
    print('enter_phone_manualy')
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    # get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_phone_manualy_fin")

    await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш номер телефона:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_phone_manualy_fin")
async def user_enter_phone(message: Message, state: FSMContext):
    print('enter_phone_manualy_fin')
    # user_id = int(call.data.split(":")[1])
    get_user = get_userx(user_id=message.from_user.id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        phone = str(message.text)
        update_userx(message.from_user.id, user_phone=phone)

    await message.delete()
    await message.answer(f"<b>✅ Номер телефон был успешно изменен на следующий:</b>\n"
                         + phone, reply_markup=accept_saved_phone(message.from_user.id))

@dp.callback_query_handler(text_startswith="enter_address_manualy", state="*")
async def enter_address_man(call: CallbackQuery, state: FSMContext):
    print('enter_address_manualy')
    # user_id = int(call.data.split(":")[1])
    # user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    # get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_address_manualy_fin")

    await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш адрес:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_address_manualy_fin")
async def user_enter_addr(message: Message, state: FSMContext):
    print('enter_address_manualy_fin')
    #user_id = int(message.split(":")[1])
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        address = str(message.text)
        update_userx(message.from_user.id, user_address=address)

    await message.delete()
    await message.answer(f"<b>✅ Адрес доставки был успешно изменен на следующий:</b>\n"
                         + address, reply_markup=accept_saved_adr(message.from_user.id))

# Выбор количества товаров для покупки
@dp.callback_query_handler(text_startswith="buy_item_select", state="*")
async def buy_item_select(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        if get_count > len(get_items): get_count = len(get_items)
    else:
        get_count = len(get_items)

    if int(get_user['user_balance']) >= int(get_position['position_price']):
        if get_count == 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Количество: <code>1шт</code>\n"
                                      f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                      reply_markup=products_confirm_finl(position_id, 1))
        elif get_count >= 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.set_state("here_item_count")

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Введите количество товаров для покупки</b>\n"
                                      f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
        else:
            await call.answer("🎁 Товаров нет в наличии")
    else:
        #await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)
        #await call.message.delete()
        await call.message.answer(f"<b>❗ У вас недостаточно средств. Пополните баланс</b>", reply_markup=charge_button_add(0))

# -------------------------------------------------------------------------------------
# Выбор количества товаров для покупки
@dp.callback_query_handler(text_startswith="buy_item_select", state="*")
async def user_purchase_select(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        if get_count > len(get_items): get_count = len(get_items)
    else:
        get_count = len(get_items)

    if int(get_user['user_balance']) >= int(get_position['position_price']):
        if get_count == 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Количество: <code>1шт</code>\n"
                                      f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                      reply_markup=products_confirm_finl(position_id, 1))
        elif get_count >= 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.set_state("here_item_count")

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Введите количество товаров для покупки</b>\n"
                                      f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
        else:
            await call.answer("🎁 Товаров нет в наличии")
    else:
        #await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)
        #await call.message.delete()
        await call.message.answer(f"<b>❗ У вас недостаточно средств. Пополните баланс</b>", reply_markup=charge_button_add(0))

# Принятие количества товаров для покупки
@dp.message_handler(state="here_item_count")
async def user_purchase_select_count(message: Message, state: FSMContext):
    position_id = (await state.get_data())['here_cache_position_id']

    get_position = get_positionx(position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        if get_count > len(get_items): get_count = len(get_items)
    else:
        get_count = len(get_items)

    send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Введите количество товаров для покупки\n" \
                   f"▶ От <code>1</code> до <code>{get_count}</code>\n" \
                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n" \
                   f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>"

    if message.text.isdigit():
        get_count = int(message.text)
        amount_pay = int(get_position['position_price']) * get_count

        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                if int(get_user['user_balance']) >= amount_pay:
                    await state.finish()
                    await message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                         f"📦 Количество: <code>{get_count}шт</code>\n"
                                         f"💰 Сумма к покупке: <code>{amount_pay}₽</code>",
                                         reply_markup=products_confirm_finl(position_id, get_count))
                else:
                    await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n" + send_message)
            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n" + send_message)
        else:
            await state.finish()
            await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>")
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n" + send_message)

# Подтверждение покупки товара
@dp.callback_query_handler(text_startswith="xbuy_item", state="*")
async def user_purchase_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    get_count = int(call.data.split(":")[3])

    if get_action == "yes":
        await call.message.edit_text("<b>🔄 Ждите, товары подготавливаются</b>")

        get_position = get_positionx(position_id=position_id)
        get_items = get_itemsx(position_id=position_id)
        get_user = get_userx(user_id=call.from_user.id)

        amount_pay = int(get_position['position_price'] * get_count)

        if 1 <= int(get_count) <= len(get_items):
            if int(get_user['user_balance']) >= amount_pay:
                save_items, send_count, split_len = buy_itemx(get_items, get_count)

                if get_count != send_count:
                    amount_pay = int(get_position['position_price'] * send_count)
                    get_count = send_count

                receipt = get_unix()
                buy_time = get_date()

                await call.message.delete()
                if split_len == 0:
                    await call.message.answer("\n\n".join(save_items), parse_mode="None")
                else:
                    for item in split_messages(save_items, split_len):
                        await call.message.answer("\n\n".join(item), parse_mode="None")
                        await asyncio.sleep(0.3)

                update_userx(get_user['user_id'], user_balance=get_user['user_balance'] - amount_pay)
                add_purchasex(get_user['user_id'], get_user['user_login'], get_user['user_name'], receipt, get_count,
                              amount_pay, get_position['position_price'], get_position['position_id'],
                              get_position['position_name'], "\n".join(save_items), buy_time, receipt,
                              get_user['user_balance'], int(get_user['user_balance'] - amount_pay))

                await notify(dp, f"Продана позиция: {get_position['position_name']}")
                await call.message.answer(f"<b>✅ Вы успешно купили товар(ы)</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"🧾 Чек: <code>#{receipt}</code>\n"
                                          f"🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>\n"
                                          f"🕰 Дата покупки: <code>{buy_time}</code>",
                                          reply_markup=menu_frep(call.from_user.id))
            else:
                await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
        else:
            await call.message.answer("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                                      reply_markup=menu_frep(call.from_user.id))
    else:
        if len(get_all_categoriesx()) >= 1:
            await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                         reply_markup=products_item_category_open_fp(0,0))
        else:
            await call.message.edit_text("<b>✅ Вы отменили покупку товаров.</b>")

