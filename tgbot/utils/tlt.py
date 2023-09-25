import asyncio
#from telethon.sync import TelegramClient
import os, sys
from sys import stdout
from os import path
import config
import requests, socks
import random
from telethon import TelegramClient, events
from telethon.extensions import html
from telethon import functions, types
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.users import GetUsersRequest, GetFullUserRequest
from telethon.utils import get_input_peer, get_peer_id
from telethon.tl.types import User, Chat, Channel, InputPeerEmpty, InputPeerChannel, InputPeerUser, InputPeerChat, PeerChat, PeerChannel
from telethon.errors import UserBannedInChannelError, ChannelInvalidError, ChannelPrivateError, ChatWriteForbiddenError, SlowModeWaitError, UsernameInvalidError, ChatGuestSendForbiddenError, ForbiddenError, ChatAdminRequiredError, PeerFloodError, UsernameNotOccupiedError, FloodWaitError
from tgbot.services.api_db_mysql import *
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)


sys.path.append(parent)

#PROXY

#api_id = 27173025
#api_hash = 'aa7e0b3f2c3c579993372ce86e95e993'
#client = TelegramClient('Forwarder3', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
#cl_name = "Forwarder3"


async def get_entity(chat_url):

    if config.PROXY_ENABLED:
        s = socks.socksocket()
    rnd_proxy = random.choice(config.PROXY_IPS).split(":")


    api_id = 20974935
    api_hash = '9fbac23d7f44aa3cdb065237998a4b14'
    client = TelegramClient('Forwarder2', api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )

    await client.start()

    if not await client.is_user_authorized():
        print('Telegram client failed to start.')
    return

    try:
        target_group = await client.get_entity(chat_url)
        entity = await client.get_input_entity(target_group)
        return target_group, entity

    except FloodWaitError as e:
        print(f"FloodWaitError: {chat_url}, {e.seconds}")
        #datetime = get_date()
        #await add_sending_positions(chat_url, 0, "1234567", f"FloodWaitError:{chat_url}:{e.seconds}", datetime)
        await asyncio.sleep(e.seconds)

    except UsernameInvalidError:
        print(f"Invalid username: {chat_url}")
        #datetime = get_date()
        #await add_sending_positions(chat_url, 0, "1234567", f"UsernameInvalidError:{chat_url}", datetime)
        await asyncio.sleep(30)

    except UsernameNotOccupiedError:
        print(f"Username does not exist: {chat_url}")
        #datetime = get_date()
        #await add_sending_positions(chat_url, 0, "12345678", f"UsernameNotOccupiedError:{chat_url}", datetime)
        await asyncio.sleep(20)

    await client.close()


async def get_tlt_group_info(chat_id):
    result = await check_chat(chat_id)
    print(len(result), result)
    furl = f"https://t.me/{chat_id}"
    entity, ientity = await get_entity(chat_id)
    print("SS")
    return entity, ientity

