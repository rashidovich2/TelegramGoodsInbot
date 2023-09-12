# - *- coding: utf- 8 - *-
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton as ikb

import json
from tgbot.keyboards.inline_admin import payment_choice_finl
from tgbot.loader import dp
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_yoo import YooAPI
from tgbot.services.api_cb import CoinbaseAPI
from tgbot.services.api_sqlite import update_paymentx, get_paymentx, get_upaycount, get_upaymentx, update_upaymentx, get_userx, get_admin_crypto_address, update_admin_crypto_address, create_admin_crypto_payment_row
from tgbot.utils.misc.bot_filters import IsAdmin, IsAdminorShopAdmin
from tgbot.utils.misc_functions import validate_trx_address, validate_bsc_address
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
from tgbot.middlewares.i18n import I18nMiddleware

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext

###################################################################################
############################# ВЫБОР СПОСОБА ПОПОЛНЕНИЯ ############################
# Открытие способов пополнения
@dp.message_handler(IsAdminorShopAdmin(), text=["🖲 Способы пополнения", "🖲 Payment Methods"], state="*")
async def payment_systems(message: Message, state: FSMContext):
    await state.finish()
    print("PAYMENT METHODS")
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    print(user_role, lang)
    if user_role in ['Admin', 'ShopAdmin']:
        await message.answer(_("<b>🖲 Выберите способ пополнения</b>", locale=lang), reply_markup=payment_choice_finl(user_id, lang))


# Включение/выключение самих способов пополнения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="change_payment:")
async def payment_systems_edit(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]
    #user_id = str(json.dumps(call.data.split(":")[3]))
    user_id = call.data.split(":")[3]
    #user_id = user_id.strip("\"")
    print(way_pay, way_status, user_id)
    #print(call.from_user.id)

    get_payment = get_upaymentx(user_id)
    #count = get_upaycount(user_id)
    if len(get_payment) == 0:
        cur = create_upayments_row(user_id)
    print(user_id, way_pay, way_status)

    if way_pay == "BTCB":
        way_payx = "way_btcb"
    elif way_pay == "TRX":
        way_payx = "way_tron"

    elif way_pay == "USDT":
        way_payx = "way_usdt"
    if way_pay is not None:
        way_payz = f"{way_payx} = {way_status}"
        update_upaymentx(user_id, way_payz)

    '''if get_payment['qiwi_login'] != "None" and get_payment['qiwi_token'] != "None" or way_status == "False":
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
        elif way_pay == "FreeCredi":
            update_upaymentx(user_id, way_freecredi=way_status)
        elif way_pay == "CoinBase":
            update_upaymentx(user_id, way_coinbase=way_status)
    else:
        await call.answer("❗ Добавьте киви кошелёк перед включением Способов пополнений.", True)'''

    try:
        await call.message.edit_text(_("<b>🖲 Выберите способ пополнения</b>", locale=lang), reply_markup=payment_choice_finl(user_id, lang))
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


# Изменение ₮ Tether, USDT(Trc-20) кошелька
@dp.message_handler(IsAdminorShopAdmin(), text=["₮ Tether адрес", "TRX, Tron(Trc20) адрес", "₿, Bitcoin(Bep-20) адрес", "Изменить номер карты"], state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()
    await state.set_state("here_admin_address")
    if message.text ==  "₮ Tether адрес":
        await state.update_data(here_type_net="USDT")
        await message.answer("<b>Введите <code>₮ Tether, USDT(Trc-20)</code> адрес</b>")
    if message.text ==  "TRX, Tron(Trc20) адрес":
        await state.update_data(here_type_net="TRX")
        await message.answer("<b>Введите <code>TRX(Trc-20)</code> адрес</b>")
    if message.text ==  "₿, Bitcoin(Bep-20) адрес":
        await state.update_data(here_type_net="BTCB")
        await message.answer("<b>Введите <code>₿, Bitcoin(Bep-20)</code> адрес</b>")
    if message.text ==  "Изменить номер карты":
        await state.update_data(here_type_net="RUB")
        await message.answer("<b>Введите <code>номер</code> карты</b>")


# Принятие Трон адреса и сохранение если нет
@dp.message_handler(IsAdminorShopAdmin(), state="here_admin_address")
async def enter_tron_address(message: Message, state: FSMContext):
    user_id = message.from_user.id
    type_net = (await state.get_data())['here_type_net']
    print(type_net)
    save = 0
    admin_address = ""

    if message.text:
        admin_address = message.text
        if admin_address == "" or admin_address is None:
            await message.answer(
                "<b>♻ Был введен пустой адрес</b>",
                reply_markup=back_to_profile_finl('ru'),
            )

        admin_addressdb = get_admin_crypto_address(type_net)
        print(admin_addressdb)
        #trx_addressdb = get_crypto_address(user_id, type_net)
        if type_net in ["TRX", "USDT"]:
            trx_address = await validate_trx_address(admin_address)
            print(trx_address)

            #await message.answer(f"<b>♻ Проверяем Ваш адрес.</b>")
            #есть ли адрес в TRC20
            if trx_address['success']:
                await message.answer(f"<b>♻ Все в порядке. {admin_address} найден в TRC20.</b>")
                save = 1
            if trx_address is False:
                await message.answer(f"<b>♻ Адреса: {admin_address} нет в сети.</b>",
                                     reply_markup=back_to_profile_finl('ru'))
                save = 0

        if type_net == "BTCB":
            bsc_addressbep = await validate_bsc_address(admin_address)

            # есть ли адрес в BEP-20
            if bsc_addressbep['message'] == 'OK':
                # если адрес есть в нашей БД
                await message.answer(f"<b>♻ Все в порядке. {admin_address} найден в BEP-20.</b>")
                save = 1
            if bsc_addressbep['message'] == 'NOTOK':
                await message.answer(f"<b>♻ Адреса: {admin_address} нет в сети.</b>", reply_markup=back_to_profile_finl('ru'))
                save = 0

        if type_net == "RUB":
            print(f"{admin_address} OK")
            save = 1

        if admin_addressdb and save == 1:
            update_admin_crypto_address(type_net, tron_address=admin_address)
            await message.answer(f"Обновляем адрес в профиле {type_net} админа.")
        elif admin_addressdb is None and save == 1:
            create_admin_crypto_payment_row(type_net, admin_address)
            await message.answer(f"Добавляем адрес в профиле {type_net} админа.")

            #await state.update_data(here_admin_address=admin_address)
            #await state.set_state("here_pay_amount")

            await message.answer(f"<b>♻ Успешно сохранили Ваш {type_net} адрес [{admin_address}] в профиле.</b>",
                                     reply_markup=back_to_profile_finl('ru'))






# Проверка работоспособности QIWI
@dp.message_handler(IsAdminorShopAdmin(), text="🥝 Проверить QIWI ♻", state="*")
async def payment_qiwi_check(message: Message, state: FSMContext):
    print("||| Проверка КИВИ админом площадки. |||")
    await state.finish()
    user_id = message.from_user.id
    print(user_id)

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
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.set_state("here_yoo_token")
    if lang == "ru":
        await message.answer(
            "<b>🥝 Введите <code>токен API</code> Yoo кошелька 🖍</b>\n"
            "❕ Получить можно тут 👉 <a href='https://yoomoney.ru/docs/wallet'><b>Нажми на меня</b></a>\n"
            "❕ При получении токена, ставьте только первые 3 галочки.",
            disable_web_page_preview=True
        )
    if lang == "en":
        await message.answer(
            "<b>🥝 Please, enter <code> API token </code> Yoo wallet 🖍</b>\n"
            "❕ You can get it here 👉 <a href='https://yoomoney.ru/docs/wallet'><b>Click Me</b></a>\n"
            "❕ When receiving a token, put only the first 3 ticks",
            disable_web_page_preview=True
        )
    #else:
        #await message.answer("<b>❌ Номер должен начинаться с + <code>(+7..., +380...)</code></b>\n"
        #                     "🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍")


# Принятие токена для QIWI
@dp.message_handler(IsAdminorShopAdmin(), state="here_qiwi_token")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_qiwi_token=message.text)
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

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
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.set_state("here_yoo_client_id")
    if lang == "ru":
        await message.answer(
            "<b>🥝 Введите <code>Клиентский ID 🖍</code></b>\n"
            "❕ Получить можно тут 👉 <a href='https://yoomoney.ru/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
            "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
            disable_web_page_preview=True
        )
    if lang == "ru":
        await message.answer(
            "<b>🥝 Plaese Enter <code>Client ID 🖍</code></b>\n"
            "❕ You can enter this here 👉 <a href='https://yoomoney.ru/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
            "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
            disable_web_page_preview=True
        )

# Принятие клиентского ID для Yoo
@dp.message_handler(IsAdminorShopAdmin(), state="here_yoo_client_id")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_yoo_client_id=message.text)
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.set_state("here_yoo_redirect_url")
    if lang == "ru":
        await message.answer(
            "<b>🥝 Введите <code>Redirect URL 🖍</code></b>\n"
            "❕ Получить можно в разделе Настройки YooMoney после аутентификации 👉 <a href='https://yoomoney.ru'><b>Нажми на меня</b></a>\n"
            "❕ Вы можете пропустить добавление оплаты по Форме, отправив: <code>0</code>",
            disable_web_page_preview=True
        )
    if lang == "en":
        await message.answer(
            "<b>🥝 Please enter <code>Redirect URL 🖍</code></b>\n"
            "❕ You can get it in the Settings section of YooMoney after authentication 👉 <a href='https://yoomoney.ru'><b>Click Me</b></a>\n"
            "❕ You can skip adding payment by Form by sending: <code>0</code>",
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
        lang = get_userx(user_id=user_id)['user_lang']

    await state.finish()
    if lang == "ru":
        cache_message = await message.answer("<b>🥝 Проверка введённых QIWI данных... 🔄</b>")
    if lang == "en":
        cache_message = await message.answer("<b>🥝 Checking the entered QIWI data... 🔄</b>")

    await asyncio.sleep(0.5)

    await (await QiwiAPI(cache_message, qiwi_login, qiwi_token, qiwi_secret, add_pass=True, suser_id=user_id)).pre_checker()


# Принятие приватного ключа для Yoo
@dp.message_handler(IsAdminorShopAdmin(), state="here_yoo_redirect_url")
async def payment_qiwi_edit_secret(message: Message, state: FSMContext):
    async with state.proxy() as data:
        acc_number = data['here_yoo_acc_number']
        token = data['here_yoo_token']
        client_id = data['here_yoo_client_id']
        user_id = message.from_user.id
        lang = get_userx(user_id=user_id)['user_lang']

        if message.text == "0": redirect_url = "None"
        if message.text != "0": redirect_url = message.text

        print(acc_number, token, client_id, redirect_url)

    await state.finish()

    if lang == "ru":
        cache_message = await message.answer("<b>🥝 Проверка введённых Yoo данных... 🔄</b>")
    if lang == "en":
        cache_message = await message.answer("<b>🥝 Checking the entered Yoo data... 🔄</b>")
    await asyncio.sleep(0.5)
    #await update_paymentx()
    await (await YooAPI(user_id, acc_number, token, client_id, redirect_url)).update_yoo()
    await message.answer(
        "<b>Данные YooMoney успешно обновлены!</b>\n",
         disable_web_page_preview=True
    )

