#!/usr/bin/env python3
from telethon.sync import TelegramClient, connection
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, ChannelParticipantsRecent
#from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.errors.rpcerrorlist import (UserPrivacyRestrictedError,
                                          UserNotMutualContactError,
                                          FloodWaitError,
                                          PeerFloodError,
                                          UserChannelsTooMuchError,
                                          UserDeactivatedBanError,
                                          PhoneNumberBannedError,
                                          UsernameInvalidError,
                                          ChatWriteForbiddenError)

from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest, GetParticipantsRequest
import config
import configparser
import tqdm
import os, sys
import socks
import csv
import traceback
from colorama import init, Fore
import datetime
import time
import random
import requests, socket
from sutils import *
from tgbot.services.api_sqlite_advert import *

print(type(datetime))

def get_time_str():
    return datetime.now().strftime("%H:%M:%S")

cur_time = datetime.datetime.now()

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]


def banner():
    print(f"""
´´´´¶¶¶¶¶¶´´´´´´¶¶¶¶¶¶
´´¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶¶¶¶¶¶
´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´¶¶¶¶¶
¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ´¶¶¶¶¶´
´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
´´´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶
´´´´´´´´´¶¶¶¶¶¶¶¶
´´´´´´´´´´´¶¶¶¶
{re}

by rashidovich
        """)

check_phones()

cpass=get_all_avtgaccounts()
print(cpass)
for cp in cpass:
    print(cp)
    try:
        account_id = cp[0]
        api_id = cp[1]
        api_hash = cp[2]
        phone = cp[3]
        wait24field = cp[8]
        print(f"Работаем с аккаунтом:{phone}.")

        if config.PROXY_ENABLED:
            s = socks.socksocket()
            rnd_proxy = random.choice(config.PROXY_IPS).split(":")
            print(f"Подключение к Телеграмм с прокси {rnd_proxy}!")
            client = TelegramClient(phone, api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
            #client.start(self.phone)
        else:
            print("Подключение к Телеграмм без прокси!")
            client = TelegramClient(phone, api_id, api_hash)
                    #client.start(self.phone)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            #os.system('clear')
            banner()
            client.sign_in(phone, input(f"{gr}[+] Enter the code for {phone}: {re}"))

    except PhoneNumberBannedError:
        print(f" | Ошибка: аккаунт {account_id} был удалён!")
        update_tgaccounts(account_id, pole="banned")
        continue

    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

#def select_scr_group(client):
    result = client(GetDialogsRequest(
                 offset_date=last_date,
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=chunk_size,
                 hash = 0
             ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except Exception:
            continue

    print(
        f'{gr}[+] Выберите группу для сбора участников из группу на аккаунте {phone}:{re}'
    )
    for i, g in enumerate(groups):
        print(f'{gr}[{cy}{str(i)}{gr}]{cy} - {g.title}')
    print('')
    g_index = input(
        f"{gr}[+] Введите номер группы для сбора пользователей или N : {re}"
    )

#    return g_index

#g_index = select_scr_group(client)
    target_group = ''

    if g_index == 'N':
        g_url = input(
            f"{gr}[+] Введите url или username группы для сбора пользователей : {re}"
        )
        try:
            group = f't.me/{str(g_url)}'
            username = client.get_entity(group)
            client(JoinChannelRequest(username))
            print(f'{lg} Зашли в группу на {phone}')
            target_group = username

        except Exception:
            print(f'{r} Ошибка входа в группу {phone}')
            continue


    else:
        target_group=groups[int(g_index)]

    print("||||||||||")
    print(target_group.title)
    print("||||||||||")

    channel = target_group

    print(f'{gr}[+] Собираем пользователей...')
    time.sleep(1)

#all_participants = self.client.get_participants(target_Group)

#all_participants = []
#while_condition = True
#my_filter = ChannelParticipantsSearch('')
#offset = 0
#while while_condition:
#	participants = self.client(GetParticipantsRequest(channel=target_Group,  offset= offset, filter = my_filter, limit=200, hash=0))
#	all_participants.extend(participants.users)
#	offset += len(participants.users)
#	print(len(participants.users))
#	if len(participants.users) < 1 :
#		while_condition = False

    offset = 0
    limit = 100
    all_participants = []
    #channel = 'building_work'
    while True:
        participants = client(GetParticipantsRequest(
            channel, ChannelParticipantsRecent(), offset, limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
        print(offset)

    print(f'{gr}[+] Сохраняем в БД...')
    time.sleep(1)
    with open("members.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        #print(f"Кол-во участников группы:"+ len(all_participants))
        for user in all_participants:
            if user.username is None: continue
            if user.username == "": continue
            if check_dbfor_username(user.username): continue
            username = user.username or ""
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            name = f'{first_name} {last_name}'.strip()
            state = "created"
            groupname = target_group.title
            groupid = target_group.id
            usah = user.access_hash
            usid = user.id
            source = 'groups'
            tag = target_group.title

            #writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
            add_tgacc_todb(username,usid,usah,name,source,groupname,groupid,tag,state)

    print(f'{gr}[+] Пользователи успешно собраны.')