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
#from pynput import keyboard
import keyboard
import time
import random
import requests, socket
from sutils import *
from tgbot.services.api_sqlite_advert import *

print(type(datetime))

#JUMP_LEFT_SEQ = '\u001b[100D'

def Ctrl_K():
    i = 1
    stopped = True

def callback(keyname):
    global stopped
    print(f'{keyname} was pressed!')
    stopped = True

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

reset = sys.argv[2]
check_phones(reset="no")

x = 0
group_target = ''
source_group = ''
users = []
chats = []
groups = []
accs_array = []
invited = 0
state = "created"
count = 110
start = 0
iter = 1
target_group=''
mode = ''
source_group_selected = 0
target_group_selected = 0
last_date = None
chunk_size = 200
first_run = 1
print(sys.argv)


#print(gr+"[1] работать целиком \n[2] работать по 5 инвайтов ")
#mode2 = int(input(gr+"Введите свой выбор( 1/2 ) : "+re))
acc_mode = 2
mode2 = 1
gusername = "goodnewsrussia1"

'''if sys.argv[1] == 'group':
    groupsdb = groups_telegram()
    print(groupsdb)
    s = 0
    for groupdb in groupsdb:
        print(gr+'['+cy+str(s)+gr+']'+cy+str(groupdb[0])+' - '+groupdb[1] +' : '+str(groupdb[2]))
        s+=1

    gso = input(gr+"[+] Выберите группу - введите id : "+re)
    source_group=gso
    source_group_name=groupdb[1]
    source_group_selected = 1'''

source_group = 1224708719 #1520545687 #1640509728 #1697116411
rows = first_grouptoinvitebyid(source_group, start, count)

if sys.argv[1] == 'geoparse': rows = firstgeo_toinvite(state, start, count)

'''async for dialog in client.iter_dialogs():
    if dialog.entity.megagroup:
        group_name = dialog.entity.title
        members_count = str(dialog.entity.participants_count)
        print(f'GROUP: {group_name} - ({members_count} members)')'''

#cpass=get_all_tgaccounts_time()

cpass=get_all_tgaccounts_to_invite()
print(cpass)

#собираем аккаунты для инвайта
for cp in cpass:
    #print(cp)
    if cp[4] == 'wait2' or cp[4] == 'banned' or cp[4] == 'wait3': continue
    try:
        account_id = cp[0]
        api_id = cp[1]
        api_hash = cp[2]
        phone = cp[3]
        inv24, send24, iter24  = cp[8], cp[9], cp[13]
        #update_tgaccounts(account_id, pole="reset")
        print(f"Работаем с аккаунтом:{phone} | ЕГО время старта: И:{inv24} | C:{send24} | Итер:{iter24} |.")

        #keyboard.add_hotkey("Ctrl+k", lambda: handle_keypress("Ctrl+k"))
        #keyboard.on_press_key("Ctrl+k", callback)
        #hotkey = keyboard.read_hotkey(suppress=False)
        #print('hotkey:', hotkey)
        #keyboard.on_press_key("alt+k", callback)
        stopped = False
        #if keyboard.is_pressed("Ctrl-k"):
        #    continue
        #if hotkey == 'alt+k':
        #    alt_k()

        if config.PROXY_ENABLED:
            s = socks.socksocket()
            rnd_proxy = random.choice(config.PROXY_IPS).split(":")
            print(f"Подключение к Телеграмм с прокси {rnd_proxy}!")
            client = TelegramClient(phone, api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
            client.start()
            print(f'[+] Успешная аутентификация - {phone}')
            current_account_id = account_id
            accs_array.append(cp)
            invited = inv24
            #client.disconnect()

        else:
            print(f"Подключение к Телеграмм без прокси!")
            client = TelegramClient(phone, api_id, api_hash)
            invited = inv24
            client.disconnect()

        client.connect()
        if not client.is_user_authorized():
            banner()
            client.start()
            print(f'[+] Успешная аутентификация - {phone}')

            print(f'[+] Проверяем и входим в группу - {phone}')
            for dialog in client.iter_dialogs():
                if dialog.entity.megagroup:
                    group_name = dialog.entity.title
                    members_count = str(dialog.entity.participants_count)
                    print(f'GROUP: {group_name} - ({members_count} members)')
                    #username = client.get_entity(group_target)
                    if gurl == dialog.entity.username:
                        print(f'Нашли нашу группу: {group_name})')
                        client.disconnect()
                        if first_run == 1:
                            client.connect()
                        x += 1
                        accs_array.append(cp)
                        continue
            #в группе нас нет - вступаем
            furl = "t.me/" + gusername
            gentity = client.get_entity(furl)
            client(JoinChannelRequest(gentity))
            print(f'Вступили в группу: {gentity.title})')
            client.disconnect()
            if first_run == 1:
                client.connect()
            client.connect()
            x += 1
            accs_array.append(cp)
                #accs_array.append(cp)
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
    if acc_mode == 1:
        continue
    else:
        #os.system('clear')
        banner()
        print(f"Аккаунты в работе:")
        print(accs_array)

        #список пользователей для инвайта
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

        furl = "t.me/" + gusername
        target_group = client.get_entity(furl)
        if(target_group.title != ''): print("||| TARGET GROUP PRESENT")

        print("||||||||||")
        print(target_group.title)
        print("||||||||||")
        target_group_entity = client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
        #print(gr+"[1] добавлять в группу по username \n[2] добавлять в группу по user ID ")
        #mode = int(input(gr+"Введите свой выбор( 1/2 ) : "+re))
        mode = 1
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
                    print(f'Работает аккаeyнт: {account_id}')
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
                    if invited_cs >= 40 or invited >= 40:
                        cur_day = cur_time.day
                        cur_hour = cur_time.hour
                        print(cur_time.hour)
                        print(f"{cur_time} | Аккаунт {account_id} набрал {invited} инвайтов !")
                        print(f"{cur_time} | Аккаунт {account_id} уходит в режим ожидания до {cur_day + 1} числа и {cur_hour + 1} часов!")
                        print(f'Обновляем данные аккаунта{account_id}')
                        update_tgaccounts(account_id, pole="iter24")
                        print("|||||=> данные аккаунта обновлены")
                        client.disconnect()

                        cpass7 = get_all_tgaccounts_to_invite()
                        print(cpass7)
                        iter += 1
                        print(f'Итерация:{iter}')
                        for cp7 in cpass7:
                            print(cp7)
                            first_run += 1
                            #if len(cp7) == 1: continue
                            try:
                                if cp7[13] > 4 or cp7[0] == current_account_id: continue
                                account_id = cp7[0]
                                api_id = cp7[1]
                                api_hash = cp7[2]
                                phone = cp7[3]
                                inv24, send24, iter24  = cp7[8], cp7[9], cp7[13]
                                #update_tgaccounts(account_id, pole="reset")
                                print(f"Работаем с аккаунтом:{phone} | ЕГО время старта: И:{inv24} | C:{send24} | Итер:{iter24} |.")

                                if config.PROXY_ENABLED:
                                    s = socks.socksocket()
                                    rnd_proxy = random.choice(config.PROXY_IPS).split(":")
                                    print(f"Подключение к Телеграмм с прокси {rnd_proxy}!")
                                    client = TelegramClient(phone, api_id, api_hash, proxy=s.set_proxy(socks.HTTP, rnd_proxy[0], rnd_proxy[1]) )
                                    client.start()
                                    print(f'[+] Успешная аутентификация - {phone}')
                                    invited = inv24
                                    client.disconnect()

                                else:
                                    print(f"Подключение к Телеграмм без прокси!")
                                    client = TelegramClient(phone, api_id, api_hash)
                                    client.start()
                                    invited = inv24
                                    client.disconnect()

                                client.connect()
                                #пауза после переклбчения аккаунта
                                current_account_id = account_id
                                #определяем группу после смены аккаунта
                                furl = "t.me/" + gusername
                                target_group = client.get_entity(furl)

                                target_group_entity = client.get_entity(InputPeerChannel(target_group.id, target_group.access_hash))
                                if(target_group_entity.title != ''): print("||| TARGET GROUP PRESENT")

                                sleeps = random.randrange(10, 15)
                                print(gr+"[+] Пауза 10-15 секунд..."+ str(sleeps))
                                time.sleep(sleeps)
                                break

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
                                    continue

                        #пауза между авторизациями
                        sleeps = random.randrange(80, 120)
                        print(gr+"[+] Пауза 80-120 секунд..."+ str(sleeps))
                        time.sleep(sleeps)
                        continue

                    sleeps = random.randrange(30, 60)
                    client.get_entity(furl)
                    print(gr+"[+] Пауза 30-60 секунд..."+ str(sleeps))

                    #sleeps = random.randrange(80, 120)
                    #print(gr+"[+] Пауза 80-120 секунд..."+ str(sleeps))
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
                    if f >= 11:
                        update_tgaccounts(account_id, pole="waitfor24")
                        break
                        #print("||||")
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

