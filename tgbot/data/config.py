# - *- coding: utf- 8 - *-
import os
import sqlite3
import configparser
import json
#from pathlib import Path
from babel import Locale
from pathlib import Path

read_config = configparser.ConfigParser()
read_config.read('settings.ini')

BOT_TOKEN = read_config['settings']['token'].strip()  # Токен бота
PATH_DATABASE = 'tgbot/data/database.db'  # Путь к БД
PATH_LOGS = 'tgbot/data/logs.log'  # Путь к Логам
BOT_VERSION = '1.0'
I18N_DOMAIN = 'mybot'
DEFAULT_LANGUAGE = read_config['settings']['default_language'].strip()
rd = Path(__file__).parents
BASE_DIR = rd[1]
LOCALES_DIR = str(f"{BASE_DIR}{os.sep}locales")
print(LOCALES_DIR)
locale = Locale('ru', 'RU')

#_ = i18n.gettext

# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())

def get_type_trade():
    return get_settingsx()['type_trade']

# Получение администраторов бота
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read('settings.ini')

    admins = read_admins['settings']['admin_id'].strip()
    admins = admins.replace(' ', '')

    if ',' in admins:
        admins = admins.split(',')
    else:
        admins = [admins] if len(admins) >= 1 else []
    while '' in admins: admins.remove('')
    while ' ' in admins: admins.remove(' ')
    while '\r' in admins: admins.remove('\r')

    admins = list(map(int, admins))
    #print(admins)
    return admins


    # Получение админов магазинов
def get_shopadmins():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_id FROM storage_users WHERE user_role='ShopAdmin'"
        allshopadmins = con.execute(sql).fetchall()
        shopadmins = [admin['user_id'] for admin in allshopadmins]
    return shopadmins


def get_shopadmins2():
    read_shopadmins = configparser.ConfigParser()
    read_shopadmins.read('settings.ini')

    shopadmins = read_shopadmins['settings']['shopadmin_id'].strip()
    shopadmins = shopadmins.replace(' ', '')

    if ',' in shopadmins:
        shopadmins = shopadmins.split(',')
    else:
        shopadmins = [shopadmins] if len(shopadmins) >= 1 else []
    while '' in shopadmins: shopadmins.remove('')
    while ' ' in shopadmins: shopadmins.remove(' ')
    while '\r' in shopadmins: shopadmins.remove('\r')

    shopadmins = list(map(int, shopadmins))

    return shopadmins

    # Получение админов магазинов
def is_shopadmin(user_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT user_id FROM storage_users "
        #sql, parameters = update_format(sql, kwargs)
        #parameters.append(user_id)
        shopadmin = con.execute(f"{sql}WHERE user_id = ?", [user_id]).fetchone()

    return shopadmin['user_id']


def check_adminproducts():
    #get_position = get_positionsx(position_user_id=message.from_user.id)

    return 1


BOT_DESCRIPTION = f'<b>⚜ Bot Version: <code>{BOT_VERSION}</code>\n' \
                  f'🔗 Topic Link: <a href="https://github.com/rashidovich2/TGGoodsinbot">Click me</a>\n' \
                  f'♻ Bot created by @raclear\n' \
                  f'🍩 Donate to the author: <a href="https://qiwi.com/n/raclear">Click me</a>\n' \
                  f'🤖 Bot channel [NEWS | UPDATES]: <a href="https://t.me/raclear">Click me</a></b>'
