import sqlite3

from geopy.geocoders import Nominatim
from tgbot.data.config import PATH_DATABASE


# проверка записи локации
def is_location(user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_city from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    return result[0] is not None

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
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    lat_min = lat - 0.5
    lat_max = lat + 0.5
    long_min = long - 0.5
    long_max = long + 0.5
    query = '''select city, id FROM data_cities where co_1 > ? and co_1 < ? and  co_2 > ? and co_2 < ?'''
    items = [lat_min, lat_max, long_min, long_max]
    cur.execute(query, items)
    result = cur.fetchone()
    conn.commit()
    return False if result is None else result

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
def add_city(city_id, city_name, user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'update storage_users set user_city_id = ?, user_city = ? where user_id = ?'
    items = [city_id, city_name, user_id]
    cur.execute(query, items)
    conn.commit()

# город по айди и записывет координаты города в профиль пользователя
def get_city(city_id, user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'select city, co_1, co_2, id from data_cities where id = ?'
    result = cur.execute(query, (city_id,)).fetchone()
    conn.commit()
    #conn2 = sqlite3.connect(PATH_DATABASE)
    cur2 = conn.cursor()
    row = f'{result[1]}, {result[2]}'
    items = [row, user_id]
    print(items)
    query = 'update storage_users set user_geocode = ? where user_id = ?'
    cur2.execute(query, items)
    conn.commit()
    return result

def set_geocode(user_id, geocode):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    row = f'{result[1]}, {result[2]}'
    items = [row, user_id]
    print(items)
    query = 'update storage_users set user_geocode = ? where user_id = ?'
    cur.execute(query, items)
    conn.commit()


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

# добавляет город в позиции
def update_artist_city(city, city_id, artist_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'update storage_artists set city = ?, city_id = ? where artist_id = ?'
    items = [city, city_id, artist_id]
    cur.execute(query, items)
    conn.commit()


# город по айди
def get_city_info(id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = 'select city, co_1, co_2  from data_cities where id = ?'
    return cur.execute(query, (id,)).fetchone()


# город пользователя по айди
# def get_user_city(user_id):
#     conn = sqlite3.connect(PATH_DATABASE)
#     cur = conn.cursor()
#     query = '''select user_city from storage_users where user_id = ?'''
#     result = cur.execute(query, (user_id,)).fetchone()