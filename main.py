# - *- coding: utf- 8 - *-
import os
import sys

import colorama
import aiogram
from aiogram import Dispatcher
from aiogram import executor
from colorama import Fore

from tgbot.data.config import get_admins
from tgbot.handlers import dp
from tgbot.loader import scheduler
from tgbot.middlewares import setup_middlewares
from tgbot.services.api_session import RequestsSession
from tgbot.services.api_sqlite import create_dbx
from tgbot.services.regular import send_message_start
from tgbot.utils.misc.bot_commands import set_commands
from tgbot.utils.misc.bot_logging import bot_logger
from tgbot.utils.misc_functions import check_update, check_bot_data, on_startup_notify, update_profit_day, \
    update_profit_week, autobackup_admin, post_every_hour, post_every_eighteen, post_every_half_hour, \
    post_half_eight, post_evening_events, posts3_every_hour, reinvite_sellers_by_city, sellers_news

#CHANNEL_ID = '-1001683374540'
#text = "test"

#async def send_message(channel_id: int, text: str):
#    await bot.send_message(channel_id, text)

# Запуск шедулеров
async def scheduler_start():
    #scheduler.add_job(send_message_start, 'interval', seconds=600)
    #scheduler.add_job(post_every_hour, "cron", hour=21, minute=43)
    #scheduler.add_job(sellers_news, "cron", hour=15, minute=9)
    #scheduler.add_job(reinvite_sellers_by_city, "cron", hour=11, minute=20)
    #scheduler.add_job(posts3_every_hour, "interval", minutes=60)
    #scheduler.add_job(post_every_hour, "interval", minutes=30)
    #scheduler.add_job(post_half_eight, "cron", hour=18, minute=30)
    #scheduler.add_job(post_evening_events, "cron", hour=22, minute=45)
    #scheduler.add_job(post_evening_events, "cron", hour=19, minute=50)
    #scheduler.add_job(post_half_eight, "interval", seconds=30)
    #scheduler.add_job(post_every_eighteen, "cron", hour=17)
    #scheduler.add_job(post_half_eight, "cron", hour=19, minute=35)
    #scheduler.add_job(post_evening_events, "cron", hour=10, minute = 40)
    #scheduler.add_job(check_order_messages, 'interval', seconds=600)
    scheduler.add_job(update_profit_week, "cron", day_of_week="mon", hour=00, minute=1)
    scheduler.add_job(update_profit_day, "cron", hour=00)
    scheduler.add_job(autobackup_admin, "cron", hour=00)

# Выполнение функции после запуска бота
async def on_startup(dp: Dispatcher):
    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)
    dp.bot['rSession'] = RequestsSession()

    await set_commands(dp)
    await check_bot_data()
    await scheduler_start()
    await on_startup_notify(dp)

    bot_logger.exception("BOT WAS STARTED")
    print(f"{Fore.LIGHTYELLOW_EX}~~~~~ Bot was started ~~~~~")
    print(f"{Fore.LIGHTBLUE_EX}~~~~~ TG developer: @raclear ~~~~~")
    print(Fore.RESET)

    if len(get_admins()) == 0: print("***** ENTER ADMIN ID IN settings.ini *****")


# Выполнение функции после выключения бота
async def on_shutdown(dp: Dispatcher):
    rSession: RequestsSession = dp.bot['rSession']
    await rSession.close()
    #
    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()
    #
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    create_dbx()

    scheduler.start()
    setup_middlewares(dp)

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
