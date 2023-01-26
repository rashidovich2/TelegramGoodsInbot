#!/usr/bin/env python3
#from telethon.sync import TelegramClient, connection
#from telethon.tl.functions.messages import GetDialogsRequest
#from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
#from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
#from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random
import requests, socket
from tgbot.services.api_sqlite import *

woman_names = ['Агафья',
               'Аглая',
               'Агния',
               'Агриппина',
               'Аза',
               'Акулина',
               'Алевтина',
               'Александра',
               'Алина',
               'Алла',
               'Анастасия',
               'Ангелина',
               'Анжела',
               'Анжелика',
               'Анна',
               'Антонина',
               'Анфиса',
               'Валентина',
               'Валерия',
               'Варвара',
               'Василиса',
               'Вера',
               'Вероника',
               'Виктория',
               'Галина',
               'Глафира',
               'Гликерия',
               'Дана',
               'Дарья',
               'Евгения',
               'Евдокия',
               'Евлалия',
               'Евлампия',
               'Евпраксия',
               'Евфросиния',
               'Екатерина',
               'Елена',
               'Елизавета',
               'Епистима',
               'Ермиония',
               'Жанна',
               'Зинаида',
               'Злата',
               'Зоя',
               'Инга',
               'Инесса',
               'Инна',
               'Иоанна',
               'Ираида',
               'Ирина',
               'Ия',
               'Капитолина',
               'Карина',
               'Каролина',
               'Кира',
               'Клавдия',
               'Ксения',
               'Лада',
               'Лариса',
               'Лидия',
               'Лилия',
               'Любовь',
               'Людмила',
               'Маргарита',
               'Марина',
               'Мария',
               'Марфа',
               'Матрёна',
               'Милица',
               'Мирослава',
               'Надежда',
               'Наталья',
               'Нина',
               'Нонна',
               'Оксана',
               'Октябрина',
               'Олимпиада',
               'Ольга',
               'Павлина',
               'Пелагея',
               'Пинна',
               'Полина',
               'Прасковья',
               'Рада',
               'Раиса',
               'Регина',
               'Римма',
               'Рогнеда',
               'Руслана',
               'Светлана',
               'Серафима',
               'Снежана',
               'София',
               'Таисия',
               'Тамара',
               'Татьяна',
               'Улита',
               'Ульяна',
               'Урсула',
               'Фаина',
               'Феврония',
               'Фёкла',
               'Феодора',
               'Целестина',
               'Юлия',
               'Яна',
               'Ярослава']
#print(woman_names)

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
        #print(len(rows))

        for row in rows:
            user = {}
            #user['id'] = int(row[0])
            user['id'] = row[0]
            user['access_hash'] = row[1]
            #user['access_hash'] = int(row[1])
            user['name'] = row[2] + " " + row[3]
            user['username'] = row[4]
            user['source'] = 'geoparse'

            try:
                username = user['username']
                usid = user['id']
                usah = user['access_hash']
                name = user['name']
                source = "geoparse"
                state = ""
                #print(username)
                #(row[2])
                #if row[2] in woman_names: print(row[2])
                #add_tgacc_todb(username,usid,usah,name,source,state)

            except:
                traceback.print_exc()
                print(re+"[!] Unexpected Error")
                continue

            users.append(user)

    print(f"Загружено:{len(users)} пользователей.")