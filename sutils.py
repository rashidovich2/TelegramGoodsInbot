#!/usr/bin/env python3
from tgbot.services.api_sqlite_advert import *
import datetime
import time

def get_time_str():
    return datetime.now().strftime("%H:%M:%S")

cur_time = datetime.datetime.now()

#выбираем аккаунты - available и wait по времени
#выбираем список для инвайта - по группе или по гео
#выбираем группу для инвайта, вводим группу для инвайта
#инвайтим - ставим отметки аккаунтам

def check_phones(reset="no"):
    all_accs=get_all_tgaccounts()
    for acc in all_accs:
        print(str(acc[0])+str(acc[4])+str(acc[8])+str(acc[9]))
        if acc[8] is None or str(acc[4]) not in ["banned", "wait2", "wait3"]: #acc[8] is None or
            update_tgaccounts(acc[0], pole='available')
        #if reset == "yes":
        #    update_tgaccounts(acc[0], pole="reset")

        if acc[4] == 'wait' and acc[8] is not None:
            dtwait = datetime.datetime.strptime(acc[10], '%Y-%m-%d %H:%M:%S')
            utime = time.mktime(cur_time.timetuple())
            print(utime)
            udtwait = time.mktime(dtwait.timetuple())
            print(udtwait)
            #Проверить если номеру пора уходить из режима ожидания
            if (utime >= udtwait and str(acc[4]) != "wait2" and str(acc[4]) != "banned" and str(acc[4]) != "wait3"):
                update_tgaccounts(acc[0], pole='available')
                print(f"{str(dtwait.hour)}:{str(dtwait.minute)}")

    return acc[0]
