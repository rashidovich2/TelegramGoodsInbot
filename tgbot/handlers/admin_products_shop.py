from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities

from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl
from tgbot.keyboards.inline_z_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl
from tgbot.keyboards.shop_keyboards import *
from tgbot.keyboards.reply_z_all import finish_load_rep, items_frep
from tgbot.keyboards.inline_z_page import position_create_open_fp
from tgbot.loader import dp
from tgbot.middlewares.throttling import rate_limit
from tgbot.services.api_sqlite_shop import *
from tgbot.services.api_sqlite import get_city_user, check_user_shop_exist
from tgbot.utils.const_functions import clear_list
from tgbot.utils.misc.bot_filters import IsAdmin, IsShopAdmin, IsAdminorShopAdmin
from tgbot.utils.misc_functions import get_position_admin, upload_text



# --------------------------------------------------------------------------------------------------------
# Создание нового магазина
@dp.message_handler(IsShopAdmin(), text="🏪 Создать магазин ➕", state="*")
async def product_category_create(message: Message, state: FSMContext):
    await state.finish()
    print("admin_products_shop - создание магазина")
    user_id=message.from_user.id
    if check_user_shop_exist(user_id):
        await message.answer("<b>🏪 Магазин уже существует 🏷</b>", parse_mode='HTML')
    else:
        await state.set_state("here_shop_name")
        await message.answer("<b>🏪 Введите название для магазина 🏷</b>", parse_mode='HTML')


# принятие названия магазина, запрос описания
@dp.message_handler(IsAdmin(), state="here_shop_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:

        print("admin_products_shop - создание магазина")
        await state.update_data(data={'name': message.text})
        await state.set_state('here_shop_description')
        await message.answer("<b>🏪 Введите описание для магазина 📜</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для магазина 🏷", parse_mode='HTML')


# принятие описания магазина, запрос адреса
@dp.message_handler(IsAdmin(), state="here_shop_description")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 600:
        if message.text == '0':
            await state.update_data(data={'description': 'None'})
        else:
            await state.update_data(data={'description': message.text})
        await state.set_state('here_shop_adress')
        await message.answer("<b>🏪 Отправьте адресс магазина 📍</b>\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


    else:
        await message.answer("<b>❌ Описание не может превышать 600 символов.</b>\n"
                             "🏪 Введите новое описание для магазина 📜\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие адреса магазина, запрос номера
@dp.message_handler(IsAdmin(), state="here_shop_adress")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.text == '0':
        await state.update_data(data={'address': 'None'})
    else:
        await state.update_data(data={'address': message.text})
    await state.set_state('here_shop_phone')
    await message.answer("<b>🏪 Отправьте телефон магазина ☎️</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие номера магазина, запрос лого
@dp.message_handler(IsAdmin(), state="here_shop_phone")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.text == '0':
        await state.update_data(data={'phone': 'None'})
    else:
        await state.update_data(data={'phone': message.text})
    await state.set_state('here_shop_logo')
    await message.answer("<b>🏪 Отправьте лого магазина 📷</b>\n"
                         "❕ Отправьте <code>0</code> чтобы пропустить.", parse_mode='HTML')


# принятие лого магазина, запрос лого
@dp.message_handler(IsAdmin(), content_types=['photo','text'], state="here_shop_logo")
async def product_category_create_name(message: Message, state: FSMContext):
    if message.content_type == 'photo':
        logo = message.photo[0].file_id
    else:
        logo = None

    async with state.proxy() as data:
        print(data)
        name = data['name']
        description = data['description']
        address = data['address']
        phone = data['phone']

    await state.finish()

    city = get_city_user(message.from_user.id)
    add_shopx(name, description, address, phone, message.from_user.id, logo, city[0], city[1], city[2])
    await message.answer("<b>🏪 Магазин был успешно создан ✅</b>", parse_mode='HTML')

################################################################################################
####################################### СОЗДАНИЕ МАГАЗИНА #####################################
# Принятие названия магазина для её создания
@dp.message_handler(IsAdmin(), state="here_shop_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        add_shopx(clear_html(message.text))

        await state.finish()
        await message.answer("<b>🏪 Магазин был успешно создан ✅</b>")
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🏪 Введите название для магазина 🏷")


# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsAdmin(), text="🏪 Изменить магазин 🖍", state="*")
async def product_category_edit(message: Message, state: FSMContext):
    await state.finish()

    shops = get_all_shopx()
    print(f'shops {shops}')

    if len(shops) >= 1:
        await message.answer("<b>🏪 Выберите магазин для изменения 🖍</b>",
                             reply_markup=shop_edit_open_fp(0, shops))
    else:
        await message.answer("<b>🏪 Магазины отсутствуют 🖍</b>")


# -----------------------------------------------------------------------------------------------------------
# Открытие страниц выбора магазина для редактирования
@dp.message_handler(IsShopAdmin(), text="🏪 Изменить магазин 🖍", state="*")
async def product_category_edit(message: Message, state: FSMContext):
    await state.finish()
    user_id=message.from_user.id
    #if get_my_shopx(user_id):
    #shops = get_all_shopx()
    print(f'shops {shops}')
    shops = get_my_shopx(user_id)
    print(shops)

    if len(shops) >= 1:
        await message.answer("<b>🏪 Выберите магазин для изменения 🖍</b>",
                             reply_markup=shop_edit_open_fp(0, shops))
    else:
        await message.answer("<b>🏪 Магазины отсутствуют 🖍</b>")


# Смена страницы выбора магазина
@dp.message_handler(IsAdmin(), text_startswith="change_shop_edit_pg:", state="*")
async def product_category_edit(call: CallbackQuery, state: FSMContext):
    await state.finish()
    page = int(str(call.data).split(':')[1])
    shops = get_all_shopx()


    if len(shops) >= 1:
        await call.message.answer("<b>🏪 Выберите магазин для изменения 🖍</b>",
                             reply_markup=shop_edit_open_fp(page, shops))
    else:
        await call.message.answer("<b>🏪 Магазины отсутствуют 🖍</b>")



# Выбор  магазина для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="shop_edit_here:", state="*")
async def product_category_edit_open(call: CallbackQuery, state: FSMContext):
    shop_id = int(call.data.split(":")[1])
    shop = get_the_shop(shop_id)

    text = f"<b>🎁 Редактировать магазин:</b>\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🏷 Название: <code>{shop[1]}</code>\n" \
           f"🏙 Город: <code>{shop[7]}</code>\n🗃 Адрес: <code>{shop[4]}</code>\n" \
           f"💰 Телефон: <code>{shop[5]}₽</code>\n{shop[3]}"

    if shop[6] is None:
        await call.message.answer(text, parse_mode='HTML')

    else:
        await call.message.answer_photo(text, parse_mode='HTML')



################################ Добавление магазина при создании позиции ########################

# Создание новой позиции
@dp.message_handler(IsAdminorShopAdmin(), text="📁 Создать позицию ➕", state="*")
async def product_position_create(message: Message, state: FSMContext):
    await state.finish()
    print("APS 182")

    #if len(get_all_shopx()) >= 1:
    await message.answer("<b>📁 Выберите категорию для позиции</b>",
                             reply_markup=position_create_open_fp(0))
    #else:
        #await message.answer("<b>❌ Отсутствуют магазины для создания позиции.</b>")


######################################## САМО ИЗМЕНЕНИЕ МАГАЗИНОВ ########################################
# Изменение названия магазина
@dp.callback_query_handler(IsAdmin(), text_startswith="shop_edit_name:", state="*")
async def product_category_edit_name(call: CallbackQuery, state: FSMContext):
    shop_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])

    await state.update_data(here_cache_shop_id=shop_id)
    await state.update_data(here_cache_shop_remover=remover)

    await state.set_state("here_change_shop_name")
    await call.message.delete()
    await call.message.answer("<b>🗃 Введите новое название для магазина 🏷</b>")


# Принятие нового имени для магазина
@dp.message_handler(IsAdmin(), state="here_change_shop_name")
async def product_shop_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            shop_id = data['here_cache_shop_id']
            remover = data['here_cache_shop_remover']
        await state.finish()

        update_shopx(shop_id, shop_name=clear_html(message.text))

        get_fat_count = len(get_positionsx(shop_id=shop_id))
        get_shop = get_shopx(shop_id=shop_id)

        await message.answer(f"<b>🗃 Категория: <code>{get_shop['category_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"📁 Кол-во позиций: <code>{get_fat_count}шт</code>",
                             reply_markup=shop_edit_open_finl(shop_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🗃 Введите новое название для магазина 🏷")



# -------------------------------------------------------------------------------------------------------------
# Окно с уточнением удалить все магазины (позиции и товары включительно)
@dp.message_handler(IsAdmin(), text="🏪 Удалить все магазины ❌", state="*")
async def product_category_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🗃 Вы действительно хотите удалить все магазины? ❌</b>\n"
                         "❗ Так же будут удалены все позиции и товары",
                         reply_markup=category_remove_confirm_inl)



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

################################################################################################
####################################### ИЗМЕНЕНИЕ МАГАЗИНА ####################################
# Следующая страница выбора магазина для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="catategory_edit_nextp:", state="*")
async def product_category_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🗃 Выберите категорию для изменения 🖍</b>",
                                 reply_markup=category_edit_next_page_fp(remover))


# Предыдущая страница выбора категорий для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="catategory_edit_backp:", state="*")
async def product_category_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.delete()
    await call.message.answer("<b>🗃 Выберите категорию для изменения 🖍</b>",
                              reply_markup=category_edit_back_page_fp(remover))




# Возвращение к списку выбора категорий для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_return:", state="*")
async def product_category_edit_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🗃 Выберите категорию для изменения 🖍</b>",
                                 reply_markup=category_edit_open_fp(remover))


