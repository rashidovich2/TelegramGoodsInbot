#!/usr/bin/env python3
from telethon.sync import TelegramClient, connection
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random
import requests, socket
from tgbot.services.api_sqlite import *


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

    #читаем список пользователей для инвайта
    os.system('clear')
    banner()
    input_file = sys.argv[1]
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {
                'id': row[0],
                'access_hash': row[1],
                'name': row[2],
                'username': row[4],
            }
            #user['id'] = 5518497581
            if user['username'] is None: continue

            users.append(user)

    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    #получение чатов пользователя
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
        print(f'{gr}[{cy}{str(i)}{gr}]{cy} - {group.title}')
    print(f'{gr}[+] Choose a group to add members')
    g_index = input(f"{gr}[+] Enter a Number : {re}")
    target_group=groups[int(g_index)]
    #target_group.id = -1001683374540
    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    print(gr+"[1] add member by user ID\n[2] add member by username ")
    mode = int(input(f"{gr}Input : {re}"))
    n = 0
    l = 0
    print(users)
    print('before for')
    for user in users:
        n += 1
        time.sleep(1)
        try:
            print(n, f"Adding {user['id']}")
            if mode == 1:
                if user['username'] in ["", "None"]:
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit(f"{re}[!] Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print(f"{gr}[+] Waiting for 10-30 Seconds...")
            #n += 1
            #if n == 40:
            #sys.exit(re+"[!] 40 пользователей приглашено.")
            time.sleep(random.randrange(10, 30))
        except PeerFloodError:
            print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
        except UserPrivacyRestrictedError:
            print(
                f"{re}[!] The user's privacy settings do not allow you to do this. Skipping."
            )
        except Exception:
            traceback.print_exc()
            print(f"{re}[!] Unexpected Error")
            continue

