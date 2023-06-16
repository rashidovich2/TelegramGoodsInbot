from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities

from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl, shop_edit_open_finl, shop_name_edit_open_finl, shop_edit_delete_finl
from tgbot.keyboards.inline_z_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl
from tgbot.keyboards.shop_keyboards import *
from tgbot.keyboards.reply_z_all import finish_load_rep, items_frep
from tgbot.keyboards.inline_z_page import position_create_open_fp
from tgbot.loader import dp
from tgbot.middlewares.throttling import rate_limit
from tgbot.services.api_sqlite_shop import *
from tgbot.services.api_sqlite import get_city_user, get_city_user3, check_user_shop_exist, get_settingsx, get_my_shopx, remove_shopx, get_userx, get_all_shopx
from tgbot.utils.const_functions import clear_list
from tgbot.utils.misc.bot_filters import IsAdmin, IsShopAdmin, IsAdminorShopAdmin
from tgbot.utils.misc_functions import get_position_admin, upload_text, get_shop_admin
# Добавлено
from tgbot.keyboards.location_keyboards import geo_1_kb
from tgbot.services.location_function import update_position_city, get_city_info


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
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
    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_shop_adress')
        await message.answer(_("<b>🏪 Отправьте адресс магазина 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')


    else:
        await message.answer(_("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите новое описание для магазина 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang), parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_adress")
async def product_category_create_name(message: Message, state: FSMContext):
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

################################################################################################
####################################### СОЗДАНИЕ МАГАЗИНА #####################################
# Принятие названия магазина для её создания
@dp.message_handler(IsAdminorShopAdmin(), state="here_shop_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        add_shopx(clear_html(message.text))

        await state.finish()
        await message.answer(_("<b>🏪 Магазин был успешно создан ✅</b>", locale=lang))
    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для магазина 🏷", locale=lang), locale=lang)

# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsAdminorShopAdmin(), text="🏪 Изменить магазин 🖍2", state="*")
async def shop_list_edit(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    shops = get_shopsxx(admin=user_id)
    print(shops)

    if len(shops) >= 1:
        await message.answer(_("<b>🏪 Выберите магазин для изменения 🖍</b>", locale=lang),
                             reply_markup=shop_edit_open_fp(0, user_id, lang))
    else:
        await message.answer(_("<b>🏪 Ваши магазины отсутствуют 🖍</b>", locale=lang))


# Смена страницы выбора магазина
@dp.message_handler(IsAdminorShopAdmin(), text_startswith="change_shop_edit_pg:", state="*")
async def shop_list_edit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    lang = get_user_lang(user_id)['user_lang']
    if len(shops) >= 1:
        remover = int(str(call.data).split(':')[1])

        await call.message.answer(_("<b>🏪 Выберите магазин для изменения 🖍</b>", locale=lang),
                             reply_markup=shop_edit_open_fp(remover, user_id, lang))
    else:
        await call.message.answer(_("<b>🏪 Магазины отсутствуют 🖍</b>", locale=lang))


# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_open:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    print('Выбор магазина для редактирования api_sqlite.py 169')
    shop_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(shop_id, remover, user_id)

    get_message, get_photo = get_shop_admin(shop_id)

    if get_photo is not None and get_photo != '':
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover, lang))
    else:
        await call.message.edit_text(get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover, lang))


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    print(user_id)
    shops = get_shopsxx(admin=user_id)

    print(shops)

    if len(shops) >= 1:
        await call.message.delete()
        await call.message.answer(_("<b>📁 Выберите нужный Вам магазин 🖍</b>", locale=lang),
                                  reply_markup=shop_edit_open_fp(0, user_id, lang))
    else:
        await call.answer("<b>❗ У Вас отсутствуют магазины</b>")

################################ Добавление магазина при создании позиции ########################

# Создание новой позиции
@dp.message_handler(IsAdminorShopAdmin(), text="📁 Создать позицию ➕2", state="*")
async def product_position_create(message: Message, state: FSMContext):
    await state.finish()
    print("APS 182")

    await message.answer(_("<b>📁 Выберите категорию для позиции</b>", locale=lang),
                             reply_markup=position_people_create_open_fp(0))
    #else:
        #await message.answer(_("<b>❌ Отсутствуют магазины для создания позиции.</b>", locale=lang))


######################################## САМО ИЗМЕНЕНИЕ МАГАЗИНОВ ########################################
# Изменение названия магазина
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_name:", state="*")
async def product_category_edit_name(call: CallbackQuery, state: FSMContext):
    print("|||| -= EDIT SHOP NAME =- ||||")

    shop_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_shop_id=shop_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_shop_remover=remover)

    await state.set_state("here_change_shop_name")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новое название для магазина 🏷</b>", locale=lang))


# Принятие нового имени для магазина
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_shop_name")
async def product_shop_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            shop_id = data['here_cache_shop_id']
            remover = data['here_cache_shop_remover']
            user_id = data['here_cache_user_id']
        await state.finish()

        update_shopx(shop_id, name=clear_html(message.text))
        get_shop = get_shopx(shop_id=shop_id)

        await message.answer(f"<b>🗃 Новое название магазина: <code>{get_shop['name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n", reply_markup=shop_name_edit_open_finl(shop_id, user_id, remover, lang))
    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🗃 Введите новое название для магазина 🏷", locale=lang))


# Изменение описания позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_description", state="*")
async def product_shop_edit_description(call: CallbackQuery, state: FSMContext):
    print("|||| -= EDIT SHOP NAME =- ||||")
    shop_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_shop_id=shop_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_shop_remover=remover)

    await state.set_state("here_change_shop_description")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новое описание для позиции 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))


# Принятие описания позиции для её изменения
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_shop_description")
async def product_shop_edit_description_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        shop_id = data['here_cache_shop_id']
        remover = data['here_cache_shop_remover']
        user_id = data['here_cache_user_id']

    try:
        if len(message.text) <= 900:
            await state.finish()

            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            update_shopx(shop_id, description=message.text)
            get_message, get_photo = get_shop_admin(shop_id)

            if get_photo is not None:
                await message.answer_photo(get_photo, get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover))
            else:
                await message.answer(get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover))
        else:
            await message.answer(_("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для магазина 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))
    except CantParseEntities:
        await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для магазина 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))

# Изменение изображения позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_photo", state="*")
async def product_shop_edit_photo(call: CallbackQuery, state: FSMContext):
    shop_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_shop_id=shop_id)
    await state.update_data(here_cache_user_id=user_id)
    await state.update_data(here_cache_shop_remover=remover)

    await state.set_state("here_change_shop_photo")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Отправьте новое изображение для позиции 📸</b>\n"
                                "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))


# Принятие нового фото для позиции
@dp.message_handler(IsAdminorShopAdmin(), content_types="photo", state="here_change_shop_photo")
@dp.message_handler(IsAdminorShopAdmin(), text="0", state="here_change_shop_photo")
async def product_shop_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        shop_id = data['here_cache_shop_id']
        user_id = data['here_cache_user_id']
        remover = data['here_cache_shop_remover']
    await state.finish()

    shop_photo = "" if "text" in message else message.photo[-1].file_id
    update_shopx(shop_id, logo=shop_photo)
    get_message, get_photo = get_shop_admin(shop_id)

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover, lang))
    else:
        await message.answer(get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover, lang))


# -------------------------------------------------------------------------------------------------------------
# Окно с уточнением удалить все магазины (позиции и товары включительно)
@dp.message_handler(text=["🏪 Удалить все магазины ❌", "🏪 Delete all shops ❌"], state="*")
async def product_category_remove(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role == "Admin":
        await message.answer("<b>🗃 Вы действительно хотите удалить все магазины? ❌</b>\n",
                             reply_markup=category_remove_confirm_inl)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
################################################################################################
####################################### ИЗМЕНЕНИЕ МАГАЗИНА ####################################

# Следующая страница позиций для их изменения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_nextp:", state="*")
async def product_position_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])

    await call.message.edit_text(_("<b>📁 Выберите магазин для изменения 🖍</b>", locale=lang), reply_markup=shop_edit_next_page_fp(remover, user_id))

# Предыдущая страница позиций для их изменения
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_backp:", state="*")
async def product_position_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])

    await call.message.edit_text(_("<b>📁 Выберите магазин для изменения 🖍</b>", locale=lang), reply_markup=shop_edit_back_page_fp(remover, user_id))


# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="shop_edit_open:", state="*")
async def shop_edit_open(call: CallbackQuery, state: FSMContext):
    print('Выбор магазина для редактирования api_sqlite.py 421')
    shop_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = int(call.data.split(":")[3])

    get_message, get_photo = get_shop_admin(shop_id)

    if get_photo is not None:
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover))
    else:
        await call.message.edit_text(get_message, reply_markup=shop_edit_open_finl(shop_id, user_id, remover))

# Следующая страница магазинов для их изменения
def shop_edit_next_page_fp(remover, user_id):
    get_shops = get_shopsxx(admin=user_id)
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_shops))):
        if count < cpage:
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(ikb(f"{get_shops[a]['name']}", callback_data=f"shop_edit_open:{get_shops[a]['shop_id']}:{remover}:{user_id}")) # | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
    if remover + cpage >= len(get_shops):
        keyboard.add(ikb("⬅ Назад", callback_data=f"shop_edit_backp:{remover - cpage}:{user_id}"), ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="...")
        )
    else:
        keyboard.add(ikb("⬅ Назад", callback_data=f"shop_edit_backp:{remover - cpage}:{user_id}"),
                     ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
                     ikb("Далее ➡", callback_data=f"shop_edit_nextp:{remover + cpage}:{user_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data="shop_edit_category_return"))

    return keyboard


# Предыдующая страница позиций для их изменения
def shop_edit_back_page_fp(remover, user_id):
    get_shops = get_shopsxx(admin=user_id)
    keyboard = InlineKeyboardMarkup()
    for count, a in enumerate(range(remover, len(get_shops))):
        if count < cpage:
            #get_items = get_itemsx(position_id=get_positions[a]['position_id'])    # | {get_shops[a]['position_price']}₽ | {len(get_items)} шт",
            keyboard.add(ikb(f"{get_shops[a]['name']}", callback_data=f"shop_edit_open:{get_shops[a]['shop_id']}:{remover}:{user_id}"))
    if remover <= 0:
        keyboard.add(
            ikb("🔸 1 🔸", callback_data="..."),
            ikb("Далее ➡", callback_data=f"shop_edit_nextp:{remover + cpage}:{user_id}")
        )
    else:
        keyboard.add(ikb("⬅ Назад", callback_data=f"shop_edit_backp:{remover - cpage}:{user_id}"),
                     ikb(f"🔸 {str(remover + cpage)[:-1]} 🔸", callback_data="..."),
                     ikb("Далее ➡", callback_data=f"shop_edit_nextp:{remover + cpage}:{user_id}"),
        )
    #keyboard.add(ikb("⬅ Вернуться ↩", callback_data="shop_edit_return"))

    return keyboard


# Окно с уточнением удалить категорию
@dp.callback_query_handler(text_startswith="shop_edit_delete", state="*")
async def shop_edit_dellete(call: CallbackQuery, state: FSMContext):
    shop_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id

    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        print("shop_edit_delete")
        await call.answer("🗃 Магазин будет удален ✅")

        await call.message.answer("<b>❗ Вы действительно хотите удалить один из магазинов?</b>", #_("<b>❗ Вы действительно хотите удалить один из магазинов?</b>", locale=lang),
                                     reply_markup=shop_edit_delete_finl(shop_id, remover, lang))

# Отмена удаления категории
@dp.callback_query_handler(text_startswith="shop_delete:", state="*")
async def shop_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    shop_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    print(get_action, shop_id, user_id)
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    print(lang, user_role)
    if user_role == "Admin":
        if get_action == "yes":
            remove_shopx(shop_id=shop_id)

            #if len(get_all_shopx()) >= 1:
            #await call.message.delete()
            await call.message.edit_text(_("🗃 Магазин был успешно удален ✅", locale=lang), reply_markup=shop_edit_open_fp(0, user_id, lang))
            #else:
            #    await call.message.delete()
        else:
            get_shop_count = len(get_shopx(store_id=shop_id))
            get_shop = get_shopx(shop_id=shop_id)

            remover = 0

            await call.message.edit_text(f"<b>🗃 Магазин: <code>{get_shop['name']}</code></b>\n"
                                         "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"📁 Кол-во позиций: <code>{get_shop_count}шт</code>", reply_markup=shop_edit_open_finl(shop_id, remover, lang))