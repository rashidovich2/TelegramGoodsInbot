# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR

from tgbot.keyboards.reply_z_all import menu_frep
from tgbot.loader import dp

from tgbot.middlewares.i18n import I18nMiddleware

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext


# Колбэк с удалением сообщения
@dp.callback_query_handler(text="close_this", state="*")
async def missed_callback_close(call: CallbackQuery, state: FSMContext):
    await call.message.delete()


# Колбэк с обработкой кнопки
@dp.callback_query_handler(text="...", state="*")
async def missed_callback_answer(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

  
# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@dp.callback_query_handler(state="*")
async def missed_callback(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except Exception:
        pass
    lang = "ru"
    await call.message.answer(_("<b>❌ Данные не были найдены из-за перезапуска скрипта.\n"
                              "♻ Выполните действие заново.</b>", locale=lang),
                              reply_markup=menu_frep(call.from_user.id, lang))

# Обработка всех неизвестных команд
@dp.message_handler()
async def missed_message(message: Message):
    lang = "ru"
    await message.answer(_("♦ Неизвестная команда.\n"
                         "▶ Введите /start", locale=lang))
