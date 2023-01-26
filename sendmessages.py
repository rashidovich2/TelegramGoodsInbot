#!/usr/bin/env python3
from telethon.sync import TelegramClient, connection
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
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

from telethon.tl.functions.channels import InviteToChannelRequest
import config
import configparser
import tqdm
import os, sys
import socks
import csv
import traceback
import datetime
import time
import random
import requests, socket
from sutils import *
from tgbot.services.api_sqlite import *

print(type(datetime))

def get_time_str():
    return datetime.now().strftime("%H:%M:%S")

cur_time = datetime.datetime.now()

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

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

#check_phones()

cpass=get_all_avtgaccountsend()
#print(cpass)
for cp in cpass:
    print(cp)
    if cp[5] == 'wait2' or cp[5] == 'banned' or cp[5] == 'wait3': continue
    try:
        account_id = cp[0]
        api_id = cp[1]
        api_hash = cp[2]
        phone = cp[3]
        waits24field = cp[9]
        print(f"Работаем с аккаунтом:{phone} | ЕГО время старта: {waits24field}.")

        if config.PROXY_ENABLED:
            s = socks.socksocket()
            rnd_proxy = random.choice(config.PROXY_IPS).split(":")
            print(f"Подключение к Телеграмм с прокси {rnd_proxy}!")
            client = TelegramClient(phone, api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
            #client.start()
            #print(f'[+] Успешная аутентификация - {phone}')
            #client.disconnect()
            client.connect()
        else:
            print(f"Подключение к Телеграмм без прокси!")
            client = TelegramClient(phone, api_id, api_hash)
            client.connect()
        if not client.is_user_authorized():
            banner()
            client.start()
            print(f'[+] Успешная аутентификация - {phone}')
            client.disconnect()
            #client.connect()
    
    except PhoneNumberBannedError:
        print(f" | Ошибка: аккаунт {account_id} был удалён!")
        update_tgaccounts(account_id, pole="banned")
        continue
    except FloodWaitError as e:
        print(
            f"{cur_time} | Ошибка: Таймаут на {e.seconds} секунд, это примерно {round(e.seconds / 60)} минут \n"
        )
        if config.CHECK_TIMEOUT:
            for i in range(e.seconds):
                time.sleep(1)
        else:
            cur_sec = cur_time.second
            sec = e.seconds + cur_sec
            sec = sec % (24 * 3600)
            hour = sec // 3600
            sec %= 3600
            min = sec // 60
            sec %= 60

            print(str(cur_time.hour)+":"+str(cur_time.minute))
            utime = time.mktime(cur_time.timetuple())
            print(f"{cur_time} | Аккаунт {account_id} уходит в режим ожидания на {hour} часов, {min} минут, {sec} секунд")
            break

    #os.system('clear')
    banner()


    state = "created"
    #sended = 0
    start = 0
    count = 39
    rows =  first_tosend(state, start, count)
    users = []
    for row in rows:
        user = {}
        user['username'] = row[1]
        user['id'] = int(row[2])
        user['access_hash'] = int(row[3])
        user['name'] = row[4]
        users.append(user)
    print(gr+"[1] send sms by user ID\n[2] send sms by username ")
    mode = int(input(gr+"Input : "+re))

    #message = input(gr+"[+] Enter Your Message : "+re)
    message = f"С наступающим Новым Годом друзья! Желаем счастья, радости, достатка и много-много интересного в Новом году! Команда @Goodsinbot"

    n = 0
    print(f"Выбрано ТГ аккаунтов для инвайта: {len(users)}")
    cur_time = datetime.datetime.now()
    print(str(account_id) + "|" + str(cur_time))
    h = get_tgaccounts_statecounts(account_id)
    print(h)
    sended = h[0]
    sended_cs = 0
    f = 0
    not_sended= 0
    #users = ['raclear', 'Oleg2023long', 'OlegDJI']
    blockedu = ['Admin', 'Bot', 'bot']

    for user in users:
        n += 1
        if 1 == 1:
            time.sleep(2)
            try:
                print (n, "Пробуем отправить сообщение пользователю с аккаунтом ID {}".format(user['id']))
                if mode == 2:
                    if user['username'] == "" or user['username'] in blockedu or user['access_hash'] < 0: # or user['username'].startswith('bot'):
                        continue
                    receiver = client.get_input_entity(user['username'])
                elif mode == 1:
                    receiver = InputPeerUser(user['id'],user['access_hash'])
                else:
                    print(re+"[!] Invalid Mode. Exiting.")
                    client.disconnect()
                    sys.exit()
                print(gr+"[+] Waiting 90 seconds.")
                time.sleep(90)
                print(gr+"[+] Sending Message to:", user['username'])
                client.send_message(receiver, message.format(user['name']))
                print(cp[0])
                print(user)
                update_tgparsex(cp[0], statesend='sended')
                update_tgaccounts(cp[0], pole='sended24')
                sended += 1
                sended_cs += 1
                print(gr+f"+ С:{sended}/СК:{sended_cs} | Отправили пользователю: {user['username']}")
                #sended += 1
                #sended_cs += 1
                print(gr+"[+] Waiting 90 seconds.")
                time.sleep(90)
                continue
            except PeerFloodError:
                print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                update_tgaccounts(cp[0], pole='waifors24')
                break
                #sys.exit()
            except Exception as e:
                print(re+"[!] Error:", e)
                print(re+"[!] Trying to continue...")
                continue
    client.disconnect()
    print("Done. Message sent to all users.")