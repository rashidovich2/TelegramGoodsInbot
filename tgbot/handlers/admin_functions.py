# - *- coding: utf- 8 - *-
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities

from tgbot.keyboards.inline_admin import profile_search_finl, profile_search_reqs
from tgbot.keyboards.inline_z_all import ad_confirm_inl, ad_add_to_plan_inl
from tgbot.loader import dp, bot
from tgbot.services.api_sqlite import *
from tgbot.utils.misc.bot_filters import IsAdmin
from tgbot.utils.misc_functions import open_profile_search, open_profile_search_req, upload_text, generate_sales_report, open_profile_search_seller
#from munch import Munch


# Рассылка
@dp.message_handler(IsAdmin(), text="📢 Рассылка", state="*")
async def functions_ad(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_ad_text")
    await message.answer("<b>📢 Введите текст для рассылки пользователям</b>\n"
                         "❕ Вы можете использовать HTML разметку")

# Рассылка
@dp.message_handler(IsAdmin(), text="📢 Рассылка2", state="*")
async def functions_ad(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_ad_post")
    await message.answer("<b>📢 Введите текст для рассылки пользователям</b>\n"
                         "❕ Вы можете использовать HTML разметку")

######################################## ПРИНЯТИЕ ДАННЫХ ########################################
# Принятие текста для рассылки
@dp.message_handler(IsAdmin(), state="here_ad_post", content_types=types.ContentType.ANY)
async def functions_ad_get(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)

    get_users = get_all_usersx()
    user_id = message.from_user.id
    mode = "tohour"

    if types.ContentType.TEXT == message.content_type:
        ct = 'text'
        await state.update_data(ct='text', here_ad_post=str(message.html_text))
        add_post_to_plan(ct, user_id, message.html_text, mode, caption='')
    elif types.ContentType.PHOTO == message.content_type:
        ct = 'photo'
        caption=message.html_text if message.caption else None
        await state.update_data(ct="photo", here_ad_photo=message.photo[-1].file_id, caption=caption)
        add_post_to_plan(ct, user_id, message.photo[-1].file_id, mode, caption=caption)
    elif types.ContentType.VIDEO == message.content_type:
        ct = 'video'
        caption=message.html_text if message.caption else None
        await state.update_data(ct="video", here_ad_video=message.video.file_id, caption=caption)
        add_post_to_plan(ct, user_id, message.video[-1].file_id, mode, caption=caption)
    elif types.ContentType.ANIMATION == message.content_type:
        ct = 'animation'
        caption=message.html_text if message.caption else None
        await state.update_data(ct="animation", here_ad_animation=message.animation.file_id, caption=caption)
        add_post_to_plan(ct, user_id, message.animation[-1].file_id, mode, caption=caption)
    post_id = get_lastpost()

    print(post_id)

    '''if types.ContentType.TEXT == message.content_type: # Если админ отправил текст
        for user in get_users:
            try:
                await dp.bot.send_message(
                    chat_id=user.user_id,
                    text=message.html_text
                )
                await sleep(0.33)
            except Exception:
                pass
        else:
            await message.answer(
                '<b> Рассылка завершена!</b>'
            )'''

    try:
        #await message.answer("Тип поста:" + ct)
        cache_msg = await message.answer("Тип поста:" + ct)
        #await cache_msg.delete()

        #await state.set_state("here_ad_plan_once")
        await state.update_data(post_id=post_id)
        print(post_id)
        #post_text, post_photo, post_video, post_animation, caption =
        await message.answer(
            f"<b>📢 Включить пост в ротацию бота?</b>\n",
            reply_markup=ad_add_to_plan_inl,
            disable_web_page_preview=True
        )
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📢 Введите текст для рассылки пользователям.\n"
                             "❕ Вы можете использовать HTML разметку.")


# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="plan_once_ad", state="*") #here_ad_plan_once")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    get_users = get_all_usersx()
    post_id = (await state.get_data())['post_id']
    ct = (await state.get_data())['ct']

    try:
        if get_action == "yes":

            cache_msg = await call.message.answer("Выбрано добавление в план:" + ct)
            await cache_msg.delete()

        await state.set_state("here_ad_post_confirm")
        post = get_postx(post_id)
        print(post)

        await call.message.answer(
            f"<b>📢 Отправить <code>{len(get_users)}</code> юзерам сообщение?</b>\n",
            #f"{message.text}",
            reply_markup=ad_confirm_inl,
            disable_web_page_preview=True
        )
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📢 Введите текст для рассылки пользователям.\n"
                             "❕ Вы можете использовать HTML разметку.")


# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_ad", state="here_ad_post_confirm")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

    ct = (await state.get_data())['ct']
    mode = "evening"
    if ct == "text":
        #print("|")
        send_message = (await state.get_data())['here_ad_post']
        #add_post_to_plan(ct, send_message, mode, 0)
    elif ct == "photo":
        #print("||")
        send_photo = (await state.get_data())['here_ad_photo']
        caption = (await state.get_data())['caption']
        #add_post_to_plan(ct, send_photo, mode, caption)
    elif ct == "video":
        #print("|||")
        send_video = (await state.get_data())['here_ad_video']
        caption = (await state.get_data())['caption']
        #add_post_to_plan(ct, send_video, mode, caption)
    elif ct == "animation":
        #print("||||")
        send_animation = (await state.get_data())['here_ad_animation']
        caption = (await state.get_data())['caption']
        #add_post_to_plan(ct, send_animation, mode, caption)

    #send_message = (await state.get_data())['here_ad_post']
    get_users = get_all_usersx()
    await state.finish()

    if get_action == "yes":
        await call.message.edit_text(f"<b>📢 Рассылка началась... (0/{len(get_users)})</b>")
        if ct == "text":
            asyncio.create_task(functions_adext_make(ct, send_message, 0, call))
        if ct == "photo":
            asyncio.create_task(functions_adext_make(ct, send_photo, caption, call))
        if ct == "video":
            asyncio.create_task(functions_adext_make(ct, send_video, caption, call))
        if ct == "animation":
            asyncio.create_task(functions_adext_make(ct, send_animation, caption, call))
    else:
        await call.message.edit_text("<b>📢 Вы отменили отправку рассылки ✅</b>")


# Поиск профиля
@dp.message_handler(IsAdmin(), text="👤 Поиск профиля 🔍", state="*")
async def functions_profile(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_profile")
    await message.answer("<b>👤 Введите логин или айди пользователя</b>")

# Поиск чеков
@dp.message_handler(IsAdmin(), text="🧾 Поиск чеков 🔍", state="*")
async def functions_receipt(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_receipt")
    await message.answer("<b>🧾 Отправьте номер чека</b>")

# Просмотр запросов продавцов
@dp.message_handler(IsAdmin(), text="🖍 Посмотреть запросы", state="*")
async def functions_seller_requests(message: Message, state: FSMContext):
    await state.finish()

    #await state.set_state("check_seller_requests")

    await message.answer("<b>🧾 Посмотрим запросы продавцов:</b>")


    all_requests = get_all_requestx()
    #print(all_requests)
    if len(all_requests) >= 1:
        await message.answer("Запросы на роль продавца" + str(len(all_requests)) + "шт.")

        for request in all_requests:

            await message.answer(open_profile_search_req(request['user_id']), reply_markup=profile_search_reqs(request['user_id']))



# Просмотр запросов продавцов
@dp.message_handler(IsAdmin(), text="📊 Отчет о продажах", state="*")
async def functions_seller_requests(message: Message, state: FSMContext):
    await state.finish()

    #await state.set_state("check_seller_requests")

    await message.answer(generate_sales_report())

    get_users = get_purchasesbysellers()
    #print(all_requests)
    if len(get_users)>= 1:
        await message.answer("Топ - продавцов" + str(len(get_users)) + "шт.")

        for user in get_users:
            #if user['user_id'] is None: continue

            await message.answer(open_profile_search_seller(user_id=user['user_id']), reply_markup=profile_search_finl(user['user_id']))

########################################### CALLBACKS ###########################################
# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_ad", state="here_ad_confirm")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

    send_message = (await state.get_data())['here_ad_text']
    get_users = get_all_usersx()
    await state.finish()

    if get_action == "yes":
        await call.message.edit_text(f"<b>📢 Рассылка началась... (0/{len(get_users)})</b>")
        asyncio.create_task(functions_ad_make(send_message, call))
    else:
        await call.message.edit_text("<b>📢 Вы отменили отправку рассылки ✅</b>")


# Покупки пользователя
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_purchases", state="*")
async def functions_profile_purchases(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    last_purchases = last_purchasesx(user_id, 10)

    if len(last_purchases) >= 1:
        await call.answer("🎁 Последние 10 покупок")
        await call.message.delete()

        for purchases in last_purchases:
            link_items = await upload_text(call, purchases['purchase_item'])

            await call.message.answer(f"<b>🧾 Чек: <code>#{purchases['purchase_receipt']}</code></b>\n"
                                      f"🎁 Товар: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}шт | {purchases['purchase_price']}₽</code>\n"
                                      f"🕰 Дата покупки: <code>{purchases['purchase_date']}</code>\n"
                                      f"🔗 Товары: <a href='{link_items}'>кликабельно</a>")

        await call.message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))
    else:
        await call.answer("❗ У пользователя отсутствуют покупки", True)


# Отправка рассылки
async def functions_adext_make(ct, message, caption, call: CallbackQuery):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()

    for user in get_users:
        try:
            if ct == "text":
                await dp.bot.send_message(user['user_id'], message, disable_web_page_preview=True)
            elif ct == "photo":
                await dp.bot.send_photo(
                    chat_id=user['user_id'],
                    photo=message, #.send_photo.file_id,
                    caption=caption if caption else None)
            elif ct == "video":
                await dp.bot.send_video(
                    chat_id=user['user_id'],
                    video=message,
                    caption=caption if caption else None)
            elif ct == "animation":
                await dp.bot.send_animation(
                    chat_id=user['user_id'],
                    animation=message,
                    caption=caption if caption else None)

            receive_users += 1
        except:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await call.message.edit_text(f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>")

        await asyncio.sleep(0.05)

    await call.message.edit_text(
        f"<b>📢 Рассылка была завершена ✅</b>\n"
        f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
        f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
    )

# Отправка рассылки
async def functions_ad_make(message, call: CallbackQuery):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()

    for user in get_users:
        try:
            await bot.send_message(user['user_id'], message, disable_web_page_preview=True)
            receive_users += 1
        except:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await call.message.edit_text(f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>")

        await asyncio.sleep(0.05)

    await call.message.edit_text(
        f"<b>📢 Рассылка была завершена ✅</b>\n"
        f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
        f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
    )

# Подтверждение запроса продавца
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_request_approve", state="*")
async def functions_shopadmin_request_approve(call: CallbackQuery, state: FSMContext):
    #await state.update_data(here_profile=call.data.split(":")[1])

    #await state.set_state("here_user_request_approve")
    #user_id = (await state.get_data())['here_profile']
    user_id = call.data.split(":")[1]
    await state.finish()

    get_user = get_userx(user_id=user_id)
    update_userx(user_id, user_role="ShopAdmin")
    update_requestx(user_id, state="Approved")

    await call.message.answer(
        f"<b>✅ Пользователю <a href='tg://user?id={user_id}'>{get_user['user_name']}</a> "
        f"изменена роль на: <code>{get_user['user_role']}</code></b>")

    await bot.send_message(user_id, f"<b> Вам была выдана роль Продавца магазина. </b>")
    #await call.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))


# Отклонение запроса продавца
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_request_decline", state="*")
async def functions_shopadmin_request_decline(call: CallbackQuery, state: FSMContext):
    #await state.update_data(here_profile=call.data.split(":")[1])
    #user_id = (await state.get_data())['here_profile']
    await state.finish()
    user_id = call.data.split(":")[1]
    print(user_id)
    #user_id = call.data.split(":")[1]
    #get_user = get_userx(user_id=user_id)
    
    #get_user = get_userx(user_id=user_id)
    #delete_requests_userx(user_id)
    delete_requests_userx(user_id)
    #call.data
    
    await call.answer(" Запрос был успешно удален.")

    #await state.set_state("here_user_request_decline")
    await bot.send_message(user_id, f"<b>Ваш запрос был отклонен. Вы можете попробовать подать следующий запрос через 14 дней.</b>")


# Выдача баланса пользователю
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_balance_add", state="*")
async def functions_profile_balance_add(call: CallbackQuery, state: FSMContext):
    await state.update_data(here_profile=call.data.split(":")[1])

    await state.set_state("here_profile_add")
    await call.message.edit_text("<b>💰 Введите сумму для выдачи баланса</b>")


# Изменение баланса пользователю
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_balance_set", state="*")
async def functions_profile_balance_set(call: CallbackQuery, state: FSMContext):
    await state.update_data(here_profile=call.data.split(":")[1])

    await state.set_state("here_profile_set")
    await call.message.edit_text("<b>💰 Введите сумму для изменения баланса</b>")


# Обновление профиля пользователя
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_refresh", state="*")
async def functions_profile_refresh(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]

    await call.message.delete()
    await call.message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))


######################################## СМЕНА СТАТУСОВ ПОЛЬЗОВАТЕЛЯ ############################

# Принятие суммы для выдачи баланса пользователю
#@dp.message_handler(IsAdmin(), state="here_user_request_approve")
@dp.callback_query_handler(IsAdmin(), state="here_user_request_approve")
async def functions_shopadmin_request_approvep(message: Message, state: FSMContext):
    user_id = (await state.get_data())['here_profile']
    await state.finish()

    get_user = get_userx(user_id=user_id)
    update_userx(user_id, user_role="ShopAdmin")

    await message.answer(
        f"<b>✅ Пользователю <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> "
        f"изменена роль на: <code>{get_user['user_role']}</code></b>")

    await message.bot.send_message(user_id, f"<b> Вам была выдана роль Продавца магазина </b>")
    await message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))


######################################## ПРИНЯТИЕ ДАННЫХ ########################################
# Принятие текста для рассылки
@dp.message_handler(IsAdmin(), state="here_ad_text")
async def functions_ad_get(message: Message, state: FSMContext):
    await state.update_data(here_ad_text="📢 Рассылка.\n" + str(message.text))
    get_users = get_all_usersx()

    try:
        cache_msg = await message.answer(message.text)
        await cache_msg.delete()

        await state.set_state("here_ad_confirm")
        await message.answer(
            f"<b>📢 Отправить <code>{len(get_users)}</code> юзерам сообщение?</b>\n"
            f"{message.text}",
            reply_markup=ad_confirm_inl,
            disable_web_page_preview=True
        )
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📢 Введите текст для рассылки пользователям.\n"
                             "❕ Вы можете использовать HTML разметку.")

# Принятие айди или логина для поиска профиля
@dp.message_handler(IsAdmin(), state="here_profile")
async def functions_profile_get(message: Message, state: FSMContext):
    find_user = message.text

    if find_user.isdigit():
        get_user = get_userx(user_id=find_user)
    else:
        if find_user.startswith("@"): find_user = find_user[1:]
        get_user = get_userx(user_login=find_user.lower())

    if get_user is not None:
        await state.finish()
        await message.answer(open_profile_search(get_user['user_id']),
                             reply_markup=profile_search_finl(get_user['user_id']))
    else:
        await message.answer("<b>❌ Профиль не был найден</b>\n"
                             "👤 Введите логин или айди пользователя.")


# Принятие суммы для выдачи баланса пользователю
@dp.message_handler(IsAdmin(), state="here_profile_add")
async def functions_profile_balance_add_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        if 0 <= int(message.text) <= 1000000000:
            user_id = (await state.get_data())['here_profile']
            await state.finish()

            get_user = get_userx(user_id=user_id)
            update_userx(user_id, user_balance=get_user['user_balance'] + int(message.text))

            await message.answer(
                f"<b>✅ Пользователю <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> "
                f"выдано <code>{message.text}₽</code></b>")

            await message.bot.send_message(user_id, f"<b>💰 Вам было выдано <code>{message.text}₽</code></b>")
            await message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))
        else:
            await message.answer("<b>❌ Сумма выдачи не может быть меньше 1 и больше 1 000 000 000</b>\n"
                                 "💰 Введите сумму для выдачи баланса")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "💰 Введите сумму для выдачи баланса")


# Принятие суммы для изменения баланса пользователя
@dp.message_handler(IsAdmin(), state="here_profile_set")
async def functions_profile_balance_set_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        if 0 <= int(message.text) <= 1000000000:
            user_id = (await state.get_data())['here_profile']
            await state.finish()

            get_user = get_userx(user_id=user_id)
            update_userx(user_id, user_balance=message.text)

            await message.answer(
                f"<b>✅ Пользователю <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> "
                f"изменён баланс на <code>{message.text}₽</code></b>")

            await message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))
        else:
            await message.answer("<b>❌ Сумма изменения не может быть меньше 0 и больше 1 000 000 000</b>\n"
                                 "💰 Введите сумму для изменения баланса")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "💰 Введите сумму для изменения баланса")


# Отправка сообщения пользователю
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_message", state="*")
async def functions_profile_user_message(call: CallbackQuery, state: FSMContext):
    await state.update_data(here_profile=call.data.split(":")[1])

    await state.set_state("here_profile_message")
    await call.message.edit_text("<b>💌 Введите сообщение для отправки</b>\n"
                                 "⚠ Сообщение будет сразу отправлено пользователю.")

# Принятие сообщения для пользователя
@dp.message_handler(IsAdmin(), state="here_profile_message")
async def functions_profile_user_message_get(message: Message, state: FSMContext):
    user_id = (await state.get_data())['here_profile']
    await state.finish()

    get_message = "<b>💌 Вам сообщение:</b>\n" + clear_html(message.text)
    get_user = get_userx(user_id=user_id)

    await message.bot.send_message(user_id, get_message)
    await message.answer(f"<b>✅ Пользователю <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> "
                         f"было отправлено сообщение:</b>\n"
                         f"{get_message}")

    await message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))


# Принятие чека для поиска
@dp.message_handler(IsAdmin(), state="here_receipt")
async def functions_receipt_search(message: Message, state: FSMContext):
    receipt = message.text[1:]

    if message.text.startswith("#"):
        get_refill = get_refillx(refill_receipt=receipt)
        get_purchase = get_purchasex(purchase_receipt=receipt)

        if get_refill is not None:
            await state.finish()

            if get_refill['refill_way'] == "Form":
                way_input = "🥝 Способ пополнения: <code>По форме</code>"
            elif get_refill['refill_way'] == "Nickname":
                way_input = "🥝 Способ пополнения: <code>По никнейму</code>"
            elif get_refill['refill_way'] == "Number":
                way_input = "🥝 Способ пополнения: <code>По номеру</code>"
            else:
                way_input = f"🥝 Способ пополнения: <code>{get_refill['refill_way']}</code>"

            await message.answer(
                f"<b>🧾 Чек: <code>#{get_refill['refill_receipt']}</code></b>\n"
                "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"👤 Пользователь: <a href='tg://user?id={get_refill['user_id']}'>{get_refill['user_name']}</a> <code>({get_refill['user_id']})</code>\n"
                f"💰 Сумма пополнения: <code>{get_refill['refill_amount']}₽</code>\n"
                f"{way_input}\n"
                f"🏷 Комментарий: <code>{get_refill['refill_comment']}</code>\n"
                f"🕰 Дата пополнения: <code>{get_refill['refill_date']}</code>"
            )
            return
        elif get_purchase is not None:
            await state.finish()

            link_items = await upload_text(message, get_purchase['purchase_item'])
            await message.answer(
                f"<b>🧾 Чек: <code>#{get_purchase['purchase_receipt']}</code></b>\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"👤 Пользователь: <a href='tg://user?id={get_purchase['user_id']}'>{get_purchase['user_name']}</a> <code>({get_purchase['user_id']})</code>\n"
                f"🏷 Название товара: <code>{get_purchase['purchase_position_name']}</code>\n"
                f"📦 Куплено товаров: <code>{get_purchase['purchase_count']}шт</code>\n"
                f"💰 Цена 1-го товара: <code>{get_purchase['purchase_price_one']}₽</code>\n"
                f"💸 Сумма покупки: <code>{get_purchase['purchase_price']}₽</code>\n"
                f"🔗 Товары: <a href='{link_items}'>кликабельно</a>\n"
                f"🔻 Баланс до покупки: <code>{get_purchase['balance_before']}₽</code>\n"
                f"🔺 Баланс после покупки: <code>{get_purchase['balance_after']}₽</code>\n"
                f"🕰 Дата покупки: <code>{get_purchase['purchase_date']}</code>"
            )
            return

    await message.answer("<b>❌ Чек не был найден.</b>\n"
                         "🧾 Отправьте номер чека")
