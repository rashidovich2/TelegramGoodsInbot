# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities

from tgbot.keyboards.inline_admin import turn_open_finl, settings_open_finl
from tgbot.loader import dp
from tgbot.services.api_sqlite import *
from tgbot.utils.misc.bot_filters import IsAdmin
from tgbot.utils.misc_functions import send_admins, get_faq


# Изменение данных
@dp.message_handler(IsAdmin(), text="🖍 Изменить данные", state="*")
async def settings_data_edit(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🖍 Изменение настроек бота.</b>", reply_markup=settings_open_finl())


# Выключатели бота
@dp.message_handler(IsAdmin(), text="🕹 Выключатели", state="*")
async def settings_turn_edit(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🕹 Включение и выключение основных функций</b>", reply_markup=turn_open_finl())


######################################## ВЫКЛЮЧАТЕЛИ ########################################
# Включение/выключение тех работ
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_twork", state="*")
async def settings_turn_twork(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = get_userx(user_id=call.from_user.id)
    update_settingsx(status_work=get_status)

    if get_status == "True":
        send_text = "🔴 Отправил бота на технические работы."
    else:
        send_text = "🟢 Вывел бота из технических работ."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=turn_open_finl())


# Включение/выключение покупок
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_buy", state="*")
async def settings_turn_buy(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = get_userx(user_id=call.from_user.id)
    update_settingsx(status_buy=get_status)

    if get_status == "True":
        send_text = "🟢 Включил покупки в боте."
    else:
        send_text = "🔴 Выключил покупки в боте."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=turn_open_finl())


# Включение/выключение пополнений
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_pay", state="*")
async def settings_turn_pay(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = get_userx(user_id=call.from_user.id)
    update_settingsx(status_refill=get_status)

    if get_status == "True":
        send_text = "🟢 Включил пополнения в боте."
    else:
        send_text = "🔴 Выключил пополнения в боте."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=turn_open_finl())


######################################## ИЗМЕНЕНИЕ ДАННЫХ ########################################
# Изменение поддержки
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_edit_support", state="*")
async def settings_support_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_support")
    await call.message.edit_text("<b>☎ Отправьте ID пользователя.</b>\n"
                                 "❕ Вводимый ID должен быть пользователем бота.")

# Изменение типа площадки
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_edit_type_trade", state="*")
async def settings_type_trade_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_trade_type")
    await call.message.edit_text("<b>ℹ Выберите тип площадки: real | digital | hybrid</b>\n")

# Изменение FAQ
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_edit_faq", state="*")
async def settings_faq_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_faq")
    await call.message.edit_text("<b>ℹ Введите новый текст для FAQ</b>\n"
                                 "❕ Вы можете использовать заготовленный синтаксис и HTML разметку:\n"
                                 "<code>▶ {username}</code>  - логин пользоваля\n"
                                 "<code>▶ {user_id}</code>   - айди пользователя\n"
                                 "<code>▶ {firstname}</code> - имя пользователя")

# Принятие нового типа площдки
@dp.message_handler(IsAdmin(), state="here_settings_trade_type")
async def settings_tt_edit(message: Message, state: FSMContext):
    get_message = get_faq(message.from_user.id, message.text)

    try:
        cache_msg = await message.answer(get_message)
        await state.finish()
        update_settingsx(type_trade=message.text)

        await cache_msg.edit_text("<b>ℹ Тип площадки был успешно обновлен ✅</b>")
        await message.answer("<b>🖍 Изменение настроек бота.</b>", reply_markup=settings_open_finl())
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "ℹ Введите новый тип real | digital | hybrid.")


# Принятие нового текста для FAQ
@dp.message_handler(IsAdmin(), state="here_settings_faq")
async def settings_faq_get(message: Message, state: FSMContext):
    get_message = get_faq(message.from_user.id, message.text)

    try:
        cache_msg = await message.answer(get_message)
        await state.finish()
        update_settingsx(misc_faq=message.text)

        await cache_msg.edit_text("<b>ℹ FAQ было успешно обновлено ✅</b>")
        await message.answer("<b>🖍 Изменение настроек бота.</b>", reply_markup=settings_open_finl())
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "ℹ Введите новый текст для FAQ")


# Принятие нового айди для поддержки
@dp.message_handler(IsAdmin(), state="here_settings_support")
async def settings_support_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        get_user = get_userx(user_id=message.text)

        if get_user is not None:
            if len(get_user['user_login']) >= 1:
                await state.finish()
                update_settingsx(misc_support=get_user['user_id'])

                await message.answer("<b>☎ Поддержка была успешно обновлена ✅</b>")
                await message.answer("<b>🖍 Изменение настроек бота.</b>", reply_markup=settings_open_finl())
            else:
                await message.answer("<b>❌ У пользоваля отсутствует юзернейм.</b>\n"
                                     "☎ Отправьте ID пользователя.")
        else:
            await message.answer("<b>❌ Пользователь не был найден.</b>\n"
                                 "☎ Отправьте ID пользователя.")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "☎ Отправьте ID пользователя.")
