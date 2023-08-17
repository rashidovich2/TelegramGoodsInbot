from telethon import TelegramClient
import random

# Тут вставляй свои данные с https://my.telegram.org/apps

api_id = "347132"
api_hash = "0878ef5125b0b4d37e4187137b9a34bf"

from telethon import TelegramClient, events
client = TelegramClient('anon', api_id, api_hash)
client.start()

@client.on(events.NewMessage(777000))
async def main(event):
	print(event.message)