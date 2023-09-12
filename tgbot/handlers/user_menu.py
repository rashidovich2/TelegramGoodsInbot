# - *- coding: utf- 8 - *-
#from pathlib import Path
import os
from os import path
import asyncio
import json
import math
import random
import gettext

from pathlib import Path
from contextvars import ContextVar

from aiogram.dispatcher import FSMContext
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.utils.markdown import hlink
from aiogram import types
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR
#from tgbot.middlewares.i18n import I18nMiddleware
#from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
from aiogram_timepicker.panel import FullTimePicker, full_timep_callback, full_timep_default, \
    HourTimePicker, hour_timep_callback, MinuteTimePicker, minute_timep_callback, \
    SecondTimePicker, second_timep_callback, \
    MinSecTimePicker, minsec_timep_callback, minsec_timep_default
from aiogram_timepicker import result, carousel, clock

from tgbot.middlewares.i18n import I18nMiddleware

from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl, payment_choice_finl, artist_edit_open_finl, select_place_finl, profile_search_reqs_finl
from tgbot.keyboards.inline_user import user_support_finl, products_open_finl, products_confirm_finl, \
    products_addcart_confirm_finl, payment_as_choice_finl, accept_saved_adr, accept_saved_phone, \
    cart_enter_message_finl, give_number_inl, reply_order_message_finl, refill_choice_finl, charge_button_add, \
    switch_category_shop_finl, shop_creation_request_finl, event_open_finl, enter_promocode_finl, cart_open_created_finl, \
    cart_open_delivery_finl, edit_delivery_settings_finl, position_select_type_finl, checkout_step2_accept_finl, confirm_cart_del_finl, profile_open_finl, profile_seller_open_finl, refill_open_finl, partners_list_finl, position_select_local_finl, unwrap_post_finl, wrap_post_finl, choise_time_finl, places_list_finl
from tgbot.keyboards.inline_z_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl, confirm_delete_user_cart_inl
from tgbot.keyboards.inline_z_all import refill_open_inl, profile_open_inl, checkout_step2_accept, order_user_refill, profile_seller_open_inl
from tgbot.keyboards.inline_z_page import *
from tgbot.keyboards.reply_z_all import finish_load_rep
from tgbot.keyboards.reply_z_all import menu_frep, items_sh_frep, events_frep
from tgbot.keyboards.shop_keyboards import shop_edit_open_fp
from tgbot.loader import dp
from tgbot.loader import bot
#from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_sqlite_shop import *
from tgbot.services.api_sqlite import *
from tgbot.utils.const_functions import get_date, split_messages, get_unix, clear_list
from tgbot.utils.misc.bot_filters import IsShopAdmin, IsAdminorShopAdmin, IsAdmin
from tgbot.utils.misc_functions import user_refill_my, calc_cart_summ, calc_order_summ, open_cart_orders, open_profile_my, upload_text, get_faq, send_admins
from tgbot.utils.misc_functions import get_position_admin, upload_text, get_artist_admin, functions_position_notify_bg, approve_new_product_notify, open_profile_search_req, post_position_to_telegraph
from tgbot.keyboards.location_keyboards import geo_1_kb
from tgbot.services.location_function import update_position_city, get_city_info, is_location, update_artist_city
from tgbot.services.location_stat import geo_choice
from tgbot.keyboards.location_keyboards import geo_11_kb

from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.upload_images import upload_image

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext



async def notify(dp: Dispatcher, msg):
    print(f'Уведомление!{msg}')
    await send_admins(msg, markup="default")



################################################################################################

# Создание новой позиции
@dp.message_handler(text=["💼 Создать вакансию", "💼 Create Vacancy"], state="*")
async def product_position_create(message: Message, state: FSMContext):
    await state.finish()
    print("APS 74")
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    await state.set_state("here_vacposition_city")
    #await state.set_state("here_position_photo")
    await dp.bot.send_message(chat_id=user_id, text="<b>Выберите город вакансии или Россия/Мир для позиций с возможностью удаленной работы.</b>", disable_web_page_preview=True, reply_markup=places_list_finl())
    #await message.answer("<b>Выберите город вакансии или Россия/Мир для позиций с возможностью удаленной работы.</b>") #, reply_markup=places_list_finl() , reply_markup=places_list_finl()


'''@dp.message_handler(IsAdminorShopAdmin(), state="here_position_name")
async def product_position_create_name(message: Message, state: FSMContext):
    print('Принятие имени для создания позиции  user_menu.py 1084')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        await state.update_data(here_position_name=clear_html(message.text))

        await state.set_state("here_vacposition_photo")
        await message.answer("<b>Добавьте изображение вакансиии и текст в описание изображения, либо введите текст, если вакансия не содержит изображения.</b>")
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")'''


@dp.callback_query_handler(text_startswith="position_city:", state="*")
async def product_position_create_name(call: CallbackQuery, state: FSMContext):
    print('Принятие города для создания позиции  user_menu.py 1084')
    place_url = call.data.split(":")[1]
    user_id = call.from_user.id
    print(place_url)
    #lang = get_userx(user_id=user_id)['user_lang']
    if place_url:
        await state.update_data(here_position_city=place_url)

        await state.set_state("here_vacposition_photo")
        await call.message.answer("<b>Добавьте изображение вакансиии и текст в описание изображения, либо введите текст, если вакансия не содержит изображения.</b>")
    else:
        await call.message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")


@dp.message_handler(state="here_position_photo")
async def product_position_create_name(message: Message, state: FSMContext):
    print('Принятие имени для создания позиции  user_menu.py 1084')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        await state.update_data(here_position_name=clear_html(message.text))

        await state.set_state("here_vacposition_photo")
        await message.answer("<b>Добавьте изображение вакансиии и текст в описание изображения, либо введите текст, если вакансия не содержит изображения.</b>")
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")


# Принятие изображения позиции для её создания
@dp.message_handler(content_types=types.ContentType.ANY, state="here_vacposition_photo")
@dp.message_handler(text="0", state="here_vacposition_photo")
async def product_position_create_photo(message: Message, state: FSMContext):
    print('Принятие изображения позиции  admin_products.py 418')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    position_type = 3
    async with state.proxy() as data:
        position_user_id = message.from_user.id
        vacs_url = data['here_position_city']
        position_state = "Created" if vacs_url == "ALL_CHANNELS" else "Approved"
            #position_name = clear_html(data['here_position_name'])

    await state.finish()

    print("POSITION ADDED")
    position_id = random.randint(1000000000, 9999999999)

    if types.ContentType.TEXT == message.content_type:
        ct = 'text'
        print("!text message entered")
        await state.update_data(ct='text', here_position_description=str(message.html_text))
    elif types.ContentType.PHOTO == message.content_type:
        ct = 'photo'
        print("!photo message entered")
        position_description=message.html_text if message.caption else None
        position_photo = "" if "text" in message else message.photo[-1].file_id
        photo_name = f"/var/local/bot3101fc/tgbot/images/position{position_id}.png"
        await message.photo[-1].download(destination_file=photo_name)
        await state.update_data(ct="photo", here_position_photo=message.photo[-1].file_id, caption=position_description)

    add_position_vacx(position_id, position_type, position_photo, position_description, position_user_id, position_state, vacs_url)

    position = get_positionx(position_id=position_id)
    shortml = 200
    descritionlen = len(position_description)
    if descritionlen >= shortml:
        shortmestext = f"{position_description[:shortml]}\n"
    else:
        shortmestext = position_description

    #||| ПОСТИМ В TELEGRAPH
    t = TelegraphPoster(use_api=True, convert_html=True, clean_html=True)
    auth = t.create_api_token('Oleg Aliullov', 'Oleg', 'https://www.aliplaces.ru/') # second and third params are optional
    print(auth)
    filex = open(photo_name, 'rb')
    print(filex)
    image = upload_image(filex)
    article = t.post(title=f'Вакансия №: {position_id}', author='', text=f'<img src={image}>{position_description}') #title='Вакансия',
    print(article)
    #author='требуется',
    update_positionx(position_id, article_url = article['url'])

    #добавляем ссылку на полную версию
    if descritionlen < shortml:
        hlinktext = hlink('читать далее..', article['url'])
        shortmestext += hlinktext
    else: shortmestext = position_description

    #|||| СОХРАНЯЕМ В JSON
    positionj = {"position_id": position_id, "position_description": position['position_description'], "position_photo": position['position_photo'], "position_file": photo_name, "article_url": article['url'], "position_state": "Created", "vacs_url": vacs_url}
    print(positionj)
    exist_positions = []
    filename = 'positions.json'
    if path.isfile('positions.json') is False:
        raise Exception("File not found")

    with open(filename) as f:
        exist_positions = json.load(f)

    print(exist_positions)

    if len(exist_positions) == 0:
        exist_positions = positionj
        print("EMPTY JSON FILE")

    else:
        print("JSON FILE WITH DATA")
        print(exist_positions)
        print(type(exist_positions))
        exist_positions.append(positionj)

    print(exist_positions)

    with open('positions.json', 'w', encoding='utf-8') as f:
        json.dump(exist_positions, f, ensure_ascii=False, indent=4, separators=(',',': '))
    f.close()


    await notify(dp, f"Создана позиция: {position_id}, пользователем ID: {position_user_id}")

    if ct == "photo":
        await message.answer_photo(photo=position_photo, caption=f"{shortmestext}")

    elif ct == "text":
        await message.answer(f"{shortmestext}")
    await message.answer(_("<b>📁 Позиция была успешно создана ✅</b>", locale=lang))
    await asyncio.create_task(await approve_new_product_notify(position_id, markup=None))


@dp.callback_query_handler(text_startswith="position_notify:", state="*")
async def product_position_notify_approve(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    decision = call.data.split(":")[2]

    print(position_id, decision)

    user_id = call.from_user.id

    if decision == "yes":
        await functions_position_notify_bg(position_id, markup=None)

    if decision == "no":
        await call.answer("<b>📁 Вы отменили рассылку позиции 🖍</b>",
                          reply_markup=menu_frep(user_id, "ru"))


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(call: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    user_id = call.from_user.id
    print(user_id)
    #await state.set_state("here_position_time_selection")
    if selected:
        #async with state.proxy() as data:
        #    position_id = data['here_position_id']
        #    print(position_id)
        lang = "ru"
        await dp.bot.send_message(
            chat_id=user_id,
            text=f'Вы выбрали: {date.strftime("%d/%m/%Y")}',
            reply_markup=menu_frep(user_id, lang)
            )

        '''await dp.bot.send_message(
            chat_id=user_id,
            text=f"Пожалуйста, выберите время для постинга позиции:",
            reply_markup=choise_time_finl(position_id)
            )'''

@dp.callback_query_handler(text="choise_time", state="here_position_time_selection")
async def full2_picker_handler(call: CallbackQuery):
    position_id = int(call.data.split(":")[1])
    print("PT")
    await call.message.answer(
        "Пожалуйста, выберите время публикации вакансии: ",
        reply_markup=await HourTimePicker().start_picker()
    )



@dp.callback_query_handler(hour_timep_callback.filter())
async def process_hour_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await HourTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        user_id = call.from_user.id
        lang = "ru"
        await call.message.answer(
            f'Вы выбрали {r.hours}',
            reply_markup=menu_frep(user_id, lang)
        )
        await state.update_data(here_position_plan_hour=r.hours)
        await state.set_state("here_vacposition_plan_post_position")
        await call.message.delete_reply_markup()


@dp.message_handler(state="here_vacposition_plan_post_position")
async def full2_picker_handler(message: Message, state: FSMContext):

    async with state.proxy() as data:
        position_plan_date = data['here_position_plan_date']
        position_plan_time = data['here_position_plan_time']
        position_id = data['here_position_id']

        update_positionx(position_id, position_datetime=f"{position_plan_date} {position_plan_time}")

    await message.answer(
        "Время публикации поста установлено успешно! ",
        reply_markup=menu_frep(user_id, lang)
    )


@dp.callback_query_handler(text_startswith="position_planning:", state="*")
async def product_position_planning_approve(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    decision = call.data.split(":")[2]

    print(position_id, decision)

    user_id = call.from_user.id

    if decision == "yes":
        await state.set_state("position_planning")
        await state.update_data(here_position_id=position_id)
        #await functions_position_planning(position_id, markup=None)
        await dp.bot.send_message(
            chat_id=user_id,
            text="Пожалуйста, выберите дату для постинга позиции:",
            reply_markup=await SimpleCalendar().start_calendar(),
        )

    if decision == "no":
        await update_positionx(position_id, position_state="Approved")
        #await functions_position_notify_bg(position_id, markup=None)
        await call.answer("<b>📁 Отправляем позицию в канал 🖍</b>",
                          reply_markup=menu_frep(user_id, "ru"))


@dp.callback_query_handler(text_startswith="pr_broadcast:", state="*")
async def product_position_planning_approve(call: CallbackQuery):
    position_id = int(call.data.split(":")[1])
    decision = call.data.split(":")[2]

    if decision == "yes":
        await update_positionx(position_id, position_state="Broadcast")

        user_id = call.from_user.id

        await call.answer("<b>📁 Начинаем броадкаст поста 🖍</b>",
                          reply_markup=menu_frep(user_id, "ru"))


# Заявка на продавца магазина
# Открытие товаров
@dp.message_handler(text=["Я продавец", "I'm seller"], state="*")
async def user_seller_request(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    print("LLLLLL")
    if user_requests := get_requestx(requester=user_id):
        await message.answer("У Вас уже есть запросы продавца |||| Если админ Вам не подтвердил запрос, напишите: @raclear")
        #for request in user_requests:
        #print(request)
        await message.answer(open_profile_search_req(user_id, lang), reply_markup=menu_frep(user_id, lang))
    await state.set_state("here_seller_request_direction")
    await message.answer(_("<b>📁 Введите тип товара, который Вы будете продавать:</b>", locale=lang))

# Открытие товаров
@dp.message_handler(text=["Админ Афиши", "Events Admin"],state="*")
async def user_seller_request(message: Message, state: FSMContext):
    # await state.finish()
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    await state.set_state("here_afisha_admin_request_direction")
    await message.answer(_("<b>📁 Опишите пожалуйста события или среду, которые Вы создаете:</b>", locale=lang))


# Управление событиями IsAdminorShopAdmin(),
@dp.message_handler(text=['🎫 Управление событиями 🖍', '🎫 Events Management 🖍'], state="*")
async def admin_products(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    lang = get_userx(user_id=user_id)['user_lang']
    if user_role in ['Admin', 'ShopAdmin']:

        await state.finish()
        await message.answer(_("<b>🎫 Редактирование событий.</b>", locale=lang), reply_markup=events_frep(lang))
    else:

        await state.finish()
        await message.answer("<b>🎫 У Вас недостаточно прав для доступа в данный раздел.</b>")


# Развернуть пост
@dp.callback_query_handler(text_startswith="unwrap_post:", state="*")
async def unwrap_post(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])
    post_id = int(call.data.split(":")[2])
    print(user_id, post_id)

    get_post = get_postx(post_id)
    get_spost = get_sending_postxx(user_id, post_id)
    #print(get_post)
    #if get_post['ct']=="text":
    #mtext = get_post['post_text']
    #mtext = "DFGHFGHFGHGH"
    #print(mtext)

    #await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text=mtext, disable_web_page_preview=True, reply_markup=wrap_post_finl(user_id, post_id))
    #await call.message.edit_text(chat_id=call.from_user.id, message_id=get_post['msgid'], text=mtext, reply_markup=wrap_post_finl(user_id, post_id))
    #await dp.bot.edit_message_text(chat_id=call.from_user.id, message_id=get_spost['msgid'], text=mtext, disable_web_page_preview=True, reply_markup=wrap_post_finl(user_id, post_id))
    if get_post['ct']=="text":
        mtext = get_post['post_text']
        await dp.bot.edit_message_text(chat_id=call.from_user.id, message_id=get_spost['msgid'], text=mtext, disable_web_page_preview=True, reply_markup=wrap_post_finl(user_id, post_id))
    if get_post['ct']=="photo":
        mtext = get_post['post_text']
        await dp.bot.edit_message_caption(chat_id=call.from_user.id, message_id=get_spost['msgid'], caption=mtext, disable_web_page_preview=True, reply_markup=wrap_post_finl(user_id, post_id))


# Свернуть пост
@dp.callback_query_handler(text_startswith="wrap_post:", state="*")
async def wrap_post(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])
    post_id = int(call.data.split(":")[2])
    print(user_id, post_id)

    get_post = get_postx(post_id)
    get_spost = get_sending_postxx(user_id, post_id)
    #print(get_post)
    #if get_post['ct']=="text":
    #mtext = get_post['post_text']
    #shortmtext = mtext[0:400]
    #await call.message.edit_text(chat_id=call.from_user.id, message_id=get_post['msgid'], text=shortmtext, reply_markup=wrap_post_finl(user_id, post_id))
    #await dp.bot.message.edit_text(chat_id=call.from_user.id, text=mtext, disable_web_page_preview=True, reply_markup=unwrap_post_finl(user_id, post_id))
    if get_post['ct']=="text":
        mtext = get_post['post_text']
        await dp.bot.edit_message_text(chat_id=call.from_user.id, message_id=get_spost['msgid'], text=mtext, disable_web_page_preview=True, reply_markup=unwrap_post_finl(user_id, post_id))
    if get_post['ct']=="photo":
        mtext = get_post['post_text']
        await dp.bot.edit_message_caption(chat_id=call.from_user.id, message_id=get_spost['msgid'], caption=mtext, disable_web_page_preview=True, reply_markup=unwrap_post_finl(user_id, post_id))

# Управление товарами
@dp.message_handler(IsShopAdmin(), text="🎁 Управление товарами дмаг.🖍", state="*")
async def shopadmin_products(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    await state.finish()
    await message.answer(_("<b>🎁 Редактирование товаров дмаг.</b>", locale=lang), reply_markup=items_sh_frep())


@dp.message_handler(text=["🗃 Создать категорию ➕", "🗃 Create Category ➕"], state="*")
async def product_category_create(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)

    await state.finish()
    await state.set_state("here_category_name")
    await message.answer(_("<b>🗃 Введите название для категории 🏷</b>", locale=lang))


# Начальные категории для изменения позиции
@dp.message_handler(text=["📁 Изменить позицию 🖍", "📁 Edit Position 🖍"], state="*")  # !!!!!!!   Изменить позицию
async def product_position_edit(message: Message, state: FSMContext):
    print('📁 Изменить позицию 🖍 user_menu.py 56')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    city_id = get_city_user(user_id)[0]

    if user_role in ["Admin", "ShopAdmin"]:
        await state.finish()
        action = "edit"
        await message.answer(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                             reply_markup=products_item_category_swipe_fp(0, 0, city_id, action, lang))

# Открытие товаров
@dp.message_handler(text=["🎁 Купить", "🎁 Buy"], state="*")
async def user_shop(message: Message, state: FSMContext):
    print('Открытие категорий товаров user_menu.py 154')
    await state.finish()

    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    action = "open"

    get_settings = get_settingsx()
    if(get_settings['type_trade'] != 'digital'):
        user_city = get_user_city(message.from_user.id)
        user_city_id = user_city[1]
        user_city_name = user_city[0]
        print(user_city_id)

        if len(get_category_in_city(user_city_id)) >= 1:
            await message.answer(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                 reply_markup=products_item_category_swipe_fp(0, 0, user_city_id, action, lang))
        else:
            await message.answer(_("<b>🎁 В Вашем городе товаров нет, но Вы можете разместить свои, отправив запрос продавца или как частное лицо, выбрав пункт Продать</b>"
                                 "\n"
                                 "🏙 Изменить город вы можете в личном кабинете", locale=lang))
    else:
        await message.answer(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                             reply_markup=products_item_category_swipe_fp(0, 0, 0, action, lang))


# Открытие товаров
@dp.callback_query_handler(text_startswith="privateMarket", state="*")
async def private_user_shop(call: CallbackQuery, state: FSMContext):
    print('Открытие барахолки user_menu.py 65')
    await state.finish()
    category_id, remover, level, parent, city_id = 0, 0, 0, 0, 0
    print("<*|||privateMarket|||*>")
    action = "open"

    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print("IIII")

    pm_cats = get_pm_category_count()

    get_settings = get_settingsx()
    print("IIIII")
    if(get_settings['type_trade'] != 'digital'):
        user_city = get_user_city(call.from_user.id)
        city_id = user_city[1]
        user_city_name = user_city[0]
        print(city_id)
        print(category_id, remover, level, parent, city_id, action, lang)

        #if len(get_category_in_city(city_id)) >= 1:
        if len(pm_cats) > 0:
            await call.message.edit_text(_("<b>🎁 Выберите нужную вам категорию:</b>", locale=lang),
                                 reply_markup=position_people_create_open_fp(category_id, remover, level, parent, city_id, action, lang))
        else:
            await call.message.edit_text("<b>🎁 В вашем городе товаров нет, выберите другой город</b>\n"
                                      "🏙 Изменить город вы можете в личном кабинете")
    else:
        await call.message.edit_text(_("<b>🎁 Выберите нужную вам категорию:</b>", locale=lang),
                             reply_markup=position_people_create_open_fp(category_id, remover, level, parent, city_id, action, lang))




# Открытие товаров
@dp.message_handler(text=["🏫 Кружки", "🏫 Сources"], state="*")
async def user_shop(message: Message, state: FSMContext):
    print('Открытие категорий товаров  user_menu.py 65')
    await state.finish()

    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    source = "people"
    action = "open"

    get_settings = get_settingsx()
    if (get_settings['type_trade'] != 'digital'):
        city_id = get_city_user(message.from_user.id)[0]

    await message.answer(_("<b>📁 Выберите категорию для Вашей позиции</b>", locale=lang),
                         reply_markup=cources_opcr_fp(0, 0, 0, 0, city_id, action, lang))


# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="cources_category_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    level = int(call.data.split(":")[3])
    parent = int(call.data.split(":")[4])
    city_id = int(call.data.split(":")[5])
    action = call.data.split(":")[6]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)

    await call.message.edit_text("<b>🌐 Выберите категорию:</b>",
                                 reply_markup=cources_opcr_fp(category_id, remover, level, parent, city_id, action, lang))


# Выбор категории для создания позиции 1TODO
@dp.callback_query_handler(text_startswith="cources_open_here:", state="*")
async def product_position_open_select_category(call: CallbackQuery, state: FSMContext):
    print('position_people_open_here - user_menu 160')
    category_id = int(call.data.split(":")[1])
    print(category_id)
    get_category = get_curcategory_in_citypx(category_id=category_id)
    #if len(get_category) == 0: category_id = 0
    city_id = get_city_user(call.from_user.id)[0]
    get_positions = get_cources_in_cityx(category_id=category_id, position_city_id=city_id, flagallc=1, position_type=1)  # get_positionsx(category_id=category_id)
    print(get_positions)
    print(category_id, city_id)
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(get_positions) >= 1:
        #source = "people"
        await call.message.edit_text(f"<b>🎁 Курсы в локации: {get_category['category']}</b>",
                                     reply_markup=products_item_position_swipe_fp(0, category_id, city_id, lang))
    else:
        await call.answer(f"❕ Товары в категории {get_category['category']} отсутствуют")

# Открытие товаров
@dp.message_handler(text=["🌐 Продать", "🌐 Sell"], state="*")
async def user_shop(message: Message, state: FSMContext):
    print('Открытие категорий товаров  user_menu.py 65')
    await state.finish()

    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    source = "people"
    action = "create"

    get_settings = get_settingsx()
    if (get_settings['type_trade'] != 'digital'):
        city_id = get_city_user(message.from_user.id)[0]

    await message.answer(_("<b>📁 Выберите категорию для Вашей позиции</b>", locale=lang),
                         reply_markup=position_people_create_open_fp(0, 0, 0, 0, city_id, action, lang))

# Открытие товаров
@dp.message_handler(text=["🎁 Магазины", "🎁 Shops"], state="*")
async def user_shop(message: Message, state: FSMContext):
    print('Открытие магазинов товаров  user_menu.py 65')
    await state.finish()

    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    get_settings = get_settingsx()
    if(get_settings['type_trade'] != 'digital'):
        city_id = get_city_user(message.from_user.id)[0]
        if len(get_shops_on_city(city=city_id)) >= 1:
            await message.answer(_("<b>🎁 Выберите нужный вам магазин:</b>", locale=lang),
                                 reply_markup=products_item_shop_swipe_fp(0, city_id, lang))
        else:
            await message.answer("<b>🎁 В вашем городе товаров нет, выберите другой город</b>\n\n"
                                 "🏙 Изменить город вы можете в личном кабинете")
    else:
        await message.answer(_("<b>🎁 Выберите нужный вам магазин:</b>", locale=lang),
                             reply_markup=products_item_shop_swipe_fp(0, 0, lang))


# Открытие товаров
@dp.message_handler(text=["Афиша", "Events"], state="*")
async def user_afisha(message: Message, state: FSMContext):
    print('Открытие афишы  user_menu.py 115')
    await state.finish()

    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if is_location(message.from_user.id) == True:
        user_city = get_user_city(message.from_user.id)
        user_city_id = user_city[1]
        user_city_name = user_city[0]
        print(user_city_id, lang)
        if len(get_events_in_cityx(user_city_id, flagallc=1, position_type=1)) >= 1:
            await message.answer(_("<b>Выберите интересное для Вас:</b>", locale=lang),
                                 reply_markup=events_in_city_swipe_fp(0, user_city_id, lang))
        else:
            await message.answer("<b>🎁 В Вашем городе событий пока на размещено, но Вы можете разместить сами, отправив запрос Администратора Афишы.</b>\n\n"
                                 "🏙 Чтобы посмотреть события в другом городе достаточно изменить город в Профиле.")

    else:
        await geo_choice.location.set()
        await message.answer(_('Отправьте локацию или выберите город из списка чтобы увидеть события в Вашем городе', locale=lang), reply_markup=geo_11_kb(lang))


# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="events_city_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if remover == 0:
        await call.message.answer(_("<b>События в городе, выберите что-нибудь интересное:</b>", locale=lang),
                                  reply_markup=events_in_city_swipe_fp(remover, city_id, lang))
    else:
        await call.message.edit_text(_("<b>События в городе, выберите что-нибудь интересное:</b>", locale=lang),
                                     reply_markup=events_in_city_swipe_fp(remover, city_id, lang))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="events_place_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    place_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if remover == 0:
        await call.message.answer(_("<b>События в месте, выберите что-нибудь интересное:</b>", locale=lang),
                                  reply_markup=events_in_place_swipe_fp(remover, place_id, city_id, lang))
    else:
        await call.message.edit_text(_("<b>События в месте, выберите что-нибудь интересное:</b>", locale=lang),
                                     reply_markup=events_in_place_swipe_fp(remover, place_id, city_id, lang))


# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="places_city_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    await call.message.edit_text(_("<b>События в городе, выберите что-нибудь интересное:</b>", locale=lang),
                                 reply_markup=places_in_city_swipe_fp(remover, city_id, lang))



# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="open_inline_support", state="*")
async def open_inline_support(call: CallbackQuery, state: FSMContext):
    user_support = get_settingsx()['misc_support']

    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if str(user_support).isdigit():
        get_user = get_userx(user_id=user_support)
        await call.message.answer(_("<b>Напишите, что Вы хотите добавить, мы добавим.:</b>", locale=lang),
                                  reply_markup=user_support_finl(get_user['user_login']))
        return
    else:
        update_settingsx(misc_support="None")
        await message.answer(f"☎ Поддержка. Измените их в настройках бота.\n➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}",
                             disable_web_page_preview=True)

# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="book_event_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print('Карточка товара: user_menu.py  152')
    event_id = int(call.data.split(":")[1])
    place_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    city_id = get_city_user(call.from_user.id)[0]
    get_event = get_eventxx(event_id=event_id)

    get_settings = get_settingsx()
    print(get_event)

    if get_event['event_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_event['event_description']}"

    send_msg = f"<b>Мероприятие:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_event['event_name']}</code>\n" \
               f"🏙 Город: <code>{get_event['event_city']}</code>\n" \
               f"{text_description}"

    print(get_settings['type_trade'])
    tt = get_settings['type_trade']

    if (
        tt != "digital"
        and len(get_event['event_photo']) >= 5
        or tt == "digital"
        and len(get_position['event_photo']) >= 5
    ):
        print("\|")
        await call.message.delete()
        await call.message.answer_photo(get_event['event_photo'],
                                        send_msg, reply_markup=event_open_finl(event_id, 0, place_id, city_id, lang))
    else:
        print("\||")
        await call.message.edit_text(send_msg,
                                     reply_markup=event_open_finl(event_id, 0, place_id, city_id, lang))

# Открытие пополнения счета
@dp.message_handler(text=["💰 Пополнить", "💰 Top Up"], state="*")
async def user_refill_b(message: Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    print(lang)

    await message.answer(user_refill_my(message.from_user.id, lang), reply_markup=refill_open_finl(lang))


# Открытие профиля
@dp.message_handler(text=["👤 Профиль", "👤 Profile"], state="*")
async def user_profile(message: Message, state: FSMContext):
    print("||==")
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    print("|||===")
    if user_role in ["ShopAdmin", "Admin"]:
        await state.finish()
        print("||||+===")
        await message.answer(open_profile_my(message.from_user.id), reply_markup=profile_seller_open_inl) #await (lang)message.answer(open_profile_my(message.from_user.id), reply_markup=profile_seller_open_finl(lang))
        #await message.answer(open_profile_my(message.from_user.id), reply_markup=profile_seller_open_finl(lang)) #profile_seller_open_finl(lang)(lang)
    else:
        await state.finish()
        print("||||++====")
        await message.answer(open_profile_my(message.from_user.id), reply_markup=profile_open_inl) #(lang)

# Открытие профиля
@dp.message_handler(text=["Партнеры", "Partners"], state="*")
async def open_partners_list(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Наши славные партнеры:", reply_markup=partners_list_finl())

# Открытие корзины
@dp.message_handler(text=['🧮 Корзина', '🚛 Заказы', '🧮 Cart', '🚛 Orders'], state="*")
async def user_cart(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    orderdata = []
    if message.text in ['🧮 Корзина', '🧮 Cart']: #заказы покупателя
        orderdata = get_params_orderx(user_id=user_id)
        if len(orderdata) == 0:
            await message.answer("В Вашей корзине пока нет товаров. Посмотрите категории[кнопка Купить] или товары Магазинов.")

    if message.text in ['🚛 Заказы', '🚛 Orders']: #заказы продавца | представление от заказа к строке
        if user_id in get_userx(user_role='ShopAdmin') or user_id in get_userx(user_role='Admin'):
            orderdata = get_params_orderxx(owner_uid=user_id)
        elif user_id in get_admins():
            orderdata = get_alladmin_orderx()
        else:
            await message.answer("Недостаточно доступа для просмотра заказов!")

    if message.text == '🚛 Заказы А': #заказы админа площадки
        orderdata = get_params_orderxx(owner_uid=user_id)

    #print(orderdata)

    for order in orderdata:
        #print(order['order_state'])

        if order['order_state'] == 'delivery':
            await message.answer(open_cart_orders(order['order_id'], lang), reply_markup=cart_open_delivery_finl(order['order_id'], lang)) #cart_open_delivery_finl(order['order_id'], lang)
        if order['order_state'] == 'created':
            await message.answer(open_cart_orders(order['order_id'], lang), reply_markup=cart_open_created_finl(order['order_id'], lang)) #cart_open_created_finl(order['order_id'], lang)
        if order['order_state'] == 'submited':
            await message.answer(f"<b>Активных заказов нет.</b>\n")

# Открытие FAQ
@dp.message_handler(text=["ℹ FAQ", "/faq"], state="*")
async def user_faq(message: Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    send_message = get_settingsx()['misc_faq']
    if send_message == "None":
        if lang == 'ru':
            send_message = f"ℹ Информация. Измените её в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}"
        if lang == 'en':
            send_message = f"ℹ Information. You can change this in bot settings.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}"

    await message.answer(get_faq(message.from_user.id, send_message), disable_web_page_preview=True)

###############################################################################################
##### ***** ###### *****         СОЗДАНИЕ АРТИСТА
###############################################################################################
# -----------------------------------------------------------------------------------------------------------
# Создание нового магазина
@dp.message_handler(IsAdminorShopAdmin(), text=["🏪 Создать артиста ➕", "🏪 Create Artist ➕"], state="*")
async def product_shop_create(message: Message, state: FSMContext):
    print("user_menu - создание артиста")
    print("-")
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    print(user_id)
    my_artist = check_user_artist_exist(user_id)
    print(my_artist)
    if my_artist == True:
        print("|")
        await state.finish()
        await message.answer(f"<b>🏪 Артист уже существует 🏷 Выбирайте его в каталоге при создании позиций: {my_artist} </b>", parse_mode='HTML')
    else:
        print("||")
        await state.finish()
        await state.set_state("here_artist_name")
        await message.answer(_("<b>🏪 Введите название артиста или коллектива 🏷</b>", locale=lang), parse_mode='HTML')


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdminorShopAdmin(), state="here_artist_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        print("admin_products_shop - создание артиста")
        await state.update_data(data={'name': message.text})
        await state.set_state('here_artist_description')
        await message.answer("<b>🏪 Введите Bio артиста 📜</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для артиста 🏷", parse_mode='HTML')

# принятие описания магазина, запрос адреса
@dp.message_handler(IsAdminorShopAdmin(), state="here_artist_description")
async def product_category_create_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_artist_webadress')
        await message.answer("<b>🏪 Отправьте веб-сайт артиста 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


    else:
        await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите новое Bio для артиста 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdminorShopAdmin(), state="here_artist_webadress")
async def product_category_create_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if message.text == '0':
        await state.update_data(data={'webaddress': 'None'})
    else:
        await state.update_data(data={'webaddress': message.text})
    await state.set_state('here_artist_logo')
    await message.answer("<b>🏪 Отправьте лого артиста 📷</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')

# принятие лого магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), content_types=['photo','text'], state="here_artist_logo")
async def product_category_create_logo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    logo = message.photo[0].file_id if message.content_type == 'photo' else None
    async with state.proxy() as data:
        print(data)
        name = data['name']
        description = data['description']
        webaddress = data['webaddress']

    await state.finish()

    type_trade = get_settingsx()
    if type_trade['type_trade'] != "digital":
        city = get_city_user3(message.from_user.id)
        print(city)
        city_id = city[0]
        geocode = city[1]
        city_name = city[2]
    else:
        city_id = 0
        geocode = ''
        city_name = ''
    add_artistx(name, description, webaddress, message.from_user.id, logo, city_id, geocode, city_name)
    await message.answer(_("<b>🏪 Карточка артиста была успешно создана ✅</b>", locale=lang), parse_mode='HTML')


# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsAdminorShopAdmin(), text=["🏪 Изменить артиста 🖍", "🏪 Edit Artist 🖍"], state="*")
async def artist_list_edit(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id)['user_lang']
    artists = get_artistsxx(admin=user_id)
    print(artists)

    if len(artists) >= 1:
        await message.answer("<b>🏪 Выберите артиста для изменения 🖍</b>",
                             reply_markup=artist_edit_open_fp(0, user_id))
    else:
        await message.answer("<b>🏪 Ваши артисты отсутствуют 🖍</b>")


# Смена страницы выбора магазина
@dp.message_handler(IsAdminorShopAdmin(), text_startswith="change_artist_edit_pg:", state="*")
async def artist_list_edit_pg(call: CallbackQuery, state: FSMContext):
    await state.finish()
    remover = int(str(call.data).split(':')[1])
    #user_id = message.from_user.id
    user_id = int(str(call.data).split(':')[2])
    lang = get_user_lang(user_id)['user_lang']
    artists = get_artistsxx(admin=user_id)

    if len(artists) >= 1:
        await call.message.answer("<b>🏪 Выберите артиста для изменения 🖍</b>",
                                  reply_markup=artist_edit_open_fp(remover, user_id))
    else:
        await call.message.answer("<b>🏪 Артисты отсутствуют 🖍</b>")


# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit:", state="*")
async def artist_edit_open(call: CallbackQuery, state: FSMContext):
    print('Выбор артиста для редактирования api_sqlite.py 496')
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    lang = get_user_lang(user_id)['user_lang']
    remover = int(call.data.split(":")[3])
    print(artist_id, user_id, remover)

    get_message, get_photo = get_artist_admin(artist_id)

    if get_photo is not None and get_photo != '':
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message,
                                        reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await call.message.edit_text(get_message,
                                     reply_markup=artist_edit_open_finl(artist_id, user_id, remover))


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_return", state="*")
async def artist_edit_return(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    artists = get_artistsxx(admin=user_id)
    print(artists)

    if len(artists) >= 1:
        await call.message.delete()
        await call.message.answer("<b>📁 Выберите нужного Вам артиста 🖍</b>",
                                  reply_markup=artist_edit_open_fp(0, user_id))
    else:
        await call.answer("<b>❗ У Вас отсутствуют Артисты</b>")


# Создание новой позиции
@dp.message_handler(IsAdminorShopAdmin(), text=["📁 Создать позицию ➕", "📁 Create Position ➕"], state="*")
async def product_position_create(message: Message, state: FSMContext):
    await state.finish()
    print("APS 182")
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)

    await message.answer(_("<b>📁 Выберите категорию для позиции</b>", locale=lang),
                         reply_markup=position_create_open_fp(0, lang))
    #else:
    #await message.answer("<b>❌ Отсутствуют магазины для создания позиции.</b>")

###############################################################################################
##### ***** ###### *****         СОЗДАНИЕ АРТИСТА
###############################################################################################
# -----------------------------------------------------------------------------------------------------------
# Создание нового магазина
@dp.message_handler(IsAdminorShopAdmin(), text=["📁 Создать событие ➕", "📁 Create Event ➕"], state="*")
async def product_shop_create(message: Message, state: FSMContext):
    await state.finish()
    print("user_menu - создание события")
    print("-")
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    print(user_id)
    my_event = check_user_events_exist(user_id)
    print(my_event)
    city_id = get_city_user3(user_id)[2]
    print(city_id)

    if my_event == True:
        print("|")
        await message.answer(f"<b>🏪 Событие уже существует 🏷 Выбирайте его в каталоге при создании отзывов: {my_event} </b>", parse_mode='HTML')
    else:
        #if len(get_all_shopx()) >= 1:
        await state.set_state("here_event_name")
        await message.answer("<b>🏪 Введите название события 🏷</b>", parse_mode='HTML')

        '''await message.answer("<b>📁 Выберите место события или укажите <code>0</code></b>",
                             reply_markup=select_place_in_city_swipe_fp(city_id))'''

# Создание новой позиции
@dp.message_handler(IsAdminorShopAdmin(), text_startswith="here_event_place:", state="*")
async def product_position_create(message: Message, state: FSMContext):
    place = int(str(message.data).split(':')[1])
    await state.update_data(data={'place_id': place})

    print("||")
    await state.set_state("here_event_name")
    await message.answer("<b>🏪 Введите название события 🏷</b>", parse_mode='HTML')


# Создание новой позиции
@dp.message_handler(IsAdminorShopAdmin(), text_startswith="here_event_place2:", state="*")
async def product_position_create(call: CallbackQuery, state: FSMContext):
    place = int(str(call.data).split(':')[1])
    await state.update_data(data={'place_id': place})

    print("||")
    await state.set_state("here_event_name")
    await message.answer("<b>🏪 Введите название события 🏷</b>", parse_mode='HTML')


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdminorShopAdmin(), state="here_event_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        print("admin_products_shop - создание события")
        await state.update_data(data={'name': message.text})
        await state.set_state('here_event_description')
        await message.answer("<b>🏪 Введите Bio ведущих 📜</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для ведущих 🏷", parse_mode='HTML')


# принятие описания магазина, запрос адреса
@dp.message_handler(IsAdminorShopAdmin(), state="here_event_description")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_event_webadress')
        await message.answer("<b>🏪 Отправьте описание события 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')
    else:
        await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите веб-сайт события 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdminorShopAdmin(), state="here_event_webadress")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.text == '0':
        await state.update_data(data={'webaddress': 'None'})
    else:
        await state.update_data(data={'webaddress': message.text})
    await state.set_state('here_event_logo')
    await message.answer("<b>🏪 Отправьте лого события 📷</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие лого магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), content_types=['photo','text'], state="here_event_logo")
async def product_category_create_logo(message: Message, state: FSMContext):
    logo = message.photo[0].file_id if message.content_type == 'photo' else None
    async with state.proxy() as data:
        print(data)
        name = data['name']
        description = data['description']
        webaddress = data['webaddress']

    await state.finish()
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    type_trade = get_settingsx()
    if type_trade['type_trade'] != "digital":
        city = get_city_user3(message.from_user.id)
        print(city)
        city_id = city[0]
        geocode = city[1]
        city_name = city[2]
    else:
        city_id = 0
        geocode = ''
        city_name = ''
    add_eventx(name, description, webaddress, message.from_user.id, logo, city_id, geocode, city_name)
    await message.answer(_("<b>🏪 Карточка события была успешно создана ✅</b>", locale=lang), parse_mode='HTML')


# -----------------------------------------------------------------------------------------------------------
# Создание нового магазина
@dp.message_handler(text=["🏪 Создать магазин ➕", "🏪 Create Shop ➕"], state="*")
async def product_shop_create(message: Message, state: FSMContext):
    await state.finish()
    print("user_menu - создание магазина")
    print("-")
    user_id = message.from_user.id
    print(user_id)
    my_shop = check_user_shop_exist(user_id)
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role in ["Admin", "ShopAdmin"]:
        print(my_shop)
        if my_shop:
            print("|")
            await message.answer(f"<b>🏪 Магазин уже существует 🏷 Выбирайте его в каталоге при создании позиций: {my_shop} </b>", parse_mode='HTML')
        else:
            print("||")
            await state.set_state("here_shop_name")
            await message.answer(_("<b>🏪 Введите название для магазина 🏷</b>", locale=lang), parse_mode='HTML')


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        user_id = message.from_user.id
        lang = get_user_lang(user_id)['user_lang']

        print("admin_products_shop - создание магазина")
        await state.update_data(data={'name': message.text})
        await state.set_state('here_shop_description')
        await message.answer(_("<b>🏪 Введите описание для магазина 📜</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')
    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для магазина 🏷", locale=lang), parse_mode='HTML')


# принятие описания магазина, запрос адреса
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_description")
async def product_category_create_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_shop_adress')
        await message.answer(_("<b>🏪 Отправьте адрес магазина 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')

    else:
        await message.answer(_("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите новое описание для магазина 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_adress")
async def product_category_create_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    if message.text == '0':
        await state.update_data(data={'address': 'None'})
    else:
        await state.update_data(data={'address': message.text})
    await state.set_state('here_shop_phone')
    await message.answer(_("<b>🏪 Отправьте телефон магазина ☎️</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')


# принятие номера магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_phone")
async def product_category_create_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    if message.text == '0':
        await state.update_data(data={'phone': 'None'})
    else:
        await state.update_data(data={'phone': message.text})
    await state.set_state('here_shop_logo')
    await message.answer(_("<b>🏪 Отправьте лого магазина 📷</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')


# принятие лого магазина, запрос лого
@dp.message_handler(IsAdminorShopAdmin(), content_types=['photo','text'], state="here_shop_logo")
async def product_category_create_logo(message: Message, state: FSMContext):
    logo = message.photo[0].file_id if message.content_type == 'photo' else None
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    async with state.proxy() as data:
        print(data)
        name = data['name']
        description = data['description']
        address = data['address']
        phone = data['phone']

    await state.finish()

    type_trade = get_settingsx()
    if type_trade['type_trade'] != "digital":
        city = get_city_user3(message.from_user.id)
        print(city)
        city_id = city[0]
        geocode = city[1]
        city_name = city[2]
    else:
        city_id = 0
        geocode = ''
        city_name = ''
    add_shopx(name, description, address, phone, message.from_user.id, logo, city_id, geocode, city_name)
    await message.answer(_("<b>🏪 Магазин был успешно создан ✅</b>", locale=lang), parse_mode='HTML')


# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(text=["🏪 Изменить магазин 🖍", "🏪 Edit Shop 🖍"], state="*")
async def shop_list_edit(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role == "Admin":
        shops = get_shopsxy()
    elif user_role == "ShopAdmin":
        shops = get_shopsxx(admin=user_id)
    print(shops)

    if len(shops) >= 1:
        await message.answer(_("<b>🏪 Выберите магазин для изменения 🖍</b>", locale=lang),
                             reply_markup=shop_edit_open_fp(0, user_id, lang))
    else:
        await message.answer(_("<b>🏪 Ваши магазины отсутствуют 🖍</b>", locale=lang))


# Смена страницы выбора магазина
@dp.message_handler(text_startswith="change_shop_edit_pg:", state="*")
async def shop_list_edit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role in ["Admin", "ShopAdmin"]:
        if len(shops) >= 1:
            page = int(str(call.data).split(':')[1])

            await call.message.answer(_("<b>🏪 Выберите магазин для изменения 🖍</b>", locale=lang),
                                      reply_markup=shop_edit_open_fp(0, user_id, lang))
        else:
            await call.message.answer(_("<b>🏪 Магазины отсутствуют 🖍</b>", locale=lang))


# Открытие сообщения с ссылкой на поддержку
@dp.message_handler(text=["☎ Поддержка", "/support", "support"], state="*")
async def user_support(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    if get_user['user_login'] is None:
            username = "Не заполнено"
    else: username = get_user['user_login']
    #lang = get_userx(user_id=user_id)['user_lang']

    user_support = get_settingsx()['misc_support']
    if str(user_support).isdigit():
        get_user = get_userx(user_id=user_support)

        if len(get_user['user_login']) >= 1:
            await message.answer("<b>☎ Нажмите кнопку ниже для связи с Администратором.</b>",
                                 reply_markup=user_support_finl(get_user['user_login']))
            #await notify(dp, f"Пользователь запрашивает диалог с поддержкой, Username: {user_name}, пользователем ID: {user_id}")
            return
        else:
            update_settingsx(misc_support="None")

    await message.answer(f"☎ Поддержка. Измените их в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}",
                         disable_web_page_preview=True)

# Создание запроса на продавца
@dp.message_handler(state="here_seller_request_direction")
async def user_seller(message: Message, state: FSMContext):
    await state.finish()

    # message.answer(message.text)
    seller_request = create_seller_request(message.from_user.id, message.text)
    await message.answer("👌 Ваш запрос успешно отправлен.")

# Просмотр истории покупок
@dp.callback_query_handler(text="create_seller_request5", state="*")
async def user_seller(call: CallbackQuery, state: FSMContext):
    seller_request = create_seller_request(call.from_user.id)
    await call.answer("🎁 Запрос успешно создан")
    await notify(dp, "Поступил новый запрос продавца!")
    # await bot.send_message(get_admins(), "ntcnnnnnn")

# Подтверждение удаления всех позиций
@dp.message_handler(IsShopAdmin(), text=["📁 Удалить все позиции ❌", "📁 Delete all Positions ❌"], state="*")
async def product_position_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>📁 Вы действительно хотите удалить все позиции? ❌</b>\n"
                         "❗ Так же будут удалены все товары",
                         reply_markup=position_remove_confirm_inl)

# Удаление позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_delete", state="*")
async def product_position_edit_delete(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await call.message.delete()
    await call.message.answer(_("<b>📁 Вы действительно хотите удалить позицию? ❌</b>", locale=lang),
                              reply_markup=position_edit_delete_finl(position_id, category_id, remover))


# Подтверждение удаления позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_delete", state="*")
async def product_position_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    remover = int(call.data.split(":")[4])

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        remove_positionx(position_id=position_id)

        await call.answer("📁 Вы успешно удалили позицию и её товары ✅")

        if len(get_positionsx(category_id=category_id)) >= 1:
            await call.message.edit_text(_("<b>📁 Выберите нужную вам позицию 🖍</b>", locale=lang),
                                         reply_markup=position_edit_open_fp(remover, category_id))
        else:
            await call.message.delete()
    else:
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Согласие очистики позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_clear", state="*")
async def product_position_edit_clear_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    remover = int(call.data.split(":")[4])

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        await call.answer("📁 Вы успешно удалили все товары позиции ✅")

    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message,
                                        reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await call.message.edit_text(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Открытие способов пополнения
@dp.message_handler(IsShopAdmin(), text=["🖲 Способы пополнения7", "🖲 Payment Methods7"], state="*")
async def payment_systems(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    print(user_role)
    if user_role in ["Admin", "ShopAdmin"]: #user_id in get_admins(): #
        await message.answer(_("<b>🖲 Выберите способ пополнения</b>", locale=lang), reply_markup=payment_as_choice_finl(user_id, lang))


# Включение/выключение самих способов пополнения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="change_payment7:")
async def payment_systems_edit7(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]
    user_id = json.dumos(call.data.split(":")[3])
    print("Админ магазина")
    # print(call.data.split(":")[0])
    print(call.from_user.id)
    user_id = call.from_user.id

    count = get_upaycount(user_id)
    print(count['paycount'])
    if count['paycount'] == 0:
        cur = create_upayments_row(user_id)
    else:
        get_payment = get_upaymentx(user_id)

    if get_payment['qiwi_login'] != "None" and get_payment['qiwi_token'] != "None" or way_status == "False":
        if way_pay == "Form":
            if get_payment['qiwi_secret'] != "None" or way_status == "False":
                update_upaymentx(user_id, way_form=way_status)
            else:
                await call.answer(
                    "❗ Приватный ключ отсутствует. Измените киви и добавьте приватный ключ для включения оплаты по Форме",
                    True)
        elif way_pay == "ForYm":
            if get_payment['yoo_token'] != "None" or way_status == "False":
                update_upaymentx(user_id, way_formy=way_status)
            else:
                await call.answer(
                    "❗ Номер счета отсутствует. Измените YooMoney и добавьте токен для включения оплаты по Форме YooMoney",
                    True)
        elif way_pay == "Number":
            update_update_upaymentx(user_id, way_number=way_status)
        elif way_pay == "Nickname":
            status, response = await (await QiwiAPI(call)).get_nickname()
            if status:
                update_upaymentx(user_id, way_nickname=way_status, qiwi_nickname=response)
            else:
                await call.answer(response, True)
    else:
        await call.answer("❗ Добавьте киви кошелёк перед включением Способов пополнений.", True)

    try:
        await call.message.edit_text(_("<b>🖲 Выберите способ пополнения</b>", locale=lang), reply_markup=payment_as_choice_finl())
    except Exception:
        pass


####################################### QIWI ######################################
# Изменение QIWI кошелька
@dp.message_handler(IsShopAdmin(), text=["🥝 Изменить QIWI 🖍", "🥝 Change QIWI 🖍"], state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_qiwi_login")
    await message.answer(_("<b>🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍</b>", locale=lang))


# Проверка работоспособности QIWI
@dp.message_handler(IsAdminorShopAdmin(), text=["🥝 Проверить QIWI ♻", "🥝 Check QIWI ♻"], state="*")
async def payment_qiwi_check(message: Message, state: FSMContext):
    print("||| Проверка КИВИ админом площадки. |||")
    await state.finish()
    user_id = message.from_user.id
    print(user_id)

    await (await QiwiAPI(message, suser_id=user_id, check_pass=True)).pre_checker()


# Баланс QIWI
@dp.message_handler(IsAdminorShopAdmin(), text=["🥝 Баланс QIWI 👁", "🥝 Balance QIWI 👁"], state="*")
async def payment_qiwi_balance(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    await (await QiwiAPI(message, suser_id=user_id)).get_balance()


######################################## ПРИНЯТИЕ QIWI ########################################
# Принятие логина для QIWI
@dp.message_handler(IsShopAdmin(), state="here_qiwi_login")
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


# Принятие токена для QIWI
@dp.message_handler(IsShopAdmin(), state="here_qiwi_token")
async def payment_qiwi_edit_token(message: Message, state: FSMContext):
    await state.update_data(here_qiwi_token=message.text)

    await state.set_state("here_qiwi_secret")
    await message.answer(
        "<b>🥝 Введите <code>Секретный ключ 🖍</code></b>\n"
        "❕ Получить можно тут 👉 <a href='https://qiwi.com/p2p-admin/transfers/api'><b>Нажми на меня</b></a>\n"
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

    cache_message = await message.answer(_("<b>🥝 Проверка введённых QIWI данных... 🔄</b>", locale=lang))
    await asyncio.sleep(0.5)

    await (await QiwiAPI(cache_message, qiwi_login, qiwi_token, qiwi_secret, add_pass=True, suser_id=user_id)).pre_checker()


################################################################################################
###################################### УДАЛЕНИЕ ВСЕХ ПОЗИЦИЙ ###################################
# Согласие на удаление всех позиций и товаров
@dp.callback_query_handler(IsShopAdmin(), text_startswith="confirm_remove_position:", state="*")
async def product_position_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    print("SA DEL POSITIONS")
    user_id = call.from_user.id
    print(user_id)

    if get_action == "yes":

        get_positions = len(get_all_my_positionsnx(position_user_id=user_id))
        print(get_positions)
        get_items = len(get_all_my_itemsnx(creator_id=user_id))
        print(get_items)

        remove_positionx(position_user_id=user_id)
        remove_itemx(creator_id=user_id)

        await call.message.edit_text(
            f"<b>📁 Вы удалили все позиции<code>({get_positions}шт)</code> и товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text(_("<b>📁 Вы отменили удаление всех позиций ✅</b>", locale=lang))

#################### УДАЛЕНИЕ ТОВАРОВ ###################
# Кнопки с подтверждением удаления всех категорий
@dp.message_handler(IsShopAdmin(), text=["🎁 Удалить все товары ❌", "🎁 Delete all goods ❌"], state="*")
async def product_item_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(_("<b>🎁 Вы действительно хотите удалить все товары? ❌</b>\n", locale=lang),
                         reply_markup=item_remove_confirm_inl)

##################################### УДАЛЕНИЕ ВСЕХ ТОВАРОВ ####################################
# Согласие на удаление всех товаров
@dp.callback_query_handler(IsShopAdmin(), text_startswith="confirm_remove_item:", state="*")
async def product_item_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    if get_action == "yes":
        user_id = call.from_user.id

        get_items = len(get_all_my_itemsnx(creator_id=user_id))
        remove_itemx(creator_id=user_id)

        await call.message.edit_text(f"<b>🎁 Вы удалили все товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text(_("<b>🎁 Вы отменили удаление всех товаров ✅</b>", locale=lang))


# Удаление определённых товаров
@dp.message_handler(IsShopAdmin(), text=["🎁 Удалить товары 🖍", "🎁 Delete Goods 🖍"], state="*")
async def product_item_delete(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_items_delete")
    await message.answer("<b>🖍 Вводите айди товаров, которые нужно удалить</b>\n"
                         "❕ Получить айди товаров можно при изменении позиции\n"
                         "❕ Если хотите удалить несколько товаров, отправьте ID товаров через запятую или пробел. Пример:\n"
                         "<code>▶ 123456,123456,123456</code>\n"
                         "<code>▶ 123456 123456 123456</code>")

################################################################################################
####################################### УДАЛЕНИЕ ТОВАРОВ ######################################
# Принятие айди товаров для их удаления
@dp.message_handler(IsAdminorShopAdmin(), state="here_items_delete")
async def product_item_delete_get(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id

    remove_ids, cancel_ids = [], []  # Айди удалённых и ненайденных товаров
    get_item_ids_one, get_item_ids_two = [], [[]]
    save_ids = []

    if "," in message.text:
        get_item_ids_one = clear_list(message.text.split(","))
    else:
        get_item_ids_one = clear_list([message.text])

    get_item_ids_two.extend(
        item.split(" ") for item in get_item_ids_one if " " in item
    )
    if len(get_item_ids_two) == 1:
        get_item_ids_two.append(get_item_ids_one)

    for check_item in get_item_ids_two:
        save_ids.extend(iter(clear_list(check_item)))
    save_ids = clear_list(save_ids)

    for item_id in save_ids:
        check_item = get_itemx(item_id=item_id, creator_id=user_id)
        if check_item is not None:
            remove_itemx(item_id=item_id)
            remove_ids.append(item_id)
        else:
            cancel_ids.append(item_id)

    remove_ids = ", ".join(remove_ids)
    cancel_ids = ", ".join(cancel_ids)

    await message.answer(f"<b>✅ Успешно удалённые товары:\n"
                         f"▶ <code>{remove_ids}</code>\n"
                         f"➖➖➖➖➖➖➖➖➖➖\n"
                         f"❌ Ненайденные товары:\n"
                         f"▶ <code>{cancel_ids}</code></b>")
###############################################################################################
################################################################################################
####################################### ДОБАВЛЕНИЕ ПОЗИЦИЙ #####################################
# Следующая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_create_nextp:", state="*")
async def product_position_create_next(call: CallbackQuery, state: FSMContext):
    print('выбора категорий для создания позиций  user_menu.py 126')
    remover = int(call.data.split(":")[1])
    lang = call.data.split(":")[2]
    print(remover)

    await call.message.edit_text(_("<b>📁 Выберите категорию для позиции ➕</b>", locale=lang),
                                 reply_markup=position_create_next_page_fp(remover, lang))

# Предыдущая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_create_backp:", state="*")
async def product_position_create_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    lang = call.data.split(":")[2]

    await call.message.edit_text(_("<b>📁 Выберите категорию для позиции ➕</b>", locale=lang),
                                 reply_markup=position_create_back_page_fp(remover, lang))


# Выбор категории для создания позиции
@dp.callback_query_handler(text_startswith="position_people_create_here:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_people_create_here - user_menu 160')
    category_id = int(call.data.split(":")[1])
    await state.update_data(here_cache_change_category_id=category_id)
    await state.update_data(here_position_source="people")
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role in ["Admin", "ShopAdmin"]:
        await state.set_state("here_position_name")
        await call.message.edit_text("<b>📁 Введите название для позиции 🏷</b>")

# Выбор категории для создания позиции
@dp.callback_query_handler(text_startswith="position_people_open_here:", state="*")
async def product_position_open_select_category(call: CallbackQuery, state: FSMContext):
    print('position_people_open_here - user_menu 1397')
    category_id = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[3])
    print(category_id, city_id)
    get_category = get_category_people(category_id=category_id)
    #if city_id == 0:
    #    city_id = get_city_user(call.from_user.id)[0]
    #else: city_id = int(call.data.split(":")[3])
    print(category_id, city_id, get_category)

    get_positions = get_people_positions_in_cityx(category_id=category_id, position_city_id=city_id, flagallc=1, position_type=1)  # flagallc=1,  get_positionsx(category_id=category_id)
    print(category_id, city_id)
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    #user_role = get_userx(user_id=user_id)['user_role']
    #if user_role == "Admin" or user_role == "ShopAdmin":
    if len(get_positions) >= 1:
        source = "people"
        #source = "people"
        await call.message.edit_text(f"<b>🎁 Товары частных лиц в категории: {get_category['category']}</b>",
                                     reply_markup=products_item_position_swipe_fp(0, "open", category_id, city_id, source, lang))
    else:
        await call.answer(f"❕ Товары в категории {get_category['category']} отсутствуют")



# Выбор категории для создания позиции
@dp.callback_query_handler(text_startswith="position_edit_category_open", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_edit_here - user_menu 160')
    category_id = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])

    await state.update_data(here_cache_change_category_id=category_id)
    await state.update_data(here_position_source="commercial")

    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    get_cat_pos = get_positionsx(category_id=category_id)
    print(get_cat_pos)
    if user_role in ['Admin', 'ShopAdmin']:
        if len(get_cat_pos) >= 1:
            action = "edit"
            source = "commercial"
            await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                                         reply_markup=products_item_position_swipe_fp(0, action, category_id, city_id, source, lang))
            await state.set_state("here_position_addtoshop")


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_create_here:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_create_here - user_menu 160')
    category_id = int(call.data.split(":")[1])
    await state.update_data(here_cache_change_category_id=category_id)
    await state.update_data(here_position_source="commercial")

    print('position_addtoshop - user_menu 555')
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    get_user_shops = get_shopsxx(admin=user_id)
    if len(get_user_shops) >= 1:
        await call.message.edit_text(_("<b>Выберите магазин для добавления позиции.</b>", locale=lang),
                                     reply_markup=position_select_shop_fp(0, lang))
    else:
        await call.message.edit_text(_("<b>У Вас еще нет магазина на площадке, но Вы можете его создать.</b>", locale=lang),
                                     reply_markup=shop_creation_request_finl(lang))
        await state.set_state("here_position_addtoshop")


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="here_position_addtoshop:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('here_position_addtoshop: - user_menu 566')
    key = call.data.split(":")[1]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if key != "NoCreate":
        shop_id = int(call.data.split(":")[1])
        await state.update_data(here_cache_change_shop_id=shop_id)
    else: await state.update_data(here_cache_change_shop_id=0)

    await state.set_state("here_position_name")
    await call.message.edit_text(_("<b>📁 Введите название для позиции 🏷</b>", locale=lang))


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Заготовка под принятие города магазином
# Принятие города для создания позиции
# @dp.message_handler(IsShopAdmin(), state="here_position_city")
# async def product_position_create_name(message: Message, state: FSMContext):
#     print(f'Принятие города для создания позиции  admin_products_shop.py 344')
#     city_user = get_city_user(message.from_user.id)
# Принятие имени для создания позиции


@dp.message_handler(IsAdminorShopAdmin(), state="here_position_name")
async def product_position_create_name(message: Message, state: FSMContext):
    print('Принятие имени для создания позиции  user_menu.py 1084')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        await state.update_data(here_position_name=clear_html(message.text),
                                here_position_city=get_citytext_user(message.from_user.id)[0]
                                , position_city_id=get_city_user(message.from_user.id)[0])

        await state.set_state("here_position_type")
        await message.answer(_("<b>📁 Введите тип позиции 1 - реальная, 2 - цифровая</b>", locale=lang), reply_markup=position_select_type_finl(lang))
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")


@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="here_position_type:", state="*")
async def product_position_create_type(call: CallbackQuery, state: FSMContext):
    print('Принятие имени для создания позиции  user_menu.py 1084')
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    position_type_txt = call.data.split(":")[1]
    position_type = 1 if position_type_txt == "real" else 2
    print(position_type_txt)

    if len(position_type_txt) <= 7:
        await state.update_data(here_position_type=position_type,
                                here_position_city=get_citytext_user(call.from_user.id)[0]
                                , position_city_id=get_city_user(call.from_user.id)[0])

    if position_type_txt == "real":
        await state.set_state("here_position_local")
        await call.message.answer("<b>📁 Выберите значение признака Местный [местный - позиция отображается только в городе продавца, глобальный - позиция отображается во всех городах]</b>", reply_markup=position_select_local_finl(lang))

    elif position_type_txt == "digital":
        await state.set_state("here_position_price")
        await call.message.answer(_("<b>📁 Введите цену для позиции 💰</b>", locale=lang))


@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="here_position_local:", state="*")
async def product_position_create_type(call: CallbackQuery, state: FSMContext):
    print('Принятие имени для создания позиции  user_menu.py 1084')
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    position_local_txt = call.data.split(":")[1]
    position_local = 1 if position_local_txt == 1 else 2

    if len(position_local_txt) <= 7:
        await state.update_data(here_position_local=position_local,
                                here_position_city=get_citytext_user(call.from_user.id)[0]
                                , position_city_id=get_city_user(call.from_user.id)[0])

        await state.set_state("here_position_price")
        await call.message.answer(_("<b>📁 Введите цену для позиции 💰</b>", locale=lang))
    else:
        await call.message.answer("<b>❌ Признак местный позиции не может отличаться от перечисленных значений. Местный или глобальный.</b>\n"
                             "📁 Введите тип позиции 🏷")


# Принятие цены позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), state="here_position_price")
async def product_position_create_price(message: Message, state: FSMContext):
    print('Принятие цены позиции  admin_products.py 366')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.update_data(here_position_price=message.text)
        else:
            await message.answer("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰")

    position_data = await state.get_data()
    print(position_data['here_position_type'])
    position_type = position_data['here_position_type']

    if position_type == 1:
        await state.set_state("here_position_rest")
        await message.answer(_("<b>📁 Введите остаток для позиции 📜</b>", locale=lang))

    elif position_type == 2:
        await state.set_state("here_position_rest")
        await product_position_create_in_rest(message, state)


# Принятие цены позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), state="here_position_rest")
async def product_position_create_in_rest(message: Message, state: FSMContext):
    print('Принятие остатка позиции  admin_products.py 366')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    #position_data = await state.get_data()
    async with state.proxy() as data:
        #print(position_data['here_position_type'])
        print(data['here_position_type'])
        #position_type = position_data['here_position_type']
        position_type = data['here_position_type']
    if position_type == 1:
        if message.text.isdigit():
            if 0 <= int(message.text) <= 10000:
                await state.update_data(here_position_rest=message.text)
            else:
                await message.answer("<b>❌ Остаток не может быть меньше 0 или больше 10 000.</b>\n"
                                     "📁 Введите остаток позиции 💰")
        else:
            await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                                 "📁 Введите остаток позиции 💰")
    elif position_type == 2:
        await state.update_data(here_position_rest=0)

    await state.set_state("here_position_description")
    await message.answer("<b>📁 Введите описание для позиции 📜</b>\n"
                         "❕ Вы можете использовать HTML разметку\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие описания позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), state="here_position_description")
async def product_position_create_description(message: Message, state: FSMContext):
    print('Принятие описания позиции  admin_products.py 386')

    try:
        if len(message.text) <= 900:
            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            await state.update_data(here_position_description=message.text)

            await state.set_state("here_position_photo")
            await message.answer("<b>📁 Отправьте изображение для позиции 📸</b>\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
        else:
            await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для позиции 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие изображения позиции для её создания
@dp.message_handler(IsAdminorShopAdmin(), content_types="photo", state="here_position_photo")
@dp.message_handler(IsAdminorShopAdmin(), text="0", state="here_position_photo")
async def product_position_create_photo(message: Message, state: FSMContext):
    print('Принятие изображения позиции  admin_products.py 418')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    async with state.proxy() as data:
        position_user_id = message.from_user.id
        position_name = clear_html(data['here_position_name'])
        position_price = data['here_position_price']
        position_type = data['here_position_type']

        if position_type == 1:
            position_city = data['here_position_city']
            position_city_id = data['position_city_id']
            position_rest = data['here_position_rest']
            position_local = data['here_position_local']
        elif position_type == 2:
            position_rest = 0
            position_city = 0
            position_city_id = 0
            position_local = 0
        catategory_id = data['here_cache_change_category_id']
        position_source = data['here_position_source']
        if position_source == "commercial":
            position_shop_id = data['here_cache_change_shop_id']
        elif position_source == "people":
            position_shop_id = 0
        position_description = data['here_position_description']
        position_source = data['here_position_source']
    await state.finish()

    position_photo = "" if "text" in message else message.photo[-1].file_id
    position_id = random.randint(1000000000, 9999999999)
    add_positionx(position_id, position_city, position_city_id, position_name, position_price, position_type, position_rest, position_description, position_photo,
                  catategory_id, position_shop_id, position_user_id, position_source, position_local)
    #new_position_notify(position_id)

    #async def on_notify(dp: Dispatcher, msg, markup):
    #    await send_admins(msg, markup="default")

    await notify(dp, f"Создана позиция: {position_name}, пользователем ID: {position_user_id}")
    #await asyncio.create_task(post_position_to_telegraph(position_id))
    await message.answer(_("<b>📁 Позиция была успешно создана ✅</b>", locale=lang))
    await asyncio.create_task(await approve_new_product_notify(position_id, markup=None))


@dp.callback_query_handler(text_startswith="position_notify:", state="*")
async def product_position_notify_approve(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    decision = call.data.split(":")[2]

    print(position_id, decision)

    user_id = call.from_user.id

    if decision == "yes":
        await functions_position_notify_bg(position_id, markup=None)
    if decision == "no":
        await call.answer("<b>📁 Вы отменили рассылку позиции 🖍</b>",
                                 reply_markup=menu_frep(user_id, "ru"))

################################################################################################
####################################### ИЗМЕНЕНИЕ ПОЗИЦИЙ #####################################
# Возвращение к начальным категориям для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                                 reply_markup=position_edit_category_open_fp(0))


# Следующая страница категорий для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_nextp:", state="*")
async def product_position_edit_category_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                                 reply_markup=position_edit_category_next_page_fp(remover))


# Предыдущая страница категорий для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_backp:", state="*")
async def product_position_edit_category_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                                 reply_markup=position_edit_category_back_page_fp(remover))


# Выбор категории с нужной позицией
@dp.callback_query_handler(text_startswith="position_edit_category_swipe:", state="*")
async def product_position_edit_category_open(call: CallbackQuery, state: FSMContext):
    print(category_id, city_id, lang)
    category_id = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])
    lang = call.data.split(":")[3]
    user_id = call.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    #print("SWIPE_CAT1")
    if user_role in ["Admin", "ShopAdmin"]:
        #print(i18n.get_user_locale('position_edit', user_id=message.from_user.id))
        action = "edit"
        #print("SWIPE_CAT2")
        await call.message.edit_text(_("<b>📁 Выберите нужную вам позицию 🖍</b>", locale=lang),
                                     reply_markup=products_item_category_swipe_fp(0, category_id, city_id, action, lang))


# Следующая страница позиций для их изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_nextp:", state="*")
async def product_position_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                                 reply_markup=position_edit_next_page_fp(remover, category_id))


# Предыдущая страница позиций для их изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_backp:", state="*")
async def product_position_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                                 reply_markup=position_edit_back_page_fp(remover, category_id))


# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_edit:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    print('Выбор позиции для редактирования api_sqlite.py 1707')
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    city_id = int(call.data.split(":")[4])
    lang = call.data.split(":")[5]
    user_id = call.from_user.id
    user_role = get_userx(user_id=user_id)['user_role']
    print(position_id, category_id, remover, city_id, lang)

    # IsProductShopAdmin()
    adminspos = check_position_owner(user_id, position_id)
    if adminspos is True:

        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await call.answer("<b>❗ У Вас нет прав редактировать данную позицию.</b>")


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    city_id = get_userx(user_id=user_id)['user_city_id']
    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.delete()
        action = "edit"
        source = "commercial"

        await call.message.answer(_("<b>📁 Выберите нужную вам позицию 🖍</b>", locale=lang),
                                  reply_markup=products_item_position_swipe_fp(remover, action, category_id, city_id, source, lang))
    else:
        await call.answer("<b>❗ Позиции в данной категории отсутствуют</b>")


######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_name", state="*")
async def product_position_edit_name(call: CallbackQuery, state: FSMContext):
    print('Изменение имени позиции api_sqlite.py 529')
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_name")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новое название для позиции 🏷</b>", locale=lang))


# Принятие имени позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_name")
async def product_position_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            position_id = data['here_cache_position_id']
            category_id = data['here_cache_category_id']
            remover = data['here_cache_position_remover']
        await state.finish()

        update_positionx(position_id, position_name=clear_html(message.text))
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message,
                                       reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите новое название для позиции 🏷")

# Изменение цены позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_price", state="*")
async def product_position_edit_price(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_price")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новую цену для позиции 💰</b>", locale=lang))


# Принятие цены позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_price")
async def product_position_edit_price_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            async with state.proxy() as data:
                position_id = data['here_cache_category_id']
                category_id = data['here_cache_position_id']
                remover = data['here_cache_position_remover']
            await state.finish()

            update_positionx(position_id, position_price=message.text)
            get_message, get_photo = get_position_admin(position_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message,
                                           reply_markup=position_edit_open_finl(position_id, category_id, remover))
            else:
                await message.answer(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰")


# Изменение описания позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_description", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_description")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое описание для позиции 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие описания позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_description")
async def product_position_edit_description_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_category_id']
        category_id = data['here_cache_position_id']
        remover = data['here_cache_position_remover']

    try:
        if len(message.text) <= 600:
            await state.finish()

            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            update_positionx(position_id, position_description=message.text)
            get_message, get_photo = get_position_admin(position_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message,
                                           reply_markup=position_edit_open_finl(position_id, category_id, remover))
            else:
                await message.answer(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для позиции 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.")


# Изменение изображения позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_photo", state="*")
async def product_position_edit_photo(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    #get_position = get_positionx(position_id=position_id)


    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_photo")
    await call.message.delete()
    await call.message.answer(f"<b>📁 Отправьте новое изображение для позиции 📸</b>\n"
                              f":{position_id}\n"
                              f"❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие нового фото для позиции
@dp.message_handler(IsShopAdmin(), content_types="photo", state="here_change_position_photo")
@dp.message_handler(IsShopAdmin(), text="0", state="here_change_position_photo")
async def product_position_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_category_id']
        category_id = data['here_cache_position_id']
        remover = data['here_cache_position_remover']
    await state.finish()

    position = get_positionx(position_id=position_id)
    print(position['position_name'])

    position_photo = "" if "text" in message else message.photo[-1].file_id
    update_positionx(position_id, position_photo=position_photo)
    get_message, get_photo = get_position_admin(position_id)
    await notify(dp, f"Была отредактирована позиция: {position['position_name']}")

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message,
                                   reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover))

# Изменение города продукта
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_city", state="*")
async def product_position_edit_description2(call: CallbackQuery, state: FSMContext):
    print('Изменение города продукта  admin_products.py 715')
    print(call.data)
    category_id = int(call.data.split(":")[2])
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[3])

    current_city = get_city_user(call.from_user.id)[0]
    get_user_shops = get_shopsxx(admin=user_id)
    if len(get_user_shops) >= 1:
        await call.message.edit_text(_("<b>Выберите магазин для добавления позиции.</b>", locale=lang),
                                     reply_markup=position_select_shop_fp(0))

    await state.set_state("here_change_shop")

    # await state.update_data(here_cache_category_id=category_id)
    # await state.update_data(here_cache_position_id=position_id)
    # await state.update_data(here_cache_position_remover=remover)


    #await state.update_data({'position_id': position_id, 'category_id': category_id, 'remover': remover})
    #await call.message.delete()
    #await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
    #                          "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
    #                          f"❕  Город товара: <code>{current_city}</code>", reply_markup=geo_1_kb())


# ---------------------------  Добавлено 12.08.22 ------------------------------------------

# Изменение города продукта
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_edit_city", state="*")
async def product_position_edit_city(call: CallbackQuery, state: FSMContext):
    print('Изменение города продукта  admin_products.py 715')
    print(call.data)
    category_id = int(call.data.split(":")[2])
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[3])

    current_city = get_city_user(call.from_user.id)[0]

    # await state.update_data(here_cache_category_id=category_id)
    # await state.update_data(here_cache_position_id=position_id)
    # await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_city")
    await state.update_data({'position_id': position_id, 'category_id': category_id, 'remover': remover})
    await call.message.delete()
    await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
                              "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
                             f"❕ Город товара: <code>{current_city}</code>", reply_markup=geo_1_kb(lang))


# принятие новой геопозиции для позиции
@dp.callback_query_handler(text_startswith='geo_chosen_cities', state='here_change_city')
async def geo_5(cb: CallbackQuery, state: FSMContext):
    info = int(str(cb.data).split('#')[1])
    if info == 0:
        async with state.proxy() as data:
            city = data['city']
            position_id = int(data['position_id'])
            category_id = data['category_id']
            remover = data['remover']
            city_id = data['city_id']

    else:
        async with state.proxy() as data:
            position_id = int(data['position_id'])
            category_id = data['category_id']
            remover = data['remover']

        city_id = info
        city = get_city_info(info)

    await state.finish()
    update_position_city(city, city_id, position_id)

    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await cb.message.answer_photo(get_photo, get_message,
                                      reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await cb.message.answer(get_message,
                                reply_markup=position_edit_open_finl(position_id, category_id, remover))

######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_name", state="*")
async def tgartist_edit_name(call: CallbackQuery, state: FSMContext):
    print('Изменение имени артиста api_sqlite.py 529')
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await state.set_state("here_change_artist_name")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое название для артиста 🏷</b>")


# Принятие имени артиста для его изменения
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_artist_name")
async def artist_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            artist_id = data['here_cache_artist_id']
            user_id = data['here_cache_user_id']
            remover = data['here_cache_artist_remover']
        await state.finish()

        update_artistx(artist_id, name=clear_html(message.text))
        get_message, get_photo = get_artist_admin(artist_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message,
                                       reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
        else:
            await message.answer(get_message, reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите новое название для артиста 🏷")
################################################################################################
# РЕДАКТИРОВАНИЕ ОПИСАНИЯ АРТИСТА
###################################
# Изменение описания артиста
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_description", state="*")
async def artist_edit_description(call: CallbackQuery, state: FSMContext):
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await state.set_state("here_change_artist_description")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое описание для артиста 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие описания позиции для её изменения
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_artist_description")
async def product_artist_edit_description_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        artist_id = data['here_cache_artist_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_artist_remover']

    try:
        if len(message.text) <= 600:
            await state.finish()

            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            update_artistx(artist_id, description=clear_html(message.text))
            get_message, get_photo = get_artist_admin(artist_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message,
                                           reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
            else:
                await message.answer(get_message,
                                     reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
        else:
            await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для артиста 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для артиста 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.")
##############################################################################################
########################## ARTIST _____ EDIT ________ PHOTO
##############################################################################################
# Изменение изображения позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_photo", state="*")
async def artist_edit_photo(call: CallbackQuery, state: FSMContext):
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await state.set_state("here_change_artist_photo")
    await call.message.delete()
    await call.message.answer("<b>📁 Отправьте новое изображение для артиста 📸</b>\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие нового фото для позиции
@dp.message_handler(IsAdminorShopAdmin(), content_types="photo", state="here_change_artist_photo")
@dp.message_handler(IsAdminorShopAdmin(), text="0", state="here_change_artist_photo")
async def product_artist_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        artist_id = data['here_cache_artist_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_artist_remover']
    await state.finish()

    artist = get_artistx(artist_id = artist_id)
    print(artist['name'])

    artist_photo = "" if "text" in message else message.photo[-1].file_id
    update_artistx(artist_id, logo=artist_photo)
    get_message, get_photo = get_artist_admin(artist_id)
    await notify(dp, f"Был отредактирован артист: {artist['name']}")

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message,
                                   reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await message.answer(get_message, reply_markup=artist_edit_open_finl(artist_id, user_id, remover))


# Изменение города продукта
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_city", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    print('Изменение города артиста  admin_products.py 715')
    print(call.data)
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    current_city = get_city_artist(artist_id=artist_id)[0]

    # await state.update_data(here_cache_category_id=category_id)
    # await state.update_data(here_cache_position_id=position_id)
    # await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_city_artist")
    await state.update_data({'artist_id': artist_id, 'user_id': user_id, 'remover': remover})
    await call.message.delete()
    await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
                              "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
                              f"❕ Город артиста: <code>{current_city}</code>", reply_markup=geo_1_kb(lang))


# принятие новой геопозиции для позиции
@dp.callback_query_handler(text_startswith='geo_chosen_cities', state='here_change_city_artist')
async def geo_5(cb: CallbackQuery, state: FSMContext):
    info = int(str(cb.data).split('#')[1])
    if info == 0:
        async with state.proxy() as data:
            city = data['city']
            artist_id = int(data['artist_id'])
            user_id = data['user_id']
            remover = data['remover']
            city_id = data['city_id']

    else:
        async with state.proxy() as data:
            artist_id = int(data['artist_id'])
            user_id = data['user_id']
            remover = data['remover']

        city_id = info
        city = get_city_info(info)

    await state.finish()
    update_artist_city(city, city_id, artist_id)

    # update_positionx(position_id)
    get_message, get_photo = get_artist_admin(artist_id)

    if get_photo is not None:
        await cb.message.answer_photo(get_photo, get_message,
                                      reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
    else:
        await cb.message.answer(get_message,
                                reply_markup=artist_edit_open_finl(artist_id, user_id, remover))

# Удаление позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_edit_delete", state="*")
async def artist_edit_delete(call: CallbackQuery, state: FSMContext):
    artist_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_artist_id=artist_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_artist_remover=remover)

    await call.message.delete()
    await call.message.answer(_("<b>📁 Вы действительно хотите удалить позицию? ❌</b>", locale=lang),
                              reply_markup=artist_edit_delete_finl())


# Подтверждение удаления позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="artist_delete", state="*")
async def artist_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    async with state.proxy() as data:
        artist_id = data['here_cache_artist_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_artist_remover']
    await state.finish()

    if get_action == "yes":
        #remove_itemx(position_id=position_id)
        remove_artistx(artist_id=artist_id)

        await call.answer("📁 Вы успешно удалили артиста ✅")

        if len(get_artistx(admin=user_id)) >= 1:
            await call.message.edit_text("<b>📁 Выберите нужного Вам артиста 🖍</b>",
                                         reply_markup=artist_edit_open_fp(remover, user_id))
        else:
            await call.message.delete()
    else:
        get_message, get_photo = get_artist_admin(artist_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=artist_edit_open_finl(artist_id, user_id, remover))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=artist_edit_open_finl(artist_id, user_id, remover))

# Просмотр истории покупок
@dp.callback_query_handler(text="user_history", state="*")
async def user_history(call: CallbackQuery, state: FSMContext):
    last_purchases = last_purchasesx(call.from_user.id, 5)

    if len(last_purchases) >= 1:
        await call.answer("🎁 Последние 5 покупок")
        await call.message.delete()

        for purchases in last_purchases:
            link_items = await upload_text(call, purchases['purchase_item'])

            await call.message.answer(f"<b>🧾 Чек: <code>#{purchases['purchase_receipt']}</code></b>\n"
                                      f"🎁 Товар: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}шт | {purchases['purchase_price']}₽</code>\n"
                                      f"🕰 Дата покупки: <code>{purchases['purchase_date']}</code>\n"
                                      f"🔗 Товары: <a href='{link_items}'>кликабельно</a>")

        await call.message.answer(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)
    else:
        await call.answer("❗ У вас отсутствуют покупки", True)


# Возвращение к профилю
@dp.callback_query_handler(text="user_profile", state="*")
async def user_profile_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)


# Возвращение к корзине
@dp.callback_query_handler(text="user_cart", state="*")
async def user_cart_return(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    get_user = get_userx(user_id=user_id)
    orderdata = get_params_orderx(user_id=user_id)

    for order in orderdata:
        order_id = orderdata['order_id']
        if order['order_state'] == 'created':
            await call.message.answer(open_cart_orders(order_id, user_id), reply_markup=cart_open_created_inl) #(orderdata['order_id'], lang)
        if order['order_state'] == 'delivery':
            await call.message.answer(open_cart_orders(order_id , user_id), reply_markup=cart_open_delivery_inl)
        if order['order_state'] == 'submited':
            await call.message.answer(f"<b>🎁 Активных заказов нет.</b>\n")

################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
########################################### КАТЕГОРИИ ##########################################
# Открытие категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_open:", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print('Открытие категорий для покупки user_menu.py 133')
    category_id = int(call.data.split(":")[1])
    #type_platform = get_settingsx()['type_trade']
    #if type_platform == "digital":
    #    city_id=0
    city_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    get_category = get_categoryx(category_id=category_id)
    #city_id = get_city_user(call.from_user.id)[0]
    get_positions = get_positions_cx(category_id=category_id) #, position_city_id=city_id
    #get_positions = get_positions_in_cityx(category_id=category_id, position_city_id=city_id)  #, position_city_id=city_id # , flagallc=1, position_type=1 get_positionsx(category_id=category_id)
    print(get_positions)
    print(category_id, city_id)
    if get_positions:
        source = "commercial"
        action = "open"
        await call.message.edit_text(_("<b>🎁 Товары категории:</b>", locale=lang) + get_category['category_name'],
                                     reply_markup=products_item_position_swipe_fp(0, action, category_id, city_id, source, lang))
    else:
        await call.answer(f"❕ Товары в категории {get_category['category_name']} отсутствуют")

######################################### ПОКУПКА ТОВАРА #######################################
########################################### КАТЕГОРИИ ##########################################
# Открытие категорий для покупки
@dp.callback_query_handler(text_startswith="hpeople_category_open:", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print('Открытие категорий для покупки user_menu.py 133')
    category_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    get_category = get_categoryx(category_id=category_id)
    city_id = get_city_user(call.from_user.id)[0]
    get_positions = get_positions_in_cityx(category_id=category_id, position_city_id=city_id, flagallc=1, position_type=1)  # get_positionsx(category_id=category_id)
    print(category_id, city_id)
    if len(get_positions) >= 1:
        source = "people"
        action = "open"
        await call.message.edit_text(_("<b>🎁 Товары категории:</b>", locale=lang) + get_category['category_name'],
                                     reply_markup=products_item_position_swipe_fp(0, action, category_id, city_id, source))
    else:
        await call.answer(f"❕ Товары в категории {get_category['category_name']} отсутствуют")



# Рейтинг позиции
@dp.callback_query_handler(text_startswith="rate_position:", state="*")
async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    rate = int(call.data.split(":")[2])
    get_settings = get_settingsx()
    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    print("LLLLL")
    
    city_id = 0

    add_ratex(position_id, user_id, rate)
    #remover, parent_id, city_id, action, lang
    await call.answer("❇️ Ваш оценка позиции успешно сохраненв!")
    #await call.message.edit_text("Ваша оценка сохранена.", reply_markup=products_item_category_swipe_fp(0, 0, city_id, "open", lang))
    #await call.answer("! ")

# Вернуться к категориям для покупки
@dp.callback_query_handler(text_startswith="buy_category_return", state="*")
async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
    get_categories = get_all_categoriesx()
    get_settings = get_settingsx()
    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']

    city_id = 0
    if get_settings['type_trade'] != 'digital':
        city_id = get_city_user(call.from_user.id)[0]

    if len(get_categories) >= 1:
        await call.message.edit_text(_("<b>🎁 Товары категории:</b>", locale=lang) + get_category['category_name'],
                                     reply_markup=products_item_category_swipe_fp(0, city_id, lang))
    else:
        await call.message.edit_text(_("<b>🎁 Товары в данное время отсутствуют.</b>", locale=lang))
        await call.answer("❗ Категории были изменены или удалены")


############################################ МАГАЗИН => КАТЕГОРИИ #############################
########################################### МАГАЗИНЫ ##########################################
# Открытие магазина для покупки
@dp.callback_query_handler(text_startswith="buy_shop_open", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print('Открытие магазина для покупки user_menu.py 1902')
    shop_id = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])
    lang = call.data.split(":")[3]
    print(shop_id, city_id, lang)
    get_shop = get_shopsxx(shop_id=shop_id)
    print(get_shop)
    user_id = call.from_user.id
    #lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    #city_id = get_city_user(user_id)[0]
    get_positions = get_shopposition_on_city(shop_id, city_id)

    if len(get_positions) >= 1:
        if len(get_shop[0]['logo']) >= 5:
            logo = get_shop[0]['logo']
            print(logo)
            if lang == "ru":
                await call.message.answer_photo(logo, f"<b>Магазин : {get_shop[0]['name']}</b>\n" \
                                                      f"Адрес : {get_shop[0]['address']}\n" \
                                                      f"Телефон : {get_shop[0]['phone']}\n" \
                                                      f"О магазине : {get_shop[0]['description']}")
            if lang == "en":
                await call.message.answer_photo(logo, f"<b>Shop : {get_shop[0]['name']}</b>\n" \
                                                      f"Address : {get_shop[0]['address']}\n" \
                                                      f"Phone : {get_shop[0]['phone']}\n" \
                                                      f"About Shop : {get_shop[0]['description']}")
        elif get_shop[0]['logo'] is Null:
            print("+++")
            if lang == "ru":
                await call.message.answer(f"<b>Магазин : {get_shop[0]['name']}</b>\n" \
                                                      f"Адрес : {get_shop[0]['address']}\n" \
                                                      f"Телефон : {get_shop[0]['phone']}\n" \
                                                      f"О магазине : {get_shop[0]['description']}")
            if lang == "en":
                await call.message.answer(f"<b>Shop : {get_shop[0]['name']}</b>\n" \
                                                      f"Address : {get_shop[0]['address']}\n" \
                                                      f"Phone : {get_shop[0]['phone']}\n" \
                                                      f"About Shop : {get_shop[0]['description']}")

        source = "commercial"
        #await call.message.answer_photo(logo, "<b>🎁 Выберите нужный вам товар:</b>",
        #                                    reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id))
        #else:
        #media = types.MediaGroup()
        #media.attach_photo(types.InputFile('media/Starbucks_Logo.jpg'), 'Превосходная фотография')
        #media.attach_photo(types.InputFile('media/Starbucks_Logo_2.jpg'), 'Превосходная фотография 2')
        #await bot.send_media_group(call.message.chat.id, media=media)

        await call.message.answer(_("<b>🎁 Товары магазина:</b>", locale=lang) + get_shop[0]['name'],
                                  reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id, source, lang))
    else:
        if lang == "ru":
            await call.answer(f"❕ Товары в магазине {get_shop[2]} отсутствуют")
        if lang == "en":
            await call.answer(f"❕ Products in shop <code>{get_shop[2]}</code> is not exist.")


# Открытие магазина для покупки
@dp.callback_query_handler(text_startswith="book_place_open", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print('Открытие магазина для покупки user_menu.py 133')
    place_id = int(call.data.split(":")[1])
    #get_shop = get_shopx(shop_id=shop_id)
    get_place = get_placesx(place_id=place_id)
    print(get_place)
    #if get_shop[8] != None: logo = get_shop[8]
    user_id = call.from_user.id
    city_id = get_city_user(user_id)[0]
    print("|||")
    print(city_id, get_place['place_id'])
    #print(remover, place_id, city_id)
    #get_events = get_events_in_place(place_id)  # get_positionsx(category_id=category_id)

    if get_place['place_id'] != "":
        print("|||->")
        logo = get_place['logo']
        await call.message.answer_photo(logo, f"<b>Место : {get_place['name']}</b>\n" \
                                              f"Адрес : {get_place['address']}\n" \
                                              f"Телефон : {get_place['phone']}")

        await call.message.answer("<b>Выберите что-нибудь интересное:</b>",
                                  reply_markup=events_in_place_swipe_fp(0, place_id, city_id))
    else:
        await call.answer(f"❕Cобытия места не загружены: {get_place['name']}, уточнить можно по телефону: {get_place['phone']}")


# Открытие магазина для покупки
@dp.callback_query_handler(text_startswith="book_event_open", state="*")
async def user_evebt_in_city_open(call: CallbackQuery, state: FSMContext):
    print('Открытие городских событий user_menu.py 1368')
    event_id = int(call.data.split(":")[1])
    get_event = get_eventxx(event_id=event_id)
    #city_id = int(call.data.split(":")[1])
    #get_shop = get_shopx(shop_id=shop_id)
    #get_events_in_city
    #get_shop = get_shopsxx(place_id=place_id)
    print(get_event)
    #if get_shop[8] != None: logo = get_shop[8]
    user_id = call.from_user.id
    #city_id = get_city_user(user_id)[0]
    get_positions = get_shopposition_on_city(shop_id, city_id)  # get_positionsx(category_id=category_id)

    if len(get_positions) >= 1:
        #if get_shop['logo'] != None:
        logo = get_shop[0]['logo']
        await call.message.answer_photo(logo, f"<b>Магазин : {get_shop[0]['name']}</b>\n" \
                                              f"Адрес : {get_shop[0]['address']}\n" \
                                              f"Телефон : {get_shop[0]['phone']}\n" \
                                              f"О магазине : {get_shop[0]['description']}")
        source = "commercial"
        #await call.message.answer_photo(logo, "<b>🎁 Выберите нужный вам товар:</b>",
        #                                    reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id))
        #else:
        #media = types.MediaGroup()
        #media.attach_photo(types.InputFile('media/Starbucks_Logo.jpg'), 'Превосходная фотография')
        #media.attach_photo(types.InputFile('media/Starbucks_Logo_2.jpg'), 'Превосходная фотография 2')
        #await bot.send_media_group(call.message.chat.id, media=media)

        await call.message.answer(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                  reply_markup=products_shopitem_position_swipe_fp(0, shop_id, city_id, source, lang))
    else:
        await call.answer(f"❕ Товары в магазине {get_shop[2]} отсутствуют")

########################################### ПОЗИЦИИ ##########################################
# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="book_event_open2:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print('Карточка товара: user_menu.py  1194')
    event_id = int(call.data.split(":")[1])
    #link = await get_start_link(str(f"deep_link&event_id&{event_id}"), encode=True)

    print(event_id)
    get_event = get_eventx(event_id=event_id)
    #if category_id != 0: get_category = get_categoryx(category_id=category_id)
    #else: get_category['category_name'] = 0
    #get_items = get_itemsx(position_id=position_id)
    get_settings = get_settingsx()
    #get_shop = get_shopx(shop_id=shop_id)
    print("|")

    if get_event['event_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_event['event_description']}"
    #get_shop['name']
    send_msg = f"<b>Карточка:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_position['position_name']}</code>\n" \
               f"🏙 Магазин: <code>{get_shop['name']}</code>\n" \
               f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
               f"🗃 Категория: <code></code>\n" \
               f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
               f"{text_description}"

    print(get_settings['type_trade'])
    tt = get_settings['type_trade']
    print("||")

    if tt != "digital":
        print("|||-")
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(1, position_id, remover, 0, shop_id))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(1, position_id, remover, 0, shop_id))
    else:
        print("|||--")
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, 0, shop_id))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(0, position_id, remover, 0, shop_id))

# Вернуться к категориям для покупки
@dp.callback_query_handler(text_startswith="buy_parcategory_return", state="*")
async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
    get_categories = get_all_categoriesx()
    get_settings = get_settingsx()
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang)
    city_id = 0
    if get_settings['type_trade'] != 'digital':
        city_id = get_city_user(call.from_user.id)[0]

    if len(get_categories) >= 1:
        await call.message.edit_text(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                     reply_markup=products_item_shop_open_fp(0, shop_id, city_id, lang))
    else:
        await call.message.edit_text(_("<b>🎁 Товары в данное время отсутствуют.</b>", locale=lang))
        await call.answer("❗ Категории были изменены или удалены")

########################################### ПОЗИЦИИ ##########################################
# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_parposition_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print('Карточка товара: user_menu.py  um2082')
    if call.data.split(":")[4]: city_id = 0
    position_id = int(call.data.split(":")[1])
    #category_id = int(call.data.split(":")[2])
    shop_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    city_id = int(call.data.split(":")[4])
    lang = call.data.split(":")[5]
    print(lang)
    print(position_id, shop_id, remover, city_id, lang)
    link = await get_start_link(str(f"deep_link&position_id&{position_id}"), encode=True)
    get_position = get_positionx(position_id=position_id)
    #get_items = get_itemsx(position_id=position_id)
    get_settings = get_settingsx()
    #get_shop = get_shopx(shop_id=shop_id)
    print("|")

    if lang == "en":
        description = "📜 Description:"
        cardtitle = "<b>Product Card:</b>"
        cardname = "🏷 Name:"
        cardlink = "🏷 Link:"
        cardshop = "🏙 Shop:"
        cardcity = "🏙 City:"
        cardcategory = "🗃 Category:"
        cardcost = "💰 Price:"

    elif lang == "ru":
        description = "📜 Описание:"
        cardtitle = "<b>Карточка:</b>"
        cardname = "🏷 Название:"
        cardlink = "🏷 Ссылка:"
        cardshop = "🏙 Магазин:"
        cardcity = "🏙 Город:"
        cardcategory = "🗃 Категория:"
        cardcost = "💰 Стоимость:"

    '''if get_position['position_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n{description}\n" \
                           f"{get_position['position_description']}"'''

    send_msg = f"{cardtitle}\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"{cardname} <code>{get_position['position_name']}</code>\n" \
               f"{cardlink} <code>{link}</code>\n" \
               f"{cardcity} <code>{get_position['position_city']}</code>\n" \
               f"{cardcost} <code>{get_position['position_price']}₽</code>\n"

    #f"{cardshop} <code>{get_shop['name']}</code>\n"
    #f"{cardcategory} <code>{category}</code>\n" \
    print(get_settings['type_trade'])
    tt = get_settings['type_trade']
    print("||")

    if get_position['position_type'] == 1: #tt != "digital":
        print("|||-")
        #    product_markup = products_open_finl(position_id, remover, category_id)
        # product_markup = products_open_cart_finl(position_id, remover, category_id)
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(1, position_id, remover, 0, shop_id, lang))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(1, position_id, remover, 0, shop_id, lang))
    elif get_position['position_type'] == 2:
        print("|||--")
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, 0, shop_id, lang))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(0, position_id, remover, 0, shop_id, lang))

# Вернуться к позициям для покупки
@dp.callback_query_handler(text_startswith="buy_parposition_return", state="*")
async def user_purchase_position_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    shop_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])

    print("buy_parposition_return")
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    print(lang)

    get_positions = get_all_positionsx()
    city_id = get_city_user(call.from_user.id)[0]

    if len(get_positions) >= 1:
        await call.message.delete()
        await call.message.answer(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                  reply_markup=products_shopitem_position_open_fp(remover, shop_id, city_id, lang))
    else:
        await call.message.edit_text(_("<b>🎁 Товары в данное время отсутствуют.</b>", locale=lang))
        await call.answer("❗ Позиции были изменены или удалены")

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_parcategory_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                 reply_markup=products_item_category_swipe_fp(remover))

# Переключение страницы позиций для покупки
@dp.callback_query_handler(text_startswith="buy_parposition_swipe:", state="*")
async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
    shop_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])
    source = call.data.split(":")[4]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    get_shop = get_shopx(shop_id=shop_id)

    await call.message.edit_text(f"<b>🎁 Текущий магазин: <code>{get_shop['name']}</code></b>",
                                 reply_markup=products_shopitem_position_swipe_fp(remover, shop_id, city_id, source, lang))

# Переключение страницы позиций для покупки
@dp.callback_query_handler(text_startswith="buy_position_swipe:", state="*")
async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    source = "commercial"
    action = "open"

    get_category = get_categoryx(category_id=category_id)

    await call.message.edit_text(_("<b>🎁 Текущая категория:</b>", locale=lang) + get_category['category_name'],
                                 reply_markup=products_item_position_swipe_fp(remover, action, category_id, city_id, source, lang))

# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_position_open:", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print('Карточка товара: user_menu.py  152')
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    city_id = int(call.data.split(":")[4])
    lang = call.data.split(":")[5]

    if lang == "en":
        description = "📜 Description: "
        cardtitle = "<b>Product Card:</b>"
        cardname = "🏷 Name:"
        cardlink = "🏷 Link:"
        cardrest = "🏷 Rest:"
        cardcity = "🏙 City:"
        cardcategory = "🗃 Category:"
        cardcost = "💰 Price:"

    elif lang == "ru":
        description = "📜 Описание:"
        cardtitle = "<b>Карточка:</b>"
        cardname = "🏷 Название:"
        cardlink = "🏷 Ссылка:"
        cardrest = "🏷 Остаток:"
        cardcity = "🏙 Город:"
        cardcategory = "🗃 Категория:"
        cardcost = "💰 Стоимость:"
    print(position_id, category_id, remover, city_id, lang)
    get_category = ""
    category = ""
    link = await get_start_link(str(f"deep_link&position_id&{position_id}"), encode=True)

    get_position = get_positionx(position_id=position_id)
    position_source = get_position['source']
    if position_source == "commercial":
        get_category = get_categoryx(category_id=category_id)
        category = get_category['category_name']
    elif position_source == "people":
        get_category = get_category_people(category_id=category_id)
        category = get_category['category']

    if get_position['position_type'] == 1:
        position_rest = get_position['position_rest']
    elif get_position['position_type'] == 2:
        position_rest = len(get_itemsx(position_id=position_id))

    get_settings = get_settingsx()

    if get_position['position_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n{description}\n\n" \
                           f"{get_position['position_description']}"

    if get_position['position_type'] == 1:
        send_msg = f"{cardtitle}\n" \
                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"{cardname} <code>{get_position['position_name']}</code>\n" \
                   f"{cardlink} <code>{link}</code>\n" \
                   f"{cardcity} <code>{get_position['position_city']}</code>\n" \
                   f"{cardcategory} <code>{category}</code>\n" \
                   f"{cardrest} <code>{position_rest}шт</code>\n" \
                   f"{cardcost} <code>{get_position['position_price']}₽</code>\n" \
                   f"{text_description}"

    if get_position['position_type'] == 2:
        send_msg = f"{cardtitle}\n" \
                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"{cardname} <code>{get_position['position_name']}</code>\n" \
                   f"{cardlink} <code>{link}</code>\n" \
                   f"{cardcategory} <code>{category}</code>\n" \
                   f"{cardrest} <code>{position_rest}шт</code>\n" \
                   f"{cardcost} <code>{get_position['position_price']}₽</code>\n" \
                   f"{text_description}"

    print(get_settings['type_trade'])
    tt = get_settings['type_trade']

    if tt == "digital":
        if len(get_position['position_photo']) >= 5:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, category_id, 0, lang))
        else:
            await call.message.edit_text(send_msg,
                                         reply_markup=products_open_finl(0, position_id, remover, category_id, 0, lang))

    elif tt == "hybrid" and len(get_position['position_photo']) >= 5:
        #print(get_position['position_photo'])
        if get_position['position_type'] == 1:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(1, position_id, remover, category_id, 0, lang))

        if get_position['position_type'] == 2:
            await call.message.delete()
            await call.message.answer_photo(get_position['position_photo'],
                                            send_msg, reply_markup=products_open_finl(0, position_id, remover, category_id, 0, lang))

    elif len(get_position['position_photo']) < 6:
        print("0O0O0")
        #if path is None:
            #rd = Path(__file__).parents
            #base_dir = rd[1]
            #path = str(f"{base_dir}{os.sep}images")
        #photop = f"./../images/{get_position['position_photo']}.jpg"
        #print(photop)
        #photo = open(photop, 'rb')

        #await call.message.answer_photo(photo,
        #                            send_msg, reply_markup=products_open_finl(1, position_id, remover, category_id, 0, lang))
        await call.message.edit_text(send_msg,
                                     reply_markup=products_open_finl(1, position_id, remover, category_id, 0, lang))
    else:
        await call.message.edit_text(send_msg,
                                     reply_markup=products_open_finl(1, position_id, remover, category_id, 0, lang))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="artist_edit_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])

    await call.message.edit_text(_("<b>🎁 Выберите нужного артиста:</b>", locale=lang),
                                 reply_markup=artist_edit_open_fp(remover, user_id))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_people_category_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    level = int(call.data.split(":")[3])
    parent = int(call.data.split(":")[4])
    city_id = int(call.data.split(":")[5])
    action = call.data.split(":")[6]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(lang, city_id)

    await call.message.edit_text(_("<b>🌐 Выберите категорию:</b>", locale=lang),
                                 reply_markup=position_people_create_open_fp(category_id, remover, level, parent, city_id, action, lang))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    #level = int(call.data.split(":")[2])
    parent_id = int(call.data.split(":")[2])
    city_id = int(call.data.split(":")[3])
    action = call.data.split(":")[4]
    #level = int(call.data.split(":")[5])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    #await call.message.edit_text
    #await call.message.delete()

    await call.message.edit_text(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                 reply_markup=products_item_category_swipe_fp(remover, parent_id, city_id, action, lang))

# Переключение страниц категорий для покупки
@dp.callback_query_handler(text_startswith="buy_shop_swipe:", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    city_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                 reply_markup=products_item_shop_swipe_fp(remover, city_id, lang))

# Вернуться к позициям для покупки
@dp.callback_query_handler(text_startswith="buy_position_return", state="*")
async def user_purchase_position_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    shop_id = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    #get_positions = get_all_positionsx()
    city_id = get_city_user(call.from_user.id)[0]
    print(remover, category_id, shop_id, city_id)
    print("buy_position_return")
    source = "commercial"
    #if len(get_positions) >= 1:
    await call.message.delete()
    if shop_id == 0:
        print("||||--=")
        #user_id = call.from_user.id
        #lang = get_user_lang(user_id)['user_lang']
        action = "open"

        await call.message.answer(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                  reply_markup=products_item_position_swipe_fp(remover, action, category_id, city_id, source, lang))
    elif category_id == 0:
        print("||||--==---")
        await call.message.answer(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                  reply_markup=products_shopitem_position_swipe_fp(remover, shop_id, city_id, source, lang))
    #else:
    #    await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
    #    await call.answer("❗ Позиции были изменены или удалены")


########################################### ПОКУПКА ##########################################
# Выбор количества товаров в корзине
@dp.callback_query_handler(text_startswith="add_item_cart", state="*")
async def user_purchase_addcart(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    print("Добавление в корзину")
    get_position = get_positionx(position_id=position_id)
    print(get_position)
    get_user = get_userx(user_id=get_position['position_user_id'])
    get_payments = get_upaymentx(get_position['position_user_id'])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']


    if get_position['position_type'] == 1:
        get_count = get_position['position_rest']
    elif get_position['position_type'] == 2:
        get_items = get_itemsx(position_id=position_id)
        get_count = len(get_items)

    await state.update_data(here_cache_position_type = get_position['position_type'])
    await state.update_data(here_cache_get_count = get_count)



    if get_payments['way_freecredi'] == 'True':
        await state.update_data(here_cache_skipchkbalance = 1)

    source = get_position['source']

    if get_count == 1:
        await state.update_data(here_cache_position_id=position_id)
        await state.finish()

        await call.message.delete()
        if lang == "ru":
            await call.message.answer(f"<b>1 шт. в наличии. Добавить товар(ы) в корзину?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Остаток: <code>1шт</code>\n"
                                      f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                      reply_markup=products_addcart_confirm_finl(position_id, 1, lang))
        if lang == "en":
            await call.message.answer(f"<b>1 pcs. in stock. Add goods to cart?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Goods: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Rest: <code>1шт</code>\n"
                                      f"💰 Amount to order: <code>{get_position['position_price']}R</code>",
                                      reply_markup=products_addcart_confirm_finl(position_id, 1, lang))
    elif get_count >= 1:
        await state.update_data(here_cache_position_id=position_id)
        await state.set_state("here_itemsadd_cart")

        await call.message.delete()
        if lang == "ru":
            await call.message.answer(f"<b>🎁 Введите количество товаров для покупки</b>\n"
                                      f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
        if lang == "en":
            await call.message.answer(f"<b>🎁 Enter quantity of goods to order</b>\n"
                                      f"▶ From <code>1</code> till <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Good: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Your balance: <code>{get_user['user_balance']}R</code>")
    else:
        if lang == "ru":
            await call.answer("🎁 Товара нет в наличии")
        if lang == "en":
            await call.answer("🎁 Sorry. Product not in stock.")


# Принятие количества товаров в корзине
@dp.message_handler(state="here_itemsadd_cart")
async def user_purchase_select_count(message: Message, state: FSMContext):
    position_id = (await state.get_data())['here_cache_position_id']
    get_position = get_positionx(position_id=position_id)
    #user_id=message.from_user.id
    #данные пользователя
    get_user = get_userx(user_id=get_position['position_user_id'])
    #данные платежных систем
    get_payments = get_upaymentx(get_position['position_user_id'])
    print(get_payments)
    #данные пользователя
    get_user = get_userx(user_id=message.from_user.id)
    lang = get_userx(user_id=message.from_user.id)['user_lang']

    skipchkbalance = 1 if get_payments['way_freecredi'] == 'True' else 0
    get_count = (await state.get_data())['here_cache_get_count']
    position_type = (await state.get_data())['here_cache_position_type']

    if position_type == 1:
        get_items = get_position['position_rest']
        get_count = get_position['position_rest']
        if get_position['position_price'] != 0 and skipchkbalance != 1:
            get_count_balance = int(get_user['user_balance'] / get_position['position_price'])

    elif position_type == 2:
        get_items = get_itemsx(position_id=position_id)
        get_count = len(get_items)
        get_count = min(get_count, len(get_items))

    if lang == "ru":
        send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                       f"🎁 Введите количество товаров для покупки\n" \
                       f"▶ От <code>1</code> до <code>{get_count}</code>\n" \
                       f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                       f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n" \
                       f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>"
    if lang == "en":
        send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                       f"🎁 Enter quantity of good to order\n" \
                       f"▶ From <code>1</code> till <code>{get_count}</code>\n" \
                       f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                       f"🎁 Goods: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n" \
                       f"💰 Your balance: <code>{get_user['user_balance']}R</code>"

    if message.text:
        get_buy = int(message.text)
        amount_pay = int(get_position['position_price']) * get_buy
        print(get_count)

        if position_type == 1 and get_count >= 1:
            await state.finish()
            if lang == "ru":
                await message.answer(f"<b>🎁 Вы действительно хотите добавить в корзину товар(ы)?</b>\n"
                                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                     f"📦 Остаток: <code>{get_count}шт</code>\n"
                                     f"💰 Сумма добавляемых товаров: <code>{amount_pay}₽</code>",
                                     reply_markup=products_addcart_confirm_finl(position_id, get_buy, lang))
            if lang == "en":
                await message.answer(f"<b>🎁 Do you wannna add goods to order?</b>\n"
                                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"🎁 Good: <code>{get_position['position_name']}</code>\n"
                                     f"📦 Rest: <code>{get_count}pcs</code>\n"
                                     f"💰 Amount to add: <code>{amount_pay}R</code>",
                                     reply_markup=products_addcart_confirm_finl(position_id, get_buy, lang))
        else:
            await state.finish()
            await message.answer(_("<b>🎁 Товар который вы хотели купить, закончился</b>", locale=lang))
    else:
        await message.answer(_("<b>❌ Данные были введены неверно.</b>", locale=lang))


# Подтверждение добавления товара в корзину
@dp.callback_query_handler(text_startswith="xaddcart_item", state="*")
async def user_addcart_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    get_buy = int(call.data.split(":")[3])
    lang = call.data.split(":")[4]
    get_position = get_positionx(position_id=position_id)
    if get_action == "yes":
        await call.message.edit_text(_("<b>🔄 Ждите, товары подготавливаются</b>", locale=lang))

        get_position = get_positionx(position_id=position_id)

        position_type = get_position['position_type']

        if position_type == 1:
            get_count = get_position['position_rest']
            get_items = get_count
        elif position_type == 2:
            get_items = get_itemsx(position_id=position_id)
            get_count = len(get_items)

        get_user = get_userx(user_id=call.from_user.id)

        amount_pay = int(get_position['position_price'] * get_buy)

        if position_type == 1:
            await notify(dp, f"Позиция: {get_position['position_name']} добавлена в корзину пользователем: {call.from_user.id}.")

            send_count = get_buy
            # уточнение цены за количество в наличии
            if get_buy != send_count:
                amount_pay = int(get_position['position_price'] * send_buy)

            receipt = get_unix()
            add_time = get_date()
            print(add_time)

            await call.message.delete()

            await asyncio.sleep(0.3)

            users_order = get_params_orderx(user_id=get_user['user_id'], order_state='created')
            print(users_order)
            alength = len(users_order)
            i = 0
            for i in range(alength):
                print(users_order[i]['order_id'])

            print('test2')

            if not users_order:
                create_orderx(call.from_user.id, get_user['user_login'], get_user['user_name'], 'created', str(add_time), receipt)
                users_order = get_params_orderx(user_id=get_user['user_id'], order_state='created')

            print('test3')
            for i in range(alength):
                print(users_order[i]['order_id'])
            order_id = users_order[i]['order_id']

            add_order_itemx(call.from_user.id, order_id, position_id, get_buy, get_position['position_price'], receipt, get_position['position_user_id'])
            new_position_rest = int(get_position['position_rest']) - get_buy
            update_positionx(get_position['position_id'], position_rest=new_position_rest)

            auser = (
                get_user['user_login']
                if len(get_user['user_login']) >= 1
                else get_user['user_id']
            )
            await notify(dp, f"Позиция: {get_position['position_name']} добавлена в корзину. Пользователь: @{auser}.")

            if lang == "ru":
                await call.message.answer(f"<b>✅ Вы успешно добавили товар(ы) в корзину</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"🧾 Чек: <code>#{receipt}</code>\n"
                                          f"🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>\n"
                                          f"🕰 Дата покупки: <code>{add_time}</code>",
                                          reply_markup=menu_frep(call.from_user.id, lang))
            if lang == "en":
                await call.message.answer(f"<b>✅ Goods has been added to cart successfully</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"🧾 Receipt: <code>#{receipt}</code>\n"
                                          f"🎁 Good: <code>{get_position['position_name']} | {get_count}pcs | {amount_pay}R</code>\n"
                                          f"🕰 Date: <code>{add_time}</code>",
                                          reply_markup=menu_frep(call.from_user.id, lang))
        elif position_type == 2:
            if 1 <= get_buy <= len(get_items):
                save_items, send_count, split_len = buy_itemx(get_items, get_buy)
                await notify(dp, f"Позиция: {get_position['position_name']} добавлена в корзину пользователем: {call.from_user.id}.")
            await call.message.answer(_("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>", locale=lang),
                                      reply_markup=menu_frep(call.from_user.id, lang))
        else:
            await call.message.answer(_("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>", locale=lang),
                                      reply_markup=menu_frep(call.from_user.id, lang))
    elif len(get_all_categoriesx()) >= 1:
        await call.message.edit_text(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                     reply_markup=category_edit_open_fp(0, lang))
    else:
        await call.message.edit_text(_("<b>✅ Вы отменили покупку товаров.</b>", locale=lang))


# Удаление корзины
@dp.callback_query_handler(text_startswith="del_user_cart", state="*")
async def del_user_cart(call: CallbackQuery, state: FSMContext):
    order_id = int(call.data.split(":")[1])
    print("||||")
    user_id=call.from_user.id
    user = get_userx(user_id=user_id)
    lang = user['user_lang']
    print(lang)
    await state.finish()
    await call.message.edit_text(_("<b> Удалить корзину и ее позиции?</b>", locale=lang),
                                 reply_markup=confirm_delete_user_cart_inl(order_id, lang))

# Подтверждение удаления корзины
@dp.callback_query_handler(text_startswith="confirm_del_user_cart", state="*")
async def confirm_del_user_cart(call: CallbackQuery, state: FSMContext):
    order_id = int(call.data.split(":")[1])
    print(order_id)
    user_id=call.from_user.id
    print(user_id)
    #lang = get_userx(user_id=user_id)['user_lang']
    order_id=order['order_id']
    #возврат количества в товаров в позиции
    orderdata = get_orderxo(order_id=order_id)
    print(orderdata)
    ouser_id = orderdata['user_id']
    oget_user = get_userx(user_id=ouser_id)
    user_role = oget_user['user_role']
    print(user_role)
    #получаем баланс пользователя
    ub = oget_user['user_balance']
    #username
    if oget_user['user_login']:
        userid = f"Логин пользователя: <code>@{oget_user['user_login']}</code>"
    else: userid = f"Телеграм ID: <code>{oget_user['user_id']}</code>"
    #позиции заказа
    get_positions = []
    get_positions = get_cart_positionsx(order_id=order_id)

    this_items = []
    this_itemst = this_itemst2 = this_itemst3 = ''
    for position in get_positions:
        current_position = get_positionx(position_id=position['position_id'])
        new_position_rest = current_position['position_rest'] + position['count']
        update_positionx(position['position_id'], position_rest=new_position_rest)

    remove_ordersx(order_id=order_id)
    remove_orders_itemx(order_id=order_id)

    print("|||| -   - ||||")
    await call.message.edit_text(f"<b>✅ Вы удалили корзину #{order_id}.</b>")


#######################################################################################
# **************************  CHECK OUT CART ******************************************
#######################################################################################

# Оформление заказа по корзине - Адрес
@dp.callback_query_handler(text_startswith="checkout_start", state="*")
async def checkout_start(call: CallbackQuery, state: FSMContext):
    order_id = int(call.data.split(":")[1])
    print(order_id)
    user_id = call.from_user.id
    get_user = get_userx(user_id=user_id)
    ub = get_user['user_balance']
    order_sum = calc_order_summ(order_id=order_id)
    dso = get_delivery_seller_options(order_id)['free_delivery_point']
    print(dso)
    delivery_rate = get_delivery_seller_options(order_id)['delivery_rate']
    print(delivery_rate)
    delivery = 0 if order_sum > dso else delivery_rate
    print(f"Доставка:{str(delivery)}")
    print("|||->")
    order_total = order_sum + delivery
    adr = geo = phone = 0
    touser_id = get_cart_sellersx(order_id)
    get_payment = get_upaymentx(user_id=touser_id) #True / False - постоплата
    freecredi_method = 1 if get_payment['way_freecredi'] else 0
    print(user_id)

    if get_user['user_address'] != "":
        print("Адрес есть")
        adr = 1
    if get_user['user_geocode'] != "":
        print("Геокод есть")
        geo = 1
    if get_user['user_phone'] != "":
        print("Телефон есть")
        phone = 1

    await call.message.answer(f"<b> Начинаем оформление заказа.</b>\n")

    if phone == 0:
        await state.set_state("enter_phone_auto")

    if adr == 0:
        await state.set_state("enter_address_manualy")

    if ub < order_total and freecredi_method == 0:
        await state.set_state("user_balance_lower_than_cart")
        await call.message.delete()
        await call.message.answer(f"<b>Суммы на Вашем балансе не достаточно для оформления заказа.</b>\n"
                                  f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                  f" Баланс: <code>{ub}</code>\n"
                                  f" Сумма заказа: <code>{order_total}</code>\n",
                                  reply_markup=order_user_refill)
    else:
        await state.set_state("checkout_finish")
        await call.message.answer(f"<b>Продолхить оформление заказа:.</b>\n",
                                  reply_markup=checkout_step2_accept_finl(order_id))


# Принятие адреса для доставки
@dp.callback_query_handler(text_startswith="checkout_finish:", state="*")
async def checkout_finish(call: CallbackQuery, state: FSMContext):
    order_id = int(call.data.split(":")[1])
    print('checkout_finish')
    print(order_id)
    #проверка - есть вопросы без ответов
    touser_id = call.from_user.id
    if cm := get_user_messagesx(to_uid=touser_id, state='created'):
        print(f"Messages present:{str(touser_id)}")
    #статус заказа - delivery
    print("|||->")
    print("||||->>>>")
    print(order_id)
    os = update_orderx(order_id=order_id, order_state='delivery')
    await call.message.answer("<b>Начинаем доставку товара Вашей корзины.</b>")

    print('Сумма заказа на холде')
    order_sum = calc_order_summ(order_id=order_id)
    dso = get_delivery_seller_options(order_id)['free_delivery_point']
    print(dso)
    delivery_rate = get_delivery_seller_options(order_id)['delivery_rate']
    print(delivery_rate)

    delivery = 0 if order_sum > dso else delivery_rate
    print(f"Доставка:{str(delivery)}")
    print("||||-")
    amount = order_sum + delivery
    await notify(dp, f"Оформлен заказ: {order_id},\n"
                     f"пользователя: {touser_id}\n"
                     f"на сумму: {order_sum}\n"
                     f"с доставкой: {delivery}")

    buyer = touser_id
    print("||||--")
    order_sellers = get_order_sellers(order_id)
    print(order_sellers)
    if(len(order_sellers)>1): print("продавцов более 1")

    print(type(order_sellers))
    order_sellers = order_sellers.strip('[[')
    order_sellers = order_sellers.strip(']]')

    get_payment = get_upaymentx(user_id=order_sellers) #True / False - постоплата
    freecredi_method = 1 if get_payment['way_freecredi'] else 0
    if freecredi_method == 0:
        state = 'created'
        validity = 5
        h = create_holdx(
            order_id,
            int(buyer),
            int(str(order_sellers)),
            int(amount),
            validity,
            state,
        )
        i = update_userx(user_id = buyer, user_hold = amount)
        await call.message.answer(f"<b>Денежные средства в размере {amount}р. успешно заблокированы до \n"
                                  f"подтверждения получения покупателем товара.</b>")
    elif freecredi_method == 1:
        await call.message.answer(
            "<b>Заказ начал выполняться. Подтвердите получение товара по факту.</b>"
        )

# Оформление заказа по корзине - Адрес
@dp.callback_query_handler(text_startswith="pay_after_delivery", state="*")
async def pay_after_delivery(call: CallbackQuery, state: FSMContext):
    order_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    print(order_id)
    order_sellers = get_order_sellers(order_id)
    print(order_sellers)
    if(len(order_sellers)>1): print("продавцов более 1")
    print(type(order_sellers))
    order_sellers = order_sellers.strip('[[')
    order_sellers = order_sellers.strip(']]')
    print(order_sellers)
    get_payment = get_upaymentx(user_id=order_sellers) #True / False - постоплата
    if get_payment['way_freecredi']:
        freecredi_method = 1
        os = update_orderx(order_id=order_id, payafterdelivery=1)
        await call.message.answer(f"<b>Постоплата применена к заказу успешно!</b>\n")
    else:
        freecredi_method = 0
        await call.message.answer(f"<b>Постоплата не поддерживается продавцом по Вашему заказу!</b>\n")


# Оформление заказа по корзине - Адрес
@dp.callback_query_handler(text_startswith="submit_order", state="*")
async def submit_order(call: CallbackQuery, state: FSMContext):
    order_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    buyer_data = get_userx(user_id=user_id)
    print(buyer_data)
    #order_data = get_orderx(user_id=user_id)
    #order_id = order_data['order_id']

    order_sum = calc_order_summ(order_id=order_id)
    dso = get_delivery_seller_options(order_id)['free_delivery_point']
    print(dso)
    #free_delivery_point = dso['free_delivery_point']
    #print(free_delivery_point)
    delivery_rate = get_delivery_seller_options(order_id)['delivery_rate']
    print(delivery_rate)
    #delivery = 200
    delivery = 0 if order_sum > dso else delivery_rate
    print(f"Доставка:{str(delivery)}")
    print("||||-")
    amount = order_sum + delivery

    print(order_id)
    order_sellers = get_order_sellers(order_id)

    print(order_sellers)
    if(len(order_sellers)>1): print("продавцов более 1")
    #for seller in order_sellers:
    print(type(order_sellers))
    order_sellers = order_sellers.strip('[[')
    order_sellers = order_sellers.strip(']]')
    print(int(order_sellers))
    get_payment = get_upaymentx(user_id=int(order_sellers)) #True / False - постоплата
    print(get_payment)
    seller_data = ""
    if get_payment['way_freecredi']:
        freecredi_method = 1
        #транзакция с холдом
        seller_rest = int(seller_data['user_balance'])+int(amount)
    else:
        freecredi_method = 0
        hold_data = get_orders_holdsx(order_id)
        #hold_data = hold_data.strip('[')
        #hold_data = hold_data.strip(']')
        print(hold_data)
        #print(hold_data[0]['seller'])
        #seller
        seller_data = get_userx(user_id=hold_data[0]['seller'])
        print(seller_data)
        #hold_data['seller']
        #изменение статуса заказа   submitted
        #снятие холда с суммы заказа
        a = update_holdx(order_id = order_id, state = 'released')
        #транзакция с холдом
        seller_rest = int(seller_data['user_balance'])+int(hold_data[0]['amount'])
        buyer_rest = int(buyer_data['user_balance'])-int(hold_data[0]['amount'])
        #списание у покупателя
        b = update_userx(user_id, user_balance=buyer_rest)
    #buyer_rest = int(buyer_data['user_balance'])-int(hold_data[0]['amount'])
    #списание у покупателя
    #b = update_userx(user_id, user_balance=buyer_rest)
    #пополнение у продавца
    c = update_userx(order_sellers, user_balance=seller_rest)
    os = update_orderx(order_id=order_id, order_state='submitted', active=0)
    await call.message.answer(f"<b>Покупка завершена, возвращайтесь!</b>\n")

@dp.callback_query_handler(text="reply_toorder_message", state="*")
async def reply_toorder_message(call: CallbackQuery, state: FSMContext):
    print('reply_toorder_message')
    # order_id = int(call.data.split(":")[1])
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    print(user_id)
    get_user = get_userx(user_id=user_id)

    # get_user = get_userx(user_id=call.from_user.id)
    await state.set_state("reply_toorder_message_fin")

    # await call.message.delete()
    await call.message.answer(f"<b>Пожалуйста, введите сообщение для покупателя:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="reply_toorder_message_fin")
async def reply_toorder_message_fin(message: Message, state: FSMContext):
    print('reply_toorder_message_fin')
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    users_order = get_user_orderx(user_id)
    order_id = users_order['order_id']
    await state.finish()

    if message.text:
        messagetxt = str(message.text)
        print(str(user_id) + messagetxt)
        touser_id = get_cart_sellersx(order_id)
        print(touser_id)

        add_messagex(from_id=user_id, to_id=touser_id, order_id = order_id, txtmessage=messagetxt, photo='', state='responded')

    await message.delete()
    await message.answer(f"<b>✅ Было отправлено следующее сообщение покупателю:</b>\n"
                         + messagetxt, reply_markup=cart_enter_message_finl(user_id))

    cm = get_user_messagesx(to_uid=touser_id, state='responded')
    if len(cm) > 0:
        print(f"Messages present:{str(touser_id)}")

    await dp.bot.send_message(
        chat_id=touser_id,
        text=f"Сообщение/вопрос по заказу от продавца:{messagetxt}",
        reply_markup=reply_order_message_finl(order_id),
    )

@dp.callback_query_handler(text="enter_message_manualy", state="*")
async def enter_message_manualy(call: CallbackQuery, state: FSMContext):
    print('enter_message_manualy')
    user_id = call.from_user.id
    print(user_id)
    get_user = get_userx(user_id=user_id)

    await state.set_state("enter_message_manualy_fin")

    await call.message.answer(f"<b>Пожалуйста, введите сообщение для продавца:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_message_manualy_fin")
async def enter_message_manualy_fin(message: Message, state: FSMContext):
    print('enter_message_manualy_fin')
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    users_order = get_user_orderx(user_id)
    order_id = users_order['order_id']
    await state.finish()

    if message.text:
        messagetxt = str(message.text)
        print(str(user_id) + messagetxt)
        touser_id = get_cart_sellersx(order_id)
        print(touser_id)

        add_messagex(from_id=user_id, to_id=touser_id, order_id = order_id, txtmessage=messagetxt, photo='', state='created')

    await message.delete()
    await message.answer(f"<b>✅ Было отправлено следующее сообщение продавцу:</b>\n"
                         + messagetxt, reply_markup=cart_enter_message_finl(user_id))

    cm = get_user_messagesx(to_uid=touser_id, state='created')
    if len(cm) > 0:
        print(f"Messages present:{str(touser_id)}")

    await dp.bot.send_message(
        chat_id=touser_id,
        text=f"Сообщение/вопрос по заказу от покупателя:{messagetxt}",
        reply_markup=reply_order_message_finl(order_id),
    )

@dp.callback_query_handler(text_startswith="enter_phone_auto", state="*")
async def enter_phone_man(call: CallbackQuery, state: FSMContext):
    print('enter_phone_auto')
    user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_phone_auto_fin")

    button_phone = KeyboardButton(text="Делись!", request_contact=True)
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button_phone)
    await call.message.answer(
        "<b>✅ Вы можете поделиться своим номером телефона.</b>",
        reply_markup=menu_frep(message.from_user.id),
    )

    '''await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш номер телефона:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")'''

@dp.message_handler(content_types=['contact'], state="enter_phone_auto_fin")  # content_types=ContentType.CONTACT,
async def contacts(message: Message, state: FSMContext):
    phone = message.contact.phone_number

    print(phone)
    phone = str(message.text)
    phone = message.contact.phone_number
    update_userx(message.from_user.id, user_phone=phone)

    await message.answer(f"Ваш номер сохранен в Вашем личном кабинете: {message.contact.phone_number}",
                         reply_markup=ReplyKeyboardRemove())  # , reply_markup=types.ReplyKeyboardRemove()
    await state.finish()

    await message.answer(f"<b>✅ Номер телефон был успешно изменен на следующий:</b>\n"
                         + str(phone), reply_markup=accept_saved_phone(message.from_user.id))


'''
    await message.answer("🔸 Мы снова с Вами!.\n"
                     "🔸 Если не появились вспомогательные кнопки\n"
                     "▶ Введите /start",
                     reply_markup=menu_frep(message.from_user.id)) '''


# Принятие адреса для доставки
@dp.message_handler(state="enter_phone_auto_fin2")
async def user_get_phone(message: Message, state: FSMContext):
    print('enter_phone_auto_fin')
    phone = message.contact.phone_number
    get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    print(phone)

    await message.delete()
    await message.answer(f"<b>✅ Номер телефон был успешно изменен на следующий:</b>\n"
                         + phone, reply_markup=accept_saved_phone(message.from_user.id))

@dp.callback_query_handler(text_startswith="enter_phone_manualy", state="*")
async def enter_phone_man(call: CallbackQuery, state: FSMContext):
    print('enter_phone_manualy')
    user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_phone_manualy_fin")

    await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш номер телефона:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_phone_manualy_fin")
async def user_enter_phone(message: Message, state: FSMContext):
    print('enter_phone_manualy_fin')
    # user_id = int(call.data.split(":")[1])
    get_user = get_userx(user_id=message.from_user.id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        phone = str(message.text)
        update_userx(message.from_user.id, user_phone=phone)

    await message.delete()
    await message.answer(f"<b>✅ Номер телефон был успешно изменен на следующий:</b>\n"
                         + phone, reply_markup=accept_saved_phone(message.from_user.id))

@dp.callback_query_handler(text_startswith="enter_address_manualy", state="*")
async def enter_address_man(call: CallbackQuery, state: FSMContext):
    print('enter_address_manualy')
    # user_id = int(call.data.split(":")[1])
    # user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    # get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_address_manualy_fin")

    await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш адрес:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_address_manualy_fin")
async def user_enter_addr(message: Message, state: FSMContext):
    print('enter_address_manualy_fin')
    #user_id = int(message.split(":")[1])
    user_id = message.from_user.id
    get_user = get_userx(user_id=user_id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        address = str(message.text)
        update_userx(message.from_user.id, user_address=address)

    await message.delete()
    await message.answer(f"<b>✅ Адрес доставки был успешно изменен на следующий:</b>\n"
                         + address, reply_markup=accept_saved_adr(message.from_user.id))

# Выбор количества товаров для покупки
@dp.callback_query_handler(text_startswith="buy_item_select", state="*")
async def buy_item_select(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)
    lang = get_user['user_lang']

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        #get_count = min(get_count, len(get_items))
    else:
        get_count = len(get_items)

    if get_items == 0: get_count = 0

    if int(get_user['user_balance']) >= int(get_position['position_price']):
        if get_count == 0:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            await call.message.delete()
            await call.message.answer(f"<b>🎁 К сожалению данный товар закончился!</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code>",
                                      reply_markup=products_confirm_finl(position_id, 1, lang))

        if get_count == 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Количество: <code>1шт</code>\n"
                                      f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                      reply_markup=products_confirm_finl(position_id, 1, lang))
        elif get_count >= 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.set_state("here_item_count")

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Введите количество товаров для покупки</b>\n"
                                      f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
        else:
            await call.answer("🎁 Товаров нет в наличии")
    else:
        #await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)
        #await call.message.delete()
        await call.message.answer("<b>❗ У вас недостаточно средств. Пополните баланс</b>", reply_markup=charge_button_add(0))


@dp.callback_query_handler(text_startswith="edit_delivery_settings", state="*")
async def enter_phone_man(call: CallbackQuery, state: FSMContext):
    print('edit_delivery_settings')
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)

    # get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("edit_delivery_settings_fin")

    await call.message.delete()
    await call.message.answer(f"<b>Введите минимальный порог бесплатной доставки X и ставку доставки по городу Y через пробел:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="edit_delivery_settings_fin")
async def user_enter_phone(message: Message, state: FSMContext):
    print('edit_delivery_settings_fin')
    # user_id = int(call.data.split(":")[1])
    get_user = get_userx(user_id=message.from_user.id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        free_delivery_point, delivery_rate = str(message.text).split()
        if free_delivery_point and delivery_rate:
            update_userx(message.from_user.id, free_delivery_point=free_delivery_point, delivery_rate=delivery_rate)
            await message.delete()
            await message.answer(f"<b>✅ Настройки были установлены: X={free_delivery_point}, Y={delivery_rate}.</b>\n"
                                 , reply_markup=edit_delivery_settings_finl())
        else:
            await message.delete()
            await message.answer(f"<b>⭕ Настройки не были установлены. Проверьте написание или уточните там, где Вы его получили.</b>\n"
                                 , reply_markup=edit_delivery_settings_finl())


@dp.callback_query_handler(text_startswith="enter_promocode", state="*")
async def enter_phone_man(call: CallbackQuery, state: FSMContext):
    print('enter_promocode')
    # user_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    get_user = get_userx(user_id=call.from_user.id)
    # get_user = get_userx(user_id=call.from_user.id)

    await state.set_state("enter_promocode_fin")

    await call.message.delete()
    await call.message.answer(f"<b>🎁 Введите Ваш промокод и мы его применим:</b>\n"
                              f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n")

# Принятие адреса для доставки
@dp.message_handler(state="enter_promocode_fin")
async def user_enter_phone(message: Message, state: FSMContext):
    print('enter_promocode_fin')
    # user_id = int(call.data.split(":")[1])
    get_user = get_userx(user_id=message.from_user.id)
    # get_user = get_userx(user_id=message.from_user.id)
    await state.finish()

    if message.text:
        promocodeutxt = str(message.text)
        if promocode := get_promocodex(promocode=promocodeutxt):
            update_userx(message.from_user.id, promocode=promocodeutxt)
            await message.delete()
            await message.answer(f"<b>✅ Ваш промокод был успешно применен. Размер Вашей скидки теперь: {promocode['discount']} </b>\n"
                                 , reply_markup=enter_promocode_finl())
        else:
            await message.delete()
            await message.answer(f"<b>⭕ Ваш промокод не был найден. Проверьте написание или уточните там, где Вы его получили.</b>\n"
                                 , reply_markup=enter_promocode_finl())


# -------------------------------------------------------------------------------------
# Выбор количества товаров для покупки
@dp.callback_query_handler(text_startswith="buy_item_select", state="*")
async def user_purchase_select(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] / get_position['position_price'])
        get_count = min(get_count, len(get_items))
    else:
        get_count = len(get_items)

    if int(get_user['user_balance']) >= int(get_position['position_price']):
        if get_count == 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Количество: <code>1шт</code>\n"
                                      f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                      reply_markup=products_confirm_finl(position_id, 1))
        elif get_count >= 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.set_state("here_item_count")

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Введите количество товаров для покупки</b>\n"
                                      f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
        else:
            await call.answer("🎁 Товаров нет в наличии")
    else:
        #await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)
        #await call.message.delete()
        await call.message.answer(
            "<b>❗ У вас недостаточно средств. Пополните баланс</b>",
            reply_markup=charge_button_add(0),
        )

# Принятие количества товаров для покупки
@dp.message_handler(state="here_item_count")
async def user_purchase_select_count(message: Message, state: FSMContext):
    position_id = (await state.get_data())['here_cache_position_id']

    get_position = get_positionx(position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)
    lang = get_user['user_lang']
    if lang is None: lang = "ru"
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_type'] == 1:
        #get_count = len(get_items)
        get_count = int(get_user['user_balance'] / get_position['position_price'])
    elif get_position['position_type'] == 2:
        get_count = get_position['position_rest']


    print("|||||")
    print(get_count, get_items)

    send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Введите количество товаров для покупки\n" \
                   f"▶ От <code>1</code> до <code>{get_count}</code>\n" \
                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n" \
                   f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>"
    

    if message.text.isdigit():
        get_count = int(message.text)
        amount_pay = int(get_position['position_price']) * get_count

        if len(get_items) >= 1:
            if 1 <= get_count <= len(get_items):
                if int(get_user['user_balance']) >= amount_pay:
                    await state.finish()
                    await message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
                                         f"📦 Количество: <code>{get_count}шт</code>\n"
                                         f"💰 Сумма к покупке: <code>{amount_pay}₽</code>",
                                         reply_markup=products_confirm_finl(position_id, get_count, lang))
                else:
                    await message.answer(
                        f"<b>❌ Недостаточно средств на счете.</b>\n{send_message}"
                    )
            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n{send_message}")
        else:
            await state.finish()
            await message.answer(_("<b>🎁 Товар который вы хотели купить, закончился</b>", locale=lang))
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n{send_message}")

# Подтверждение покупки товара
@dp.callback_query_handler(text_startswith="xbuy_item", state="*")
async def user_purchase_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    get_count = int(call.data.split(":")[3])
    #print(get_action, position_id, get_count)
    get_user = get_userx(user_id=call.from_user.id)
    lang = get_user['user_lang']
    if lang is None: lang = "ru"

    if get_action == "yes":
        await call.message.edit_text("<b>🔄 Ждите, товары подготавливаются</b>") #_("<b>🔄 Ждите, товары подготавливаются</b>", locale=lang))

        get_position = get_positionx(position_id=position_id)
        get_items = get_itemsx(position_id=position_id)
        #get_user = get_userx(user_id=call.from_user.id)
        #lang = get_user['user_lang']
        #print(get_position, get_items, get_user, lang, amount_pay)

        amount_pay = int(get_position['position_price'] * get_count)

        #print(get_position, get_items, get_user, lang, amount_pay)

        if 1 <= get_count <= len(get_items):
            if int(get_user['user_balance']) >= amount_pay:
                save_items, send_count, split_len = buy_itemx(get_items, get_count)

                if get_count != send_count:
                    amount_pay = int(get_position['position_price'] * send_count)
                    get_count = send_count

                receipt = get_unix()
                buy_time = get_date()

                await call.message.delete()
                if split_len == 0:
                    await call.message.answer("\n\n".join(save_items), parse_mode="None")
                else:
                    for item in split_messages(save_items, split_len):
                        await call.message.answer("\n\n".join(item), parse_mode="None")
                        await asyncio.sleep(0.3)

                update_userx(get_user['user_id'], user_balance=get_user['user_balance'] - amount_pay)
                add_purchasex(get_user['user_id'], get_user['user_login'], get_user['user_name'], receipt, get_count,
                              amount_pay, get_position['position_price'], get_position['position_id'],
                              get_position['position_name'], "\n".join(save_items), buy_time, receipt,
                              get_user['user_balance'], int(get_user['user_balance'] - amount_pay))

                await notify(dp, f"Продана позиция: {get_position['position_name']}")
                await call.message.answer(f"<b>✅ Вы успешно купили товар(ы)</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"🧾 Чек: <code>#{receipt}</code>\n"
                                          f"🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>\n"
                                          f"🕰 Дата покупки: <code>{buy_time}</code>",
                                          reply_markup=menu_frep(call.from_user.id, lang))
            else:
                await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
        else:
            await call.message.answer(_("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>", locale=lang),
                                      reply_markup=menu_frep(call.from_user.id, lang))
    elif len(get_all_categoriesx()) >= 1:
        await call.message.edit_text(_("<b>🎁 Выберите нужный вам товар:</b>", locale=lang),
                                     reply_markup=category_edit_open_fp(0))
    else:
        await call.message.edit_text(_("<b>✅ Вы отменили покупку товаров.</b>", locale=lang))

