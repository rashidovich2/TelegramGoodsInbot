# - *- coding: utf- 8 - *-
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

import json
from tgbot.keyboards.inline_admin import payment_choice_finl
from tgbot.loader import dp
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_yoo import YooAPI
from tgbot.services.api_sqlite import update_paymentx, get_paymentx, get_upaycount, get_upaymentx, update_upaymentx
from tgbot.utils.misc.bot_filters import IsAdmin, IsAdminorShopAdmin


###################################################################################
############################# ВЫБОР СПОСОБА ПОПОЛНЕНИЯ ############################
# Открытие способов пополнения
@dp.message_handler(IsAdminorShopAdmin(), text="🖲 Способы пополнения", state="*")
async def payment_systems(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    print(user_id)

    await message.answer("<b>🖲 Выберите способ пополнения</b>", reply_markup=payment_choice_finl(user_id))


# Включение/выключение самих способов пополнения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="change_payment:")
async def payment_systems_edit(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]
    user_id = str(json.dumps(call.data.split(":")[3]))
    user_id = user_id.strip("\"")
    print(user_id)
    print(call.from_user.id)

    count = get_upaycount(user_id)
    if count == 0:
        cur = create_upayments_row(user_id)
    else:
        #get_payment = get_paymentx
        get_payment = get_upaymentx(user_id)
        print(get_payment)

    if get_payment['qiwi_login'] != "None" and get_payment['qiwi_token'] != "None" or way_status == "False":
        if way_pay == "Form":
            if get_payment['qiwi_secret'] != "None" or way_status == "False":
                update_upaymentx(user_id, way_form=way_status)
            else:
                await call.answer(
                    "❗ Приватный ключ отсутствует. Измените киви и добавьте приватный ключ для включения оплаты по Форме",
                    True)
        elif way_pay == "ForYm":
            if get_payment['yoo_client_id'] != "None" or way_status == "False":
                update_upaymentx(user_id, way_formy=way_status)
            else:
                await call.answer(
                    "❗ Приватный ключ отсутствует. Измените киви и добавьте приватный ключ для включения оплаты по Форме",
                    True)
        elif way_pay == "Number":
            update_upaymentx(user_id, way_number=way_status)
        elif way_pay == "Nickname":
            status, response = await (await QiwiAPI(call)).get_nickname()
            if status:
                update_upaymentx(user_id, way_nickname=way_status, qiwi_nickname=response)
            else:
                await call.answer(response, True)
    else:
        await call.answer("❗ Добавьте киви кошелёк перед включением Способов пополнений.", True)

    try:
        await call.message.edit_text("<b>🖲 Выберите способ пополнения</b>", reply_markup=payment_choice_finl(user_id))
    except Exception:
        pass


###################################################################################
####################################### QIWI ######################################
# Изменение QIWI кошелька
@dp.message_handler(IsAdminorShopAdmin(), text="🥝 Изменить QIWI 🖍", state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_qiwi_login")
    await message.answer("<b>🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍</b>")


# Проверка работоспособности QIWI
@dp.message_handler(IsAdminorShopAdmin(), text="🥝 Проверить QIWI ♻", state="*")
async def payment_qiwi_check(message: Message, state: FSMContext):
    print("||| Проверка КИВИ админом площадки. |||")
    await state.finish()
    user_id = message.from_user.id

    await (await QiwiAPI(message, check_pass=True)).pre_checker()


# Баланс QIWI
@dp.message_handler(IsAdminorShopAdmin(), text="🥝 Баланс QIWI 👁", state="*")
async def payment_qiwi_balance(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    await (await QiwiAPI(message)).get_balance()

######################################## YooMoney ################################
# Изменение реквизитов Yoo
@dp.message_handler(IsAdminorShopAdmin(), text="💳 Изменить Yoo 🖍", state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_yoo_acc_number")
    await message.answer("<b>💳 Введите <code>номер счета </code> Yoo аккаунта 🖍</b>")


######################################## ПРИНЯТИЕ QIWI ########################################
# Принятие логина для QIWI
@dp.message_handler(IsAdminorShopAdmin(), state="here_qiwi_login")
async def payment_qiwi_edit_login(message: Message, state: FSMContext):
    if message.text.startswith("+"):
        await state.update_data(here_qiwi_login=message.text)

        await state.set_state("here_qiwi_token")
        await message.answer(
            "<b>🥝 Введите <code>токен API</code> QIWI кошелька 🖍</b>\n"
            "❕ Получить можно тут 👉 <a href='https://qiwi.com/api'><b>Нажми на меня</b></a>\n"
            "❕ При получении токена, ставьте только первые 3 галочки.",
            disable_web_page_preview=True
        )
    else:
        await message.answer("<b>❌ Номер должен начинаться с + <code>(+7..., +380...)</code></b>\n"
                             "🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍")


# Принятие acc_number для Yoo
@dp.message_handler(IsAdminorShopAdmin(), state="here_yoo_acc_number")
async def payment_qiwi_edit_login(message: Message, state: FSMContext):
    #if message.text.startswith("+"):
        await state.update_data(here_yoo_acc_number=message.text)

        await state.set_state("here_yoo_token")
        await message.answer(
            "<b>🥝 Введите <code>токен API</code> Yoo кошелька 🖍</b>\n"
            "❕ Получить можно тут 👉 <a href='https://yoomoney.ru/api'><b>Нажми на меня</b></a>\n"
            "❕ При получении токена, ставьте только первые 3 галочки.",
            disable_web_page_preview=True
        )
    #else:
        #await message.answer("<b>❌ Номер должен начинаться с + <code>(+7..., +380...)</code></b>\n"
        #                     "🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍")


# Принятие токена для QIWI
@dp.message_handler(IsAdminorShopAdmin(), state="here_qiwi_token")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_qiwi_token=message.text)

    await state.set_state("here_qiwi_secret")
    await message.answer(
        "<b>🥝 Введите <code>Секретный ключ 🖍</code></b>\n"
        "❕ Получить можно тут 👉 <a href='https://qiwi.com/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
        "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
        disable_web_page_preview=True
    )

# Принятие токена для Yoo
@dp.message_handler(IsAdminorShopAdmin(), state="here_yoo_token")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_yoo_token=message.text)

    await state.set_state("here_yoo_client_id")
    await message.answer(
        "<b>🥝 Введите <code>Клиентский ID 🖍</code></b>\n"
        "❕ Получить можно тут 👉 <a href='https://yoomoney.ru/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
        "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
        disable_web_page_preview=True
    )

# Принятие клиентского ID для Yoo
@dp.message_handler(IsAdminorShopAdmin(), state="here_yoo_client_id")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_yoo_client_id=message.text)

    await state.set_state("here_yoo_redirect_url")
    await message.answer(
        "<b>🥝 Введите <code>Redirect URL 🖍</code></b>\n"
        "❕ Получить можно тут 👉 <a href='https://yoomoney.ru/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
        "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
        disable_web_page_preview=True
    )


# Принятие приватного ключа для QIWI
@dp.message_handler(IsAdminorShopAdmin(), state="here_qiwi_secret")
async def payment_qiwi_edit_secret(message: Message, state: FSMContext):
    async with state.proxy() as data:
        qiwi_login = data['here_qiwi_login']
        qiwi_token = data['here_qiwi_token']
        if message.text == "0": qiwi_secret = "None"
        if message.text != "0": qiwi_secret = message.text
        user_id = message.from_user.id

    await state.finish()

    cache_message = await message.answer("<b>🥝 Проверка введённых QIWI данных... 🔄</b>")
    await asyncio.sleep(0.5)

    await (await QiwiAPI(cache_message, qiwi_login, qiwi_token, qiwi_secret, True)).pre_checker()


# Принятие приватного ключа для Yoo
@dp.message_handler(IsAdminorShopAdmin(), state="here_yoo_redirect_url")
async def payment_qiwi_edit_secret(message: Message, state: FSMContext):
    async with state.proxy() as data:
        acc_number = data['here_yoo_acc_number']
        token = data['here_yoo_token']
        client_id = data['here_yoo_client_id']
        if message.text == "0": redirect_url = "None"
        if message.text != "0": redirect_url = message.text

    await state.finish()

    cache_message = await message.answer("<b>🥝 Проверка введённых Yoo данных... 🔄</b>")
    await asyncio.sleep(0.5)
    #await update_paymentx()
    await (await YooAPI(acc_number, token, client_id, redirect_url)).update_yoo()
    await message.answer(
        "<b>Данные yoomoney успешно обновлены!</b>\n"
        "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
         disable_web_page_preview=True
    )

