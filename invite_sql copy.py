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

from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
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

check_phones()

mode=''

cpass=get_all_avtgaccounts()
print(cpass)
target_group = ''
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

    #os.system('clear')
    banner()
    #input_file = sys.argv[1]
    users = []
    state = "created"
    count = 110
    start = 0

    print(sys.argv)
    if sys.argv[1] == 'group': rows = first_toinvite(state, start, count)
    if sys.argv[1] == 'geoparse': rows = firstgeo_toinvite(state, start, count)
    #rows = first_toinvite(state, start, count)

    #with open(input_file, encoding='UTF-8') as f:
    #    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    #next(rows, None)

    for row in rows:
        #if row[2] == "ID": continue
        #if row[1] == "None": continue  #in('restricted', 'notexist', 'invited', )
        #if row[9] is None or len(row[9]) == 0: continue
        if row[9] in('noncontact', 'restricted', 'notexist', 'overg', 'deleted', 'invited'): continue
        print(row)
        user = {
            'acc_id': row[0],
            'username': row[1],
            'id': int(row[2]),
            'access_hash': int(row[3]),
            'name': row[4],
        }
        users.append(user)

    #если установлена группа - не запрашиваем
    if(target_group != ''): print("||| TARGET GROUP PRESENT")
    #чаты пользователя
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

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

    for i, group in enumerate(groups):
        print(f'{gr}[{cy}{str(i)}{gr}]{cy} - {group.title}|{group.title}')
    print('')
    if (target_group == ''):
        g_index = input(
            f"{gr}[+] Введите номер группы для инвайта пользователей или N : {re}"
        )

    #    return g_index

    #g_index = select_scr_group(client)
    #target_group = ''

    if g_index == 'N':
        g_url = input(
            f"{gr}[+] Введите url или username группы для инвайта пользователей : {re}"
        )
        try:
            group_target = f't.me/{str(g_url)}'
            username = client.get_entity(group_target)
            client(JoinChannelRequest(username))
            print(f'{lg} Зашли в группу на {phone}')
            target_group = group

        except Exception:
            print(gr+'[!] Ошибка входа в группу {phone}'+re)

    else:
        target_group=groups[int(g_index)]

    print("||||||||||")
    print(target_group.title)
    print("||||||||||")

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    #if(mode != ''):
    #    print("| Режим выбран")
    #else:
    print(gr+"[1] добавлять в группу по username \n[2] добавлять в группу по user ID ")
    mode = int(input(f"{gr}Введите свой выбор( 1/2 ) : {re}"))
    n = 0
    print(f"Выбрано аккаунтов для инвайта: {len(users)}")

    cur_time = datetime.datetime.now()
    print(f"{str(account_id)}|{str(cur_time)}")
    h = get_tgaccount_statecounts(account_id)
    print(h)
    invited = h[0]
    invited_cs = 0
    #print(h['invited24'])
    not_invited = 0

    for user in users:
        n += 1
        time.sleep(1)
        try:
            print(n, f"Пробуем добавить аккаунт ID {user['id']}")
            if mode == 1:
                if user['username'] == "":
                    update_tgparsex(user['acc_id'], state='nousname')
                    print("NOusName\n")
                    #user_to_add = InputPeerUser(user['id'], user['access_hash'])
                    continue
                if check_dbfor_invited_username(user['username']):
                    print(user['username']+" был приглашен в БД.\n")
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit(f"{re}[!] Выбран некорректный режим работы. Попробуйте еще раз.")
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print(user['acc_id'])
            update_tgparsex(user['acc_id'], state='invited')
            update_tgaccounts(account_id, pole='invited24')
            invited += 1
            invited_cs += 1
            print(
                f"{gr}+ И:{invited}/ИК:{invited_cs} | Добавили пользователя: {user['username']}"
            )
            if invited >= 40: #invited_cs >= 5 or
                cur_day = cur_time.day
                cur_hour = cur_time.hour
                print(cur_time.hour)
                #cur_hour = datetime.datetime.now().hour
                #cur_min = datetime.datetime.now().minute
                #cur_sec = datetime.datetime.now().second
                print(f"{cur_time} | Аккаунт {account_id} набрал {config.INV_CNT} инвайтов !")
                print(f"{cur_time} | Аккаунт {account_id} уходит в режим ожидания до {cur_day + 1} числа и {cur_hour + 1} часов!")
                #self.lists.add_check(self.phone, [cur_day + 1, cur_hour + 1, cur_min, cur_sec])
                update_tgaccounts(account_id, pole="waitfor24")
                break

            #n += 1
            #if n == 40:
            #sys.exit(re+"[!] 40 пользователей приглашено.")
            print(f"{gr}[+] Пауза 10-30 секунд...")
            time.sleep(random.randrange(10, 30))
            continue
        except UserPrivacyRestrictedError:
            print(f"{cur_time} | Ошибка: {user} не приглашён!")
            print(f"Пользователь {user} запретил приглашать себя!")
            not_invited += 1
            time.sleep(config.ERR_KD)
            update_tgparsex(user['acc_id'], state='restricted')
            #self.lists.add_ban(user)
            continue
        except UserChannelsTooMuchError:
            print(f"{cur_time} | Ошибка: {user} не приглашён!")
            print(f"Пользователь {user} ебанутый!")
            not_invited += 1
            time.sleep(config.ERR_KD)
            update_tgparsex(user['acc_id'], state='overg')
            #self.lists.add_ban(user)
            continue
        except UserDeactivatedBanError:
            print(f"{cur_time} | Ошибка: {user} не приглашён!")
            print(f"Пользователь {user} удалён!")
            not_invited += 1
            time.sleep(config.ERR_KD)
            update_tgparsex(user['acc_id'], state='deleted')
            continue
        except UserNotMutualContactError:
            print(f"{cur_time} | Ошибка: {user} не приглашён!")
            print(f"Пользователь {user} не взаимный контакт !")
            not_invited += 1
            time.sleep(config.ERR_KD)
            update_tgparsex(user['acc_id'], state='noncontact')
            continue
        except (ValueError, UsernameInvalidError):
            print(f"{cur_time} | Ошибка: {user} не приглашён!")
            print(f"Пользователя с ником {user} не существует!")
            not_invited += 1
            time.sleep(config.ERR_KD)
            update_tgparsex(user['acc_id'], state='notexist')
            continue
        except FloodWaitError as e:
            print(
                f"{cur_time} | Ошибка: Таймаут на {e.seconds} секунд, это примерно {round(e.seconds / 60)} минут \n",
                f"За время работы бот успел пригласить {invited} пользователей"
            )
            if config.CHECK_TIMEOUT:
                for _ in range(e.seconds):
                    time.sleep(1)
            else:
                cur_sec = cur_time.second
                sec = e.seconds + cur_sec
                sec = sec % (24 * 3600)
                hour = sec // 3600
                sec %= 3600
                min = sec // 60
                sec %= 60

                print(f"{cur_time.hour}:{cur_time.minute}")
                utime = time.mktime(cur_time.timetuple())
                print(f"{cur_time} | Аккаунт {account_id} уходит в режим ожидания на {hour} часов, {min} минут, {sec} секунд")
                #self.lists.add_check(self.phone, [cur_day, cur_hour+hour, cur_min+min, sec])
                update_tgaccounts(account_id, pole="waitfor24")
                break
        except ChatWriteForbiddenError:
            print(
                f"{cur_time} | Ошибка: чат-цель недоступен, возможно вы не вошли в него!"
            )
            break
        except PeerFloodError as e:
            print(f"{cur_time} | Ошибка: Слишком много запросов!")
            cur_day = cur_time.day
            cur_hour = cur_time.hour
            cur_min = cur_time.minute
            cur_sec = cur_time.second
            print(f"{cur_time} | Аккаунт {account_id} уходит в режим ожидания до {cur_day + 1} числа и {cur_hour+1} часов!")
            #self.lists.add_check(self.phone, [cur_day + 1, cur_hour+1, cur_min, cur_sec])
            update_tgaccounts(account_id, pole="waitfor24")
            break

        except KeyboardInterrupt:
            break

        except Exception:
            print(f"{cur_time} | Неизвестная ошибка: ", sys.exc_info())
            continue

