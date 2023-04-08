import requests
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle, pyfiglet
from colorama import init, Fore
import os, random
import subprocess
from time import sleep, time
#from tgbot.services.api_sqlite import *
from tgbot.services.api_sqlite_advert import *
import configparser

init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]

def banner():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('TelegramRa')
    print(f'{random.choice(colors)}{banner}{n}')
    print(f'{r}  Версия: 1.0 |  Автор: Rashidovich{n}' + '\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clr()
    banner()
    print(f'{r}[] Аккаунты{n}')
    print(f'{cy}[1] Добавить новые аккаунты{n}')
    print(f'{cy}[2] Удалить все аккаунты в бане{n}')
    print(f'{cy}[3] Показать список всех аккаунтов{n}')
    print(f'{cy}[4] Удалить конкретный аккаунт{n}')
    print(f'{cy}[5] Перевести аккаунты из Создан в Доступен{n}')
    print(f'{cy}[6] Перевести аккаунт из Ожидает в Доступен{n}')
    print(f'{cy}[7] Перевести аккаунт в Ожидает{n}')
    print(f'{cy}[8] Перевести аккаунт в Забанен{n}')
    print(f'{r}[] Парсинг и загрузка в БД{n}')
    print(f'{cy}[9] Загрузить контакты из гео в БД{n}')
    print(f'{cy}[10] Cпарсить группу и загрузить контакты в БД{n}')
    print(f'{cy}[11] Статистика БД аккаунтов{n}')
    print(f'{r}[] Инвайт участников из БД{n}')
    print(f'{cy}[12] Инвайт из групп в группу{n}')
    print(f'{cy}[13] Инвайт по гео в группу{n}')
    print(f'{r}[] Рассылка сообщений{n}')
    print(f'{cy}[14] Рассылка сообщений{n}')
    #print(lg+'[5] Update your Genisys'+n)
    print(f'{r}[] Прогрев аккаунтов 20 минут{n}')
    print(f'{cy}[15] Прогрев акаунтов{n}')
    print(f'{cy}[99] Настройки')
    print(f'{cy}[16] Выход')
    a = int(input(f'\nВведите номер пункта и нажмите Enter: {r}'))
    if a == 1:
        g = get_all_tgaccounts()
        registered = []
        while True:
            a = int(input(f'\n{lg}Введите API ID: {r}'))
            b = str(input(f'{lg}Введите API Hash: {r}'))
            c = str(input(f'{lg}Введите номер телефона: {r}'))
            p = ''.join(c.split())
            #pickle.dump([a, b, p], g)
            add_account_todb(a, b, p, 0,'created')
            nacc=get_lasttgaccount()
            print(nacc)
            registered.append([nacc, a, b, p])
            ab = input(f'\nХотите ли добавить еще аккаунты?[y/n]: ')
            if 'y' not in ab:
                print('\n'+lg+'[i] Все аккаунты сохранены в базе данных'+n)
                sleep(3)
                clr()
                print(lg + '[*] Аутентификация новых аккаунтов...\n')
                for added in registered:
                    c = TelegramClient(f'{added[3]}', added[1], added[2])
                    try:
                        c.start()
                        print(f'n\n{lg}[+] Успешная аутентификация - {added[3]}')
                        c.disconnect()
                        update_tgaccounts(nacc, pole='available')
                    except PhoneNumberBannedError:
                        print(f'{r}[!] {added[2]} в бане! Удалите его, используя опцию 2')
                        continue
                    print('\n')
                input(f'\n{lg}Нажмите enter чтобы вернуться в главное меню...')
                break

    elif a == 2:
        accounts = []
        banned_accs = []
        accounts = get_all_tgaccounts_time()
        if len(accounts) == 0:
            print(f'{r}[!] У Вас нет аккаунтов! Пожалуйста добавьте и повторите еще раз')
            sleep(3)
        else:
            for account in accounts:
                acc_id = int(account[0])
                api_id = int(account[1])
                api_hash = str(account[2])
                phone = str(account[3])
                client = TelegramClient(f'{phone}', api_id, api_hash)
                client.connect()
                print(f'{r}[!] Аккаунт {phone}:')
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        client.sign_in(phone, input('[+] Введите код: '))
                    except PhoneNumberBannedError:
                        print(r + phone + ' в бане!' + n)
                        remove_accountx(account_id=acc_id)
                        banned_accs.append(account)
            if not banned_accs:
                print(f'{lg}Поздравляем! Нет аккаунтов в бане')
            else:
                for _ in banned_accs:
                    remove_accountx(state='banned')
                print(f'{lg}[i] Все аккаунты из бана удалены{n}')
            input('\nНажмите enter чтобы вернуться в главное меню')
    elif a == 3:
        display = []
        j = get_all_tgaccounts_time()
        #while True:
        #    try:
        #        display.append(pickle.load(j))
        #    except EOFError:
        #        break
        #j.close()
        print(f'\n{cy}')
        print(
            ' #     |   API ID  |     Номер телефона  |    Статус   |    Приглашено24  |  Время старта'
        )
        print(
            '================================================================================================================'
        )
        for z in j:
            print(f'{z[0]} | {z[1]} | {z[3]}  | {z[4]} | {z[7]}  | {z[8]}')
        print(
            '========================================================================='
        )
        input('\nНажмите enter чтобы вернуться в главное меню')

    elif a == 4:
        f = get_all_tgaccounts()
        accs = list(f)
        print(f'{lg}[i] Выберите аккаунт для удаления\n')
        for i, acc in enumerate(f):
            print(f'{lg}[{i}] {acc[3]} {acc[4]} {n}')
        index = int(input(f'\n{lg}[+] Введите выбор: {n}'))
        acc_to_del = int(accs[index][0])
        phone = accs[index][3]
        session_file = f'{phone}.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        dacc = delete_tgacc(accs[index][0])
        #del accs[index]
        f = get_all_tgaccounts()
        for account in f:
            #print("||||DEL|||")
            print(f'{cy}[{account[0]}] {account[3]} {account[4]} {n}')
            #pickle.dump(account, f)
        print(f'\n{n}[+] Аккаунт удален{n}')
        input(f'{lg}Нажмите enter чтобы вернуться в главное меню{n}')
                #f.close()
    elif a == 5:
        display = []
        j = get_all_tgaccounts_time()
        i = 0
        for indacc in j:
            if(indacc[4]=='created'):
                update_tgaccounts(indacc[0], pole='available')
                print(f'{cy}[{indacc[0]}] {indacc[3]} {indacc[4]} {i}')
                i += 1
        print('=====================================================')
    elif a == 6:
        f = get_all_tgaccounts_time()
        accs = list(f)
        print(f'{lg}[i] Выберите аккаунт для перевода в available\n')
        for i, acc in enumerate(f):
            print(f'{lg}[{i}] {acc[3]} {acc[4]} {n}')
        index = int(input(f'\n{lg}[+] Введите выбор: {n}'))
        acc_to_change = int(accs[index][0])
        phone = accs[index][3]
        #session_file = phone + '.session'
        #if os.name == 'nt':
        #    os.system(f'del sessions\\{session_file}')
        #else:
        #    os.system(f'rm sessions/{session_file}')
        #dacc = delete_tgacc(accs[index][0])
        update_tgaccounts(accs[index][0], pole='available')
        #del accs[index]
        f = get_all_tgaccounts()
        for account in f:
            #print("||||DEL|||")
            print(f'{cy}[{account[0]}] {account[3]} {account[4]} {n}')
            #pickle.dump(account, f)
        print(f'\n{n}[+] Статус аккаунта изменен {n}')
        input(f'{lg}Нажмите enter чтобы вернуться в главное меню{n}')
            #f.close()
    elif a == 7:
        f = get_all_tgaccounts_time()
        accs = list(f)
        i = 0
        print(f'{lg}[i] Выберите аккаунт для перевода в Ожидание\n')
        for acc in f:
            print(f'{lg}[{i}] {acc[3]} {acc[4]} {n}')
            i += 1
        index = int(input(f'\n{lg}[+] Введите выбор: {n}'))
        acc_to_change = int(accs[index][0])
        phone = accs[index][3]
        update_tgaccounts(accs[index][0], pole='banned')
        f = get_all_tgaccounts()
        for account in f:
            print(f'{cy}[{account[0]}] {account[3]} {account[4]} {n}')
        print(f'\n{n}[+] Статус аккаунта изменен {n}')
        input(f'{lg}Нажмите enter чтобы вернуться в главное меню{n}')

    elif a == 8:
        accs = []
        f = get_all_tgaccounts_time()
        for indacc in f:
            accs.append(indacc)
        i = 0
        print(f'{lg}[i] Выберите аккаунт для перевода в Забанен\n')
        for acc in f:
            print(f'{lg}[{i}] {acc[3]} {acc[4]} {n}')
            i += 1
        index = int(input(f'\n{lg}[+] Введите выбор: {n}'))
        acc_to_change = int(accs[index][0])
        phone = accs[index][3]
        update_tgaccounts(accs[index][0], pole='banned')
        f = get_all_tgaccounts()
        for account in f:
            print(f'{cy}[{account[0]}] {account[3]} {account[4]} {n}')
        print(f'\n{n}[+] Статус аккаунта изменен {n}')
        input(f'{lg}Нажмите enter чтобы вернуться в главное меню{n}')
    elif a == 9:
        subprocess.run(["python3", "lo_geo.py"])
        sleep(1.5)

    elif a == 10:
        subprocess.run(["python3", "lo_groups.py"])
        sleep(1.5)

    elif a == 11:
        display = []
        j = get_all_tgaccounts_states()
        print(f'\n{cy}')
        print('Источник |   Группа  |   ID   | Статус  |  Количество  | ')
        print(
            '============================================================================================================='
        )
        for z in j:
            print(f'{z[0]} | {z[1]}  | {z[2]} | {z[3]} |  {z[4]} |')
        print('======================================================================')
        input('\nНажмите enter чтобы вернуться в главное меню')

    elif a == 12:
        subprocess.run(["python3", "invite_sql.py", "group", "no"])
        sleep(1.5)

    elif a == 13:
        subprocess.run(["python3", "invite_sql.py", "geoparse"])
        sleep(1.5)

    elif a == 14:
        subprocess.run(["python3", "sendmessages.py", "group"])
        sleep(1.5)

    elif a == 99:
        read_config = configparser.ConfigParser()
        read_config.read('settings.ini')
        TARGET_GROUP_USERNAME = read_config['settings']['TGU'].strip()
        str(input(f'\n{lg}[+] Введите имя пользователя группы: {TARGET_GROUP_USERNAME}{n}'))
        subprocess.run(["python3", "sendmessages.py", "group"])
        sleep(1.5)

    elif a == 17:
        accs_to_join = ['https://t.me/sportsru', ]
        accs = []
        f = get_all_tgaccounts()
        for indacc in f:
            accs.append(indacc)
        #f.close()
        i = 0
        print(f'{lg}[i] Выберите аккаунт для прогрева или all для created\n')
        for acc in f:
            print(f'{lg}[{i}] {acc[3]} {acc[4]} {n}')
            i += 1
        index = int(input(f'\n{lg}[+] Введите выбор: {n}'))
        if index == "all":
            f = get_all_createdaccounts()
        for acc in f:
        #добавляем пользователей и пишем им
        #вступаем в группы и задаем вопрос
        #делаем паузу
            acc_to_change = int(accs[index][0])
            phone = accs[index][3]
            remove_accountx(account_id=acc_id)
            update_tgaccounts(accs[index][0], pole='available')
            f = get_all_tgaccounts()
        for account in f:
            print(f'{cy}[{account[0]}] {account[3]} {account[4]} {n}')
        print(f'\n{n}[+] Статус аккаунта изменен {n}')
        input(f'{lg}Нажмите enter чтобы вернуться в главное меню{n}')


    elif a == 16:
        clr()
        banner()
        quit()