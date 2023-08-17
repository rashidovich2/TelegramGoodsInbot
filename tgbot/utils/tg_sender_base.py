import asyncio
from telethon import TelegramClient, events
from telethon.extensions import html
from telethon import functions, types
from telethon.errors import UserBannedInChannelError, ChannelPrivateError, ChatWriteForbiddenError, SlowModeWaitError, UsernameInvalidError, ChatGuestSendForbiddenError
from aiogram.utils.markdown import hlink
import os, sys
from sys import stdout
from os import path
import datetime
import time
import aiosqlite
import sqlite3
import urllib.request
import json
#from tgbot.services.api_sqlite import *
#from tgbot.utils.misc_functions import get_position_admin

print("RUN SENDER*->")

api_id = 22110947
api_hash = '4c1dbb99b7785215a23c6a049b6633a5'
#client = TelegramClient('Forwarder', api_id, api_hash)
print("2")
#client.start()

# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())

# Получение позиции
def get_new_positionx():
    print('Получение позиции api_sqlite.py 318')
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position WHERE state='Approved'" #increment>740
        #sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql).fetchall()

# Изменение позиции
def update_positionx(position_id, **kwargs):
    print('Изменение позиции api_sqlite.py 306')
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_position SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(position_id)
        con.execute(f"{sql}WHERE position_id = ?", parameters)
        con.commit()



async def download_image(url, file_path):
    print("3")
    f = urllib.request.urlretrieve(url, file_path)
    print(f)


async def callback_pr(current, total):
    print('Uploaded', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))


async def send_message(success_chats, client, chat_id, message_type="photo", message_text=None, caption=None, image_url=None, file_path=None):
    try:
        #while True:
        # Check for GeneratorExit and exit the coroutine if raised
        if asyncio.current_task().cancelled():
            return
        # Your other code here
        print(client)
        if message_type == 'photo':
            if image_url:
                file_path = '/var/local/bot3101fc/images/photo.png'
                await download_image(image_url, file_path)
                print("4")
                print(image_url, file_path)
                #await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr)
                try:
                    #client.parse_mode = "HTML"
                    #caption = client.parse(caption)
                    caption = caption.replace("<b>", "*bold \*").replace("</b>", "*")
                    img = await client.upload_file(file_path, progress_callback=callback_pr)
                    await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr) #, parse_mode='HTML'
                    '''await client(
                        functions.messages.SendMediaRequest(
                            peer=chat_id,
                            media=types.InputMediaUploadedPhoto(img),
                            message=caption,
                        )
                    )'''
                except UserBannedInChannelError:
                    print("Приехали 5.")
                    print("5")
                    return

            elif file_path:
                try:
                    client.parse_mode = "HTML"
                    await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr)
                    await asyncio.sleep(60)

                except UserBannedInChannelError:
                    print(f"Аккаунт забанен в этом чате:{chat_id}.")
                    del success_chats[chat_id]
                    await asyncio.sleep(30)
                    pass

                except ChannelPrivateError:
                    print(f"Чат оказался приватным: {chat_id}.")
                    del success_chats[chat_id]
                    await asyncio.sleep(30)
                    pass

                except ChatWriteForbiddenError:
                    print(f"Аккаунту запретили писать в этот чат: {chat_id}.")
                    del success_chats[chat_id]
                    await asyncio.sleep(30)
                    pass

                except ChatGuestSendForbiddenError:
                    print(f"Необхдоимо вступить в группу: {chat_id}.")
                    del success_chats[chat_id]
                    await asyncio.sleep(30)
                    pass

                except SlowModeWaitError as e:
                    print(f"В чате медленный режим для аккаунта, пауза на {e.seconds}: {chat_id}.")
                    pass

            else:
                await client.send_file(chat_id, '/var/local/bot3101fc/images/photo.png', caption=caption)
                print("4-2")

        elif message_type == 'text':
            await client.send_message(chat_id, message_text)
        else:
            print('Invalid message type')

    except GeneratorExit:
        # Clean up resources or perform finalization tasks
        pass

async def tg_send_message(client, message_type="photo", message_text=None, caption=None, image_url=None): #, caption=None, image_url=None

    #caption = sys.argv[1]
    #image_url = sys.argv[2]
    #await print("2")
    await client.start()

    if not await client.is_user_authorized():
        print('Telegram client failed to start.')
        return


    chat_list1 = ['goodnewsrussia1',
                 'TG_PR',
                 'GruppaZS',
                 'wildberries_chatwb',
                 'market_place_rf',
                 'go_marketplace',
                 'tentinder',
                 'certificat_centr',
                 'poiskinvest',
                 'packingBOX_Ff',
                 'photoshooting595',
                 'otcAsd',
                 'wildberries_chat_help',
                 'rabota_biznes_freelance',
                 'textiles2022',
                 'WB_infoChat',
                 'it_chat7/3195',
                 'google_fb_chat',
                 'fb_google_chat',
                 'avito_no_ban',
                 'zashivayus',
                 'textiles2022',
                 'duaoptom',
                 'sertficat_chat',
                 'packingBOX_Ff',
                 'newbusinesscommunity',
                 'Techno_printt',
                 'wb_ozon_fotos',
                 'mpgroup_wildberries',
                 'rieltor_top',
                 'pro_sewubusiness',
                 'PenzaBaraholka',
                 'scladchina_mphelp']  # replace [...] with the list of chat IDs or usernames

    success_chats = {}
    chat_list = ['depress',
                 'investing4all',
                 'startupchat',
                 'ru_f1',
                 'pppixel_chat',
                 'tashkentchatroom',
                 'telha',
                 'znakomstva_rus',
                 'lepreco',
                 'NeLiOne',
                 'tranies',
                 'chatnight',
                 'Gaysiti',
                 'lovesup',
                 'andromedica',
                 'sosedka_tg',
                 'mi_mino',
                 'VideoChat1',
                 'paradisechat',
                 'poshlyekhabarovsk',
                 'bropickup',
                 'dating74',
                 'cfriends',
                 'gchate',
                 'razv',
                 'Znacomstva',
                 'professionallogisticgroup',
                 'orendating',
                 'mysql_ru',
                 'ponyorm',
                 'clickhouse_ru',
                 'sqlcom',
                 'tarantoolru',
                 'bigdata_en',
                 'neuroworkshop',
                 'mailrucontests',
                 'pythontelegrambotgroup',
                 'habrachat',
                 'violachat',
                 'leprachat',
                 'ropogXA',
                 'habragram',
                 'tavernofoverwatch',
                 'apple_lepra',
                 'krjok',
                 'abody',
                 'chatshiz',
                 'tmmarketing',
                 'myusadba',
                 'casinoch',
                 'vdohnovenyevokrug',
                 'kzn_ch',
                 'themamaideti',
                 'mos_cosmetics',
                 'tatarstan_chat',
                 'RestoRadio',
                 'ritualMSK',
                 'TGweapon',
                 'rucrash',
                 'blackpiratexx',
                 'darkcompany',
                 'helpmePR',
                 'crypto_guide',
                 'happyandfree',
                 'tattoo_anomalia',
                 'auction38',
                 'kommersantsouth',
                 'BestTatts',
                 'nya_vintage',
                 'byvilain',
                 'drive_club',
                 'this_is_interesting',
                 'Burenie_RF',
                 'mbcrussia',
                 'procrastinatorfm',
                 'putin_in_focus',
                 'minmaksgrupsuper777',
                 'kvadratour_hot',
                 'nezanesli',
                 'Safeweb',
                 'Myusli_4e',
                 'crimea_nice',
                 'prtalk',
                 'belarus_bikers',
                 'GunFreak',
                 'ruzh_ps4',
                 'TGRare_chat',
                 'autoekb',
                 'helpauto',
                 'spamimvse',
                 'MobiDevices',
                 'cryptoreports',
                 'driveracmsk',
                 'mkflourish',
                 'geraclea',
                 'hvostovil',
                 'vsamoletecom',
                 'alltarget',
                 'karapuziki']

    perm_list = ['test_rabota_permi_101', 'goodnewsrussia1']

    for chat in perm_list:
        print(f"Чат:{chat}|||||||||||||||||||||||||||||||||")
        if isinstance(chat, str):  # check if the item in the list is a username
            try:
                response = await client.get_entity(chat)  # get the entity (user or chat) from the username
                chat_id = response.id  # get the chat_id from the entity
                success_chats = {chat_id:chat}
                success_chats_json = json.dumps(success_chats)
                print(success_chats_json)

            except ValueError as e:
                print (f'Value Error{e}')
                print(success_chats)
                continue

            except UsernameInvalidError as e:
                print (f'Value Error{e}')
                print(success_chats)
                continue


        else:
            chat_id = chat  # if it's already a chat_id, use it directly

        #читаем файл позиций
        filename = '/var/local/bot3101fc/positions.json'
        if path.isfile('/var/local/bot3101fc/positions.json') is False:
            raise Exception("File not found")

        with open(filename) as f:
            exist_positions = json.load(f)

        positions = get_new_positionx()
        for position in positions:
            position_description = position['position_description']
            file_path = f"/var/local/bot3101fc/tgbot/images/position{position['position_id']}.png"
            print(position['position_id'])
            found_values = []
            for row in exist_positions:
                if 'position_id' in row and row['position_id'] == position['position_id']:
                    article_url = row['article_url']
                    found_values.append(row['article_url'])
            print(found_values)

            if position_description:
                shortml = 200
                descritionlen = len(position_description)
                if descritionlen >= shortml:
                    shortmestext = f"{position_description[0:shortml]}\n\n"
                elif descritionlen < shortml:
                    shortmestext = position_description

                #shortmestext = md(shortmestext)
                #добавляем ссылку на полную версию
                hlinktext = hlink('читать далее..', article_url)
                htlinktext = f"<a href={article_url}>читать далее...</a>"
                alinktext = f"[читать далее...]({article_url})"
                shortmestext += htlinktext

            else: shortmestext = "Текст отсутствует"

            message_type = 'photo'  # replace with your type variable  file='file_id'
            #message_text = 'Рекламное сообщение'  # replace with your message text
            #caption = 'Рекламное сообщение'  # replace with your photo caption
            #image_url = 'https://example.com/image.jpg'
            #with open('data.json', 'w', encoding='utf-8') as f:
            #    json.dump(success_chats, f, ensure_ascii=False, indent=4)

            await send_message(success_chats, client, chat_id, message_type="photo", message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path)
            #await update_positionx(position['position_id'], state="Posted")
            await asyncio.sleep(30)

    print('Успешно продублировано в канал.')
    print(success_chats)

    await client.disconnect()

    '''task = asyncio.current_task()
    if task is not None:
        task.cancel()'''


print(sys.argv)

print("1")
api_id = 28712772
api_hash = '2e3785d00832ceee5cb453d7138b99ea'
#image = "https://www.donzella.ru/images/thumbs/000/0007490_erstnoj-kostm-ermenegildo-zegna_1002.jpeg"
#asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None, caption="ADV MESSAGE TEST", image_url=image))
async def send_telegram_message(message_type="photo", message_text=None, caption=None, image_url=None):
#async def send_telegram_message(client=TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None, caption=None, image_url=None):
    #asyncio.get_event_loop().run_until_complete(await tg_send_message(message_type="photo", message_text=message_text, caption=caption, image_url=image_url))
    #asyncio.run(await tg_send_message(message_type="photo", message_text=message_text, caption=caption, image_url=image_url))
    print("1")
    api_id = 28712772
    api_hash = '2e3785d00832ceee5cb453d7138b99ea'
    await tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type=message_type, message_text=message_text, caption=caption, image_url=image_url)


#await tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type=message_type, message_text=message_text, caption=caption, image_url=image_url)
#asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None)) #, caption=caption, image_url=image_url
x = 0
try:
    while True:
        asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash), message_type="photo", message_text=None, caption=None, image_url=None)) #, caption=caption, image_url=image_url
        x+=1
        print(f"Итерация:{x}")

        time.sleep(30)

except GeneratorExit:
    # Clean up resources or perform finalization tasks
    pass