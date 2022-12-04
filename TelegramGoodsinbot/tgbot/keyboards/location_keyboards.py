from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import sqlite3


def geo_11_kb():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=1)
  #  bt1 = KeyboardButton('📡 Отправить своё местоположение', request_location=True)
    #bt2 = KeyboardButton('📋 Выбрать из списка')
    bt3 = KeyboardButton('⬆️ Вперёд')
    markup.add(bt3)
    return markup


def geo_1_kb():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=1)
    bt1 = KeyboardButton('📡 Отправить своё местоположение',
                         request_location=True)
    bt2 = KeyboardButton('📋 Выбрать из списка')
    markup.add(bt1, bt2)
    return markup


def geo_2_kb(city):
    markup = InlineKeyboardMarkup(row_width=1)
    bt1 = InlineKeyboardButton(
        'Подтвердить', callback_data=f'geo_chosen_cities#{city}')
    bt2 = InlineKeyboardButton(
        'Выбрать из списка', callback_data='choice_city_list')
    markup.add(bt1, bt2)
    return markup


def geo_3_kb():
    markup = InlineKeyboardMarkup(row_width=6)
    letters_list = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л',
                    'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Х', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
    for letter in letters_list:
        button = InlineKeyboardButton(
            letter, callback_data=f'geo_first_letter#{letter}')
        markup.insert(button)
    return markup


def geo_4_kb(info):
    conn = sqlite3.connect('tgbot/data/data_cities.db')
    cur = conn.cursor()
    query = f'''select id, city FROM cities where temp = ?  '''
    cur.execute(query, (info,))
    cities = cur.fetchall()
    conn.commit()
    markup = InlineKeyboardMarkup(row_width=1)
    for city in cities:
        button = InlineKeyboardButton(
            str(city[1]), callback_data=f'geo_chosen_cities#{city[0]}')
        markup.add(button)
    return markup
