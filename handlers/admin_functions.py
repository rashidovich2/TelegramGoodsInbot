# - *- coding: utf- 8 - *-
import asyncio
import math
import random
import json
import gettext
import urllib.request
from pathlib import Path
from contextvars import ContextVar

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink
from aiogram.utils.exceptions import CantParseEntities

from babel import Locale
from tgbot.data.config import BOT_TOKEN, get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
from tgbot.middlewares.i18n import I18nMiddleware

from tgbot.keyboards.inline_user import unwrap_post_finl, wrap_post_finl
from tgbot.keyboards.inline_admin import profile_search_finl, profile_search_reqs_finl, ad_add_to_plan_finl, ad_confirm_finl, ad_telegraph_finl, position_approve_reqs_finl, fund_add_confirmation_finl
from tgbot.keyboards.inline_z_all import ad_confirm_inl, ad_add_to_plan_inl
from tgbot.loader import dp, bot
from tgbot.services.api_sqlite import *
from tgbot.utils.misc.bot_filters import IsAdmin, IsAdminorShopAdmin
from tgbot.utils.misc_functions import open_profile_search, open_profile_search_req, upload_text, generate_sales_report, open_profile_search_seller, get_position_admin, get_refill_admin

#from munch import Munch

from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.upload_images import upload_image

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
print(i18n)
_ = i18n.gettext

async def track_message_send(user_id, post_id):
    await add_sending_postx(user_id, post_id)
    await asyncio.sleep(5)

# Рассылка
@dp.message_handler(IsAdmin(), text="📢 Рассылка_lite", state="*")
async def functions_mail(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_mail_text")
    await message.answer("<b>📢 Введите текст для рассылки пользователям</b>\n"
                         "❕ Вы можете использовать HTML разметку")

@dp.message_handler(IsAdmin(), state="here_mail_text")
async def functions_mail_get(message: Message, state: FSMContext):
    await state.update_data(here_mail_text="📢 Рассылка.\n" + str(message.text))
    get_users = get_all_usersx()

    try:
        cache_msg = await message.answer(message.text)
        await cache_msg.delete()

        await state.set_state("here_mail_confirm")
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

# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="plan_once_ad", state="*")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    get_users = get_all_usersx()
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    post_id = (await state.get_data())['post_id']
    ct = (await state.get_data())['ct']

    try:
        if get_action == "yes":
            cache_msg = await call.message.answer(f"Выбрано добавление в план:{ct}")
            await cache_msg.delete()

        await state.set_state("here_ad_post_confirm")
        post = get_postx(post_id)
        print(post)

        await call.message.answer(f"<b>📢 Отправить <code>{len(get_users)}</code> юзерам сообщение?</b>\n",
                                  reply_markup=ad_confirm_inl,
                                  disable_web_page_preview=True
                                  )
    except CantParseEntities:
        await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                               "📢 Введите текст для рассылки пользователям.\n"
                               "❕ Вы можете использовать HTML разметку.", locale=lang))


# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_ad", state="here_mail_confirm")
async def functions_mail_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

    send_message = (await state.get_data())['here_mail_text']
    get_users = get_all_usersx()
    await state.finish()

    if get_action == "yes":
        await call.message.edit_text(f"<b>📢 Рассылка началась... (0/{len(get_users)})</b>")
        asyncio.create_task(functions_mail_make(send_message, call))
    else:
        await call.message.edit_text("<b>📢 Вы отменили отправку рассылки ✅</b>")


# Сама отправка рассылки
async def functions_mail_make(message, call: CallbackQuery):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()
    get_time = get_unix()

    for user in get_users:
        try:
            await bot.send_message(user['user_id'], message, disable_web_page_preview=True)
            receive_users += 1
        except:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await call.message.edit_text(f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>")

        await asyncio.sleep(0.08)

    await call.message.edit_text(
        f"<b>📢 Рассылка была завершена за <code>{get_unix() - get_time}сек</code></b>\n"
        f"👤 Всего пользователей: <code>{len(get_users)}</code>\n"
        f"✅ Пользователей получило сообщение: <code>{receive_users}</code>\n"
        f"❌ Пользователей не получило сообщение: <code>{block_users}</code>"
    )


# Рассылка PRO
@dp.message_handler(text=["📢 Рассылка", "📢 Mass Send"], state="*")
async def functions_ad(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        await state.set_state("here_ad_post")
        await message.answer(_("<b>📢 Введите текст для рассылки пользователям</b>", locale=lang))

######################################## ПРИНЯТИЕ ДАННЫХ ########################################
# Принятие текста для рассылки
@dp.message_handler(state="here_ad_post", content_types=types.ContentType.ANY)
async def functions_ad_get(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    get_users = get_all_usersx()
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang, user_role)
    ct = 0
    shortlen = 450
    shortmestext = message.html_text[:449]

    if user_role in ["Admin", "ShopAdmin"]:
        print("P10P20R")
        mode = "tohour"
        if types.ContentType.TEXT == message.content_type:
            ct = 'text'
            print("!text message entered")
            await state.update_data(ct='text', here_ad_post=str(message.html_text))
            add_post_to_plan(ct, user_id, message.html_text, mode, caption='')
        elif types.ContentType.PHOTO == message.content_type:
            ct = 'photo'
            print("!photo message entered")
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

        try:
            cache_msg = await message.answer(f"Тип поста:{ct}")
            await state.update_data(post_id=post_id)
            print(post_id)
            user_id = message.from_user.id
            lang = get_userx(user_id=user_id)['user_lang']
            print(lang)
            await message.answer(_("<b>📢 Включить пост в ротацию бота?</b>", locale=lang),
                reply_markup=ad_add_to_plan_finl(post_id),
                disable_web_page_preview=True
            )
        except CantParseEntities:
            await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                                 "📢 Введите текст для рассылки пользователям.\n"
                                 "❕ Вы можете использовать HTML разметку.", locale=lang))



# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="telegraph_add", state="*")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    post_id = call.data.split(":")[1]
    get_action = call.data.split(":")[2]

    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    ct = (await state.get_data())['ct']
    print("ПУТЬ: Telegraph")
    #caption = (await state.get_data())['caption']
    #shortmestext = caption[0:400]

    t = TelegraphPoster(use_api=True)
    auth = t.create_api_token('Oleg Aliullov', 'Oleg', 'https://www.aliplaces.ru/') # second and third params are optional
    print(auth)

    #send_message = (await state.get_data())['here_ad_post']
    postt = get_postx(post_id)
    postj = {'post_id':postt['post_id'], 'post_text':postt['post_text'], 'post_photo':postt['post_photo'], 'post_file':f"{postt['post_id']}.png"}
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(postj, f, ensure_ascii=False, indent=4)

    if ct == "text":
        posttext = postt['post_text']
        image = upload_image("post_header.jpg")
    if ct == "photo":
        posttext = postt['caption']
        file_info = await bot.get_file(postt['post_photo'])
        print(file_info)
        destfilename = file_info.file_path.split('photos/')[1]
        filepath = file_info.file_path
        #path = str(f"{base_dir}{os.sep}photos")
        #fnum = random.randint(000000000, 999999999)
        #fname = f"{str(fnum)}.png"
        fname = f"{str(post_id)}.png"
        pdestf = f"/var/local/bot3101fc/tgbot/photos/{fname}"
        #pdestf = "/photos/" + destfilename
        print(pdestf)
        #fnum = random.randint(000000000, 999999999)
        #fname = fnum+".png"
        #print(destfilename, pdestf, filepatch)
        #await urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{filepath}', f'./{destifilename}')
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{filepath}', pdestf)
        filex = open(pdestf, 'rb')
        print(filex)
        #filex = open(photo_file, 'rb')
        image = upload_image(filex)
    #post = t.post(text=f'<blockquote>{posttext}</blockquote>')
    #print(post)
    post = t.post(title='Вакансия', author='требуется', text=f'<img src={image}><blockquote>{posttext}</blockquote>')
    print(post)

    shortmestext = f"{posttext[:400]}\n"
    print(shortmestext)
    hlinktext = hlink('читать далее..', post['url'])
    #shortmesturl = post['url']
    shortmestext += hlinktext
    print(shortmestext)

    users = [919148970,5620443733,5891026661]
    for user in users:
        if ct == "text":
            await dp.bot.send_message(user, shortmestext, disable_web_page_preview=True, parse_mode='HTML') #, reply_markup=unwrap_post_finl(user, post_id)
        if ct == "photo":
            await db.bot.send_photo(chat_id=user, photo=postt['post_photo'], caption=shortmestext, disable_web_page_preview=True)
            #await dp.bot.send_message(user, shortmestext, disable_web_page_preview=True, parse_mode='HTML')
    #image = upload_image("post_header.jpg")
    #print(image)
    #post = t.post(text=f'<img src={image}><blockquote>Really soft way</blockquote>')
    #print(post)

    #await dp.bot.send_photo(919148970, message, disable_web_page_preview=True)

    #post_id = (await state.get_data())['post_id']
    #print(post_id)
    mode = "evening"
    '''if ct == "text":
        #print("|")
        send_message = (await state.get_data())['here_ad_post']
        shortmestext = send_message[0:400]
        post = t.post(text=f'<blockquote>{send_message}</blockquote>')
        print(post)
        shortmestext += f'<a href={post.url}>читать далее..</a>'
        print(shortmestext)
        await dp.bot.send_message(919148970, shortmestext, disable_web_page_preview=True)
    elif ct == "photo":
        #print("||")
        send_photo = (await state.get_data())['here_ad_photo']
        caption = (await state.get_data())['caption']
        shortmestext = caption[0:400]
        post = t.post(text=f'<blockquote>{caption}</blockquote>')
        shortmestext += f'<a href={post.url}>читать далее..</a>'
        await dp.bot.send_photo(919148970, send_photo, shortmestext, disable_web_page_preview=True)
    elif ct == "video":
        print("|||")
        send_video = (await state.get_data())['here_ad_video']
        caption = (await state.get_data())['caption']
    elif ct == "animation":
        #print("||||")
        send_animation = (await state.get_data())['here_ad_animation']
        caption = (await state.get_data())['caption']

    get_users = get_all_usersx()
    await state.finish()

    if get_action == "yes":
        #await call.answer(f"{post_id}")
        await call.message.edit_text(f"<b>📢 Рассылка началась... (0/{len(get_users)})</b>")
        if ct == "text":
            asyncio.create_task(functions_adext_make(post_id, ct, send_message, 0, call))
        if ct == "photo":
            asyncio.create_task(functions_adext_make(post_id, ct, send_photo, caption, call))
        if ct == "video":
            asyncio.create_task(functions_adext_make(post_id, ct, send_video, caption, call))
        if ct == "animation":
            asyncio.create_task(functions_adext_make(post_id, ct, send_animation, caption, call))
    else:
        await call.message.edit_text(_("<b>📢 Вы отменили отправку рассылки ✅</b>", locale=lang))'''



# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_ad", state="here_ad_post_confirm")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    post_id = call.data.split(":")[1]
    get_action = call.data.split(":")[2]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    ct = (await state.get_data())['ct']
    #post_id = (await state.get_data())['post_id']
    #print(post_id)
    mode = "evening"
    if ct == "text":
        #print("|")
        send_message = (await state.get_data())['here_ad_post']
    elif ct == "photo":
        #print("||")
        send_photo = (await state.get_data())['here_ad_photo']
        caption = (await state.get_data())['caption']
    elif ct == "video":
        print("|||")
        send_video = (await state.get_data())['here_ad_video']
        caption = (await state.get_data())['caption']
    elif ct == "animation":
        #print("||||")
        send_animation = (await state.get_data())['here_ad_animation']
        caption = (await state.get_data())['caption']

    get_users = get_all_usersx()
    await state.finish()

    if get_action == "yes":
        #await call.answer(f"{post_id}")
        await call.message.edit_text(f"<b>📢 Рассылка началась... (0/{len(get_users)})</b>")
        if ct == "text":
            asyncio.create_task(functions_adext_make(post_id, ct, send_message, 0, call))
        if ct == "photo":
            asyncio.create_task(functions_adext_make(post_id, ct, send_photo, caption, call))
        if ct == "video":
            asyncio.create_task(functions_adext_make(post_id, ct, send_video, caption, call))
        if ct == "animation":
            asyncio.create_task(functions_adext_make(post_id, ct, send_animation, caption, call))
    else:
        await call.message.edit_text(_("<b>📢 Вы отменили отправку рассылки ✅</b>", locale=lang))


# Поиск профиля
@dp.message_handler(IsAdmin(), text=["🔍 Поиск профиля", "🔍 Find Profile"], state="*")
async def functions_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    await state.finish()

    await state.set_state("here_profile")
    await message.answer(_("<b>👤 Введите логин или айди пользователя</b>", locale=lang))


# Поиск чеков
@dp.message_handler(IsAdmin(), text=["🧾 Поиск чеков 🔍", "🧾 Find Receipts 🔍"], state="*")
async def functions_receipt(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    await state.finish()

    await state.set_state("here_receipt")
    await message.answer(_("<b>🧾 Отправьте номер чека</b>", locale=lang))


# Просмотр запросов продавцов
@dp.message_handler(text=["🧾 Ожидают подтверждения", "🧾 Успешные", "🧾 Wait Confirmation", "🧾 Success"], state="*")
async def functions_seller_requests(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        #await message.answer("<b>Все пополнения</b>")

        if message.text in ["🧾 Ожидают подтверждения", "🧾 Wait Confirmation"]:
            print("WAITCONFIRM")
            state = "waitconfirm"
        if message.text in ["🧾 Успешные", "🧾 Success"]:
            print("SUCCESS")
            state = "success"

        all_refills = get_all_funds_adds_stated(state)
        print(all_refills)

        if len(all_refills) >= 1: #(_("<b>🧾 Посмотрим поданные вакансии:</b>", locale=lang)
            await message.answer("<b>🧾 Пополнения:</b>")
            for refill in all_refills:
                #print(refill['refill_receipt'])
                get_message = await get_refill_admin(refill['refill_receipt'])
                await message.answer(get_message, reply_markup=fund_add_confirmation_finl(refill['refill_receipt'], lang))


# Просмотр запросов продавцов
@dp.message_handler(text=["🖍 Вакансии Созданные", "🖍 Positions Created", "🖍 Вакансии Согласованные", "🖍 Positions Approved", "🖍 Вакансии Опубликованные", "🖍 Positions Posted", "🖍 Вакансии в Вещании", "🖍 Positions in Broadcast"], state="*")
async def functions_seller_requests(message: Message, state: FSMContext):

    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        await message.answer(_("<b>🧾 Посмотрим поданные вакансии:</b>", locale=lang))

    if message.text in ["🖍 Вакансии Созданные", "🖍 Positions Created"]:
        print("CREATED")
        state = "Created"
    if message.text in ["🖍 Вакансии Согласованные", "🖍 Positions Approved"]:
        print("APPROVED")
        state = "Approved"
    if message.text in ["🖍 Вакансии Опубликованные", "🖍 Positions Posted"]:
        print("POSTED")
        state = "Posted"
    if message.text in ["🖍 Вакансии в Вещании", "🖍 Positions in Broadcasting"]:
        print("BROADCAST")
        state = "Broadcast"

    all_positions = get_all_positions_requestx_stated(state)

    if len(all_positions) >= 1:
        await message.answer(_("<b>🧾 Посмотрим поданные вакансии:</b>", locale=lang) + str(len(all_positions)) + "шт.")
        ten = []
        for position in all_positions:
            print(position['position_id'])
            get_message, get_photo = get_position_admin(position['position_id'])
            if get_photo is not None:
                await message.answer_photo(get_photo, get_message, reply_markup=position_approve_reqs_finl(position['position_id'], lang))
            else:
                await message.answer(get_position_admin(position['position_id']), reply_markup=position_approve_reqs_finl(position['position_id'], lang))


# Просмотр запросов продавцов
@dp.message_handler(text=["🖍 Посмотреть запросы", "🖍 Show list requests", "🖍 запросы Created", "🖍 запросы Approved", "🖍 requests Created", "🖍 requests Approved"], state="*")
async def functions_seller_requests(message: Message, state: FSMContext):

    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    if user_role in ['Admin', 'ShopAdmin']:
        await message.answer(_("<b>🧾 Посмотрим запросы продавцов:</b>", locale=lang))

    if message.text in ["🖍 запросы Created", "🖍 requests Created"]:
        print("CREATED")
        state = "created"
    if message.text in ["🖍 запросы Approved", "🖍 requests Approved"]:
        print("APPROVED")
        state = "Approved"
    if message.text in ["🖍 запросы Posted", "🖍 requests Posted"]:
        print("POSTED")
        state = "Posted"


    all_requesters = get_all_requestx_stated(state)

    #all_requesters = get_all_requestx()

    if len(all_requesters) >= 1:
        await message.answer(_("Запросы на роль продавца:", locale=lang) + str(len(all_requesters)) + "шт.")

        for requester in all_requesters:
            print(requester)
            #await state.finish()
            await message.answer(open_profile_search_req(requester['user_id'], lang), reply_markup=profile_search_reqs_finl(requester['user_id'], lang))



# Просмотр запросов продавцов
@dp.message_handler(IsAdmin(), text=["📊 Отчет о продажах", "📊 Sales Report"], state="*")
async def functions_seller_requests(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']

    await message.answer(generate_sales_report())

    '''get_users = get_purchasesbysellers()

    if len(get_users)>= 1:
        await message.answer(_("Топ - продавцов", locale=lang) + str(get_users) + _("шт.", locale=lang))

        for user in get_users:

            await message.answer(open_profile_search_seller(user_id=user['user_id']), reply_markup=profile_search_finl(user['user_id']))'''

########################################### CALLBACKS ###########################################
# Подтверждение отправки рассылки
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_ad2", state="here_ad_confirm")
async def functions_ad_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    send_message = (await state.get_data())['here_ad_text']
    get_users = get_all_usersx()
    await state.finish()

    if get_action == "yes":
        await call.message.edit_text(_("<b>📢 Рассылка началась... (0/", locale=lang) + len(get_users) + _(")</b>", locale=lang))
        asyncio.create_task(functions_ad_make(send_message, call))
    else:
        await call.message.edit_text(_("<b>📢 Вы отменили отправку рассылки ✅</b>", locale=lang))


# Покупки пользователя
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_purchases", state="*")
async def functions_profile_purchases(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    lang = get_userx(user_id=user_id)['user_lang']
    last_purchases = last_purchasesx(user_id, 10)

    if len(last_purchases) >= 1:
        await call.answer(_("🎁 Последние 10 покупок", locale=lang))
        await call.message.delete()

        for purchases in last_purchases:
            link_items = await upload_text(call, purchases['purchase_item'])
            if lang == "ru":
                await call.message.answer(f"<b>🧾 Чек: <code>#{purchases['purchase_receipt']}</code></b>\n"
                                          f"🎁 Товар: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}шт | {purchases['purchase_price']}₽</code>\n"
                                          f"🕰 Дата покупки: <code>{purchases['purchase_date']}</code>\n"
                                          f"🔗 Товары: <a href='{link_items}'>кликабельно</a>")
            if lang == "en":
                await call.message.answer(f"<b>🧾 Receipt: <code>#{purchases['purchase_receipt']}</code></b>\n"
                                          f"🎁 Product: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}pcs | {purchases['purchase_price']}₽</code>\n"
                                          f"🕰 Purchase Date: <code>{purchases['purchase_date']}</code>\n"
                                          f"🔗 Products: <a href='{link_items}'>clickable</a>")

        await call.message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))
    else:
        if lang == "ru":
            await call.answer("❗ У пользователя отсутствуют покупки", True)
        if lang == "en":
            await call.answer("❗ User don't have purchases", True)


# Отправка рассылки
async def functions_adext_make(post_id, ct, message, caption, call: CallbackQuery):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()
    user_id = call.from_user.id
    print(user_id)
    lang = get_userx(user_id=user_id)['user_lang']
    ANNOUNCE_ID = 1655831466
    #shortlen = 400
    print(post_id)

    for user in get_users:
        try:
            if ct == "text":
                shortmestext = message[:400]
                msg = await dp.bot.send_message(user['user_id'], shortmestext, disable_web_page_preview=True, reply_markup=unwrap_post_finl(user_id, post_id))
                msgid = msg.message_id
                print(post_id, msgid, "afterap01")
                sending_id = random.randint(1000000000, 9999999999)
                print(sending_id)
                add_sending_postx7(sending_id, user['user_id'], post_id, msgid, 'wrapped')

                await asyncio.sleep(0.5)

            elif ct == "photo":
                shortmestext = caption[:400]
                msg = await dp.bot.send_photo(
                    chat_id=user['user_id'],
                    photo=message,
                    caption=shortmestext or None,
                    disable_web_page_preview=True,
                    reply_markup=unwrap_post_finl(user_id, post_id)
                )

                msgid = msg.message_id
                print(post_id, msgid, "afterap02")
                sending_id = random.randint(1000000000, 9999999999)
                print(sending_id)
                add_sending_postx7(sending_id, user['user_id'], post_id, msgid, 'wrapped')

                await asyncio.sleep(0.5)

            elif ct == "video":
                await dp.bot.send_video(
                    chat_id=user['user_id'],
                    video=message,
                    caption=caption or None,
                )
            elif ct == "animation":
                await dp.bot.send_animation(
                    chat_id=user['user_id'],
                    animation=message,
                    caption=caption or None,
                )

            receive_users += 1
        except Exception:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await call.message.edit_text(
                f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>"
            )
        #_("<b>📢 Рассылка началась... (", locale=lang)
        await asyncio.sleep(0.05)

    if lang == "ru":
        await call.message.edit_text(
            f"<b>📢 Рассылка была завершена ✅</b>\n"
            f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
            f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
        )
    if lang == "en":
        await call.message.edit_text(
            f"<b>📢 Mass Sending has been finished ✅</b>\n"
            f"👤 Users Received Messages: <code>{receive_users} ✅</code>\n"
            f"👤 Users not Received Messages: <code>{block_users} ❌</code>"
        )

# Отправка рассылки
async def functions_adext_make7(post_id, ct, message, caption, call: CallbackQuery):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()
    #user_id = call.data.split(":")[1]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    ANNOUNCE_ID = 1655831466

    #shortlen = 400
    shortmestext = message[:400]
    #post_id = (await state.get_data())['post_id']
    print(post_id)

    for user in get_users:
        try:
            if ct == "text":
                msg = await dp.bot.send_message(user['user_id'], shortmestext, disable_web_page_preview=True)
                #asyncio.create_task(add_sending_postx(user['user_id'], post_id))
                await add_sending_postx(user['user_id'], post_id)
                await add_sending_postx3(user['user_id'], post_id)
                await add_sending_postx7(user['user_id'], post_id)
                await print(user['user_id'])
                #asyncio.create_task(track_message_send(user['user_id'], post_id))
                '''await dp.bot.forward_message(
                chat_id=1655831466, #1671959455,
                from_chat_id=user['user_id'], #6136080448, #message.chat.id,
                message_id=msg.message_id
                )'''
            elif ct == "photo":
                shortmestext = caption[:400]
                await dp.bot.send_photo(
                    chat_id=user['user_id'],
                    photo=message,
                    caption=shortmestext or None,
                )
                '''await dp.bot.forward_message(
                    chat_id=ANNOUNCE_ID,
                    from_chat_id=message.chat.id,
                    message_id=message.reply_to_message.message_id
                )'''
            elif ct == "video":
                await dp.bot.send_video(
                    chat_id=user['user_id'],
                    video=message,
                    caption=caption or None,
                )
            elif ct == "animation":
                await dp.bot.send_animation(
                    chat_id=user['user_id'],
                    animation=message,
                    caption=caption or None,
                )

            receive_users += 1
        except Exception:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await call.message.edit_text(
                f"<b>📢 Рассылка началась... ({how_users}/{len(get_users)})</b>"
            )
        #_("<b>📢 Рассылка началась... (", locale=lang)
        await asyncio.sleep(0.05)

    if lang == "ru":
        await call.message.edit_text(
            f"<b>📢 Рассылка была завершена ✅</b>\n"
            f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
            f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
        )
    if lang == "en":
        await call.message.edit_text(
            f"<b>📢 Mass Sending has been finished ✅</b>\n"
            f"👤 Users Received Messages: <code>{receive_users} ✅</code>\n"
            f"👤 Users not Received Messages: <code>{block_users} ❌</code>"
        )

# Отправка рассылки
async def functions_ad_make(message, call: CallbackQuery):
    receive_users, block_users, how_users = 0, 0, 0
    get_users = get_all_usersx()

    for user in get_users:
        try:
            await bot.send_message(user['user_id'], message, disable_web_page_preview=True)
            receive_users += 1
        except Exception:
            block_users += 1

        how_users += 1

        if how_users % 10 == 0:
            await call.message.edit_text(_("<b>📢 Рассылка началась... (", locale=lang) + str(how_users) + "/" + str(len(get_users)) + "</b>")

        await asyncio.sleep(0.05)

    await call.message.edit_text(
        f"<b>📢 Рассылка была завершена ✅</b>\n"
        f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
        f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>"
    )

# Подтверждение запроса продавца
@dp.callback_query_handler(IsAdmin(), text_startswith="position_post_request_approve", state="*")
async def functions_shopadmin_request_approve(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]

    user_id = call.from_user.id
    position = get_positionx(position_id=position_id)
    #update_userx(user_id, user_role="ShopAdmin")
    update_positionx(position_id, position_state="Approved")
    lang = "ru"
    #photo = f"img/seller_approved.png"
    #print(photo)

    #image = open(photo, 'rb')

    #await state.finish()
    #await call.message.answer_photo(image,
    #                                f"<b>✅ Пользователю <a href='tg://user?id={user_id}'>{get_user['user_name']}</a> "
    #                                f"изменена роль на: <code>{get_user['user_role']}</code></b>", reply_markup=menu_frep(user_id, lang))
    await call.message.answer(f"<b>✅ Позиция {position['position_id']}\n "
                              f"изменила статус на: <code>Согласовано</code></b>") #, reply_markup=menu_frep(user_id, lang)

    await dp.bot.send_message(position['position_user_id'], "<b> Поздравляем! Ваша вакансия была согласована и будет размещена в течении ближайшего часа.</b>")


# Отклонение запроса продавца
@dp.callback_query_handler(IsAdmin(), text_startswith="position_post_request_decline", state="*")
async def functions_shopadmin_request_decline(call: CallbackQuery, state: FSMContext):
    await state.finish()
    position_id = call.data.split(":")[1]
    print(position_id)
    position = get_positionx(position_id=position_id)
    update_positionx(position_id, position_state="Declined")
    #delete_position_requests_userx(position_id)

    #await call.answer(_(" Запрос был успешно удален.", locale=lang))
    await call.message.answer(f"<b>✅ Позиция {position['position_id']}\n "
                              f"изменила статус на: <code>Отклонена</code></b>") #, reply_markup=menu_frep(user_id, lang)

    await dp.bot.send_message(
        position['position_user_id'],
        "<b>Ваш запрос был отклонен. Вы можете попробовать подать следующий запрос через 4 часа.</b>"
    )

# Отклонение запроса продавца
@dp.callback_query_handler(IsAdmin(), text_startswith="position_post_request_delete", state="*")
async def functions_shopadmin_request_decline(call: CallbackQuery, state: FSMContext):
    await state.finish()
    position_id = call.data.split(":")[1]
    print(position_id)
    position = get_positionx(position_id=position_id)
    delete_position_requests_userx(position_id)

    await call.message.answer(f"<b> Вакансия ID {position_id} была удалена успешно.</b>")

    '''await dp.bot.send_message(
        user_id,
        _("<b>Ваши запросы на продавца былы удалены Администратором бота.</b>",
          locale=lang,
          ),
    )'''

# Выдача баланса пользователю
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_balance_add", state="*")
async def functions_profile_balance_add(call: CallbackQuery, state: FSMContext):
    await state.update_data(here_profile=call.data.split(":")[1])
    auser_id = call.from_user.id
    lang, user_role = get_userx(user_id=auser_id)['user_lang'], get_userx(user_id=auser_id)['user_role']

    await state.set_state("here_profile_add")
    await call.message.edit_text(_("<b>💰 Введите сумму для выдачи баланса</b>", locale=lang))


# Изменение баланса пользователю
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_balance_set", state="*")
async def functions_profile_balance_set(call: CallbackQuery, state: FSMContext):
    await state.update_data(here_profile=call.data.split(":")[1])
    auser_id = call.from_user.id
    lang, user_role = get_userx(user_id=auser_id)['user_lang'], get_userx(user_id=auser_id)['user_role']

    await state.set_state("here_profile_set")
    await call.message.edit_text(_("<b>💰 Введите сумму для изменения баланса</b>", locale=lang))


# Обновление профиля пользователя
@dp.callback_query_handler(IsAdmin(), text_startswith="admin_user_refresh", state="*")
async def functions_profile_refresh(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    auser_id = call.from_user.id
    lang, user_role = get_userx(user_id=auser_id)['user_lang'], get_userx(user_id=auser_id)['user_role']

    await call.message.delete()
    await call.message.answer(open_profile_search(user_id, lang), reply_markup=profile_search_finl(user_id))


######################################## СМЕНА СТАТУСОВ ПОЛЬЗОВАТЕЛЯ ############################

# Принятие суммы для выдачи баланса пользователю
@dp.callback_query_handler(IsAdmin(), state="here_user_request_approve")
async def functions_shopadmin_request_approvep(message: Message, state: FSMContext):
    user_id = (await state.get_data())['here_profile']
    await state.finish()

    get_user = get_userx(user_id=user_id)
    update_userx(user_id, user_role="ShopAdmin")
    lang = get_user(user_id=user_id)['user_lang']

    await message.answer(
        f"<b>✅ Пользователю <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> "
        f"изменена роль на: <code>{get_user['user_role']}</code></b>")

    await message.bot.send_message(
        user_id,
        _("<b> Вам была выдана роль Продавца магазина </b>", locale=lang),
    )
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
        await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📢 Введите текст для рассылки пользователям.\n"
                             "❕ Вы можете использовать HTML разметку.", locale=lang))

# Принятие айди или логина для поиска профиля
@dp.message_handler(IsAdmin(), state="here_profile")
async def functions_profile_get(message: Message, state: FSMContext):
    find_user = message.text
    auser_id = message.from_user.id
    lang, user_role = get_userx(user_id=auser_id)['user_lang'], get_userx(user_id=auser_id)['user_role']

    if find_user.isdigit():
        get_user = get_userx(user_id=find_user)
    else:
        if find_user.startswith("@"): find_user = find_user[1:]
        print(find_user)
        get_user = get_userx(user_login=find_user.lower())

    if get_user is not None:
        await state.finish()
        await message.answer(open_profile_search(get_user['user_id'], lang),
                             reply_markup=profile_search_finl(get_user['user_id'], lang))
    else:
        await message.answer(_("<b>❌ Профиль не был найден</b>"
                             "👤 Введите логин или айди пользователя.", locale=lang))


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
            await message.answer(_("<b>❌ Сумма выдачи не может быть меньше 1 и больше 1 000 000 000</b>\n"
                                 "💰 Введите сумму для выдачи баланса", locale=lang))
    else:
        await message.answer(_("<b>❌ Данные были введены неверно.</b>\n"
                             "💰 Введите сумму для выдачи баланса", locale=lang))


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
            await message.answer(_("<b>❌ Сумма изменения не может быть меньше 0 и больше 1 000 000 000</b>\n"
                                 "💰 Введите сумму для изменения баланса", locale=lang))
    else:
        await message.answer(_("<b>❌ Данные были введены неверно.</b>\n"
                             "💰 Введите сумму для изменения баланса", locale=lang))


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
    auser_id = message.from_user.id
    lang = get_userx(user_id=auser_id)['user_lang']
    await state.finish()

    get_message = _("<b>💌 Вам сообщение:</b>", locale=lang) + clear_html(message.text)
    get_user = get_userx(user_id=user_id)

    await message.bot.send_message(user_id, get_message)
    await message.answer(_("<b>✅ Пользователю ", locale=lang) + f"<a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a> "
                         + _("было отправлено сообщение:</b>", locale=lang) +
                         f"{get_message}")

    await message.answer(open_profile_search(user_id), reply_markup=profile_search_finl(user_id))


# Принятие чека для поиска
@dp.message_handler(IsAdminorShopAdmin(), state="here_receipt")
async def functions_receipt_search(message: Message, state: FSMContext):
    receipt = message.text[1:]
    get_refill = ""
    user_id = message.from_user.id
    #lang = get_userx(user_id=user_id)['user_lang']
    lang = "ru"

    if message.text.startswith("#"):
        get_refill = get_refillx(refill_receipt=receipt)
        get_purchase = get_purchasex(purchase_receipt=receipt)

        if get_refill is not None:
            await state.finish()

            '''if get_refill['refill_way'] == "Form":
                way_input = _("🥝 Способ пополнения: <code>По форме</code>", locale=lang)
            elif get_refill['refill_way'] == "Nickname":
                way_input = _("🥝 Способ пополнения: <code>По никнейму</code>", locale=lang)
            elif get_refill['refill_way'] == "Number":
                way_input = _("🥝 Способ пополнения: <code>По номеру</code>", locale=lang)
            else:'''
            way_input = f"🥝 Способ пополнения: <code>{get_refill['refill_way']}</code>"

            if lang == "en":
                await message.answer(
                    f"<b>🧾 Receipt: <code>#{get_refill['refill_receipt']}</code></b>\n"
                    "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                    f"👤 User: <a href='tg://user?id={get_refill['user_id']}'>{get_refill['user_name']}</a> <code>({get_refill['user_id']})</code>\n"
                    f"💰 Charge Amount: <code>{get_refill['refill_amount']}₽</code>\n"
                    f"{way_input}\n"
                    f"🏷 Comment: <code>{get_refill['refill_comment']}</code>\n"
                    f"🕰 Date of charge: <code>{get_refill['refill_date']}</code>"
                )
            elif lang == "ru":
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
            if lang == "en":
                await message.answer(
                    f"<b>🧾 Receipt: <code>#{get_purchase['purchase_receipt']}</code></b>\n"
                    f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                    f"👤 User: <a href='tg://user?id={get_purchase['user_id']}'>{get_purchase['user_name']}</a> <code>({get_purchase['user_id']})</code>\n"
                    f"🏷 Name of Product: <code>{get_purchase['purchase_position_name']}</code>\n"
                    f"📦 Products Purchased: <code>{get_purchase['purchase_count']}pcs</code>\n"
                    f"💰 Price for One Pieces: <code>{get_purchase['purchase_price_one']}R</code>\n"
                    f"💸 Summ of Purchaces: <code>{get_purchase['purchase_price']}R</code>\n"
                    f"🔗 Items: <a href='{link_items}'>кликабельно</a>\n"
                    f"🔻 Balance Before Purchase: <code>{get_purchase['balance_before']}R</code>\n"
                    f"🔺 Balance After Purchase: <code>{get_purchase['balance_after']}R</code>\n"
                    f"🕰 Purchase Date: <code>{get_purchase['purchase_date']}</code>"
                )

            elif lang == "ru":
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

    await message.answer(_("<b>❌ Чек не был найден.</b>\n"
                         "🧾 Отправьте номер чека", locale=lang))
