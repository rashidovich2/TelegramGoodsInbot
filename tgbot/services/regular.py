# - *- coding: utf- 8 - *-
import asyncio
import os
from datetime import datetime
#import requests

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types


from tgbot.utils.misc_functions import get_position_of_day

#API_TOKEN = '5402212470:AAGFv7hY2bYGeaCOi_77cZJlOd31crtXK9k'
#API_TOKEN = '5502549363:AAH2d3qoCiA8pQ8EDpT4CZ9rxD55eh2lmHo'
#API_TOKEN = '5328800059:AAEv2GffGt2jJREnStKPYxkUdR1rqJ6-YuQ'
API_TOKEN = '5337905343:AAFnZEexDdOAhn16AEw1zofEzVrPPEag89Q'
#API_TOKEN = '5337905343:AAFnZEexDdOAhn16AEw1zofEzVrPPEag89Q'
CHANNEL_ID = -1001683374540
#CHANNEL_ID = 5328800059
#CHANNEL_ID =  5337905343
#CHANNEL_ID = 5402212470

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

def tick():
    print('Tick! The time is: %s' % datetime.now())
#get_message, get_image = get_position_of_day()


def send_photo_telegram(file_id):
    files = {'photo': open({file_id}, 'rb')}
    token = "5337905343:AAFnZEexDdOAhn16AEw1zofEzVrPPEag89Q"
    chat_id = "-1001683374540" # если у вас группа то будет так chat_id = "-1009999999"
    r = requests.post("https://api.telegram.org/bot"+token+"/sendPhoto?chat_id=" + chat_id, files=files)
    if r.status_code != 200:
        raise Exception("post_text error")


async def send_message_start():
    position, image = get_position_of_day()
    #await send_message(CHANNEL_ID, '<b>tttt</b>')
    #get_position = get_positionx(position_id=4875164059)
    print(image)
    #await send_photo_telegram(image)
    #await send_photo(CHANNEL_ID, photo='file_id_' + image)
    await send_photo(CHANNEL_ID, photo=image, caption=position)
    #await send_message(CHANNEL_ID, position)
    #await send_photo(chat_id=CHANNEL_ID, photo=image, caption=position, parse_mode=ParseMode.MARKDOWN)
    #if len(image) >= 5:
    #    photo = types.InputMediaPhoto(image)
    #    await send_photo(CHANNEL_ID, photo, position)
    #else:
        

    #await send_message(CHANNEL_ID, position)
    #await send_message(CHANNEL_ID, '<div> ||| </div>')


async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.add_job(send_message_start, 'interval', seconds=5)
    #scheduler.add_job(send_message_start, 'interval', next_run_time=datetime.now())
    
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass