import sqlite3

from geopy.geocoders import Nominatim
from tgbot.data.config import PATH_DATABASE


# проверка записи локации
def is_location(user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    if result[0] == None:
        return False
    else:
        return True

# Nominatim geo 2 address
def search_address(lat, long):
    geolocator = Nominatim(user_agent="TGGoodsinbot")
    location = geolocator.reverse(f'{lat}, {long}')
    return location.address

def add_address(address, user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'update storage_users set user_address = ? where user_id = ?'
    #row = f'{lat}, {long}'
    items = [address, user_id]
    cur.execute(query, items)
    conn.commit()


# поиск города в радиусе 0.5' вокруг пользователя
def search_city(lat, long):
    conn = sqlite3.connect('tgbot/data/data_cities.db')
    cur = conn.cursor()
    lat_min = lat - 0.5
    lat_max = lat + 0.5
    long_min = long - 0.5
    long_max = long + 0.5
    query = f'''select city, id FROM cities where co_1 > ? and co_1 < ? and  co_2 > ? and co_2 < ?'''
    items = [lat_min, lat_max, long_min, long_max]
    cur.execute(query, items)
    result = cur.fetchone()
    conn.commit()
    if result == None:
        return False
    else:
        return result

# добавляет геокод в бд
def add_geocode(lat, long, user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'update storage_users set user_geocode = ? where user_id = ?'
    row = f'{lat}, {long}'
    items = [row, user_id]
    cur.execute(query, items)
    conn.commit()

# добавляет город в бд
def add_city(city, user_id, city_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'update storage_users set user_city = ?, user_city_id = ? where user_id = ?'
    items = [city, city_id, user_id]
    cur.execute(query, items)
    conn.commit()

# город по айди и записывет координаты города в профиль пользователя
def get_city(id, user_id):
    conn = sqlite3.connect('tgbot/data/data_cities.db')
    cur = conn.cursor()
    query = 'select city, co_1, co_2, id from cities where id = ?'
    result = cur.execute(query, (id,)).fetchone()
    conn.commit()
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    row = f'{result[1]}, {result[2]}'
    items = [row, user_id]
    query = 'update storage_users set user_geocode = ? where user_id = ?'
    cur.execute(query, items)
    conn.commit()
    return result

# ==============================================================================================================
# =========================  функции для локации позиции (магазина)   =========================================

# добавляет город в позиции
def update_position_city(city, city_id, user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'update storage_position set position_city = ?, position_city_id = ? where position_id = ?'
    items = [city, city_id, user_id]
    cur.execute(query, items)
    conn.commit()

# город по айди
def get_city_info(id):
    conn = sqlite3.connect('tgbot/data/data_cities.db')
    cur = conn.cursor()
    query = 'select city, co_1, co_2  from cities where id = ?'
    result = cur.execute(query, (id,)).fetchone()
    return result


# город пользователя по айди
# def get_user_city(user_id):
#     conn = sqlite3.connect(PATH_DATABASE)
#     cur = conn.cursor()
#     query = '''select user_city from storage_users where user_id = ?'''
#     result = cur.execute(query, (user_id,)).fetchone()