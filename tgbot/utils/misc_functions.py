# - *- coding: utf- 8 - *-
import asyncio
import aiohttp
import json
import os, random
import subprocess
from datetime import datetime, timedelta
import time

import sys
import hashlib
import base58

import urllib.request
import requests
import subprocess


import aiogram
from aiogram import Dispatcher
from aiogram import executor, exceptions
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.types import Message
#from aiogram.utils import exceptions, executor
#from aiogram.methods import SendMessage, SendPhoto, SendVideo, SendAnimation
import tronpy
from aiogram.utils.deep_linking import get_start_link, decode_payload
from bs4 import BeautifulSoup
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
from tgbot.middlewares.i18n import I18nMiddleware
#from tgbot.data.config import get_admins, BOT_VERSION, BOT_DESCRIPTION
from tgbot.keyboards.reply_z_all import menu_frep
from tgbot.services.api_session import AsyncSession
from tgbot.loader import bot
from tgbot.keyboards.inline_user import products_open_finl
from tgbot.services.api_sqlite import get_settingsx, update_settingsx, get_userx, get_all_positionsx, \
    update_positionx, get_all_categoriesx, get_all_purchasesx, get_all_refillx, get_all_usersx, get_all_itemsx, \
    get_itemsx, get_positionx, get_categoryx, get_all_positionsidx, get_requestx, get_user_orderx, get_cart_positionsx, \
    get_orderx, get_purchasesx, get_purchasesxx, get_shopx, get_artistx, get_planed_postx, get_planed_eventsx, get_tohour_postx,\
    update_tohour_postx, get_users_by_cities, get_users_by_citiesx, get_delivery_seller_options, get_params_orderx, get_orderxo, \
    get_userxxx, get_upaymentx, get_userxx, get_userxn, get_user_lang, add_refillx, get_refillx, get_refills_to_confirm

from tgbot.utils.const_functions import get_unix, convert_day, get_date, ded
#from tgbot.utils.tg_sender import *

from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.upload_images import upload_image

#bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext


async def fetch_token(user_login, password):
    async with aiohttp.ClientSession() as session:
        url = f"http://46.23.98.123:8081/login?login={user_login}&password={password}"

        async with session.get(url) as resp:
            token = await resp.text()

            #return token
    #await send_user(919148970, msg, markup="default")


# Уведомление и проверка обновления при запуске бота
async def on_startup_notify(dp: Dispatcher):
    if len(get_admins()) >= 1:
        await send_admins(f"<b>✅ Бот был успешно запущен</b>\n"
                          f"➖➖➖➖➖➖➖➖➖➖\n"
                          f"<code>❗ Данное сообщение видят только администраторы бота.</code>",
                          markup="default")
        await check_update()

#уведомление пользователю
async def user_notify(dp: Dispatcher, user_id, msg):
    print(f'Уведомление для пользователя!' + msg)
    await send_user(user_id, msg, markup="default")

# Рассылка сообщения пользователю
async def send_user(user_id, message, markup=None):
    try:
        await bot.send_message(user_id, message, reply_markup=markup, disable_web_page_preview=True)
    except Exception:
        pass


async def post_position_to_telegraph(position_id):
    get_message, get_photo = get_position_admin(position_id)
    t = TelegraphPoster(use_api=True)
    auth = t.create_api_token('TelegramGoodsinBot', 'RaClear', 'https://t.me/Goodsindemobot/') # second and third params are optional
    image = upload_image(get_photo)
    post = await t.post(title='TelegramGoodsinBot', author='RaClear', text=f'<img src={image}><blockquote>{get_message}</blockquote>')
    print(post['url'])
    return await post['url']


async def approve_new_product_notify(position_id, markup=None):
    print("::::LLLLLL::::::")
    inline_kb = InlineKeyboardMarkup()
    inline_btn1 = InlineKeyboardButton('Рассылка в боте: Да', callback_data=f'position_notify:{position_id}:yes')
    inline_btn2 = InlineKeyboardButton('Рассылка в боте: Нет', callback_data=f'position_notify:{position_id}:no')
    inline_btn3 = InlineKeyboardButton('Отправить сейчас', callback_data=f'position_planning:{position_id}:no')
    inline_btn4 = InlineKeyboardButton('Запланировать пост', callback_data=f'position_planning:{position_id}:yes')
    inline_btn5 = InlineKetboardButton('Вещание в PR чатах', callback_data=f'pr_broadcast:{position_id}:yes')
    inline_kb.insert(inline_btn1)
    inline_kb.insert(inline_btn2)
    inline_kb.insert(inline_btn3)
    inline_kb.insert(inline_btn4)
    inline_kb.insert(inline_btn5)
    print("::::LLLLLL::::::|||||")
    get_message, get_photo = get_position_admin(position_id)

    await bot.send_photo(chat_id=919148970,
                         photo=get_photo,
                         caption=get_message, reply_markup=inline_kb)


# Рассылка сообщения всем администраторам
async def send_admins(message, markup=None, not_me=0):
    for admin in get_admins():
        if markup == "default":
            lang=get_userx(user_id=admin)['user_lang']
            if lang is None:
                lang = "ru"
            print(lang)
            markup = menu_frep(admin, lang)

        try:
            if str(admin) != str(not_me):
                await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
        except Exception:
            pass

# Автоматическая очистка ежедневной статистики после 00:00
async def update_profit_day():
    await send_admins(get_statisctics())
    update_settingsx(misc_profit_day=get_unix())

# Автоматическая очистка еженедельной статистики в понедельник 00:01
async def update_profit_week():
    update_settingsx(misc_profit_week=get_unix())

async def check_refills_for_confirmation():
    print("Start Function")
    new_refills = get_refills_to_confirm()
    if len(new_refills) > 0:
        await send_admins(message="📢 Появилось пополнение картой, посмотрите пожалуйста в админке")

def catch_transactions(address):
    print("start to catch transactions")
    address = 'TQanL97TYygHiycDZ1up8XNqt1mHcGJ4Nv'
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=20)
    while datetime.now() < end_time:
        x=+1
        print("minutes in catching" + x)
        transactions = tron.get_account_transactions(address)
        confirmed_transactions = [tx for tx in transactions if tx.get('ret', [{}])[0].get('contractRet') == 'SUCCESS']
        # Your code here
        print(confirmed_transactions)
        asyncio.sleep(60)


async def catch_transactions20m(address_from, address_to):
    print("start to catch transactions")
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=20)
    print(start_time, end_time)
    st = get_unix()
    am = ""

    while True:
        await check_trx_now(address_from, st, address_to)
        await asyncio.sleep(60)

async def check_btc_now(address_from, st, address_to):
    print("BTC_NOW!!!")
    url = f'https://api.bscscan.com/api?module=account&action=tokentx&address={address_to}&page=1&offset=5&startblock=0&endblock=999999999&sort=asc&apikey=MRGP3KDXP7K9BP8Q4E3I2Y1FYVMAE961VV'
    response = requests.get(url) #, headers={"TRON-PRO-API-KEY": "5c4c149e-83d1-4926-8d73-78dac1ab2d38"})
    json_data = json.loads(response.text)
    try:
        txs = json_data['result']
        for transaction in txs:
            st = st
            bts = int(transaction['timeStamp'])
            dts = bts - st
            print(f"Transaction Hash: {transaction['blockHash']}")
            print(f"Transaction Value: {transaction['value']}")
            #amount = float(transaction['value'])*0.000000000000000001
            amount = float(transaction['value'])
            if transaction["from"] == address_from and transaction["to"] == address_to: # and dts < 0:
                #print(st, bts, dts)
                return float(amount), bts
            else:
                print(st, bts, dts, transaction['timeStamp'], transaction['value'])
                return float(amount), bts

    except json.JSONDecodeError:
        print("Empty response")


async def check_trx_address(address):
    print("CHECK_TRX_NOW!!!")
    url = f"https://api.trongrid.io/wallet/validateaddress"
    req = requests.get(url, headers={"TRON-PRO-API-KEY": "5c4c149e-83d1-4926-8d73-78dac1ab2d38"})
    result = json.loads(req.text)
    return result


async def validate_trx_address(address):
    response = requests.get(f'https://api.trongrid.io/v1/accounts/{address}')
    if response.status_code == 200:
        #print("1")
        result = json.loads(response.text)
        print(result)
        return result
    else:
        return False

async def validate_bsc_address(address):
    print(address)
    response = requests.get(f"https://api.bscscan.com/api?module=account&action=balance&address={address}&apikey=MRGP3KDXP7K9BP8Q4E3I2Y1FYVMAE961VV")
    if response.status_code == 200:
        result = json.loads(response.text)
        print(result)
        return result
    else:
        return False



async def check_trx_now(address_from, st, address_to):
    print("TRX_NOW!!!")
    url = f"https://api.trongrid.io/v1/accounts/{address_to}/transactions/trc20"
    transactions = requests.get(url, headers={"TRON-PRO-API-KEY": "5c4c149e-83d1-4926-8d73-78dac1ab2d38"})
    transactions2 = json.loads(transactions.text)
    amount = 0
    total = 0
    for transaction in transactions2['data']:
        #print(transaction)
        amount = transaction['value']
        #total += int(amount)
        st = st
        #bts = int(str(transaction['block_timestamp'])[:10])
        bts = int(transaction['block_timestamp']/1000)
        dts = bts - st
        if transaction["from"] == address_from and transaction["to"] == address_to: # and dts < 0:
            #print(st, bts, dts)
            return int(amount), bts
        else:
            print(st, bts, dts, transaction['transaction_id'], transaction['value']) #st, bts, dts,

    return 0, bts

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
    cities = get_users_by_cities()
    posttype = "photo"
    #get_users = get_userxx(user_city_id=34)
    #print(get_users)
    #posttype = "photo"
    #message = "(((999)))"
    test = "no"

    for city in cities:
        print(city)
        if city['user_city_id'] is None:
            #message = "Выберите пожалуйста Ваш город в боте."
            message = f"Выберите пожалуйста Ваш город в боте.\n" \
                      f"Мы сможем предложить Вам товары \n" \
                      f"от продавцов в Вашем городе."
            message = f"Мы добавили английски/русский языки, платежи в криптовалютах USDT, TRX и BTC.\n" \
                      f"Мы добавили интеграцию с CRM МойСКлад, товары в каталоге бота, заказы в МойСклад.\n" \
                      f"Магазины, Каталог, Афиша и Барахолка в Вашем городе!\n" \
                      f"Хорошего дня!."
            get_users = get_userxn()
            print(get_users)
            print(message)
        elif city['user_city_id'] != 0:
            message = str(city['user_city']) + ", привет. Я Telegram Goods In Bot из Telegram."
            #'Продавайте товары в своем городе или по всей России!'
            print(message)
            cityr = city['user_city_id']
            #get_users = get_all_usersx()
            #if cityr is not None:
            print(cityr)
            get_users = get_userxx(user_city_id=cityr)

        test = "no"
        #get_users = get_userxx(user_city_id=int(cityr))
        #get_users = get_all_usersxx()
        receive_users, block_users, how_users = 0, 0, 0
        for user in get_users:
            #print(user)
            if user['user_city_id'] is None: photo = "img/gbmes.png"
            else:
                photo = f"img/msg0007{user['user_city_id']}.png"
                print(photo)
            #photo = "img/msg34.png"
            #image = InputFile(f"img/msg{city['user_city_id']}.png")
            image = open(photo, 'rb')
            #message = str(user['user_city']) + ", продавцы товаров, добро пожаловать!"
            #elif user['user_city_id']:
            #    message = "Выберите пожалуйста свой город в профиле, наш бот Вам предложит товары в Вашем городе."
            try:
                if test == "yes": user['user_id'] = 919148970
                if posttype == "text":
                    await bot.send_message(user['user_id'], message, disable_web_page_preview=True)
                elif posttype == "photo":
                    await bot.send_photo(
                        chat_id=user['user_id'],
                        photo=image,
                        caption=message) #post[9] if post[9] else None)
                elif post[1] == "video":
                    await bot.send_video(
                        chat_id=user['user_id'],
                        video=post[5],
                        caption=post[9] or None,
                    )
                elif post[1] == "animation":
                    await bot.send_animation(
                        chat_id=user['user_id'],
                        animation=message,
                        caption=post[9] or None,
                    )

                receive_users += 1

            except Exception:
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

async def get_or_create_tron_account(wallet_user, wallet_net):
# Получение платежных реквизитов продавца
    tron_profile =  get_tron_profile(wallet_user, wallet_net)
    #print(get_tron_profile['tron_wallet'], get_tron_profile['private_key'], get_tron_profile['type_net'])
    if len(tron_profile['tron_wallet']) > 1:
        check = True
        return tron_profile, check
    else:
        check = False
        return tron_profile, check

#api_id = 28712772
#api_hash = '2e3785d00832ceee5cb453d7138b99ea'
#client = TelegramClient('Forwarder', api_id, api_hash)




async def functions_position_notify_bg(position_id, markup=None):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()
    test = "no"
    print(position_id)
    get_message, get_photo = get_position_admin(position_id)
    print(get_message, get_photo)
    #if get_message and get_photo:
    #t = TelegraphPoster(use_api=True)
    #auth = t.create_api_token('TelegramGoodsinBot', 'RaClear', 'https://t.me/Goodsindemobot/') # second and third params are optional
    #image = upload_image(get_photo)
    #print(image)
    image = "https://www.donzella.ru/images/thumbs/000/0007490_erstnoj-kostm-ermenegildo-zegna_1002.jpeg"

    #asyncio.get_event_loop().run_until_complete(await tg_send_message(message_type="photo", message_text=None, caption=get_message, image_url=image))
    #subprocess.run(["python3", "/var/local/bot3101fc/tgbot/utils/tg_sender.py", f"{get_message}", f"{image}"])

    #asyncio.create_task(await send_telegram_message(message_type="photo", message_text=None, caption=get_message, image_url=image))
    #await tg_send_message("photo", message_text=None, caption=get_message, image_url=image)

    get_position = get_positionx(position_id=position_id)
    position_type = get_position['position_type']
    if position_type == 1: cart = 1
    if position_type == 2: cart = 0
    if position_type != 3:
        position_category_id = get_position['category_id']
    else:
        position_category_id = 0
        cart = 0
    shop_id = 0

    if markup == "default":
        markup = menu_frep(admin)

    for user in get_users:
        try:
            if test == "yes": user['user_id'] = 919148970
            if get_message and get_photo:
                await bot.send_photo(
                    chat_id=user['user_id'],
                    photo=get_photo,
                    caption=get_message or None,
                    reply_markup=None, #products_open_finl(cart, position_id, 0, position_category_id, shop_id, "ru")
                )
            elif get_message == 0:
                await bot.send_message(user['user_id'], get_message, disable_web_page_preview=True)
            elif get_message == 3:
                await bot.send_video(
                    chat_id=user['user_id'],
                    video=get_photo,
                    caption=get_message or None,
                )
            elif get_message == 4:
                await bot.send_animation(
                    chat_id=user['user_id'],
                    animation=get_photo,
                    caption=get_message or None,
                )

            receive_users += 1
        except Exception:
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
                    photo=post[4],
                    caption=post[13] or None,
                )
            elif post[1] == "video":
                await bot.send_video(
                    chat_id=user['user_id'],
                    video=post[5],
                    caption=post[9] or None,
                )
            elif post[1] == "animation":
                #print("|_>>>>>")
                await bot.send_animation(
                    chat_id=user['user_id'],
                    animation=message,
                    caption=post[9] or None,
                )

            receive_users += 1
        except Exception:
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
            else:
                await bot.send_photo(
                    chat_id=user['user_id'],
                    photo=event[0],
                    caption=event[1])   #event[4] if event[4] else None) #.send_photo.file_id, if event[2] else None
            receive_users += 1
        except Exception:
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
    except Exception:
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

#Конвертация адреса из HEX в 58
def hex_to_address(hexaddr):
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(hexaddr)).digest()).digest()[0:4].hex()
    addrchecksum = hexaddr + checksum
    base58addr = base58.b58encode(bytes.fromhex(addrchecksum)).decode('utf-8')
    return base58addr

#Конвертация адреса из 58 в HEX
def address_to_hex(base58addr):
    addrchecksum = base58.b58decode(base58addr).hex()
    address = addrchecksum[0:42]
    checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(address)).digest()).digest()[0:4].hex()
    if checksum != addrchecksum[42:]:
        raise ValueError("Invalid checksum")
    return address



# Получить информацию о позиции для админа
def get_position_of_day():
    print('Получить информацию о случайной позиции для админа misc_functions.py 127')
    print(len(get_all_positionsx()))
    pos_id = random.choice(get_all_positionsidx())
    print(pos_id['position_id'])
    # pos_id=random.choice(get_all_positionsidx())
    get_items = get_itemsx(position_id=pos_id['position_id'])
    get_position = get_positionx(position_id=pos_id['position_id'])
    position_rest = get_position['position_rest']
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
                  f"📦 Остаток: <code>{position_rest}шт</code>\n" \
                  f"📸 Изображение: {photo_text}\n" \
                  f"📜 Описание: {text_description}"

    return get_message, get_photo


# Получить информацию о позиции для админа
def get_artist_admin(artist_id):
    print('Получить информацию об артисте для админа misc_functions.py 127')
    get_artist = get_artistx(artist_id=artist_id)

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
def get_position3_admin(position_id):
    print('Получить информацию о позиции для админа misc_functions.py 465')

    get_position = get_positionx(position_id=position_id)

    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if len(get_position['position_photo']) > 5:
        photo_text = "<code>Присутствует ✅</code>"
        get_photo = get_position['position_photo']

    if get_position['position_description'] != "0":
        text_description = f"\n{get_position['position_description']}"

    get_message = f"<b>📁 Позиция: <code>{get_position['position_id']}</code></b>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                  f"📜 Описание: {text_description}"

    return get_message, get_photo


# Получить информацию о позиции для админа
def get_position_admin(position_id):
    print('Получить информацию о позиции для админа misc_functions.py 465')
    #get_items = get_itemsx(position_id=position_id)
    get_position = get_positionx(position_id=position_id)
    #position_rest = get_position['position_rest']
    if get_position['position_type'] != 3:
        get_category = get_categoryx(category_id=get_position['category_id'])

    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if len(get_position['position_photo']) > 5:
        photo_text = "<code>Присутствует ✅</code>"
        #if get_position['position_type'] != 3:
        get_photo = get_position['position_photo']
        print("LLL:0001")
        #elif get_position['position_type'] == 3:
        #    get_photo = f"/var/local/bot3101fc/tgbot/images/position{position_id}.jpg"

    if get_position['position_description'] != "0":
        text_description = f"\n{get_position['position_description']}"

    if get_position['position_type'] == 1:
        position_rest = get_position['position_rest']
    elif get_position['position_type'] == 2:
        position_rest = len(get_itemsx(position_id=position_id))
    elif get_position['position_type'] == 3:
        print("LLL:0002")
        get_message = f"<b>📁 Позиция: <code>{get_position['position_id']}</code></b>\n" \
                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                      f"📜 Описание: {text_description}"

    if get_position['position_type'] == 1:
        get_message = f"<b>📁 Позиция: <code>{get_position['position_name']}</code></b>\n" \
                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                      f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
                      f"🗃 Категория: <code>{get_category['category_name']}</code>\n" \
                      f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
                      f"📦 Остаток: <code>{position_rest}шт</code>\n" \
                      f"📸 Изображение: {photo_text}\n" \
                      f"📜 Описание: {text_description}"

    elif get_position['position_type'] == 2:
        get_message = f"<b>📁 Позиция: <code>{get_position['position_name']}</code></b>\n" \
                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                      f"🗃 Категория: <code>{get_category['category_name']}</code>\n" \
                      f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
                      f"📦 Остаток: <code>{position_rest}шт</code>\n" \
                      f"📸 Изображение: {photo_text}\n" \
                      f"📜 Описание: {text_description}"

    return get_message, get_photo

# Принятие чека для поиска
async def get_refill_admin(receipt):
    print(receipt)
    #print("OLOL")
    #get_refill = ""
    #get_message = ""
    #lang = get_userx(user_id=get_refill['user_id'])['user_lang']
    #print(lang)
    lang = "ru"
    #print(lang)
    get_refill = get_refillx(refill_receipt=receipt)
    print(get_refill)
    #get_purchase = get_purchasex(purchase_receipt=receipt)
    #print(get_purchase)

    if get_refill is not None:
        '''if get_refill['refill_way'] == "Form":
            way_input = _("🥝 Способ пополнения: <code>По форме</code>", locale=lang)
        elif get_refill['refill_way'] == "Nickname":
            way_input = _("🥝 Способ пополнения: <code>По никнейму</code>", locale=lang)
        elif get_refill['refill_way'] == "Number":
            way_input = _("🥝 Способ пополнения: <code>По номеру</code>", locale=lang)
        else:'''
        way_input = f"🥝 Способ пополнения: <code>{get_refill['refill_way']}</code>"

        if lang == "ru":
            get_message = ded(f"<b>🧾 Чек: <code>#{get_refill['refill_receipt']}</code></b>\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"👤 Пользователь: <a href='tg://user?id={get_refill['user_id']}'>{get_refill['user_name']}</a> <code>({get_refill['user_id']})</code>\n"
                f"💰 Сумма пополнения: <code>{get_refill['refill_amount']}₽</code>\n"
                f"{way_input}\n"
                f"🏷 Комментарий: <code>{get_refill['refill_comment']}</code>\n"
                f"🕰 Дата пополнения: <code>{get_refill['refill_date']}</code>")

        if lang == "en":
            get_message = ded(f"<b>🧾 Receipt: <code>#{get_refill['refill_receipt']}</code></b>\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"👤 User: <a href='tg://user?id={get_refill['user_id']}'>{get_refill['user_name']}</a> <code>({get_refill['user_id']})</code>\n"
                f"💰 Charge Amount: <code>{get_refill['refill_amount']}₽</code>\n"
                f"{way_input}\n"
                f"🏷 Comment: <code>{get_refill['refill_comment']}</code>\n"
                f"🕰 Date of charge: <code>{get_refill['refill_date']}</code>")

    '''elif get_purchase is not None:
        link_items = await upload_text(message, get_purchase['purchase_item'])
        if lang == "ru":
            get_message += ded(
                f"<b>🧾 Чек: <code>#{get_purchase['purchase_receipt']}</code></b>\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"👤 Пользователь: <a href='tg://user?id={get_purchase['user_id']}'>{get_purchase['user_name']}</a> <code>({get_purchase['user_id']})</code>\n"
                f"🏷 Название товара: <code>{get_purchase['purchase_position_name']}</code>\n"
                f"📦 Куплено товаров: <code>{get_purchase['purchase_count']}шт</code>\n"
                f"💰 Цена 1-го товара: <code>{get_purchase['purchase_price_one']}₽</code>\n"
                f"💸 Сумма покупки: <code>{get_purchase['purchase_price']}₽</code>\n"
                f"🔗 Товары: <a href='{link_items}'>кликабельно</a>\n"
                f"🔻 Баланс до покупки: <code>{get_purchase['balance_before']}₽</code>\n"
                f"🔺 Баланс после покупки: <code>{get_purchase['balance_after']}₽</code>\n"
                f"🕰 Дата покупки: <code>{get_purchase['purchase_date']}</code>"
            )
        if lang == "en":
            get_message += ded(
                f"<b>🧾 Receipt: <code>#{get_purchase['purchase_receipt']}</code></b>\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"👤 User: <a href='tg://user?id={get_purchase['user_id']}'>{get_purchase['user_name']}</a> <code>({get_purchase['user_id']})</code>\n"
                f"🏷 Name of Product: <code>{get_purchase['purchase_position_name']}</code>\n"
                f"📦 Products Purchased: <code>{get_purchase['purchase_count']}pcs</code>\n"
                f"💰 Price for One Pieces: <code>{get_purchase['purchase_price_one']}R</code>\n"
                f"💸 Summ of Purchaces: <code>{get_purchase['purchase_price']}R</code>\n"
                f"🔗 Items: <a href='{link_items}'>кликабельно</a>\n"
                f"🔻 Balance Before Purchase: <code>{get_purchase['balance_before']}R</code>\n"
                f"🔺 Balance After Purchase: <code>{get_purchase['balance_after']}R</code>\n"
                f"🕰 Purchase Date: <code>{get_purchase['purchase_date']}</code>"
            )'''

    return get_message




def user_refill_my(user_id, lang):
    return _("<b>Нажмите пожалуйста кнопку:</b>", locale=lang)

def open_profile_my2(user_id):
    print("||||A+===")
    get_user = get_userx(user_id=user_id)
    #get_purchases = get_purchasesx(user_id=user_id)
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    #user_promocode = get_userx(user_id=user_id)['user_promocode'] or "None"
    #user_unix = get_user['user_unix'] // 60 // 60 // 24
    print(lang)
    count_items = 0
    #how_days = get_unix() - user_unix
    print("||||B+===")
    '''if get_user['user_role'] in ["ShopAdmin", "Admin"]:
        free_delivery_point = get_user['free_delivery_point']
        delivery_rate = get_user['delivery_rate']
        selleradd = _("📄 Бесплатная доставка от: ", locale=lang) + str(get_user['free_delivery_point']) + "\n"
        selleradd += _("📄 Ставка доставки: ", locale=lang) + str(get_user['delivery_rate'])
    else: selleradd = "None"
    print(selleradd)'''

    '''if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += int(items['purchase_count'])'''


    get_message = ded(f"""
                  <b>📁 Позиция: <code>{get_position['position_name']}</code></b>
                  ➖➖➖➖➖➖➖➖➖➖
                  🗃 Категория: <code>{get_category['category_name']}</code>
                  💰 Стоимость: <code>{get_position['position_price']}₽</code>
                  📦 Количество: <code>{len(get_items)}шт</code>
                  📸 Изображение: {photo_text}
                  📜 Описание: {text_description}

                  💸 Продаж за День: <code>{show_profit_count_day}шт</code> - <code>{show_profit_amount_day}₽</code>
                  💸 Продаж за Неделю: <code>{show_profit_count_week}шт</code> - <code>{show_profit_amount_week}₽</code>
                  💸 Продаж за Всё время: <code>{show_profit_count_all}шт</code> - <code>{show_profit_amount_all}₽</code>
                  """)

    #get_settings = get_settingsx()
    #profile_text = f"<b>👤 Ваш профиль:</b>"
    profile_text = _("<b>👤 Ваш профиль:</b>", locale=lang) + "\n"
    profile_text += "➖➖➖➖➖➖➖➖➖➖\n"
    profile_text += _("🆔 ID: <code>", locale=lang) + str(get_user['user_id']) + "</code>\n"
    profile_text += _("💰 Баланс: <code>", locale=lang) + str(get_user['user_balance']) + "₽</code>\n"
    profile_text += _("📄 Скидка(промокод): <code>", locale=lang) + prmtxt + "</code>\n"
    profile_text += _("🎁 Куплено товаров: <code>", locale=lang) + str(count_items) +"шт</code>\n"
    profile_text += _("🕰 Регистрация: <code>", locale=lang) + str(get_user['user_date'].split(' ')[0]) + " " + str(convert_day(how_days)) + "</code>\n"
    profile_text += _("🏙 Город: <code>", locale=lang) + get_user['user_city'] + "</code>\n"
    profile_text += _("📄 Роль: <code>", locale=lang) + user_role + "</code>\n"

    return profile_text


def open_profile_my(user_id):
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24
    count_items = sum([items['purchase_count'] for items in get_purchases])

    return ded(f"""
           <b>👤 Ваш профиль:</b>
           ➖➖➖➖➖➖➖➖➖➖
           🆔 ID: <code>{get_user['user_id']}</code>
              Роль: <code>{get_user['user_role']}</code>
           💰 Баланс: <code>{get_user['user_balance']}₽</code>
           🎁 Куплено товаров: <code>{count_items}шт</code>
           🕰 Регистрация: <code>{get_user['user_date'].split(' ')[0]} ({convert_day(how_days)})</code>
           """)

           #🎁 Куплено товаров: <code>{count_items}шт</code>
          # 🕰 Регистрация: <code>{get_user['user_date'].split(' ')[0]} ({convert_day(how_days)})</code>
# Открытие своего профиля
def open_profile_my2(user_id):
    #get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)

    #how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24
    #count_items = sum([items['purchase_count'] for items in get_purchases])
    profile_text = f"""<b>👤 Ваш профиль:</b>
           ➖➖➖➖➖➖➖➖➖➖
           🆔 ID: <code>{get_user['user_id']}</code>
           💰 Баланс: <code>{get_user['user_balance']}₽</code>
           """

    return profile_text

#🎁 Куплено товаров: <code>{count_items}шт</code>
#🕰 Регистрация: <code>{get_user['user_date'].split(' ')[0]} ({convert_day(how_days)})</code>

def open_partners_list2():
    get_partners = get_all_partnersx()

    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for partner in get_partners:
        buttons_to_add = append(types.InlineKeyboardButton(text=f"{partner['name']}", url=f"{partner['link']}"))
    keyboard.add(*buttons_to_add)

    return keyboard

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
    get_positions = []
    totalm = 0
    get_positions = get_cart_positionsx(order_id=order_id)
    for position in get_positions:
        poscost = position['count'] * position['position_price']
        totalm += poscost
    return totalm

# Открытие корзины
def open_cart_orders(order_id, lang):
    orderdata = []
    #данные заказа
    orderdata = get_orderxo(order_id=order_id)
    print(orderdata)
    #покупатель
    order_user_id = orderdata['user_id']
    #данные покупателя
    order_user = get_userx(user_id=order_user_id)
    #роль покупателя user_role
    if order_user['user_role'] != "None": user_role = order_user['user_role']
    else: user_role = "User"
    if order_user['user_balance'] != "None": ub = order_user['user_balance']
    else: ub = 0
    #юзер userid
    if order_user['user_login']: userid = f"Имя пользователя: <code>@{order_user['user_login']}</code>"
    else: userid = f"Телеграм ID: <code>{order_user['user_id']}</code>"

    #позиции заказа
    get_positions = []
    get_positions = get_cart_positionsx(order_id=order_id)
    this_itemst = this_itemst2 = this_itemst3 = ''
    totalm = 0

    this_items = ["| Наименование | Цена | Количество | Стоимость |"]
    for position in get_positions:
        poscost = position['count'] * position['position_price']
        totalm += poscost  # собираем стоимость корзины
        this_items.append(f"{position['position_name']} | {position['position_price']}₽ | {position['count']}шт. | {poscost}₽")
        this_itemst += f"{position['position_name']} | {position['position_price']}₽ | {position['count']}шт. | {poscost}₽ \n"
        print(f"{position['position_name']} | {position['position_price']}₽ | {position['count']}шт.| {poscost}₽")

    this_itemst3 += f"Всего по всем позициям: {str(totalm)}" + "\n"

    dso = get_delivery_seller_options(order_id)['free_delivery_point']
    #print(dso)

    delivery_rate = get_delivery_seller_options(order_id)['delivery_rate']
    #print(delivery_rate)
    delivery = 0 if totalm > dso else delivery_rate
    #print(f"Доставка:{str(delivery)}")
    totalm2 = totalm + delivery
    #print(totalm2)

    if ub >= totalm2: this_itemst2 = "Заказ возможно оплатить с баланса целиком."
    else:
        torefill = totalm2 - ub
        this_itemst2 = f"Для оформления заказа потребуется пополнение в размере:{str(torefill)}₽"
    #print(this_itemst2)
    print(lang)
    if lang == "ru":
        return f"<b>👤 Ваша Корзина:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖\n" \
               f"🆔 Корзина ID: <code>{orderdata['order_id']}</code>\n" \
               f"🆔 Статус: <code>{orderdata['order_state']}</code>\n" \
               f"💳 Баланс: <code>{ub}₽</code>\n" \
               f"🗃 Всего товаров: <code>{totalm}</code>\n" \
               f"   <code>{this_itemst}</code>\n" \
               f"🏙 Итого корзина: <code>{totalm2}₽</code>\n" \
               f"🏙 Примечание: <code>{this_itemst2}</code>"

    if lang == "en":
        return f"<b>👤 Your Cart:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖\n" \
               f"🆔 Cart ID: <code>{orderdata['order_id']}</code>\n" \
               f"🆔 State: <code>{orderdata['order_state']}</code>\n" \
               f"💳 Balance: <code>{ub}₽</code>\n" \
               f"🗃 Total Goods: <code>{totalm}</code>\n" \
               f"   <code>{this_itemst}</code>\n" \
               f"🏙 Total Cart: <code>{totalm2}₽</code>\n" \
               f"🏙 Aditional Text: <code>{this_itemst2}</code>"

def open_profile_search(user_id, lang):
    get_purchases = get_purchasesx(user_id=user_id)
    get_user = get_userx(user_id=user_id)
    count_items = 0

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24

    if len(get_purchases) >= 1:
        for items in get_purchases:
            count_items += items['purchase_count']

    if lang == "ru":
        message =  f"<b>👤 Профиль пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
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

    if lang == "en":
        message = f"<b>👤 User Profile: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖\n" \
                  f"🆔 userID: <code>{get_user['user_id']}</code>\n" \
                  f"👤 Login: <b>@{get_user['user_login']}</b>\n" \
                  f"👤 Role: <b>{get_user['user_role']}</b>\n" \
                  f"Ⓜ Name: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
                  f"🕰 Registration: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                  f"💰 Balance: <code>{get_user['user_balance']}₽</code>\n" \
                  f"💰 Total Charged: <code>{get_user['user_refill']}₽</code>\n" \
                  f"🎁 Products Purchased: <code>{count_items}шт</code>"

    return message

# Открытие профиля при поиске
def open_profile_search_req(user_id, lang):
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
            total_items += f"| {str(items['requesttxt'])} | \n"
            '''if items['state']:
                state = items['state']
            else:
                state = "None"'''


#            total_ids += " " + str(items['increment']) + " "

    if lang == "ru":
        message = f"<b>👤 Запрос от пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖\n" \
               f"Группа товаров: <b>{total_items}</b>\n" \
               f"🆔 Статус: <code>{items['state']}</code>\n" \
               f"🆔 userID: <code>{get_user['user_id']}</code>\n" \
               f"👤 Логин: <b>@{get_user['user_login']}</b>\n" \
               f"👤 Роль: <b>{get_user['user_role']}</b>\n" \
               f"Ⓜ Имя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
               f"🕰 Регистрация: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"💰 Баланс: <code>{get_user['user_balance']}₽</code>\n" \
               f"💰 Всего пополнено: <code>{get_user['user_refill']}₽</code>\n" \
               f"🎁 Куплено товаров: <code>{count_items}шт</code>"

    if lang == "en":
        message = f"<b>👤 Request from User: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖\n" \
               f"Product Group: <b>{total_items}</b>\n" \
               f"🆔 userID: <code>{get_user['user_id']}</code>\n" \
               f"👤 Login: <b>@{get_user['user_login']}</b>\n" \
               f"👤 Role: <b>{get_user['user_role']}</b>\n" \
               f"Ⓜ Name: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n" \
               f"🕰 Registration: <code>{get_user['user_date']} ({convert_day(how_days)})</code>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"💰 Balance: <code>{get_user['user_balance']}₽</code>\n" \
               f"💰 Total Charged: <code>{get_user['user_refill']}₽</code>\n" \
               f"🎁 Products Purchased: <code>{count_items}шт</code>"

    return message

#f"  requestID: <code>{items['increment']}</code>\n" \
    # Статистика бота
def get_statisctics(lang):
    show_profit_all, show_profit_day, show_profit_week = 0, 0, 0
    show_refill_all, show_refill_day, show_refill_week = 0, 0, 0
    show_money_users, show_money_sellers, show_buy_items, show_city_users, top_sellers = 0, 0, 0, "", 0
    show_users_all, show_users_day, show_users_week = 0, 0, 0

    get_categories = get_all_categoriesx()
    get_positions = get_all_positionsx()
    get_purchases = get_all_purchasesx()
    get_refill = get_all_refillx()
    get_settings = get_settingsx()
    get_items = get_all_itemsx()
    get_users = get_all_usersx()
    get_all_users_by_cities = get_users_by_cities()
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
        #print(user)
        show_users_all += 1
        if user['user_unix'] - get_settings['misc_profit_day'] >= 0:
            show_users_day += 1
        if user['user_unix'] - get_settings['misc_profit_week'] >= 0:
            show_users_week += 1
        if user['user_role'] == "ShopAdmin":
            show_money_sellers += user['user_balance']
        elif user['user_role'] is None:
            show_money_users += user['user_balance']
        #if user['user_role'] == "ShopAdmin" and user['user_balance'] >= 0:
        #    top_sellers += user['user_name'] + str(user['user_balance']) + "|"

    #cities = json.loads(get_all_users_by_cities)
    for city in get_all_users_by_cities:
        print(city)
        #show_city_users += city['user_city']
        #show_city_users += " ".join(city['user_city'])
        #print(students = json.load(f))
        #cityj = json.load(city)
        #show_city_users += city['user_city']
        #show_city_users += " | " + city['user_city'] + " : " + str(city['countu']) + " |"
        show_city_users += f" <b> {city['user_city']} </b>:  {str(city['countu'])} \n"
        #show_city_users .join(f"| {city['city']} : {str(city['countu'])} |")
        #show_city_users += "|" + city['user_city'] + "|"

    if lang == "ru":
        return f"<b>📊 Статистика бота</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>🔶 Пользователи: 🔶</b>\n" \
               f"┣ Юзеров за День: <code>{show_users_day}</code>\n" \
               f"┣ Юзеров за Неделю: <code>{show_users_week}</code>\n" \
               f"┗ Юзеров за Всё время: <code>{show_users_all}</code>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Средства 🔶</b>\n💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n💳 Средств на балансах пользователей: <code>{show_money_users}₽</code>\n💳 Средств на балансах продавцов: <code>{show_money_sellers}₽</code>\n💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Прочее 🔶</b>\n🎁 Товаров: <code>{len(get_items)}шт</code>\n📁 Позиций: <code>{len(get_positions)}шт</code>\n🗃 Категорий: <code>{len(get_categories)}шт</code>\nПродано товаров: <code>{show_buy_items}шт</code>\n🎁 По городам: <code>{show_city_users}</code>\n"
    if lang == "en":
        return f"<b>📊 Bot statistics</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>🔶 Users: 🔶</b>\n" \
               f"┣ Users for a Day: <code>{show_users_day}</code>\n" \
               f"┣ Users for a Week: <code>{show_users_week}</code>\n" \
               f"┗ Users in Total: <code>{show_users_all}</code>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>🔶 Finance 🔶</b>\n" \
               f"💸 Sales for 24 hours: <code>{show_profit_day}R</code>\n" \
               f"💸 Sales for a week: <code>{show_profit_week}R</code>\n" \
               f"💸 Sales for a time: <code>{show_profit_all}R</code>\n" \
               f"💳 Money in System: <code>{show_money_users}R</code>\n" \
               f"💰 Charged for a 24 hours: <code>{show_refill_day}R</code>\n" \
               f"💰 Charged for a week: <code>{show_refill_week}R</code>\n" \
               f"💰 Charged All: <code>{show_refill_all}R</code>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"<b>🔶 Other 🔶</b>\n" \
               f"🎁 Digital Items: <code>{len(get_items)}pcs</code>\n" \
               f"📁 Positions: <code>{len(get_positions)}pcs</code>\n" \
               f"🗃 Categories: <code>{len(get_categories)}pcs</code>\n" \
               f"🎁 Products Sold: <code>{show_buy_items}pcs</code>\n" \
               f" Users in Cities: {show_city_users}"


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

    return f"<b>📊 Статистика бота</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Пользователи: 🔶</b>\n👤 Пользователей: <code>{len(get_users)}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Средства 🔶</b>\n💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n💳 Средств в системе: <code>{show_money_users}₽</code>\n💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Прочее 🔶</b>\n🎁 Товаров: <code>{len(get_items)}шт</code>\n📁 Позиций: <code>{len(get_positions)}шт</code>\n🗃 Категорий: <code>{len(get_categories)}шт</code>\n🎁 Продано товаров: <code>{show_buy_items}шт</code>\n Города: <code>{show_city_users}</code>\n"



# Статистика бота
def get_statisctics2():
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

    show_city_users = "".join(
        "| " + city['user_city'] + ":" + str(city['countu']) + " |"
        for city in get_all_users_by_cities
    )
    return f"<b>📊 Статистика бота</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Пользователи: 🔶</b>\n👤 Пользователей: <code>{len(get_users)}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Средства 🔶</b>\n💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n💳 Средств в системе: <code>{show_money_users}₽</code>\n💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Прочее 🔶</b>\n🎁 Товаров: <code>{len(get_items)}шт</code>\n📁 Позиций: <code>{len(get_positions)}шт</code>\n🗃 Категорий: <code>{len(get_categories)}шт</code>\n🎁 Продано товаров: <code>{show_buy_items}шт</code>\n <b>Количество пользователей по городам:</b> \n {show_city_users} \n"

# Автобэкапы БД для админов
async def autobackup_admin():
    for admin in get_admins():
        with open(PATH_DATABASE, "rb") as document:
            try:
                await bot.send_document(admin,
                                        document,
                                        caption=f"<b>📦 AUTOBACKUP</b>\n"
                                                f"🕰 <code>{get_date()}</code>")
            except Exception:
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
        if user['user_role'] == "ShopAdmin":
            show_money_sellers += user['user_balance']
        elif user['user_role'] is None or user['user_role'] == "User":
            show_money_users += user['user_balance']
        #if user['user_role'] == "ShopAdmin" and user['user_balance'] >= 0:
        #    top_sellers += user['user_name'] + str(user['user_balance']) + "\n"

    return f"<b>📊 Отчет о продажах</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Пользователи: 🔶</b>\n👤 Пользователей: <code>{len(get_users)}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Средства 🔶</b>\n💸 Продаж за 24 часа: <code>{show_profit_day}₽</code>\n💸 Продаж за неделю: <code>{show_profit_week}₽</code>\n💸 Продаж за всё время: <code>{show_profit_all}₽</code>\n💳 Средств на балансах пользователей: <code>{show_money_users}₽</code>\n💳 Средств на балансах продавцов: <code>{show_money_sellers}₽</code>\n💰 Пополнений за 24 часа: <code>{show_refill_day}₽</code>\n💰 Пополнений за неделю: <code>{show_refill_week}₽</code>\n💰 Пополнений за всё время: <code>{show_refill_all}₽</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n<b>🔶 Прочее 🔶</b>\n🎁 Товаров: <code>{len(get_items)}шт</code>\n📁 Позиций: <code>{len(get_positions)}шт</code>\n🗃 Категорий: <code>{len(get_categories)}шт</code>\n🎁 Продано товаров: <code>{show_buy_items}шт</code>\n"

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

