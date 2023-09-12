import pyrogram
from pyrogram import Client, idle, filters, types
from pyrogram.handlers import MessageHandler
from pyrogram.enums import ChatType
from time import sleep
from os import system
import sqlite3
from tgbot.services.api_sqlite_advert import *

ids = []
old_ids = []
my_apps = []
users = []
#numbers = []
settings = {'tg_api_id':'26779608', 'tg_api_hash':'b6c80c800cab2010db3901820732e58f', 'channel_to_invite':'-1001683374540','parse_channel_ids': '@goodnewsrussia1', 'delay_msg': 60, 'count_users_send': 20,"numbers": "+639674137467", "log": 1}

try:
    with open('settings_inv.ini', 'rt', encoding='UTF8') as (f):
        file = f.readlines()
        for line in file:
            if '\n' in line:
                line = line[:-1]
            line = line.split(' = ')
            settings[line[0]] = line[1]

except:
    with open('settings.ini', 'wt', encoding='UTF8') as (f):
        for key in settings:
            f.write(f"{key} = {settings[key]}\n")
        
        print(f'Fill in the settings.ini file!')
        system('pause')
        exit(-1)

#vars
#api_id = input(">Enter api_id: ").split(', ')
#api_hash = input(">Enter api_hash: ").split(', ')
#numbers = settings['phone']
api_id = settings['tg_api_id']
api_hash = settings['tg_api_hash']
#numbers[0][0] = "+63 967 413 7467"
#numbers[0][1] = "26779608"
#numbers[0][2] = "b6c80c800cab2010db3901820732e58f"
channel_to_invite = settings['channel_to_invite']
channel_id = settings['parse_channel_ids'].split(', ')
delay_msg = float(settings['delay_msg'])
numbers = settings['numbers'].split(', ')
log = int(settings['log'])
count_users_send = int(settings['count_users_send'])
#----TODO
numbers2 = get_all_tgaccounts_phones_to_invite()
print(numbers2)
#groups_list = first_groupsavtoinvite()

for i in range(0, len(numbers2)):
    my_apps.append(Client(f"pyr{i}"))
    print(numbers2[i])
    
    with Client(f"pyr{numbers2[i][0]}", int(numbers2[i][1]), numbers2[i][2]) as my_apps[i]:
    #with Client(f"app{numbers[i]}", int(api_id[i]), api_hash[i]) as my_apps[i]:
        pass

def log_txt(m):
    if log == 1:
        print(m)

def get_online_members():
    with Client(f"pyr{numbers[0]}", api_id[0], api_hash[0]) as my_apps[0]:
        app1 = my_apps[0]
        for k in channel_id:
            log_txt('получаем участников...')
            members = app1.get_chat_members(k)
            for member in members:
                ids.append(member.user.id)
                print(member.user.id)
    #for i, my_app in enumerate(my_apps):
    #    with Client(f"app{numbers[i]}", api_id[i], api_hash[i]) as my_apps[i]:
    #        my_app[i].get_chat_members(k)


def get_offline_members(groupid):
    ids = first_idsgrouptoinvitebyid(groupid, start, count)

def inviter(app):
    old_s = ''
    s = ''
    count = 0
    for g in old_ids:
        try:
            ids.remove(g)
        except:
            pass
    while True:
        for dialog in app.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                for v in ids:
                    s = v
                    del ids[:1]

                    if old_s != s:
                        if count != count_users_send:
                            try:
                                app.add_chat_members(channel_to_invite, s)
                                count += 1
                            except pyrogram.errors.exceptions.forbidden_403.UserPrivacyRestricted:
                                print(f'У пользователя: {s} ограничение! Продолжаем!')
                            except pyrogram.errors.exceptions.bad_request_400.PeerFlood:
                                print('У этого аккаунта лимит!')
                                break
                        else:
                            print(f'Пользователи подошли к концу: {count_users_send}')
                            count = 0
                            break
                    else:
                        print('Все сделано!')
                        break

                    old_s = s

                    log_txt(f"left: {len(ids)}")
                    log_txt(f"user_send: {s}")
                    sleep(delay_msg)
                else:
                    continue
                break


if __name__ == "__main__":
    get_online_members()
    for i in range(0, len(my_apps)):
        print(f'Аккаунтов всего: {len(my_apps)}')
        with Client(f"pyr{numbers[i]}", int(api_id[i]), api_hash[i]) as my_apps[i]:
            inviter(my_apps[i])