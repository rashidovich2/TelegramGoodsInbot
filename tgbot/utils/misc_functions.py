# - *- coding: utf- 8 - *-
import asyncio
import json
import random
import datetime
import time

import requests
import subprocess

import aiogram
from aiogram import Dispatcher
from aiogram import executor
from aiogram import Bot, types
#from aiogram.types import Message
#from aiogram.utils import exceptions, executor
#from aiogram.methods import SendMessage, SendPhoto, SendVideo, SendAnimation
from aiogram.utils.deep_linking import get_start_link, decode_payload
from bs4 import BeautifulSoup

from tgbot.data.config import get_admins, BOT_VERSION, BOT_DESCRIPTION
from tgbot.keyboards.reply_z_all import menu_frep
from tgbot.services.api_session import AsyncSession
from tgbot.loader import bot
from tgbot.services.api_sqlite import get_settingsx, update_settingsx, get_userx, get_all_positionsx, \
    update_positionx, get_all_categoriesx, get_all_purchasesx, get_all_refillx, get_all_usersx, get_all_itemsx, \
    get_itemsx, get_positionx, get_categoryx, get_all_positionsidx, get_requestx, get_user_orderx, get_cart_positionsx, \
    get_orderx, get_purchasesx, get_purchasesxx, get_shopx, get_artistx, get_planed_postx, get_planed_eventsx, get_tohour_postx,\
    update_tohour_postx, get_users_by_cities, get_users_by_citiesx, get_delivery_seller_options, get_params_orderx, get_orderxo, \
    get_userxxx, get_upaymentx

from tgbot.utils.const_functions import get_unix, convert_day

#bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Уведомление и проверка обновления при запуске бота
async def on_startup_notify(dp: Dispatcher):
    if len(get_admins()) >= 1:
        await send_admins(f"<b>✅ Бот был успешно запущен</b>\n"
                          f"➖➖➖➖➖➖➖➖➖➖\n"
                          f"{BOT_DESCRIPTION}\n"
                          f"➖➖➖➖➖➖➖➖➖➖\n"
                          f"<code>❗ Данное сообщение видят только администраторы бота.</code>",
                          markup="default")
        await check_update()

# Рассылка сообщения всем администраторам
async def send_admins(message, markup=None, not_me=0):
    for admin in get_admins():
        if markup == "default":
            markup = menu_frep(admin)

        try:
            if str(admin) != str(not_me):
                await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
        except:
            pass

# Автоматическая очистка ежедневной статистики после 00:00
async def update_profit_day():
    await send_admins(get_statisctics())
    update_settingsx(misc_profit_day=get_unix())


# Автоматическая очистка еженедельной статистики в понедельник 00:01
async def update_profit_week():
    update_settingsx(misc_profit_week=get_unix())

async def post_every_eighteen():
    print("||||")
    posts = get_planed_postx(mode="evening")
    #print(posts)
    for post in posts:
        asyncio.create_task(functions_advertising_make_bg(post))

async def post_evening_events():
    print("||||)")
    events = get_planed_eventsx()
    for event in events:
         asyncio.create_task(functions_advertising_events_bg(event))

async def post_half_eight():
    print("||||_")
    posts = get_planed_postx(mode_evening="evening")
    print(posts)
    for post in posts:
         asyncio.create_task(functions_advertising_make_bg(post))
         #time.sleep(60)


async def reinvite_sellers_by_city():
    print("*CITIES CITIZENS MESSAGING*")
    cities = get_users_by_citiesx()
    for city in cities:
        print(city)
        if city['user_city_id'] is None:
            #message = "Выберите пожалуйста Ваш город в боте."
            message = f"Выберите пожалуйста Ваш город в боте.\n" \
                      f"Мы сможем предложить Вам товары \n" \
                      f"от продавцов в Вашем городе."
            print(message)
        elif city['user_city_id'] != 0:
            message = str(city['user_city']) + ", продавцы товаров, добро пожаловать!"
            print(message)

        receive_users, block_users, how_users = 0, 0, 0

        posttype = "text"
        test = "yes"
        #get_users = get_all_usersx()
        get_users = get_usersx(user_city_id=city['user_city_id'])

        #get_users = get_userxx(user_city_id=34)
        print(get_users)

        for user in get_users:
            if user['user_city_id']:
                message = str(user['user_city']) + ", продавцы товаров, добро пожаловать!"
            elif city['user_city_id']:
                message = "Выберите пожалуйста свой город в профиле, наш бот Вам предложит товары в Вашем городе."
            try:
                if test == "yes": user['user_id'] = 919148970
                if posttype == "text":
                    await bot.send_message(user['user_id'], message, disable_web_page_preview=True)
                elif post[1] == "photo":
                    await bot.send_photo(
                        chat_id=user['user_id'],
                        photo=post[4],
                        caption=post[9] if post[9] else None)
                elif post[1] == "video":
                    await bot.send_video(
                        chat_id=user['user_id'],
                        video=post[5],
                        caption=post[9] if post[9] else None)
                elif post[1] == "animation":
                    await bot.send_animation(
                        chat_id=user['user_id'],
                        animation=message,
                        caption=post[9] if post[9] else None)

                receive_users += 1

            except:
                block_users += 1

            how_users += 1

            if how_users % 10 == 0:
                await send_admins(f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>")

            await asyncio.sleep(0.05)

        #await update_post(post[0], state = "sended")
        await send_admins(
            f"<b>📢 Рассылка была завершена ✅</b>\n"
            f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
            f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
        )

async def post_every_half_hour():
    print("||||")
    posts = get_planed_postx(mode="halfhour")
    #print(posts)
    for post in posts:
         asyncio.create_task(functions_advertising_make_bg(post))
         #time.sleep(60)

async def sellers_news():
    print("||||")
    posts = get_sellers_news_postx(tag = "selnews")
    #updposts = update_tohour_postx()
    #print(posts)
    for post in posts:
        asyncio.create_task(functions_advertising_make_bg(post))

async def posts3_every_hour():
    print("||||")
    posts = get_3tohour_postx()
    #updposts = update_tohour_postx()
    #print(posts)
    for post in posts:
        asyncio.create_task(functions_advertising_make_bg(post))

async def post_every_hour():
    print("||||")
    posts = get_tohour_postx()
    updposts = update_tohour_postx()
    #print(posts)
    for post in posts:
         asyncio.create_task(functions_advertising_make_bg(post))


async def functions_advertising_make_bg(post, markup=None):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()
    #get_users = get_userx(user_id=919148970)
    test = "no"
    #print(get_usersx)
    print(post)
    #dt_create = datetime.datetime.strptime(post[7], '%Y-%m-%d %H:%M:%S')
    #utime = time.mktime(cur_time.timetuple())
    #print(utime)
    #dtpost_create = time.mktime(dt_create.timetuple())
    #print(dtpost_create)

    if markup == "default":
        markup = menu_frep(admin)
    #get_users = "919148970"

    for user in get_users:
        try:
            if test == "yes": user['user_id'] = 919148970
            if post[1] == "text":
                await bot.send_message(user['user_id'], post[3], disable_web_page_preview=True)
                #await bot.send_message(user['user_id'], post[2], reply_markup = markup, disable_web_page_preview=True)
            elif post[1] == "photo":
                await bot.send_photo(
                    chat_id=user['user_id'],
                    photo=post[4], #.send_photo.file_id,
                    caption=post[9] if post[9] else None)
            elif post[1] == "video":
                #print("|_>>>>")
                await bot.send_video(
                    chat_id=user['user_id'],
                    video=post[5],
                    caption=post[9] if post[9] else None)
            elif post[1] == "animation":
                #print("|_>>>>>")
                await bot.send_animation(
                    chat_id=user['user_id'],
                    animation=message,
                    caption=post[9] if post[9] else None)

            receive_users += 1
        except:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await send_admins(f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>")

        await asyncio.sleep(0.05)

    await update_post(post[0], state = "sended")
    await send_admins(
        f"<b>📢 Рассылка была завершена ✅</b>\n"
        f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
        f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
    )


async def functions_advertising_events_bg(event, markup=None):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()
    #print(":::")
    #get_users = get_userxx(user_city_id = post[10])
    #get_users = get_userx(user_id=919148970)
    test = "no"
    #print(get_usersx)
    print(event)
    if markup == "default":
        markup = menu_frep(admin)
        #get_users = "919148970"

    '''ev_command = event[1] if event[1] else None
    ev_desc = event[2] if event[2] else None
    ev_place = event[3] if event[3] else None
    ev_address = event[4] if event[4] else None

    caption = f" Коллектив: {ev_command}  \n"
    f"<b>🔶 Описание: 🔶</b> {ev_desc} \n"\
    f"<b>🔶 Место: 🔶</b> {ev_place} \n"\
    f"<b>🔶 Адресс: 🔶</b> {ev_address} \n"'''

    #dtevent_time = datetime.datetime.strptime(event[6], '%Y-%m-%d %H:%M:%S')

    for user in get_users:
        try:
            if test == "yes": user['user_id'] = 919148970
            if event[0] == "":
                await bot.send_message(user['user_id'], event[1], disable_web_page_preview=True)
                #await bot.send_message(user['user_id'], post[2], reply_markup = markup, disable_web_page_preview=True)
            elif event[0] != "":
                await bot.send_photo(
                    chat_id=user['user_id'],
                    photo=event[0],
                    caption=event[1])   #event[4] if event[4] else None) #.send_photo.file_id, if event[2] else None
            elif event[1] == "video":
                #print("|_>>>>")
                await bot.send_video(
                    chat_id=user['user_id'],
                    video=event[5],
                    caption=event[4] if event[4] else None)
            elif event[1] == "animation":
                #print("|_>>>>>") None
                await bot.send_animation(
                    chat_id=user['user_id'],
                    animation=message,
                    caption=event[9] if event[9] else None)

            receive_users += 1
        except:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await send_admins(f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>")

        await asyncio.sleep(0.05)

    await send_admins(
        f"<b>📢 Рассылка была завершена ✅</b>\n"
        f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
        f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
    )
    #update_post(event[0], state = 'sended')

# Автоматическая проверка обновления каждые 24 часа
async def check_update():
    update_link = ""
'''

# Автоматическая проверка обновления каждые 24 часа
async def check_update(aSession: AsyncSession):
    session = await aSession.get_session()

    try:
        response = await session.get("https://sites.google.com/view/check-update-autoshop/main-page", ssl=False)
        soup_parse = BeautifulSoup(await response.read(), "html.parser")
        get_bot_update = soup_parse.select("p[class$='CDt4Ke zfr3Q']")[0].text.split("^^^^^")

        if float(get_bot_update[0]) > float(BOT_VERSION):
            if "*****" in get_bot_update[2]:
                get_bot_update[2] = get_bot_update[2].replace("*****", "\n")

            await send_admins(f"<b>❇ Вышло обновление: <a href='{get_bot_update[1]}'>Скачать</a></b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖\n"
                              f"{get_bot_update[2]}\n"
                              f"➖➖➖➖➖➖➖➖➖➖\n"
                              f"<code>❗ Данное сообщение видят только администраторы бота.</code>")
    except Exception as ex:
        print(f"Error check update: {ex}")
'''

# Получение faq
def get_faq(user_id, send_message):
    get_user = get_userx(user_id=user_id)

    if "{user_id}" in send_message:
        send_message = send_message.replace(
            "{user_id}", f"<b>{get_user['user_id']}</b>")
    if "{username}" in send_message:
        send_message = send_message.replace(
            "{username}", f"<b>{get_user['user_login']}</b>")
    if "{firstname}" in send_message:
        send_message = send_message.replace(
            "{firstname}", f"<b>{get_user['user_name']}</b>")

    return send_message


# Загрузка текста на текстовый хостинг
async def upload_text(dp, get_text):
    session = await (dp.bot['rSession']).get_session()

    spare_pass = False
    await asyncio.sleep(0.5)

    try:
        response = await session.post("http://pastie.org/pastes/create",
                                      data={"language": "plaintext", "content": get_text})

        get_link = response.url
        if "create" in str(get_link):
            spare_pass = True
    except:
        spare_pass = True

    if spare_pass:
        response = await session.post("https://www.friendpaste.com",
                                      json={"language": "text", "title": "", "snippet": get_text})

        get_link = json.loads((await response.read()).decode())['url']

    return get_link


# Проверка на перенесение БД из старого бота, в нового или указание токена нового бота
async def check_bot_data():
    get_login = get_settingsx()['misc_bot']
    get_bot = await bot.get_me()

    if get_login not in [get_bot.username, "None"]:
        get_positions = get_all_positionsx()

        for position in get_positions:
            update_positionx(position['position_id'], position_photo="")

    update_settingsx(misc_bot=get_bot.username)


# Получить информацию о позиции для админа
def get_position_of_day():
    print('Получить информацию о случайной позиции для админа misc_functions.py 127')
    print(len(get_all_positionsx()))
    pos_id = random.choice(get_all_positionsidx())
    print(pos_id['position_id'])
    # pos_id=random.choice(get_all_positionsidx())
    get_items = get_itemsx(position_id=pos_id['position_id'])
    get_position = get_positionx(position_id=pos_id['position_id'])
    get_category = get_categoryx(category_id=get_position['category_id'])

    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if len(get_position['position_photo']) >= 5:
        photo_text = "<code>Присутствует ✅</code>"
        get_photo = get_position['position_photo']

    if get_position['position_description'] != "0":
        text_description = f"\n{get_position['position_description']}"

    get_message = f"<b>📁 Позиция: <code>{get_position['position_name']}</code></b>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                  f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
                  f"🗃 Категория: <code>{get_category['category_name']}</code>\n" \
                  f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
                  f"📦 Остаток: <code>{len(get_items)}шт</code>\n" \
                  f"📸 Изображение: {photo_text}\n" \
                  f"📜 Описание: {text_description}"

    return get_message, get_photo


# Получить информацию о позиции для админа
def get_artist_admin(artist_id):
    print('Получить информацию об артисте для админа misc_functions.py 127')
    #get_items = get_itemsx(position_id=position_id)
    get_artist = get_artistx(artist_id=artist_id)
    #get_category = get_categoryx(category_id=get_position['category_id'])

    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if len(get_artist['logo']) >= 5:
        photo_text = "<code>Присутствует ✅</code>"
        get_photo = get_artist['logo']

    if get_artist['description'] != "0":
        text_description = f"\n{get_artist['description']}"

    get_message = f"<b>📁 Артист : <code>{get_artist['name']}</code></b>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                  f"🏙 Город: <code>{get_artist['city']}</code>\n" \
                  f"📸 Изображение: {photo_text}\n" \
                  f"📜 Описание: {text_description}"

    return get_message, get_photo


# Получить информацию о позиции для админа
def get_position_admin(position_id):
    print('Получить информацию о позиции для админа misc_functions.py 127')
    get_items = get_itemsx(position_id=position_id)
    get_position = get_positionx(position_id=position_id)
    get_category = get_categoryx(category_id=get_position['category_id'])

    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if len(get_position['position_photo']) >= 5:
        photo_text = "<code>Присутствует ✅</code>"
        get_photo = get_position['position_photo']

    if get_position['position_description'] != "0":
        text_description = f"\n{get_position['position_description']}"

    get_message = f"<b>📁 Позиция: <code>{get_position['position_name']}</code></b>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                  f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
                  f"🗃 Категория: <code>{get_category['category_name']}</code>\n" \
                  f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
                  f"📦 Остаток: <code>{len(get_items)}шт</code>\n" \
                  f"📸 Изображение: {photo_text}\n" \
                  f"📜 Описание: {text_description}"

    return get_message, get_photo


def user_refill_my(user_id):
    return f"<b>Нажмите пожалуйста кнопку:</b>\n"

# Открытие своего профиля


def open_profile_my(user_id):
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)
    count_items = 0
    how_days = get_unix() - get_user['user_unix'] // 60 // 60 // 24

    if get_user['user_role'] == "ShopAdmin" or get_user['user_role'] == "Admin":
        free_delivery_point = get_user['free_delivery_point']
        delivery_rate = get_user['delivery_rate']
        selleradd = f"📄 Бесплатная доставка от: <code>{get_user['free_delivery_point']}</code>\n" \
                    f"📄 Ставка доставки: <code>{get_user['delivery_rate']}</code>"
    else: selleradd = ""

    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += int(items['purchase_count'])

    prmtxt = get_user['promocode'] if get_user['promocode'] else None
    get_settings = get_settingsx()
    profile_my = f"<b>👤 Ваш профиль:</b>\n" \
        f"➖➖➖➖➖➖➖➖➖➖\n" \
        f"🆔 ID: <code>{get_user['user_id']}</code>\n" \
        f"💰 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
        f"📄 Скидка(промокод): <code>{prmtxt}</code>\n" \
        f"🎁 Куплено товаров: <code>{count_items}шт</code>\n" \
        f"🕰 Регистрация: <code>{get_user['user_date'].split(' ')[0]} ({convert_day(how_days)})</code>\n" \
        f"🏙 Город: <code>{get_user['user_city']}</code>\n" \
        f"📄 Роль: <code>{get_user['user_role']}</code>\n" \
        + selleradd



    # if get_settings['type_trade'] != "digital":
    #  profile_my = f"{profile_my} 🏙 Город: <code>{get_user['user_city']}</code>"

    return profile_my

def open_partners_list2():
    get_partners = get_all_partnersx()

    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for partner in get_partners:
        buttons_to_add = append(types.InlineKeyboardButton(text=f"{partner['name']}", url=f"{partner['link']}"))
    keyboard.add(*buttons_to_add)

    return keyboard

#f"📡 Координаты: <code>{get_user['user_geocode']}</code>"


def calc_cart_summ(user_id):
    order = get_user_orderx(user_id=user_id)
    get_positions = []
    totalm = 0
    get_positions = get_cart_positionsx(order_id=order['order_id'])
    for position in get_positions:
        poscost = position['count'] * position['position_price']
        totalm += poscost
    return totalm

def calc_order_summ(order_id):
    #order = get_user_orderx(user_id=user_id)
    get_positions = []
    totalm = 0
    get_positions = get_cart_positionsx(order_id=order_id)
    for position in get_positions:
        poscost = position['count'] * position['position_price']
        totalm += poscost
    return totalm

# Открытие своей корзины
def open_cart_my(order_id):
    #orders = get_user_orderx(user_id=user_id)
    orderdata = []
    #заказ
    orderdata = get_orderxo(order_id=order_id)
    user_id = orderdata['user_id']
    get_user = get_userx(user_id=user_id)
    #получаем баланс пользователя
    ub = get_user['user_balance']
    #позиции заказа
    get_positions = []
    get_positions = get_cart_positionsx(order_id=order_id)

    this_items = []
    this_itemst = this_itemst2 = this_itemst3 = ''
    #delivery = 200
    totalm = 0
    print("|||")
    this_items.append(f"| Наименование | Цена | Количество | Стоимость |")

    for position in get_positions:
        poscost = position['count'] * position['position_price']
        totalm += poscost  # собираем стоимость корзины
        this_items.append(
            f"{position['position_name']} | {position['position_price']}₽ | {position['count']}шт. | {poscost}₽")

        this_itemst += f"{position['position_name']} | {position['position_price']}₽ | {position['count']}шт. | {poscost}₽ \n"

        print(f"{position['position_name']} | {position['position_price']}₽ | {position['count']}шт.| {poscost}₽")

    this_itemst3 += "Всего по всем позициям: " + str(totalm) + "\n"
    #this_itemst += this_itemst2
    #cart_sum = calc_cart_summ(user_id=touser_id)
    #cart_sum = calc_order_summ(order_id=order_id)
    get_payment = get_upaymentx(user_id=position['owner_uid'])
    if get_payment['way_freecredi']:
        freecredi_method = "Продавец поддерживает"
    else: freecredi_method = "Не поддерживается"
    dso = get_delivery_seller_options(order_id)['free_delivery_point']
    print(dso)
    #free_delivery_point = dso['free_delivery_point']
    #print(free_delivery_point)
    delivery_rate = get_delivery_seller_options(order_id)['delivery_rate']
    print(delivery_rate)
    #delivery = 200
    if totalm > dso:
        delivery = 0
    else: delivery = delivery_rate
    print("Доставка:" + str(delivery))
    #amount = cart_sum + delivery
    totalm2 = totalm + delivery

    if ub >= totalm2:
        this_itemst2 = "Заказ возможно оплатить с баланса целиком."
    elif ub < totalm2:
        torefill = totalm2 - get_user['user_balance']
        this_itemst2 = "Для оформления заказа потребуется пополнение в размере:" + \
            str(torefill) + "₽"

    this_address = get_user['user_address']
    if this_address is None:
        this_address = "Ваш адрес доставки не указан."
    # else: this_itemst += this_address

    this_phone = get_user['user_phone']
    if this_phone is None:
        this_phone = "Ваш контактный номер не указан."
    # else: this_itemst += this_phone

    return f"<b>👤 Ваша Корзина:</b>\n" \
           f"➖➖➖➖➖➖➖➖➖➖\n" \
           f"🆔 Корзина ID: <code>{orderdata['order_id']}</code>\n" \
           f"🆔 Статус: <code>{orderdata['order_state']}</code>\n" \
           f"🆔 Telegram ID: <code>{get_user['user_id']}</code>\n" \
           f"💳 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
           f"🗃 Всего товаров: <code>{totalm}</code>\n" \
           f"   <code>{this_itemst}</code>\n" \
           f"🏙 Итого корзина: <code>{totalm2}₽</code>\n" \
           f"🏙 Постоплата: <code>{freecredi_method}</code>\n" \
           f"🏙 Примечание: <code>{this_itemst2}</code>\n"
    # f"🆔 Telegram ID: <code>{get_user['user_id']}</code>\n" \
    # f"ID: {orderdata['order_id']} Статус корзины: <code>{orderdata['order_state']}</code>\n" \
    # f"🏙 Доставка: <code>{delivery}₽</code>\n" \

    # f"🕰 Адрес: <code>{this_address}</code>\n" \
    # f"📞 Телефон: <code>{this_phone}</code>\n" \


# f"📡 Координаты: <code>{get_user['user_geocode']}</code>\n" \

# Открытие профиля при поиске


def open_profile_search(user_id):
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)
    count_items = 0

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24

    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += items['purchase_count']

    return f"<b>👤 Профиль пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
           f"➖➖➖➖➖➖➖➖➖➖\n" \
           f"🆔 ID: <code>{get_user['user_id']}</code>\n" \
           f"👤 Логин: <b>@{get_user['user_login']}</b>\n" \
           f"👤 Роль: <b>{get_user['user_role']}</b>\n" \
           f"Ⓜ Имя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
           f"🕰 Регистрация: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
           f"💰 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
           f"💰 Всего пополнено: <code>{get_user['user_refill']}₽</code>\n" \
           f"🎁 Куплено товаров: <code>{count_items}шт</code>"


# Открытие профиля при поиске
def open_profile_search_req(user_id):
    get_requests = get_requestx(requester=user_id)
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)
    count_items = 0
    total_items = ''

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24

    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += items['purchase_count']

    if len(get_requests) >= 1:
        for items in get_requests:
            total_items += "|" + str(items['requesttxt'])

    return f"<b>👤 Запрос от пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
           f"➖➖➖➖➖➖➖➖➖➖\n" \
           f"Группа товаров: <b>{total_items}</b>\n" \
           f"  requestID: <code>{items['increment']}</code>\n" \
           f"🆔 userID: <code>{get_user['user_id']}</code>\n" \
           f"👤 Логин: <b>@{get_user['user_login']}</b>\n" \
           f"👤 Роль: <b>{get_user['user_role']}</b>\n" \
           f"Ⓜ Имя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
           f"🕰 Регистрация: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
           f"💰 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
           f"💰 Всего пополнено: <code>{get_user['user_refill']}₽</code>\n" \
           f"🎁 Куплено товаров: <code>{count_items}шт</code>"


# Статистика бота
def get_statisctics():
    show_profit_all, show_profit_day, show_profit_week = 0, 0, 0
    show_refill_all, show_refill_day, show_refill_week = 0, 0, 0
    show_money_users, show_buy_items, show_city_users = 0, 0, 0

    get_categories = get_all_categoriesx()
    get_positions = get_all_positionsx()
    get_purchases = get_all_purchasesx()
    get_refill = get_all_refillx()
    get_settings = get_settingsx()
    get_items = get_all_itemsx()
    get_users = get_all_usersx()
    get_all_users_by_cities = get_users_by_cities()
    print(get_all_users_by_cities)

    for purchase in get_purchases:
        show_profit_all += purchase['purchase_price']
        show_buy_items += purchase['purchase_count']
        if purchase['purchase_unix'] - get_settings['misc_profit_day'] >= 0:
            show_profit_day += purchase['purchase_price']
        if purchase['purchase_unix'] - get_settings['misc_profit_week'] >= 0:
            show_profit_week += purchase['purchase_price']

    for refill in get_refill:
        show_refill_all += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_day'] >= 0:
            show_refill_day += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_week'] >= 0:
            show_refill_week += refill['refill_amount']

    for user in get_users:
        show_money_users += user['user_balance']

    for city in get_all_users_by_cities:
        show_city_users += "| " + city['city'] + " : " + str(city['countu']) + " |"

    message = "<b>📊 Статистика бота</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Пользователи: 🔶</b>\n" \
              f"👤 Пользователей: <code>{len(get_users)}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Средства 🔶</b>\n" \
              f"💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n" \
              f"💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n" \
              f"💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n" \
              f"💳 Средств в системе: <code>{show_money_users}₽</code>\n" \
              f"💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n" \
              f"💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n" \
              f"💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Прочее 🔶</b>\n" \
              f"🎁 Товаров: <code>{len(get_items)}шт</code>\n" \
              f"📁 Позиций: <code>{len(get_positions)}шт</code>\n" \
              f"🗃 Категорий: <code>{len(get_categories)}шт</code>\n" \
              f"🎁 Продано товаров: <code>{show_buy_items}шт</code>\n"
              #f" Города: <code>{show_city_users}</code>\n"


    return message

# Открытие профиля при поиске
def open_profile_search_seller(user_id, price):
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)
    count_items = 0

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24

    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += items['purchase_count']


    return f"<b>👤 Профиль пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
           f"➖➖➖➖➖➖➖➖➖➖\n" \
           f"🆔 ID: <code>{get_user['user_id']}</code>\n" \
           f"👤 Логин: <b>@{get_user['user_login']}</b>\n" \
           f"Ⓜ Имя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
           f"🕰 Регистрация: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
           f"💰 Продано: <code>{price}₽</code>\n" \
           f"💰 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
           f"💰 Всего пополнено: <code>{get_user['user_refill']}₽</code>\n" \
           f"🎁 Куплено товаров: <code>{count_items}шт</code>"


# Открытие профиля при поиске
def open_profile_search_seller(user_id):
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)
    count_items = 0
    seller_items = ''
    totals = 0

    print(user_id)

    get_purchasessel = get_purchasesxx(user_id)
    print(get_purchasessel)

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24

    if len(get_purchasessel) >= 1:
        for items in get_purchasessel:
            name_item = items[1]
            count_items = items[2]
            name_price = items[3]
            seller_items += f"{name_item}  {count_items}шт. <code>{name_price}₽</code>\n"
            totals += items[3]


    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += items['purchase_count']


    return f"<b>👤 Профиль пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
           f"➖➖➖➖➖➖➖➖➖➖\n" \
           f"🆔 ID: <code>{get_user['user_id']}</code>\n" \
           f"👤 Логин: <b>@{get_user['user_login']}</b>\n" \
           f"Ⓜ Имя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
           f"🕰 Регистрация: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
           f"➖➖➖➖{seller_items}➖➖➖\n" \
           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
           f"Всего продано: <code>{totals}₽</code>\n" \
           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
           f"💰 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
           f"💰 Всего пополнено: <code>{get_user['user_refill']}₽</code>\n" \
           f"🎁 Куплено товаров: <code>{count_items}шт</code>"

# Статистика бота
def generate_dales_report():
    show_profit_all, show_profit_day, show_profit_week = 0, 0, 0
    show_refill_all, show_refill_day, show_refill_week = 0, 0, 0
    show_money_users, show_buy_items, show_money_users = 0, 0, 0

    get_categories = get_all_categoriesx()
    get_positions = get_all_positionsx()
    get_purchases = get_all_purchasesx()
    get_refill = get_all_refillx()
    get_settings = get_settingsx()
    get_items = get_all_itemsx()
    get_users = get_all_usersx()
    #get_users_by_cities = get_users_by_cities()

    for purchase in get_purchases:
        show_profit_all += purchase['purchase_price']
        show_buy_items += purchase['purchase_count']
        if purchase['purchase_unix'] - get_settings['misc_profit_day'] >= 0:
            show_profit_day += purchase['purchase_price']
        if purchase['purchase_unix'] - get_settings['misc_profit_week'] >= 0:
            show_profit_week += purchase['purchase_price']

    for refill in get_refill:
        show_refill_all += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_day'] >= 0:
            show_refill_day += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_week'] >= 0:
            show_refill_week += refill['refill_amount']

    for user in get_users:
        show_money_users += user['user_balance']

    message = "<b>📊 Статистика бота</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Пользователи: 🔶</b>\n" \
              f"👤 Пользователей: <code>{len(get_users)}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Средства 🔶</b>\n" \
              f"💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n" \
              f"💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n" \
              f"💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n" \
              f"💳 Средств в системе: <code>{show_money_users}₽</code>\n" \
              f"💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n" \
              f"💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n" \
              f"💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Прочее 🔶</b>\n" \
              f"🎁 Товаров: <code>{len(get_items)}шт</code>\n" \
              f"📁 Позиций: <code>{len(get_positions)}шт</code>\n" \
              f"🗃 Категорий: <code>{len(get_categories)}шт</code>\n" \
              f"🎁 Продано товаров: <code>{show_buy_items}шт</code>\n" \
              f" Города: <code>{show_city_users}</code>\n"

    return message



# Статистика бота
def get_statisctics():
    show_profit_all, show_profit_day, show_profit_week = 0, 0, 0
    show_refill_all, show_refill_day, show_refill_week = 0, 0, 0
    show_money_users, show_buy_items, show_money_users, show_city_users = 0, 0, 0, 0

    get_categories = get_all_categoriesx()
    get_positions = get_all_positionsx()
    get_purchases = get_all_purchasesx()
    get_refill = get_all_refillx()
    get_settings = get_settingsx()
    get_items = get_all_itemsx()
    get_users = get_all_usersx()
    get_all_users_by_cities = get_users_by_cities()

    for purchase in get_purchases:
        show_profit_all += purchase['purchase_price']
        show_buy_items += purchase['purchase_count']
        if purchase['purchase_unix'] - get_settings['misc_profit_day'] >= 0:
            show_profit_day += purchase['purchase_price']
        if purchase['purchase_unix'] - get_settings['misc_profit_week'] >= 0:
            show_profit_week += purchase['purchase_price']

    for refill in get_refill:
        show_refill_all += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_day'] >= 0:
            show_refill_day += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_week'] >= 0:
            show_refill_week += refill['refill_amount']

    for user in get_users:
        show_money_users += user['user_balance']

    show_city_users = ""

    for city in get_all_users_by_cities:
        show_city_users += "| " + city['user_city'] + ":" + str(city['countu']) + " |"

    message = "<b>📊 Статистика бота</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Пользователи: 🔶</b>\n" \
              f"👤 Пользователей: <code>{len(get_users)}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Средства 🔶</b>\n" \
              f"💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n" \
              f"💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n" \
              f"💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n" \
              f"💳 Средств в системе: <code>{show_money_users}₽</code>\n" \
              f"💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n" \
              f"💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n" \
              f"💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Прочее 🔶</b>\n" \
              f"🎁 Товаров: <code>{len(get_items)}шт</code>\n" \
              f"📁 Позиций: <code>{len(get_positions)}шт</code>\n" \
              f"🗃 Категорий: <code>{len(get_categories)}шт</code>\n" \
              f"🎁 Продано товаров: <code>{show_buy_items}шт</code>\n" \
              f" <b>Количество пользователей по городам:</b> \n" \
              f" {show_city_users} \n"


    return message

# Автобэкапы БД для админов
async def autobackup_admin():
    for admin in get_admins():
        with open(PATH_DATABASE, "rb") as document:
            try:
                await bot.send_document(admin,
                                        document,
                                        caption=f"<b>📦 AUTOBACKUP</b>\n"
                                                f"🕰 <code>{get_date()}</code>")
            except:
                pass

# Статистика бота
def generate_sales_report():
    show_profit_all, show_profit_day, show_profit_week = 0, 0, 0
    show_refill_all, show_refill_day, show_refill_week = 0, 0, 0
    show_money_users, show_money_sellers, show_buy_items = 0, 0, 0


    get_categories = get_all_categoriesx()
    get_positions = get_all_positionsx()
    get_purchases = get_all_purchasesx()
    #get_purchasesbysellers = get_purchasesbysellers()
    get_refill = get_all_refillx()
    get_settings = get_settingsx()
    get_items = get_all_itemsx()
    get_users = get_all_usersx()
    top_sellers = []
    top_sellersp = []
    #keyboard = InlineKeyboardMarkup()

    for purchase in get_purchases:
        show_profit_all += purchase['purchase_price']
        show_buy_items += purchase['purchase_count']
        if purchase['purchase_unix'] - get_settings['misc_profit_day'] >= 0:
            show_profit_day += purchase['purchase_price']
        if purchase['purchase_unix'] - get_settings['misc_profit_week'] >= 0:
            show_profit_week += purchase['purchase_price']

    for refill in get_refill:
        show_refill_all += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_day'] >= 0:
            show_refill_day += refill['refill_amount']
        if refill['refill_unix'] - get_settings['misc_profit_week'] >= 0:
            show_refill_week += refill['refill_amount']

    for user in get_users:
        print(user)
        if user['user_role'] == "ShopAdmin":
            show_money_sellers += user['user_balance']
        elif user['user_role'] is None:
            show_money_users += user['user_balance']
        if user['user_role'] == "ShopAdmin" and user['user_balance'] >= 0:
            top_sellers += user['user_name'] + str(user['user_balance']) + "\n"
            
    #for seller in get_purchasesbysellers:
    #    top_sellersp += user['user_login'] + str(user['price']) + "\n"

        #keyboard.add(ikb(
        #        f"{user['user_login']} | {user['user_balance']}₽", # | {len(get_items)} шт",
        #        callback_data=f"open_profile_search({user['increment']})"))

    #for position in get_positions[(remover): len(get_positions)]:
            #print(f'position {position}')
            #get_items = get_itemsx(position_id=position[1])


    message = "<b>📊 Отчет о продажах</b>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Пользователи: 🔶</b>\n" \
              f"👤 Пользователей: <code>{len(get_users)}</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Средства 🔶</b>\n" \
              f"💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n" \
              f"💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n" \
              f"💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n" \
              f"💳 Средств на балансах пользователей: <code>{show_money_users}₽</code>\n" \
              f"💳 Средств на балансах продавцов: <code>{show_money_sellers}₽</code>\n" \
              f"💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n" \
              f"💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n" \
              f"💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n" \
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
              f"<b>🔶 Прочее 🔶</b>\n" \
              f"🎁 Товаров: <code>{len(get_items)}шт</code>\n" \
              f"📁 Позиций: <code>{len(get_positions)}шт</code>\n" \
              f"🗃 Категорий: <code>{len(get_categories)}шт</code>\n" \
              f"🎁 Продано товаров: <code>{show_buy_items}шт</code>\n"

    return message

# Получить информацию о магазине для админа
def get_shop_admin(shop_id):
    print('Получить информацию о позиции для админа misc_functions.py 127')
    #get_items = get_itemsx(position_id=position_id)
    get_shop = get_shopx(shop_id=shop_id)
    #get_category = get_categoryx(category_id=get_position['category_id'])
    #link = get_start_link(str(f"deep_link&shop_id&{shop_id}"), encode=True)

    print(get_shop)

    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if get_shop['logo'] != None:
        photo_text = "<code>Присутствует ✅</code>"
        get_photo = get_shop['logo']

    if get_shop['address'] != "0":
            text_description = f"\n{get_shop['address']}"
    if get_shop['phone'] != "0":
        text_description = f"\n{get_shop['phone']}"
    if get_shop['description'] != "0":
        text_description = f"\n{get_shop['description']}"

    get_message = f"<b>📁 Магазин: <code>{get_shop['name']}</code></b>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                  f"🏙 Город: <code>{get_shop['city']}</code>\n" \
                  f"📸 Изображение: {photo_text}\n" \
                  f"📸 Адрес: {get_shop['address']}\n" \
                  f"📸 Телефон: {get_shop['phone']}\n" \
                  f"📜 Описание: {text_description}"

    return get_message, get_photo

#f"🏷 Ссылка: <code>{link}</code>\n" \
#f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \