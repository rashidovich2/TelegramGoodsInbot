# - *- coding: utf- 8 - *-
import math
import random
import sqlite3

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, get_date, clear_html

# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())



# Получение всех магазинов
def get_all_shopx():
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select shop_id, name, description, address, phone, admin, logo, city, geocode, city_id from storage_shop'''
    result = cur.execute(query).fetchall()
    cur.close()
    return result

# Получение одного магазина
def get_the_shop(shop_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select shop_id, name, description, address, phone, admin, logo, city, geocode, city_id from storage_shop where shop_id = &'''
    result = cur.execute(query, (shop_id,)).fetchall()
    cur.close()
    return result


# Добавление магазина
def add_shopx(name, description, adreess, phone, admin, logo, city, geocode, city_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_shop (shop_id, name, description, address, phone, admin, logo, city, geocode, city_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [random.randint(1000000000, 9999999999), name, description, adreess, phone, admin, logo, city, geocode, city_id])
        con.commit()


# Изменение магазина
def update_shopx(category_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_shop SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(category_id)
        con.execute(f"{sql}WHERE shop_id = ?", parameters)
        con.commit()

# Получение категории
def get_shopx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_shop"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Получение категорий
def get_positionsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()
