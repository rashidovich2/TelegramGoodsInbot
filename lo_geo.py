#!/usr/bin/env python3
import os, sys
import csv
import traceback
import glob
from tgbot.services.api_sqlite import *

woman_names = ("Агафья",
               "Аглая",
               "Агния",
               "Агриппина",
               "Аза",
               "Акулина",
               "Алевтина",
               "Александра",
               "Алина",
               "Алла",
               "Анастасия",
               "Ангелина",
               "Анжела",
               "Анжелика",
               "Анна",
               "Антонина",
               "Анфиса",
               "Валентина",
               "Валерия",
               "Варвара",
               "Василиса",
               "Вера",
               "Вероника",
               "Виктория",
               "Галина",
               "Глафира",
               "Гликерия",
               "Дана",
               "Дарья",
               "Евгения",
               "Евдокия",
               "Евлалия",
               "Евлампия",
               "Евпраксия",
               "Евфросиния",
               "Екатерина",
               "Елена",
               "Елизавета",
               "Епистима",
               "Ермиония",
               "Жанна",
               "Зинаида",
               "Злата",
               "Зоя",
               "Инга",
               "Инесса",
               "Инна",
               "Иоанна",
               "Ираида",
               "Ирина",
               "Ия",
               "Капитолина",
               "Карина",
               "Каролина",
               "Кира",
               "Клавдия",
               "Ксения",
               "Лада",
               "Лариса",
               "Лидия",
               "Лилия",
               "Любовь",
               "Людмила",
               "Маргарита",
               "Марина",
               "Мария",
               "Марфа",
               "Матрёна",
               "Милица",
               "Мирослава",
               "Надежда",
               "Наталья",
               "Нина",
               "Нонна",
               "Оксана",
               "Октябрина",
               "Олимпиада",
               "Ольга",
               "Павлина",
               "Пелагея",
               "Пинна",
               "Полина",
               "Прасковья",
               "Рада",
               "Раиса",
               "Регина",
               "Римма",
               "Рогнеда",
               "Руслана",
               "Светлана",
               "Серафима",
               "Снежана",
               "София",
               "Таисия",
               "Тамара",
               "Татьяна",
               "Улита",
               "Ульяна",
               "Урсула",
               "Фаина",
               "Феврония",
               "Фёкла",
               "Феодора",
               "Целестина",
               "Юлия",
               "Яна",
               "Ярослава")

print(woman_names)

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

print("TEST")
#читаем список пользователей для инвайта
#os.system('clear')
banner()
#input_file = sys.argv[1]
users = []
path = "/var/local/bot3101f/only_geo*.csv"
print(path)

for file in glob.glob(path):
    with open(file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        #print(len(rows))

        for row in rows:
            if row[4] is None: continue
            if row[4] == "": continue
            if row[4] == "username": continue
            if row[4] == "None": continue
            if check_dbfor_username(row[4]):
                print(row[4]+" есть в БД.\n")
                continue
            #print(row)
            user = {
                'id': row[0],
                'access_hash': row[1],
                'name': f"{row[2]} {row[3]}",
                'username': row[4],
                'source': 'geoparse',
            }
            try:
                username = user['username']
                if check_dbfor_username(row[4]): continue
                usid = user['id']
                usah = user['access_hash']
                name = user['name']
                source = "geoparse"
                state = "created"
                groupname = "REG_PENZA"
                groupid = 70077
                tag = "GEO_PNZ"
                #print(username)
                if row[2] in woman_names: print(row[2])
                add_tgacc_todb(username,usid,usah,name,source,groupname,groupid,tag,state)

            except Exception:
                traceback.print_exc()
                print(f"{re}[!] Неизвестная ошибка")
                continue

            users.append(user)
    #sleep(30)
    print(f"Загружено:{len(users)} пользователей.")