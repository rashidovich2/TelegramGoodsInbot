
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
from tgbot.data.config import PATH_DATABASE

def geo_11_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    bt1 = KeyboardButton('📡 Поделиться своим местоположением', request_location=True)
    bt2 = KeyboardButton('📋 Выбрать город из списка')
    bt3 = KeyboardButton('⬆️ Выбрать город позже')
    markup.add(bt1, bt2, bt3)
    return markup

def geo_1_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    bt1 = KeyboardButton('📡 Поделиться своим местоположением', request_location=True)
    bt2 = KeyboardButton('📋 Выбрать город из списка')
    markup.add(bt1, bt2)
    return markup

def geo_2_kb(city_id, city):
    print(city_id, city)
    markup = InlineKeyboardMarkup(row_width=1)
    bt1 = InlineKeyboardButton('✅ Подтвердить', callback_data=f"geo_chosen_cities:{city_id}:{city}")
    bt2 = InlineKeyboardButton('Выбрать город из списка', callback_data='choice_city_list')
    markup.add(bt1, bt2)
    return markup

def geo_3_kb():
    markup = InlineKeyboardMarkup(row_width=6)
    #lang = "ru"
    #if lang == "ru":
    letters_list = ['А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Х','Ч','Ш','Щ','Э','Ю','Я']
    #if lang == "en":
    #    letters_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for letter in letters_list:
        button = InlineKeyboardButton(letter, callback_data=f"geo_first_letter:{letter}")
        markup.insert(button)
    return markup

def geo_4_kb(letter):
    print(letter)
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select id, city FROM data_cities where temp = ?'''
    cur.execute(query, (letter,))
    city = 0
    cities = cur.fetchall()
    conn.commit()
    print(len(cities))
    markup = InlineKeyboardMarkup(row_width=1)
    for city in cities:
        button = InlineKeyboardButton(str(city[1]), callback_data=f"geo_chosen_cities:{city[0]}:{city[1]}")
        markup.add(button)
    return markup
