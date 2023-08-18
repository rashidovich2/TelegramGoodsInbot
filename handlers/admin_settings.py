# - *- coding: utf- 8 - *-
import gettext
from pathlib import Path
from contextvars import ContextVar

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities

from tgbot.keyboards.inline_admin import turn_open_finl, settings_open_finl
from tgbot.loader import dp
from tgbot.services.api_sqlite import *
from tgbot.utils.misc.bot_filters import IsAdmin
from tgbot.utils.misc_functions import send_admins, get_faq
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
from tgbot.middlewares.i18n import I18nMiddleware

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext
print(i18n.find_locales())

# Изменение данных
@dp.message_handler(text=["🖍 Изменить данные", "🖍 Edit settings"], state="*")
async def settings_data_edit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role == "Admin":
        await state.finish()
        await message.answer(_("<b>🖍 Изменение настроек бота.</b>", locale=lang), reply_markup=settings_open_finl(lang))

# Выключатели бота
@dp.message_handler(text=["🕹 Выключатели", "🕹 Switches"],  state="*")
async def settings_turn_edit(message: Message, state: FSMContext):
    user_role = get_userx(user_id=message.from_user.id)['user_role']
    lang = get_userx(user_id=message.from_user.id)['user_lang']
    print("::|::")
    if user_role == "Admin":
        await state.finish()
        await message.answer(_("<b>🕹 Включение и выключение основных функций</b>", locale=lang), reply_markup=turn_open_finl(lang))

######################################## ВЫКЛЮЧАТЕЛИ ########################################
# Включение/выключение тех работ
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_twork", state="*")
async def settings_turn_twork(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = get_userx(user_id=call.from_user.id)
    lang = get_user['user_lang']
    update_settingsx(status_work=get_status)

    if get_status == "True":
        send_text = "🔴 Отправил бота на технические работы."
    else:
        send_text = "🟢 Вывел бота из технических работ."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=turn_open_finl(lang))


# Включение/выключение покупок
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_buy", state="*")
async def settings_turn_buy(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = get_userx(user_id=call.from_user.id)
    lang = get_user['user_lang']
    update_settingsx(status_buy=get_status)

    if get_status == "True":
        send_text = "🟢 Включил покупки в боте."
    else:
        send_text = "🔴 Выключил покупки в боте."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=turn_open_finl(lang))


# Включение/выключение пополнений
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_pay", state="*")
async def settings_turn_pay(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = get_userx(user_id=call.from_user.id)
    lang = get_user['user_lang']
    update_settingsx(status_refill=get_status)

    if get_status == "True":
        send_text = "🟢 Включил пополнения в боте."
    else:
        send_text = "🔴 Выключил пополнения в боте."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=turn_open_finl(lang))


######################################## ИЗМЕНЕНИЕ ДАННЫХ ########################################
# Изменение поддержки
@dp.callback_query_handler(text_startswith="settings_edit_support", state="*")
async def settings_support_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_support")
    lang = get_userx(user_id=call.from_user.id)['user_lang']
    user_role = get_userx(user_id=call.from_user.id)['user_role']
    if user_role == "Admin":
        await call.message.edit_text(_("<b>☎ Отправьте ID пользователя.</b>"
                                     "❕ Вводимый ID должен быть пользователем бота.", locale=lang))

# Изменение типа площадки
@dp.callback_query_handler(text_startswith="settings_edit_type_trade", state="*")
async def settings_type_trade_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_trade_type")
    lang = get_userx(user_id=call.from_user.id)['user_lang']
    user_role = get_userx(user_id=call.from_user.id)['user_role']
    print(lang, user_role)
    if user_role == "Admin":
        await call.message.edit_text(_("<b>ℹ Выберите тип площадки: real | digital | hybrid</b>", locale=lang))

# Изменение FAQ
@dp.callback_query_handler(text_startswith="settings_edit_faq", state="*")
async def settings_faq_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_faq")
    lang = get_userx(user_id=call.from_user.id)['user_lang']
    user_role = get_userx(user_id=call.from_user.id)['user_role']
    if user_role == "Admin":
        await call.message.edit_text(_("<b>ℹ Введите новый текст для FAQ</b>"
                                     "❕ Вы можете использовать заготовленный синтаксис и HTML разметку:\n"
                                     "<code>▶ {username}</code>  - логин пользоваля\n"
                                     "<code>▶ {user_id}</code>   - айди пользователя\n"
                                     "<code>▶ {firstname}</code> - имя пользователя", locale=lang))

# Принятие нового типа площадки
@dp.message_handler(state="here_settings_trade_type")
async def settings_tt_edit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang, user_role = get_userx(user_id=user_id)['user_lang'], get_userx(user_id=user_id)['user_role']

    if user_role == "Admin":
        try:
            await state.finish()
            update_settingsx(type_trade=message.text)

            await message.answer("<b>🖍 Изменение настроек бота.</b>", reply_markup=settings_open_finl(lang))
        except CantParseEntities:
            await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>"
                                 "ℹ Введите новый тип real | digital | hybrid.", locale=lang))


# Принятие нового текста для FAQ
@dp.message_handler(state="here_settings_faq")
async def settings_faq_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_message = get_faq(user_id, message.text)
    lang, user_role = get_userx(user_id=user_id)['user_lang'], get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        try:
            cache_msg = await message.answer(get_message)
            await state.finish()
            update_settingsx(misc_faq=message.text)

            await cache_msg.edit_text("<b>ℹ FAQ было успешно обновлено ✅</b>")
            await message.answer(_("<b>🖍 Изменение настроек бота.</b>", locale=lang), reply_markup=settings_open_finl(lang))
        except CantParseEntities:
            await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                                 "ℹ Введите новый текст для FAQ", locale=lang))


# Принятие нового айди для поддержки
@dp.message_handler(state="here_settings_support")
async def settings_support_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang, user_role = get_userx(user_id=user_id)['user_lang'], get_userx(user_id=user_id)['user_role']
    print(message.text)
    if user_role == "Admin":
        if message.text.isdigit():
            get_user = get_userx(user_id=message.text)
            print(get_user)

            if get_user is None:
                await message.answer(_("<b>❌ Пользователь не был найден.</b>\n"
                                     "☎ Отправьте ID пользователя.", locale=lang))
            elif len(get_user['user_login']) >= 1:
                await state.finish()
                update_settingsx(misc_support=get_user['user_id'])

                await message.answer(_("<b>☎ Поддержка была успешно обновлена ✅</b>", locale=lang))
                await message.answer(_("<b>🖍 Изменение настроек бота.</b>", locale=lang), reply_markup=settings_open_finl(lang))
            else:
                await message.answer(_("<b>❌ У пользоваля отсутствует юзернейм.</b>"
                                     "☎ Отправьте ID пользователя.", locale=lang))
        else:
            await message.answer(_("<b>❌ Данные были введены неверно.</b>"
                                 "☎ Отправьте ID пользователя.", locale=lang))
