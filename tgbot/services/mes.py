import asyncio

from aiogram import Bot, types

#API_TOKEN = '5361635126:AAF9sQ8__qoITGGlUVBhsev-nz15NJj_QN0'
API_TOKEN = '5337905343:AAFnZEexDdOAhn16AEw1zofEzVrPPEag89Q'
CHANNEL_ID = -1001683374540
#CHANNEL_ID = 5337905343

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


async def main():
    await send_message(CHANNEL_ID, '<b>Hello!</b>')


if __name__ == '__main__':
    asyncio.run(main())
