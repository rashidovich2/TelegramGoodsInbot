# - *- coding: utf- 8 - *-
from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from tgbot.data.config import get_admins

# Команды для юзеров
user_commands = [
    BotCommand("start", "♻ Перезапустить бота"),
    BotCommand("support", "☎ Поддержка"),
    BotCommand("faq", "ℹ FAQ"),
]

# Команды для админов
admin_commands = [
    BotCommand("start", "♻ Перезапустить бота"),
    BotCommand("support", "☎ Поддержка"),
    BotCommand("faq", "ℹ FAQ"),
    BotCommand("db", "📦 Получить Базу Данных"),
    BotCommand("log", "🖨 Получить логи"),
]


# Установка команд
async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    for admin in get_admins():
        try:
            await dp.bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            pass
