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
                                          ChatWriteForbiddenError,
                                          ChatAdminRequiredError,
                                          UserBannedInChannelError)

from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
import config
import configparser
import tqdm
import os, sys
from sys import stdout
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

#JUMP_LEFT_SEQ = '\u001b[100D'

def get_time_str():
    return datetime.now().strftime("%H:%M:%S")

def enter_group(client, g_url, group):
    group_target = "t.me/" + str(g_url)
    username = client.get_entity(group_target)
    client(JoinChannelRequest(username))
    print(f'{lg} Зашли в группу на {phone}')
    target_group = group
    return target_group

def loading(cur):
    print(JUMP_LEFT_SEQ, end='')
    print(f'Прогресс: {cur:0>3}%', end='')
    stdout.flush()
    print()

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

group_target = ''
source_group = ''
users = []
chats = []
groups = []
invited = 0
state = "created"
count = 110
start = 0
target_group=''
mode = ''
source_group_selected = 0
target_group_selected = 0
last_date = None
chunk_size = 200
print(sys.argv)

print(gr+"[1] работать целиком \n[2] работать по 5 инвайтов ")
mode2 = int(input(gr+"Введите свой выбор( 1/2 ) : "+re))

#cpass=get_all_tgaccounts_time()
cpass=get_all_tgaccounts_time_wb()
print(cpass)

#подключаемся к аккаунту по времени
for cp in cpass:
    print(cp)
    if cp[4] == 'wait2' or cp[4] == 'banned' or cp[4] == 'wait3': continue
    try:
        account_id = cp[0]
        api_id = cp[1]
        api_hash = cp[2]
        phone = cp[3]
        wait24field = cp[8]
        print(f"Работаем с аккаунтом:{phone} | ЕГО время старта: {wait24field}.")

        if config.PROXY_ENABLED:
            s = socks.socksocket()
            rnd_proxy = random.choice(config.PROXY_IPS).split(":")
            print(f"Подключение к Телеграмм с прокси {rnd_proxy}!")
            client = TelegramClient(phone, api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
            client.start()
            print(f'[+] Успешная аутентификация - {phone}')
            client.disconnect()

        else:
            print(f"Подключение к Телеграмм без прокси!")
            client = TelegramClient(phone, api_id, api_hash)

        client.connect()
        if not client.is_user_authorized():
            banner()
            client.start()
            print(f'[+] Успешная аутентификация - {phone}')
            client.disconnect()
            client.connect()

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

    if sys.argv[1] == 'group':
        groupsdb = groups_telegram()
        print(groupsdb)
        s = 0
        for groupdb in groupsdb:
            print(gr+'['+cy+str(s)+gr+']'+cy+' - '+groupdb[1])
            s+=1

        gso = input(gr+"[+] Выберите группу - введите наименование : "+re)
        source_group=gso
        source_group_selected = 1

        rows = first_grouptoinvite(source_group, start, count)

    if sys.argv[1] == 'geoparse': rows = firstgeo_toinvite(state, start, count)

    for row in rows:
        if row[2] == "ID": continue
        if row[9] in('noncontact', 'restricted', 'notexist', 'bot', 'overg', 'deleted', 'invited'): continue
        print(row)
        user = {}
        user['acc_id'] = row[0]
        user['username'] = row[1]
        user['id'] = int(row[2])
        #user['id'] = 5518497581
        user['access_hash'] = int(row[3])
        user['name'] = row[4]
        users.append(user)

    if(target_group != ''): print("||| TARGET GROUP PRESENT")

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash = 0
    ))
    chats.extend(result.chats)
    print(chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    print(groups)
    i=0
    for group in groups:
        print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title+'|'+group.title)
        if group.title == gso:
            clientingroup = 1
            target_group = client.get_entity(group.id)
            client(JoinChannelRequest(target_group))
        i+=1

    g_index = ''
    if(group_target == ''):
        g_index = input(gr+"[+] Введите номер группы для инвайта пользователей или N : "+re)
        if g_index != 'N': target_group=groups[int(g_index)]

    if g_index == 'N':
        g_url = input(gr+"[+] Введите url или username группы для инвайта пользователей : "+re)
        try:
            group_target = "t.me/" + str(g_url)
            username = client.get_entity(group_target)
            client(JoinChannelRequest(username))
            print(f'{lg} Зашли в группу на {phone}')
            target_group = username
        except:
            print(gr+'[!] Ошибка входа в группу {phone}'+re)

    print("||||||||||")
    print(target_group.title)
    print("||||||||||")
    target_group_entity = client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
    print(gr+"[1] добавлять в группу по username \n[2] добавлять в группу по user ID ")
    mode = int(input(gr+"Введите свой выбор( 1/2 ) : "+re))
    n = 0
    print(f"Выбрано ТГ аккаунтов для инвайта: {len(users)}")
    cur_time = datetime.datetime.now()
    print(str(account_id) + "|" + str(cur_time))
    h = get_tgaccount_statecounts(account_id)
    print(h)
    invited = h[0]
    invited_cs = 0
    f = 0
    not_invited = 0
    for user in users:
        n += 1
        if 1 == 1:
            time.sleep(2)
            try:
                print (n, "Пробуем добавить аккаунт ID {}".format(user['id']))
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
                    sys.exit(re+"[!] Выбран некорректный режим работы. Попробуйте еще раз.")
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                print(user['acc_id'])
                update_tgparsex(user['acc_id'], state='invited')
                update_tgaccounts(account_id, pole='invited24')

                invited += 1
                invited_cs += 1
                print(gr+f"+ И:{invited}/ИК:{invited_cs} | Добавили пользователя: {user['username']}")
                if invited >= 40:
                    cur_day = cur_time.day
                    cur_hour = cur_time.hour
                    print(cur_time.hour)
                    print(f"{cur_time} | Аккаунт {account_id} набрал {config.INV_CNT} инвайтов !")
                    print(f"{cur_time} | Аккаунт {account_id} уходит в режим ожидания до {cur_day + 1} числа и {cur_hour + 1} часов!")
                    update_tgaccounts(account_id, pole="waitfor24")
                    break

                sleeps = random.randrange(80, 120)
                print(gr+"[+] Пауза 80-120 секунд..."+ str(sleeps))
                time.sleep(sleeps)
                continue
            except UserBannedInChannelError:
                print(str(account_id) + ' в бане!')
                update_tgaccounts(account_id, pole='banned')
                remove_accountx(account_id=account_id)
                break
            except UserPrivacyRestrictedError:
                print(f"{cur_time} | Ошибка: {user} не приглашён!")
                print(f"Пользователь {user} запретил приглашать себя!")
                not_invited += 1
                sleeps = random.randrange(80, 120)
                print(gr+"[+] Пауза 80-120 секунд..."+ str(sleeps))
                time.sleep(sleeps)
                #time.sleep(config.ERR_KD)
                update_tgparsex(user['acc_id'], state='restricted')
                #self.lists.add_ban(user)
                continue
            except UserChannelsTooMuchError:
                print(f"{cur_time} | Ошибка: {user} не приглашён!")
                print(f"Пользователь {user} имеет слишком много групп!")
                not_invited += 1
                sleeps = random.randrange(80, 120)
                print(gr+"[+] Пауза 80-120 секунд..."+ str(sleeps))
                time.sleep(sleeps)
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
            except ChatAdminRequiredError:
                print(f"{cur_time} | Ошибка: {user} не приглашён!")
                print(f"Пользователь {user} является ботом !")
                not_invited += 1
                time.sleep(config.ERR_KD)
                update_tgparsex(user['acc_id'], state='bot')
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
                    #self.lists.add_check(self.phone, [cur_day, cur_hour+hour, cur_min+min, sec])
                    update_tgaccounts(account_id, pole="waitfor24")
                    break
            except ChatWriteForbiddenError:
                print(
                    f"{cur_time} | Ошибка: чат-цель недоступен, возможно вы не вошли в него!"
                )
                break
            except PeerFloodError as e:
                f += 1
                if f >= 3:
                    update_tgaccounts(account_id, pole="waitfor24")
                    break
                print(f"{cur_time} | Ошибка пользователя: Слишком много запросов!")
                cur_day = cur_time.day
                cur_hour = cur_time.hour
                cur_min = cur_time.minute
                cur_sec = cur_time.second
                continue

            except KeyboardInterrupt:
                break

            except:
                print(f"{cur_time} | Неизвестная ошибка: ", sys.exc_info())
                continue

