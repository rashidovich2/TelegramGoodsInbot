import asyncio
import json
import random
import datetime
import time

import requests
import subprocess

import aiogram
from aiogram import Dispatcher
from aiogram import executor
from aiogram import Bot, types
from tgbot.loader import bot

from tgbot.services.api_sqlite import get_users_by_cities, get_users_by_citiesx, get_all_usersx, get_userx_idname


async def send_mes2():
	msg = await bot.send_photo(chat_id=919148970, photo=open("img/msg1.png", "rb"))
	file_id = msg.photo[0].file_id
	print(file_id)
	await asyncio.sleep(3)

async def send_mes(user_id, message, caption=""):
	await bot.send_photo(chat_id=user_id,
	                    photo=message,
	                    caption=caption) #post[9] if post[9] else None)await bot.send_photo(
	await bot.send_message(user_id, message, disable_web_page_preview=True)
	

cities = get_users_by_cities()
#users = get_all_usersx()
#for user in users:
for city in cities:
	#print(user)
	subprocess.run(["python3", "neon.py", f"-t{city['user_city']}, здравствуйте! Мы добавили USDT, TRX, BTC.!", f"-fimg/msg0002{city['user_city_id']}.png"])
	#image = open(f"img/msg{city['user_city_id']}.png", 'rb')
	#image = open(f"img/msg{user['user_city_id']}.png", 'rb')
	#caption="Hi"
	#send_mes(user['user_id'], image, caption)

#send_mes2()

users = get_userx_idname()
#users = get_all_usersx()
#for user in users:
for user in users:
	#print(user)
	subprocess.run(["python3", "neon.py", f"-t{user['user_name']}, привет. Хорошего дня Вам!", f"-fimg/u{user['user_id']}.png"])
#image = open(f"img/msg{city['user_city_id']}.png", 'rb')
#image = open(f"img/msg{user['user_city_id']}.png", 'rb')
#caption="Hi"
#send_mes(user['user_id'], image, caption)