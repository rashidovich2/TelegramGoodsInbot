import asyncio
#from telethon.sync import TelegramClient
from telethon import TelegramClient, events
from telethon.extensions import html
from telethon import functions, types
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.users import GetUsersRequest, GetFullUserRequest
from telethon.utils import get_input_peer, get_peer_id
from telethon.tl.types import User, Chat, Channel, InputPeerEmpty, InputPeerChannel, InputPeerUser, InputPeerChat, PeerChat, PeerChannel
from telethon.errors import UserBannedInChannelError, ChatInvalidError, ChannelInvalidError, ChannelPrivateError, ChatWriteForbiddenError, SlowModeWaitError, UsernameInvalidError, ChatGuestSendForbiddenError, ForbiddenError, ChatAdminRequiredError, PeerFloodError, UsernameNotOccupiedError, FloodWaitError, InviteRequestSentError
from aiogram.utils.markdown import hlink
import config
import os, sys
from sys import stdout
from os import path
import requests, socks
import regex
import random
from datetime import datetime
import time
import aiosqlite
import sqlite3
import urllib.request
import json
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

sys.path.append(parent)
from services.api_db_mysql import *
#from tgbot.services.api_sqlite import *
#from tgbot.utils.misc_functions import get_position_admin
#from tgbot.utils.const_functions import get_unix, get_date, clear_html

print("RUN SENDER*->")

#api_id = 22110947
#api_hash = '4c1dbb99b7785215a23c6a049b6633a5'
#client = TelegramClient('Forwarder', api_id, api_hash)

#PROXY
if config.PROXY_ENABLED:
    s = socks.socksocket()
    rnd_proxy = random.choice(config.PROXY_IPS).split(":")




#GailEstrada
#api_id = 16475416
#api_hash = '47a2ef523f116a0237605b4967d74539'
#client = TelegramClient('Forwarder4', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )


#api_id = 20974935
#api_hash = '9fbac23d7f44aa3cdb065237998a4b14'
#client = TelegramClient('Forwarder2', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )

#banned
#api_id = 27173025
#api_hash = 'aa7e0b3f2c3c579993372ce86e95e993'
#client = TelegramClient('Forwarder3', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
#cl_name = "Forwarder3"

#Olegr0978
api_id = 19431066
api_hash = '4dc8ab8e36f0133a5bc13ca67df7326f'
client = TelegramClient('Forwarder4', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )


user_id = 5952370072
#client = TelegramClient('Forwarder2', api_id, api_hash)
#client.start()

position_id = 0
message_text = ""
article_url = ""
multi_mode = 0
first = 0

#CHECK_CHAT_IN_DB
#GET_CHAT_ENTITY
#INVITE_ME_IN_CHAT
#SEND_FILE
#SAVE_RESULT

# Получение текущей даты
def get_date():
    this_date = datetime.now().replace(microsecond=0)
    this_date = this_date.strftime("%d.%m.%Y %H:%M:%S")

    return this_date

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

#Добавление отправки асихронное
async def add_chat_data(chat_id, chat_name, chat_state):
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        await con.execute("INSERT INTO chgrdb "
                          "(chat_id, chat_name, chat_type, chat_state) "
                          "VALUES (?, ?, ?, ?)",
                          [chat_id, chat_name, 'pr-chat', chat_state])
        await con.commit()



#Получение городов и url каналов
def get_chats():
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT chat_id, chat_name, chat_url FROM chgrdb WHERE chat_url is not Null and chat_type='pr-chat'"
        return con.execute(sql).fetchall()


async def get_chatsmy():
    chats = meta.tables['chgrb']
    where_clauses = [chats.c.chat_url.isnot(None), chats.c.chat_type == 'pr-chat']
    chats = await fetch_data(chats, where_clauses)
    return chats

#Получение городов и url каналов
def get_cities_places():
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT id as place_id, city as place_name, vacs_url FROM data_cities WHERE vacs_url is not Null"
        return con.execute(sql).fetchall()

#Добавление отправки асихронное
async def add_sending_positions(chat_id, position_id, position_description, resultx, datetime):
        await insert_position_sended(chat_id, position_id, position_description, resultx, datetime)


#Добавление отправки асихронное
async def add_sending_positions2(chat_id, position_id, position_description, resultx, datetime):
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        await con.execute("INSERT INTO storage_positions_sending "
                          "(chat_id, position_id, position_description, resultx, datetime) "
                          "VALUES (?, ?, ?, ?, ?)",
                          [chat_id, position_id, position_description, resultx, datetime])
        await con.commit()
        #return sending_id


SQL_TEMPLATE_CHAT_ID = "SELECT * FROM storage_chats WHERE chat_id=?"
SQL_TEMPLATE_CHAT_NAME = "SELECT * FROM storage_chats WHERE chat_name=?"

chat_list1 = ['goodnewsrussia1']

#Добавление отправки асихронное
async def get_chat_data(search_param):
    sql_query = ""

    if isinstance(search_param, int):
        sql_query = SQL_TEMPLATE_CHAT_ID
    elif isinstance(search_param, str):
        sql_query = SQL_TEMPLATE_CHAT_NAME
    else:
        raise Exception("Invalid parameter type. It should be either integer (for chat_id) or string (for chat_name).")
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        cursor = await con.execute(sql_query, (search_param,))
        records = await cursor.fetchall()
        return records

#Добавление отправки асихронное
async def get_all_chatsxs():
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        cursor = await con.execute("SELECT * FROM storage_chats")
        records = await cursor.fetchall()
        #await cursor.close()
        return records


#Добавление отправки асихронное
async def get_new_positionxs():
    async with aiosqlite.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = aiosqlite.Row
        cursor = await con.execute("SELECT * FROM storage_position WHERE position_state='Approved' OR position_state='Broadcast'")
        records = await cursor.fetchall()
        #await cursor.close()
        return records

# Получение позиции
def get_new_positionx():
    print('Получение позиции api_sqlite.py 318')
    with sqlite3.connect('/var/local/bot3101fc/tgbot/data/database.db') as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position WHERE position_state='Approved' OR position_state='Broadcast'"
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


def extract_hashtags(text):
    ht = ""
    pat = regex.compile(r'#\w*')
    hashtags = pat.findall(text)
    for ht in hashtags:
        print(ht)
    return ht

#text = '''
#In the summer, I love to travel to #beach destinations and relax under the #sun.
##VacationMode #SummerVibes
#'''

#print(hashtags)


async def download_image(url, file_path):
    print("3")
    f = urllib.request.urlretrieve(url, file_path)
    print(f)


async def callback_pr(current, total):
    print('Uploaded', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))


async def send_message(client, chat_id, position_id=None, message_type=None, message_text=None, caption=None, image_url=None, file_path=None, broadcast=0):
    try:
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
                try:
                    caption = caption.replace("<b>", "*bold \*").replace("</b>", "*")
                    img = await client.upload_file(file_path, progress_callback=callback_pr)
                    await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr) #, parse_mode='HTML'

                except UserBannedInChannelError:
                    print("Приехали 5.")
                    print("5")
                    return

            elif file_path:
                try:
                    client.parse_mode = "HTML"
                    if broadcast == 0:
                        update_positionx(position_id, position_state="Posted")
                    datetime = get_date()

                    mesfid = await client.send_file(chat_id, file_path, caption=caption, progress_callback=callback_pr)
                    print(mesfid)
                    await add_sending_positions(chat_id, position_id, "SENDING", "Posted", datetime)
                    await asyncio.sleep(10.5)

                except ChannelPrivateError:
                    print(f"CPE: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", f"ChannelPrivateError:{chat_id}", datetime)
                    await asyncio.sleep(5)

                except UserBannedInChannelError:
                    print(f"Аккаунт забанен в этом чате:{chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "User Banned", datetime)
                    await asyncio.sleep(30)

                except ChannelPrivateError:
                    print(f"Чат оказался приватным: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "Channel Private", datetime)
                    await asyncio.sleep(30)

                except ChatWriteForbiddenError:
                    print(f"Аккаунту запретили писать в этот чат: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "Chat Write Forbidden", datetime)
                    await asyncio.sleep(15)

                except ChatGuestSendForbiddenError:
                    print(f"Необхдоимо вступить в группу: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "Chat Guest Send Forbidden", datetime)
                    await asyncio.sleep(30)

                except SlowModeWaitError as e:
                    print(f"В чате медленный режим для аккаунта, пауза на {e.seconds}: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "Slow Mode Wait", datetime)

                except ForbiddenError as e:
                    print(f"В чат запрещено отправлять {e}: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "ForbiddenError", datetime)

                except ChatAdminRequiredError:
                    print(f"Необхдоимо вступить в группу: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", "Required Chat Admin", datetime)
                    await asyncio.sleep(30)

                except ValueError:
                    print(f"Отсутствует имя пользователя: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", f"ValueError:{chat_id}", datetime)
                    await asyncio.sleep(30)

                except UsernameInvalidError:
                    print(f"Отсутствует имя пользователя: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", f"UsernameInvalidError:{chat_id}", datetime)
                    await asyncio.sleep(30)

                except UsernameNotOccupiedError:
                    print(f"UsernameNotOccupiedError: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", f"UsernameNotOccupiedError:{chat_id}", datetime)
                    await asyncio.sleep(20)

                except PeerFloodError:
                    print(f"Слишком много запросов: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", f"To Many Requests:{chat_id}", datetime)
                    await asyncio.sleep(30)

                except FloodWaitError as e:
                    print(f"Надо подождать: {chat_id}.")
                    datetime = get_date()
                    await add_sending_positions(chat_id, position_id, "SENDING", f"FloodWaitError:{chat_id}:ждем{e.seconds}", datetime)
                    await asyncio.sleep(e.seconds)

                if broadcast == 1:
                    print("SLEEP 40 WHILE BC PERIOD PASSED")
                    await asyncio.sleep(5)

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


async def get_group_type(username):
    try:
        entity = await client.get_entity(username)
        if entity:
            if isinstance(entity, User):  # Check if it's a User (private chat)
                print(f"{username} is a private chat.")
            elif isinstance(entity, Channel):  # Check if it's a Channel
                print(f"{username} is a channel.")
            elif isinstance(entity, Chat):  # Check if it's a Chat (group)
                print(f"{username} is a group.")
            else:
                print(f"Unable to determine the type of {username}.")
    except ValueError as e:
        print(f"Error: {e}")

    datetime = get_date()
    fusername = f"https://t.me/{username}"
    peer = get_peer_id(fusername)
    # Check if the peer is a channel
    if await client.get_entity(PeerChat(peer)): #isinstance(peer, types.InputPeerChat):
        result = await client(ImportChatInviteRequest(peer))
        print(f"Request sent to {username}")
        await add_sending_positions(username, 0, "ChatTest", "Instance is Group", datetime)
        # Return the chat type
        return 'Chat'

    elif await client.get_entity(PeerChannel(peer)):
        # Send a request to the channel
        result = await client(JoinChannelRequest(peer))
        print(f"Request check_chat_resultxsent to {username}")
        await add_sending_positions(username, 0, "ChatTest", "Instance is Channel", datetime)
        # Return the channel type
        return 'Channel'

    # Peer is of unknown type
    else:
        print(f"Unknown peer type for {username}")
        await add_sending_positions(username, 0, "ChatTest", "Instance is Unknown", datetime)
        return 'Unknown'


async def get_group_type2(chat_id):
    try:
        datetime = get_date()
        target_group = await client.get_entity(chat_id)
        target_group_entity = await client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
        await asyncio.sleep(50)
        peerchat = get_input_peer(target_group)
        if isinstance(entity, types.PeerChat):
            request = AddChatUserRequest(peer=entity, users=[client.get_me().id], fwd_limit=100)
            if client.get_me().id not in entity.users:
                client.invoke(request)
                print(f"Request sent to {peer_id}")
            else:
                print("You are already a member of the chat.")
            return 'Chat'
        elif isinstance(entity, types.PeerChannel):
            await add_sending_positions(chat_id, 0, "ChatTest", "Instance is Channel", datetime)
            return 'Channel'
        else:
            await add_sending_positions(chat_id, 0, "ChatTest", "Instance is Unknown", datetime)
            return 'Unknown'
    except Exception as e:
        exception_type = type(e).__name__
        message = str(e)
        await add_sending_positions(chat_id, 0, message, exception_type, datetime)
        #save_exception_state(group_id, 0, 0, exception_type, datetime)
        print(f"An error occurred: {exception_type}, {message}")

def send_request_to_peer(peer_id, user_id):
    try:
        entity = client.get_entity(peer_id)
        uentity = client.get_entity(user_id)
        peerchat = get_input_peer(uentity)
        if isinstance(entity, peerchat):
            request = AddChatUserRequest(peer=entity, users=[client.get_me().id], fwd_limit=100)
            if client.get_me().id not in entity.users:
                client.invoke(request)
                print(f"Request sent to {peer_id}")
            else:
                print("You are already a member of the chat.")
        elif isinstance(entity, peerchat):
            request = JoinChannelRequest(channel=entity)
            if not client.get_entity(entity).is_member:
                client.invoke(request)
                print(f"Request sent to {peer_id}")
            else:
                print("You are already a member of the channel.")
        else:
            print(f"The peer {peer_id} is not a valid chat or channel.")
    except Exception as e:
        print(f"Error sending request to {peer_id}: {e}")



async def check_chatchannelslist(chat_list):
    verified_chats = []
    for chat in chat_list:
        print(f"Чат:{chat}|||||||||||||||||||||||||||||||||")
        chat_res = await get_chat_data(chat)
        if len(chat_res) > 0:
            print("ALSO PRESENT IN DB")
        elif len(chat_res) == 0:
            try:
                response = await client.get_entity(chat)
                print(response)
                chat_id = response.id
                #verified_chats[chat_id] = response.title
                #verified_chats[chat_id] = chat
                verified_chats.append(chat_id)
                print("CHAT ADDED IN DB")
                print(verified_chats)
                await add_chat_data(response.id, chat, "verified")

            except ValueError as e:
                print (f'Value Error{e}')
                continue

            except UsernameInvalidError as e:
                print (f'Value Error{e}')
                continue

    return verified_chats

#tr = check_chatchannelslist(chat_list2)
#print(tr)

async def get_positionafj(position_id):
    try:
        #читаем файл позиций
        filename = '/var/local/bot3101fc/positions.json'
        if path.isfile('/var/local/bot3101fc/positions.json') is False:
            raise Exception("File not found")

        with open(filename) as f:
            exist_positions = json.load(f)

        for row in exist_positions:
            if 'position_id' in row and row['position_id'] == position_id:
                article_url = row['article_url']
                return article_url

        return None

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


async def get_entity(chat_url):
    try:
        target_group = await client.get_entity(chat_url)
        if isinstance(target_group, Channel): #target_group.type == "channel":
            chtype = 'channel'
            print("Entity is a Channel")
        elif isinstance(target_group, Group): #target_group.type == "chat":
            chtype = 'chat'
            print("Entity is a Group")
        elif isinstance(target_group, User): #target_group.type == "user":
            chtype = 'user'
            print("Entity is a User")
        else:
            chtype = 'unknown'
            print("Entity type is unknown")

        entity = await client.get_input_entity(target_group)
        print(chtype, target_group, entity)
        return chtype, target_group, entity

    except FloodWaitError as e:
        print(f"FloodWaitError: {chat_url}, {e.seconds}")
        datetime = get_date()
        await add_sending_positions(chat_url, 0, "GET_ENTITY", f"FloodWaitError:{chat_url}:{e.seconds}", datetime)
        await asyncio.sleep(e.seconds)

    except UsernameInvalidError:
        print(f"Invalid username: {chat_url}")
        datetime = get_date()
        await add_sending_positions(chat_url, 0, "GET_ENTITY", f"UsernameInvalidError:{chat_url}", datetime)
        await asyncio.sleep(30)

    except UsernameNotOccupiedError:
        print(f"Username does not exist: {chat_url}")
        datetime = get_date()
        await add_sending_positions(chat_url, 0, "GET_ENTITY", f"UsernameNotOccupiedError:{chat_url}", datetime)
        await asyncio.sleep(20)


async def tg_send_message(client):

    broadcast = 0
    await client.start()

    if not await client.is_user_authorized():
        print('Telegram client failed to start.')
        return

    while True:

        success_chats = {}
        perm_list1 = ['test_rabota_permi_101', 'goodnewsrussia1']
        perm_list = ['test_rabota_permi_101']

        positions = await get_new_positionxs()

        chat_list = ""
        perm_list = ['test_rabota_permi_101']
        perm_list2 = ['goodnewsrussia1']
        vacs_list = ['goodnewsrussia1', 'vacsmsk', 'vacsspb', 'vacssam', 'vacspnz', 'vacskzn']

        if len(chat_list) > 0:
            for chat_id in chat_list:
                furl = f"t.me/{chat_id}"
                target_group = await client.get_entity(furl)
                target_group_entity = await client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
        else:

            for position in positions:
                print(position['position_id'])
                position_description = position['position_description']
                file_path = f"/var/local/bot3101fc/tgbot/images/position{position['position_id']}.png"
                article_url = await get_positionafj(position['position_id'])
                chat_id = position['vacs_url']

                if position['position_state'] == "Approved":

                    if position_description:
                        shortml = 200
                        descritionlen = len(position_description)
                        if descritionlen >= shortml:
                            shortmestext = f"{position_description[0:shortml]}...\n\n"
                            hashtags = extract_hashtags(position_description)
                        elif descritionlen < shortml:
                            shortmestext = position_description

                        #добавляем ссылку на полную версию
                        htlinktext = f"<a href={article_url}>читать далее...</a>"
                        alinktext = f"[читать далее...]({article_url})"
                        shortmestext += f"\n{htlinktext}"
                        if descritionlen >= shortml:
                            shortmestext += f"\n\n{hashtags}"

                    else: shortmestext = "Текст отсутствует"
                else: shortmestext = position_description

                message_type = 'photo'  # replace with your type variable  file='file_id'
                image_url = None
                message_text = None

                if position['vacs_url'] == "ALL_CHANNELS" and position['position_state'] == "Approved":
                    places = get_cities_places()
                    for place in places:
                        chat_id = place['vacs_url']
                        furl = f"t.me/{chat_id}"
                        target_group = await client.get_entity(furl)
                        target_group_entity = await client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
                        if chat_id != "ALL_CHANNELS":
                            broadcast = 0
                            await send_message(client, chat_id, position_id=position['position_id'], message_type=message_type, message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path, broadcast=broadcast)

                elif position['position_state'] == "Broadcast":
                    #places = get_chats()
                    places = await get_chatsmy()
                    print(places)

                    for place in places:
                        inside = 0
                        chat_id = place['chat_url']
                        resultc = await check_chat(chat_id)
                        print(len(resultc), resultc)
                        if len(resultc) >= 1:
                            continue
                        try:
                            result = await get_entity(chat_id)
                            chtype, entity, ientity = result
                            if chtype == "channel":
                                if entity.megagroup:
                                    print("MEGAGROUP IS EXIST")
                                    if entity.restricted is True:
                                        print("BUT TG RESTRICTED")
                                        continue
                                elif entity.megagroup is False:
                                    continue
                        except Exception as e:
                            # Handle any other exceptions here
                            print(f"An error occurred: {e}")
                            continue

                        #if entity.is_channel():
                        async for dialog in client.iter_dialogs():
                            print(dialog.id, dialog.name)
                            if entity.id == dialog.id:
                                print("мы в чате")
                                inside = 1
                            else:
                                print("skip")
                        if inside == 0:
                            try:
                                result = await client(JoinChannelRequest(entity))
                                await asyncio.sleep(2)

                            except InviteRequestSentError:
                                print(f"INVITE уже отправии запрос, отправим сообщение в следующе круге: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", "Invite Request Has Been Sent", datetime)
                                await asyncio.sleep(15)
                                continue

                            except ChatWriteForbiddenError:
                                print(f"INVITE Аккаунту запретили писать в этот чат: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", "Chat Write Forbidden", datetime)
                                await asyncio.sleep(15)
                                continue

                            except ConnectionError:
                                print(f"INVITE  ConnectionError: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"ConnectionError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except UserBannedInChannelError:
                                print(f"INVITE  UserBannedInChannelError: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"UserBannedInChannelError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except UsernameInvalidError:
                                print(f"INVITE  UsernameInvalidError: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"UsernameInvalidError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except ValueError:
                                print(f"INVITE Отсутствует имя пользователя: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"ValueError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except ChannelPrivateError:
                                print(f"INVITE CPE: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"ChannelPrivateError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except ChatInvalidError:
                                print(f"INVITE ChatInvalidError: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"ChatInvalidError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except ChannelInvalidError:
                                print(f"INVITE CIE: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"ChannelInvalidError:{chat_id}", datetime)
                                await asyncio.sleep(5)
                                continue

                            except FloodWaitError as e:
                                print(f"INVITE Надо подождать: {chat_id}.")
                                datetime = get_date()
                                await add_sending_positions(chat_id, position_id, "INVITE", f"FloodWaitError:{chat_id}:ждем{e.seconds}", datetime)
                                await asyncio.sleep(e.seconds)

                        broadcast = 1
                        print(position, message_type, shortmestext, image_url, file_path, broadcast)
                        await send_message(client, chat_id, position_id=position['position_id'], message_type=message_type, message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path, broadcast=broadcast)

                        #else:
                        #    continue
                        #else:
                        #    print("MIMO_____*****>>>>>>>")
                        #    datetime = get_date()
                        #    await add_sending_positions(chat_id, position_id, shortmestext, f"OTHER PATH:{chat_id}", datetime)
                else:
                    broadcast = 0

                    await send_message(client, chat_id, position_id=position['position_id'], message_type=message_type, message_text=message_text, caption=shortmestext, image_url=image_url, file_path=file_path, broadcast=broadcast)
                #await update_positionx(position['position_id'], state="Posted")
                #if multi_mode == 1:
                await asyncio.sleep(0.5)

        first = 1
        positions = None
        print('ON AIR +>>>.')
        if broadcast == 1:
            print("MAIN CYCLE SLEEP 400 WHILE BC PERIOD PASSED")
            await asyncio.sleep(400)
            #await asyncio.sleep(10)
        print("MAIN CYCLE SLEEP 30 WHILE BC PERIOD PASSED")
        await asyncio.sleep(30)
        #await client.disconnect()

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
'''x = 0
try:
    while True:
        asyncio.run(positions = get_new_positionxs())
        if len(positions) > 0:
            asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash)))
            x+=1
            print(f"Итерация:{x}")

        time.sleep(5)

except GeneratorExit:
    # Clean up resources or perform finalization tasks
    pass'''

async def process_new_records():
    positions = await get_new_positionxs()
    for position in positions:
        asyncio.get_event_loop().run_until_complete(tg_send_message(client = TelegramClient('Forwarder', api_id, api_hash)))
        await process_position(position)

async def process_record(record):
    # Perform your new function here
    print(record)


'''while True:
    try:
        asyncio.get_event_loop().run_until_complete(send_message(client))
        asyncio.sleep(20)

    except Exception as e:
        print(f"An error occurred: {e}")'''


# Run the process_new_records function asynchronously
asyncio.get_event_loop().run_until_complete(tg_send_message(client))