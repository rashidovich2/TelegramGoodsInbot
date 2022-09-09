# - *- coding: utf- 8 - *-
import math
import random
import sqlite3

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, get_date, clear_html


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


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


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя
def add_userx(user_id, user_login, user_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_users "
                    "(user_id, user_login, user_name, user_balance, user_refill, user_date, user_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, 0, 0, get_date(), get_unix()])
        con.commit()


# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        return con.execute(sql).fetchall()


# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()


# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Получение платежных систем
def get_paymentx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_payment"
        return con.execute(sql).fetchone()


# Редактирование платежных систем
def update_paymentx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_payment SET"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Получение настроек
def get_settingsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_settings"
        return con.execute(sql).fetchone()


# Редактирование настроек
def update_settingsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "UPDATE storage_settings SET"
        sql, parameters = update_format(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление пополнения
def add_refillx(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt,
                refill_way, refill_date, refill_unix):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_refill "
                    "(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way, refill_date, refill_unix) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way,
                     refill_date, refill_unix])
        con.commit()


# Получение пополнения
def get_refillx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение пополнений
def get_refillsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_refill"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пополнений
def get_all_refillx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_refill"
        return con.execute(sql).fetchall()


# Добавление категории
def add_categoryx(category_id, category_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_category (category_id, category_name) VALUES (?, ?)",
                    [category_id, category_name])
        con.commit()


# Изменение категории
def update_categoryx(category_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_category SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(category_id)
        con.execute(sql + "WHERE category_id = ?", parameters)
        con.commit()


# Получение категории
def get_categoryx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение категорий
def get_categoriesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех категорий
def get_all_categoriesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_category"
        return con.execute(sql).fetchall()


# Удаление всех категорий
def clear_categoryx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_category"
        con.execute(sql)
        con.commit()


# Удаление категории
def remove_categoryx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_category"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление категории
def add_positionx(position_id, position_name, position_price, position_description, position_photo, category_id):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_position "
                    "(position_id, position_name, position_price, position_description, position_photo, position_date, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [position_id, position_name, position_price, position_description,
                     position_photo, get_date(), category_id])
        con.commit()


# Изменение позиции
def update_positionx(position_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_position SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(position_id)
        con.execute(sql + "WHERE position_id = ?", parameters)
        con.commit()


# Получение категории
def get_positionx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение категорий
def get_positionsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех категорий
def get_all_positionsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_position"
        return con.execute(sql).fetchall()


# Удаление всех позиций
def clear_positionx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position"
        con.execute(sql)
        con.commit()


# Удаление позиции
def remove_positionx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_position"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Добавление товара
def add_itemx(category_id, position_id, get_all_items, user_id, user_name):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        for item_data in get_all_items:
            if not item_data.isspace() and item_data != "":
                con.execute("INSERT INTO storage_item "
                            "(item_id, item_data, position_id, category_id, creator_id, creator_name, add_date) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            [random.randint(1000000000, 9999999999), clear_html(item_data.strip()), position_id,
                             category_id,
                             user_id, user_name, get_date()])
        con.commit()


# Изменение товара
def update_itemx(item_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_item SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(item_id)
        con.execute(sql + "WHERE item_id = ?", parameters)
        con.commit()


# Получение товара
def get_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение товаров
def get_itemsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех товаров
def get_all_itemsx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_item"
        return con.execute(sql).fetchall()


# Очистка товаров
def clear_itemx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_item"
        con.execute(sql)
        con.commit()


# Удаление товаров
def remove_itemx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM storage_item"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()


# Покупка товаров
def buy_itemx(get_items, get_count):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        split_len, send_count, save_items = 0, 0, []

        for select_send_item in get_items:
            if send_count != get_count:
                send_count += 1
                if get_count >= 2:
                    select_data = f"{send_count}. {select_send_item['item_data']}"
                else:
                    select_data = select_send_item['item_data']

                save_items.append(select_data)
                sql, parameters = update_format_args("DELETE FROM storage_item",
                                                     {"item_id": select_send_item['item_id']})
                con.execute(sql, parameters)

                if len(select_data) >= split_len: split_len = len(select_data)
            else:
                break
        con.commit()

        split_len += 1
        get_len = math.ceil(3500 / split_len)

    return save_items, send_count, get_len


# Добавление покупки
def add_purchasex(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price, purchase_price_one,
                  purchase_position_id, purchase_position_name, purchase_item, purchase_date, purchase_unix,
                  balance_before, balance_after):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_purchases "
                    "(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price, purchase_price_one, purchase_position_id, "
                    "purchase_position_name, purchase_item, purchase_date, purchase_unix, balance_before, balance_after) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price,
                     purchase_price_one, purchase_position_id, purchase_position_name, purchase_item, purchase_date,
                     purchase_unix, balance_before, balance_after])
        con.commit()


# Получение покупки
def get_purchasex(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_purchases"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


# Получение покупок
def get_purchasesx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_purchases"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех покупок
def get_all_purchasesx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_purchases"
        return con.execute(sql).fetchall()


# Последние 10 покупок
def last_purchasesx(user_id, count):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"SELECT * FROM storage_purchases WHERE user_id = ? ORDER BY increment DESC LIMIT {count}"
        return con.execute(sql, [user_id]).fetchall()


# Создание всех таблиц для БД
def create_dbx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        # Создание БД с хранением данных пользователей
        if len(con.execute("PRAGMA table_info(storage_users)").fetchall()) == 8:
            print("DB was found(1/8)")
        else:
            con.execute("CREATE TABLE storage_users("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "user_balance INTEGER,"
                        "user_refill INTEGER,"
                        "user_date TIMESTAMP,"
                        "user_unix INTEGER)")
            print("DB was not found(1/8) | Creating...")

        # Создание БД с хранением данных платежных систем
        if len(con.execute("PRAGMA table_info(storage_payment)").fetchall()) == 7:
            print("DB was found(2/8)")
        else:
            con.execute("CREATE TABLE storage_payment("
                        "qiwi_login TEXT,"
                        "qiwi_token TEXT,"
                        "qiwi_secret TEXT,"
                        "qiwi_nickname TEXT,"
                        "way_form TEXT,"
                        "way_number TEXT,"
                        "way_nickname TEXT)")

            con.execute("INSERT INTO storage_payment("
                        "qiwi_login, qiwi_token, qiwi_secret, qiwi_nickname, way_form, way_number, way_nickname) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        ['None', 'None', 'None', 'None', 'False', 'False', 'False'])
            print("DB was not found(2/8) | Creating...")

        # Создание БД с хранением настроек
        if len(con.execute("PRAGMA table_info(storage_settings)").fetchall()) == 9:
            print("DB was found(3/8)")
        else:
            con.execute("CREATE TABLE storage_settings("
                        "status_work TEXT,"
                        "status_refill TEXT,"
                        "status_buy TEXT,"
                        "misc_faq TEXT,"
                        "misc_support TEXT,"
                        "misc_bot TEXT,"
                        "misc_update TEXT,"
                        "misc_profit_day INTEGER,"
                        "misc_profit_week INTEGER)")

            con.execute("INSERT INTO storage_settings("
                        "status_work, status_refill, status_buy, misc_faq, misc_support,"
                        "misc_bot, misc_update, misc_profit_day, misc_profit_week)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ["True", "False", "False", "None", "None", "None", "False", get_unix(), get_unix()])
            print("DB was not found(3/8) | Creating...")

        # Создание БД с хранением пополнений пользователей
        if len(con.execute("PRAGMA table_info(storage_refill)").fetchall()) == 10:
            print("DB was found(4/8)")
        else:
            con.execute("CREATE TABLE storage_refill("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "refill_comment TEXT,"
                        "refill_amount INTEGER,"
                        "refill_receipt TEXT,"
                        "refill_way TEXT,"
                        "refill_date TIMESTAMP,"
                        "refill_unix INTEGER)")
            print("DB was not found(4/8) | Creating...")

        # Создание БД с хранением категорий
        if len(con.execute("PRAGMA table_info(storage_category)").fetchall()) == 3:
            print("DB was found(5/8)")
        else:
            con.execute("CREATE TABLE storage_category("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "category_id INTEGER,"
                        "category_name TEXT)")
            print("DB was not found(5/8) | Creating...")

        # Создание БД с хранением позиций
        if len(con.execute("PRAGMA table_info(storage_position)").fetchall()) == 8:
            print("DB was found(6/8)")
        else:
            con.execute("CREATE TABLE storage_position("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "position_id INTEGER,"
                        "position_name TEXT,"
                        "position_price INTEGER,"
                        "position_description TEXT,"
                        "position_photo TEXT,"
                        "position_date TIMESTAMP,"
                        "category_id INTEGER)")
            print("DB was not found(6/8) | Creating...")

        # Создание БД с хранением товаров
        if len(con.execute("PRAGMA table_info(storage_item)").fetchall()) == 8:
            print("DB was found(7/8)")
        else:
            con.execute("CREATE TABLE storage_item("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "item_id INTEGER,"
                        "item_data TEXT,"
                        "position_id INTEGER,"
                        "category_id INTEGER,"
                        "creator_id INTEGER,"
                        "creator_name TEXT,"
                        "add_date TIMESTAMP)")
            print("DB was not found(7/8) | Creating...")

        # # Создание БД с хранением покупок
        if len(con.execute("PRAGMA table_info(storage_purchases)").fetchall()) == 15:
            print("DB was found(8/8)")
        else:
            con.execute("CREATE TABLE storage_purchases("
                        "increment INTEGER PRIMARY KEY AUTOINCREMENT,"
                        "user_id INTEGER,"
                        "user_login TEXT,"
                        "user_name TEXT,"
                        "purchase_receipt TEXT,"
                        "purchase_count INTEGER,"
                        "purchase_price INTEGER,"
                        "purchase_price_one INTEGER,"
                        "purchase_position_id INTEGER,"
                        "purchase_position_name TEXT,"
                        "purchase_item TEXT,"
                        "purchase_date TIMESTAMP,"
                        "purchase_unix INTEGER,"
                        "balance_before INTEGER,"
                        "balance_after INTEGER)")
            print("DB was not found(8/8) | Creating...")

        con.commit()
