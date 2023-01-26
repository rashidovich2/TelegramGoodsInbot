
# - *- coding: utf- 8 - *-
import asyncio
import os
import csv
from datetime import datetime
#import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types, Dispatcher
from aiogram.types import FSInputFile


#from tgbot.services.api_sqlite import get_position_of_day


API_TOKEN = '5337905343:AAFnZEexDdOAhn16AEw1zofEzVrPPEag89Q'
#API_TOKEN = '5337905343:AAFnZEexDdOAhn16AEw1zofEzVrPPEag89Q'
CHANNEL_ID = 919148970


bot = Bot(token=API_TOKEN) #ParseMode.  parse_mode=HTML
dp = Dispatcher()

positions = []


'''def send_photo_tb(photo):
    #with FSInputFile(photo) as photo:
    #with open('uploadproductdata/' + position['Photo'], 'rb') as photo:
    with open(photo, 'rb') as photo:
        id_photo =  bot.send_photo(CHANNEL_ID, photo, disable_notification=True)
        idp = id_photo['photo'][-1]['file_id'] 


        
@dp.message(content_types=['photo'])
def scan_message(message: types.Message):
    document_id = message.photo[0].file_id
    file_info = bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')
    return file_info.file_id'''

# Отправка рассылки
def function_sendphoto(message, caption='test', ct='photo'):
    try:
        print("||||")
        if ct == "text":
            bot.send_message(user['user_id'], message, disable_web_page_preview=True)
        elif ct == "photo":
            with open(message, 'rb') as photo:
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=photo, #.send_photo.file_id,
                    caption=caption if caption else None)
                print("|||")
                file_id = message.photo[0].file_id
                print(file_id)
    except:
        pass



fieldnames = ["Cat1", "Cat2", "Code", "Art", "Name", "Price", "Weight", "WeightType", "Description",  "photo"]
with open("uploadproductdata/data4.csv", encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        position = {}
        position['Cat1'] = row[0]
        position['Cat2'] = row[1]
        position['Code'] = row[2]
        position['Art'] = row[3]
        position['Name'] = row[4]
        position['Price'] = row[5]
        position['Weight'] = row[6]
        position['WeightType'] = row[7]
        position['Description'] = row[8]
        position['Photo'] = row[9]
        #photo = open("uploadproductdata/" + str(row[9]), 'rb')
        photo = "uploadproductdata/" + str(row[9])
        #photo=open(photof, 'rb')
        function_sendphoto(photo, "test", "photo")



        #idp = send_photo_tb('uploadproductdata/' + position['Photo'])
        #photof = FSInputFile('uploadproductdata/' + str(row[9])

        #id_photo = bot.send_photo(chat_id=CHANNEL_ID, photo=photo) # этот метод поможет получить file_id
        #idp = id_photo['photo'][-1]['file_id'] # 
        #with open(photof, 'rb') as photo:
        #bot.send_photo(chat_id=chat_id, photo=open(photof, 'rb'))
        #id_photo = bot.send_photo(CHANNEL_ID, photof, disable_notification=True)
        #filef_id = message.photo[-1].file_id
        #bot.send_photo(chat_id=chat_id, photo=file_id)
        #idp = id_photo['photo'][0]['file_id'] 
        #print(filef_id)

        #send_photo_tb(position['Photo'])
        #position['PhotoUrl'] = scan_message()


        print(position)

        positions.append(position)





