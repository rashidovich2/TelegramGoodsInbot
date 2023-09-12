# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities
from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR

from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl
from tgbot.keyboards.inline_z_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl
from tgbot.keyboards.inline_z_page import *
from tgbot.keyboards.reply_z_all import finish_load_rep, items_frep, items_sh_frep
from tgbot.loader import dp
from tgbot.middlewares.throttling import rate_limit
from tgbot.services.api_sqlite import *
from tgbot.utils.const_functions import clear_list
from tgbot.utils.misc.bot_filters import IsAdmin, IsShopAdmin, IsAdminorShopAdmin
from tgbot.utils.misc_functions import get_position_admin, upload_text
# Добавлено
from tgbot.keyboards.location_keyboards import geo_1_kb
from tgbot.services.location_function import update_position_city, get_city_info

from tgbot.middlewares.i18n import I18nMiddleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.gettext

# Открытие страниц выбора категорий для редактирования
@dp.message_handler(text=["🗃 Изменить категорию 🖍", "🗃 Edit category 🖍"], state="*")
async def product_category_edit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role in ["Admin", "ShopAdmin"]:
        if len(get_all_categoriesx()) >= 1:
            await state.finish()
            await message.answer(_("<b>🗃 Выберите категорию для изменения 🖍</b>", locale=lang),
                                 reply_markup=category_edit_open_fp(0, lang))
        else:
            await state.finish()
            await message.answer(_("<b>🗃 Категории отсутствуют 🖍</b>", locale=lang))


# Окно с уточнением удалить все категории (позиции и товары включительно)
@dp.message_handler(text=["🗃 Удалить все категории ❌", "🗃 Delete all categories ❌"], state="*")
async def product_category_remove(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role in ["Admin", "ShopAdmin"]:
        await message.answer(_("<b>🗃 Вы действительно хотите удалить все категории? ❌</b>\n"
                             "❗ Так же будут удалены все позиции и товары", locale=lang),
                             reply_markup=category_remove_confirm_inl)

# Начальные категории для изменения позиции
@dp.message_handler(text="📁 Изменить позицию 🖍2", state="*")
async def product_position_edit(message: Message, state: FSMContext):
    print('📁 Изменить позицию 🖍  admin_products.py 73')
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        await message.answer(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang),
                             reply_markup=position_edit_category_open_fp(0, lang))

# Подтверждение удаления всех позиций
@dp.message_handler(text=["📁 Удалить все позиции ❌", "📁 Delete all positions ❌"], state="*")
async def product_position_remove(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        await message.answer(_("<b>📁 Вы действительно хотите удалить все позиции? ❌</b>\n"
                             "❗ Так же будут удалены все товары", locale=lang),
                             reply_markup=position_remove_confirm_inl)

# Начальные категории для добавления товаров
@dp.message_handler(text=["🎁 Добавить товары ➕", "🎁 Add Goods➕"], state="*")
async def product_item_create(message: Message, state: FSMContext):
    print('🎁 Добавить товары ➕  admin_products_shop.py 93')
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role in ["Admin", "ShopAdmin"]:
        if len(get_all_positionsx()) >= 1:
            await message.answer(_("<b>🎁 Выберите категорию с нужной позицией</b>", locale=lang),
                                 reply_markup=products_add_category_open_fp(0, lang))
        else:
            await message.answer(_("<b>❌ Отсутствуют позиции для добавления товара.</b>", locale=lang))


# Удаление определённых товаров
@dp.message_handler(text=["🎁 Удалить товары 🖍", "🎁 Delete Goods 🖍"], state="*")
async def product_item_delete(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role == "Admin":
        await state.set_state("here_items_delete")
        await message.answer(_("<b>🖍 Вводите айди товаров, которые нужно удалить</b>\n"
                             "❕ Получить айди товаров можно при изменении позиции\n"
                             "❕ Если хотите удалить несколько товаров, отправьте ID товаров через запятую или пробел. Пример:\n"
                             "<code>▶ 123456,123456,123456</code>\n"
                             "<code>▶ 123456 123456 123456</code>", locale=lang))


# -------------------------------------------------------------------------------------------------------------------
# Кнопки с подтверждением удаления всех категорий
@dp.message_handler(text=["🎁 Удалить все товары ❌", "🎁 Delete All Goods ❌"], state="*")
async def product_item_remove(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']

    if user_role == "Admin":
        await message.answer(_("<b>🎁 Вы действительно хотите удалить все товары? ❌</b>\n", locale=lang),
                             reply_markup=item_remove_confirm_inl)


################################################################################################
####################################### СОЗДАНИЕ КАТЕГОРИЙ #####################################
# Принятие названия категории для её создания
@dp.message_handler(IsAdmin(), state="here_category_name")
async def product_category_create_name(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    print(lang)
    if user_role == "Admin":
        if len(message.text) <= 100:
            add_categoryx(clear_html(message.text))
            await message.answer(_("<b>🗃 Категория была успешно создана ✅</b>", locale=lang))
        else:
            await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>", locale=lang))


################################################################################################
####################################### ИЗМЕНЕНИЕ КАТЕГОРИЙ ####################################
# Следующая страница выбора категорий для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="catategory_edit_nextp:", state="*")
async def product_category_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>🗃 Выберите категорию для изменения 🖍</b>", locale=lang),
                                 reply_markup=category_edit_next_page_fp(remover, lang))

# Предыдущая страница выбора категорий для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="catategory_edit_backp:", state="*")
async def product_category_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.delete()
    await call.message.answer(_("<b>🗃 Выберите категорию для изменения 🖍</b>", locale=lang),
                              reply_markup=category_edit_back_page_fp(remover, lang))


# Выбор текущей категории для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_here:", state="*")
async def product_category_edit_open(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    get_fat_count = len(get_positionsx(category_id=category_id))
    get_category = get_categoryx(category_id=category_id)

    if lang == "ru":
        await call.message.edit_text(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                                     "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"📁 Кол-во позиций: <code>{get_fat_count}шт</code>",
                                     reply_markup=category_edit_open_finl(category_id, remover, lang))
    if lang == "en":
        await call.message.edit_text(f"<b>🗃 Category: <code>{get_category['category_name']}</code></b>\n"
                                     "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"📁 Position quantity: <code>{get_fat_count}pcs</code>",
                                     reply_markup=category_edit_open_finl(category_id, remover, lang))


# Возвращение к списку выбора категорий для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_return:", state="*")
async def product_category_edit_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>🗃 Выберите категорию для изменения 🖍</b>", locale=lang),
                                 reply_markup=category_edit_open_fp(remover, lang))


######################################## САМО ИЗМЕНЕНИЕ КАТЕГОРИИ ########################################
# Изменение названия категории
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_name:", state="*")
async def product_category_edit_name(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_category_remover=remover)

    await state.set_state("here_change_category_name")
    await call.message.delete()
    await call.message.answer(_("<b>🗃 Введите новое название для категории 🏷</b>", locale=lang))


# Принятие нового имени для категории
@dp.message_handler(IsAdmin(), state="here_change_category_name")
async def product_category_edit_name_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        async with state.proxy() as data:
            category_id = data['here_cache_category_id']
            remover = data['here_cache_category_remover']
        await state.finish()


        update_categoryx(category_id, category_name=clear_html(message.text))

        get_fat_count = len(get_positionsx(category_id=category_id))
        get_category = get_categoryx(category_id=category_id)

        if lang == "ru":
            await message.answer(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📁 Кол-во позиций: <code>{get_fat_count}шт</code>",
                                 reply_markup=category_edit_open_finl(category_id, remover, lang))
        if lang == "en":
            await message.answer(f"<b>🗃 Category: <code>{get_category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📁 Position Quantity: <code>{get_fat_count}pcs</code>",
                                 reply_markup=category_edit_open_finl(category_id, remover, lang))

    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "🗃 Введите новое название для категории 🏷", locale=lang))


# Окно с уточнением удалить категорию
@dp.callback_query_handler(text_startswith="category_edit_delete:", state="*")
async def product_category_edit_delete(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        await call.message.edit_text("<b>❗ Вы действительно хотите удалить категорию и все её данные?</b>",
                                     reply_markup=category_edit_delete_finl(category_id, remover, lang))


# Отмена удаления категории
@dp.callback_query_handler(text_startswith="category_delete:", state="*")
async def product_category_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    get_action = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        if get_action == "yes":
            remove_categoryx(category_id=category_id)
            remove_positionx(category_id=category_id)
            remove_itemx(category_id=category_id)

            if lang == "ru":
                await call.answer("🗃 Категория и все её данные были успешно удалены ✅")
            if lang == "en":
                await call.answer("🗃 Category and all of data has been deleted succesfully ✅")
            if len(get_all_categoriesx()) >= 1:
                await call.message.edit_text(_("<b>🗃 Выберите категорию для изменения 🖍</b>", locale=lang),
                                             reply_markup=category_edit_open_fp(remover, lang))
            else:
                await call.message.delete()
        else:
            get_fat_count = len(get_positionsx(category_id=category_id))
            get_category = get_categoryx(category_id=category_id)

            if lang == "ru":
                await message.answer(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                                     "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"📁 Кол-во позиций: <code>{get_fat_count}шт</code>",
                                     reply_markup=category_edit_open_finl(category_id, remover, lang))
            if lang == "en":
                await message.answer(f"<b>🗃 Category: <code>{get_category['category_name']}</code></b>\n"
                                     "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"📁 Position Quantity: <code>{get_fat_count}pcs</code>",
                                     reply_markup=category_edit_open_finl(category_id, remover, lang))


################################################################################################
#################################### УДАЛЕНИЕ ВСЕХ КАТЕГОРИЙ ###################################
# Подтверждение на удаление всех категорий (позиций и товаров включительно)
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_remove_category:", state="*")
async def product_category_remove_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    if get_action == "yes":
        get_categories = len(get_all_categoriesx())
        get_positions = len(get_all_positionsx())
        get_items = len(get_all_itemsx())

        clear_categoryx()
        clear_positionx()
        clear_itemx()

        await call.message.edit_text(
            f"<b>🗃 Вы удалили все категории<code>({get_categories}шт)</code>, "
            f"позиции<code>({get_positions}шт)</code> и товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>🗃 Вы отменили удаление всех категорий ✅</b>")


################################################################################################
####################################### ДОБАВЛЕНИЕ ПОЗИЦИЙ #####################################
# Следующая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdmin(), text_startswith="position_create_nextp:", state="*")
async def product_position_create_next(call: CallbackQuery, state: FSMContext):
    print('выбора категорий для создания позиций  admin_products_shop.py 300')
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(remover)

    await call.message.edit_text(_("<b>📁 Выберите категорию для позиции ➕</b>", locale=lang),
                                 reply_markup=position_create_next_page_fp(remover, lang))


# Предыдущая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdmin(), text_startswith="position_create_backp:", state="*")
async def product_position_create_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>📁 Выберите категорию для позиции ➕</b>", locale=lang),
                                 reply_markup=position_create_back_page_fp(remover, lang))


@dp.callback_query_handler(IsAdmin(), text_startswith="position_shop_create_here:", state="*")
async def product_position_create(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_change_shop_id=category_id)

    if len(get_all_categoriesx()) >= 1:
        await call.message.answer(_("<b>📁 Выберите категорию для позиции</b>", locale=lang),
                             reply_markup=position_create_open_fp(0, lang))
    else:
        await call.message.answer(_("<b>❌ Отсутствуют категории для создания позиции.</b>", locale=lang))


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_create_here2:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_create_here - admin_products')
    category_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    print(category_id)

    await state.update_data(here_cache_change_category_id=category_id)

    await state.set_state("here_position_name")
    await call.message.edit_text(_("<b>📁 Введите название для позиции 🏷</b>", locale=lang))

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Заготовка под принятие города магазином
# Принятие города для создания позиции
# @dp.message_handler(IsAdmin(), state="here_position_city")
# async def product_position_create_name(message: Message, state: FSMContext):
#     print(f'Принятие города для создания позиции  admin_products_shop.py 344')
#     city_user = get_city_user(message.from_user.id)


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_create_here:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_create_here - user_menu 160')
    category_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    await state.update_data(here_cache_change_category_id=category_id)

    print('position_addtoshop - user_menu 555')
    user_id = call.from_user.id
    get_user_shops = get_shopsxx(admin=user_id)
    if len(get_user_shops) >= 1:
        await call.message.edit_text(_("<b>Выберите магазин для добавления позиции.</b>", loacle=lang),
                                     reply_markup=position_select_shop_fp(user_id))

        await state.set_state("here_position_addtoshop")
        await call.message.edit_text(_("<b>📁 Введите название для позиции 🏷</b>", locale=lang))

# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="here_position_addtoshop:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('here_position_addtoshop: - user_menu 574')
    shop_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_change_shop_id=shop_id)

    await state.set_state("here_position_name")
    await call.message.edit_text(_("<b>📁 Введите название для позиции 🏷</b>", locale=lang))


# Принятие имени для создания позиции
@dp.message_handler(IsAdmin(), state="here_position_name")
async def product_position_create_name(message: Message, state: FSMContext):
    print('Принятие имени для создания позиции  admin_products.py 355')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        await state.update_data(here_position_name=clear_html(message.text), here_position_city=get_city_user(message.from_user.id)[0], position_city_id=get_city_user(message.from_user.id)[0])

        await state.set_state("here_position_price")
        await message.answer(_("<b>📁 Введите цену для позиции 💰</b>", locale=lang))
    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷", locale=lang))


# Принятие цены позиции для её создания
@dp.message_handler(IsAdmin(), state="here_position_price")
async def product_position_create_price(message: Message, state: FSMContext):
    print('Принятие цены позиции  admin_products.py 366')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.update_data(here_position_price=message.text)

            await state.set_state("here_position_description")
            await message.answer(_("<b>📁 Введите описание для позиции 📜</b>\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))
        else:
            await message.answer(_("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰", locale=lang))
    else:
        await message.answer(_("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰", locale=lang))


# Принятие описания позиции для её создания
@dp.message_handler(IsAdmin(), state="here_position_description")
async def product_position_create_description(message: Message, state: FSMContext):
    print('Принятие описания позиции  admin_products.py 386')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    try:
        if len(message.text) <= 600:
            if message.text != "0":
                cache_msg = await message.answer(message.text)
                await cache_msg.delete()

            await state.update_data(here_position_description=message.text)

            await state.set_state("here_position_photo")
            await message.answer(_("<b>📁 Отправьте изображение для позиции 📸</b>\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))
        else:
            await message.answer(_("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для позиции 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))
    except CantParseEntities:
        await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))


# Принятие изображения позиции для её создания
@dp.message_handler(IsAdmin(), content_types="photo", state="here_position_photo")
@dp.message_handler(IsAdmin(), text="0", state="here_position_photo")
async def product_position_create_photo(message: Message, state: FSMContext):
    print('Принятие изображения позиции  admin_products.py 418')
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    async with state.proxy() as data:
        position_user_id = message.from_user.id
        position_city = data['here_position_city']
        position_city_id = data['position_city_id']
        position_name = clear_html(data['here_position_name'])
        position_price = data['here_position_price']
        catategory_id = data['here_cache_change_category_id']
        position_description = data['here_position_description']
    await state.finish()

    position_photo = "" if "text" in message else message.photo[-1].file_id
    position_id = random.randint(1000000000, 9999999999)
    add_positionx(position_city, position_city_id, position_name, position_price, position_description, position_photo, catategory_id, position_user_id)

    await message.answer(_("<b>📁 Позиция была успешно создана ✅</b>", locale=lang))


################################################################################################
####################################### ИЗМЕНЕНИЕ ПОЗИЦИЙ #####################################
# Возвращение к начальным категориям для редактирования позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_category_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang), reply_markup=position_edit_category_open_fp(0, lang))


# Следующая страница категорий для редактирования позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_category_nextp:", state="*")
async def product_position_edit_category_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang), reply_markup=position_edit_category_next_page_fp(remover, lang))


# Предыдущая страница категорий для редактирования позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_category_backp:", state="*")
async def product_position_edit_category_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang), reply_markup=position_edit_category_back_page_fp(remover, lang))


# Выбор категории с нужной позицией
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_category:", state="*")
async def product_position_edit_category_open(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.edit_text(_("<b>📁 Выберите нужную вам позицию 🖍</b>", locale=lang),
                                     reply_markup=position_edit_open_fp(0, category_id, lang))
    else:
        await call.answer(_("📁 Позиции в данной категории отсутствуют", locale=lang))


# Следующая страница позиций для их изменения
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_nextp:", state="*")
async def product_position_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang), reply_markup=position_edit_next_page_fp(remover, category_id, lang))

# Предыдущая страница позиций для их изменения
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_backp:", state="*")
async def product_position_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text(_("<b>📁 Выберите категорию с нужной позицией 🖍</b>", locale=lang), reply_markup=position_edit_back_page_fp(remover, category_id, lang))

# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    print('Выбор позиции для редактирования api_sqlite.py 496')
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await call.message.edit_text(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.delete()
        await call.message.answer(_("<b>📁 Выберите нужную вам позицию 🖍</b>", locale=lang), reply_markup=position_edit_open_fp(remover, category_id, lang))
    else:
        await call.answer(_("<b>❗ Позиции в данной категории отсутствуют</b>", locale=lang))


######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_name", state="*")
async def product_position_edit_name(call: CallbackQuery, state: FSMContext):
    print('Изменение имени позиции api_sqlite.py 529')
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_name")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новое название для позиции 🏷</b>", locale=lang))


# Принятие имени позиции для её изменения
@dp.message_handler(IsAdmin(), state="here_change_position_name")
async def product_position_edit_name_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        async with state.proxy() as data:
            position_id = data['here_cache_category_id']
            category_id = data['here_cache_position_id']
            remover = data['here_cache_position_remover']
        await state.finish()

        update_positionx(position_id, position_name=clear_html(message.text))
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
        else:
            await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите новое название для позиции 🏷", locale=lang))


# Изменение цены позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_price", state="*")
async def product_position_edit_price(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_price")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новую цену для позиции 💰</b>", locale=lang))


# Принятие цены позиции для её изменения
@dp.message_handler(IsAdmin(), state="here_change_position_price")
async def product_position_edit_price_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
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
                await message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
            else:
                await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
        else:
            await message.answer(_("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰", locale=lang))
    else:
        await message.answer(_("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰", locale=lang))


# Изменение описания позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_description", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_description")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новое описание для позиции 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))


# Принятие описания позиции для её изменения
@dp.message_handler(IsAdmin(), state="here_change_position_description")
async def product_position_edit_description_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
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
                await message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
            else:
                await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
        else:
            await message.answer(_("<b>❌ Описание не может превышать 600 символов.</b>\n"
                                 "📁 Введите новое описание для позиции 📜\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))
    except CantParseEntities:
        await message.answer(_("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))

# Изменение имени позиции
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="position_edit_rest", state="*")
async def product_position_edit_name(call: CallbackQuery, state: FSMContext):
    print('Изменение имени позиции api_sqlite.py 529')
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_rest")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Введите новый остаток для позиции 🏷</b>", locale=lang))


# Принятие имени позиции для её изменения
@dp.message_handler(IsAdminorShopAdmin(), state="here_change_position_rest")
async def product_position_edit_rest_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    if len(message.text) <= 100:
        async with state.proxy() as data:
            position_id = data['here_cache_category_id']
            category_id = data['here_cache_position_id']
            remover = data['here_cache_position_remover']
        await state.finish()

        update_positionx(position_id, position_rest=clear_html(message.text))
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
        else:
            await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await message.answer(_("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите новый остаток для позиции 🏷", locale=lang))



# Изменение изображения позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_photo", state="*")
async def product_position_edit_photo(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_photo")
    await call.message.delete()
    await call.message.answer(_("<b>📁 Отправьте новое изображение для позиции 📸</b>\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.", locale=lang))


# Принятие нового фото для позиции
@dp.message_handler(IsAdmin(), content_types="photo", state="here_change_position_photo")
@dp.message_handler(IsAdmin(), text="0", state="here_change_position_photo")
async def product_position_edit_photo_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    async with state.proxy() as data:
        position_id = data['here_cache_category_id']
        category_id = data['here_cache_position_id']
        remover = data['here_cache_position_remover']
    await state.finish()

    position_photo = "" if "text" in message else message.photo[-1].file_id
    update_positionx(position_id, position_photo=position_photo)
    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))


# ---------------------------  Добавлено 12.08.22 ------------------------------------------

# Изменение города продукта
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_city", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    print('Изменение города продукта  admin_products.py 715')
    print(call.data)
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    category_id = int(call.data.split(":")[2])
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[3])

    current_city = get_city_user(call.from_user.id)[0]

    await state.set_state("here_change_city")
    await state.update_data({'position_id': position_id, 'category_id': category_id, 'remover': remover})
    await call.message.delete()
    if lang == "ru":
        await call.message.answer("<b>📁 Выберите другой город 🏙</b>\n"
                                  "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
                                  f"❕ Город товара: <code>{current_city}</code>", reply_markup=geo_1_kb())
    if lang == "en":
        await call.message.answer("<b>📁 Choose different city 🏙</b>\n"
                                  "❕ You can use geolocation or select a city from the list\n"
                                  f"❕City of product: <code>{current_city}</code>", reply_markup=geo_1_kb())

# принятие новой геопозиции для позиции
@dp.callback_query_handler(text_startswith = 'geo_chosen_cities', state='here_change_city')
async def geo_5(cb: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
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
    update_position_city(city[0], city_id, position_id)

    # update_positionx(position_id)
    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await cb.message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await cb.message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))



# Выгрузка товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_items", state="*")
async def product_position_edit_items(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    if lang == "en":
        save_items = ['IDProduct   -   Product Data', "================================"]

    elif lang == "ru":
        save_items = ['АйдиТовара   -   Данные товара', "================================"]
    if len(get_items) >= 1:
        save_items.extend(
            f"{item['item_id']} - {item['item_data']}" for item in get_items
        )
        save_items = "\n".join(save_items)

        save_items = await upload_text(call, save_items)
        if lang == "ru":
            await call.message.answer(f"<b>📥 Все товары позиции: <code>{get_position['position_name']}</code>\n"
                                  f"🔗 Ссылка: <a href='{save_items}'>кликабельно</a></b>",
                                  reply_markup=close_inl)
        if lang == "en":
            await call.message.answer(f"<b>📥 All position items: <code>{get_position['position_name']}</code>\n"
                                  f"🔗 Link: <a href='{save_items}'>Clickable</a></b>",
                                  reply_markup=close_inl)

        await call.answer()
    else:
        if lang == "ru":
            await call.answer("❕ В данной позиции отсутствуют товары", True)
        if lang == "en":
            await call.answer("❕ This position has no items", True)


# Удаление позиции
@dp.callback_query_handler(text_startswith="position_edit_delete", state="*")
async def product_position_edit_delete(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        await call.message.delete()
        await call.message.answer(_("<b>📁 Вы действительно хотите удалить позицию? ❌</b>", locale=lang), reply_markup=position_edit_delete_finl(position_id, category_id, remover, lang))


# Подтверждение удаления позиции
@dp.callback_query_handler(text_startswith="position_delete", state="*")
async def product_position_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    remover = int(call.data.split(":")[4])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    user_role = get_userx(user_id=user_id)['user_role']
    if user_role == "Admin":
        if get_action == "yes":
            remove_itemx(position_id=position_id)
            remove_positionx(position_id=position_id)

            await call.answer(_("📁 Вы успешно удалили позицию и её товары ✅", locale=lang))

            if len(get_positionsx(category_id=category_id)) >= 1:
                await call.message.edit_text(_("<b>📁 Выберите нужную вам позицию 🖍</b>", locale=lang), reply_markup=position_edit_open_fp(remover, category_id, lang))
            else:
                await call.message.delete()
        else:
            get_message, get_photo = get_position_admin(position_id)

            if get_photo is not None:
                await call.message.delete()
                await call.message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
            else:
                await call.message.edit_text(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))


# Очистка позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_clear", state="*")
async def product_position_edit_clear(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.delete()
    await call.message.answer(_("<b>📁 Вы хотите удалить все товары позиции?</b>", locale=lang), reply_markup=position_edit_clear_finl(position_id, category_id, remover, lang))


# Согласие очистики позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_clear", state="*")
async def product_position_edit_clear_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    remover = int(call.data.split(":")[4])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        await call.answer(_("📁 Вы успешно удалили все товары позиции ✅", locale=lang))

    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await call.message.delete()
        await call.message.answer_photo(get_photo, get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))
    else:
        await call.message.edit_text(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover, lang))


################################################################################################
###################################### УДАЛЕНИЕ ВСЕХ ПОЗИЦИЙ ###################################
# Согласие на удаление всех позиций и товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_remove_position:", state="*")
async def product_position_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    if get_action == "yes":
        get_positions = len(get_all_positionsx())
        get_items = len(get_all_itemsx())

        clear_positionx()
        clear_itemx()

        if lang == "ru":
            await call.message.edit_text(f"<b>📁 Вы удалили все позиции<code>({get_positions}шт)</code> и товары<code>({get_items}шт)</code> ☑</b>")
        if lang == "en":
            await call.message.edit_text(f"<b>📁 You delete all position <code>({get_positions}шт)</code> anf positions<code>({get_items}pcs)</code> ☑</b>")
    else:
        await call.message.edit_text(_("<b>📁 Вы отменили удаление всех позиций ✅</b>", locale=lang))


################################################################################################
####################################### ДОБАВЛЕНИЕ ТОВАРОВ #####################################
# Возвращение к начальным категориям для добавления товаров
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="back_add_products_to_category", state="*")
async def product_item_create(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    await call.message.edit_text(_("<b>🎁 Выберите категорию с нужной позицией</b>", locale=lang), reply_markup=products_add_category_open_fp(0, lang))

# Следующая страница выбора категории с позицией для добавления товаров
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="products_add_category_nextp", state="*")
async def product_item_load_category_next(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    remover = int(call.data.split(":")[1])

    await call.message.delete()
    await call.message.answer(_("<b>🎁 Выберите категорию с нужной позицией</b>", locale=lang), reply_markup=products_add_category_next_page_fp(remover, lang))


# Предыдущая страница выбора категории с позицией для добавления товаров
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="products_add_category_backp", state="*")
async def product_item_load_category_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.delete()
    await call.message.answer(_("<b>🎁 Выберите категорию с нужной позицией</b>", locale=lang), reply_markup=products_add_category_back_page_fp(remover, lang))


# Выбор категории с нужной позицией
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="products_add_category", state="*")
async def product_item_load_category_open(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.delete()
        await call.message.answer(_("<b>🎁 Выберите нужную вам позицию</b>", locale=lang), reply_markup=products_add_position_open_fp(0, category_id, lang))
    else:
        await call.answer(_("🎁 Позиции в данной категории отсутствуют", locale=lang))


# Следующая страница позиций для добавления товаров
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="products_add_position_nextp", state="*")
async def product_item_load_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>🎁 Выберите нужную вам позицию</b>", locale=lang), reply_markup=products_add_position_next_page_fp(remover, category_id, lang))


# Предыдущая страница позиций для добавления товаров
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="products_add_position_backp", state="*")
async def product_item_load_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await call.message.edit_text(_("<b>🎁 Выберите нужную вам позицию</b>", locale=lang), reply_markup=products_add_position_back_page_fp(remover, category_id, lang))


# Выбор позиции для добавления товаров
@rate_limit(0)
@dp.callback_query_handler(IsAdminorShopAdmin(), text_startswith="products_add_position:", state="*")
async def product_item_load_open(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']

    await state.update_data(here_cache_add_item_category_id=category_id)
    await state.update_data(here_cache_add_item_position_id=position_id)
    await state.update_data(here_count_add_items=0)

    await state.set_state("here_add_items")
    await call.message.delete()
    await call.message.answer(_("<b>📤 Отправьте данные товаров.</b>\n"
                              "❗ Товары разделяются одной пустой строчкой. Пример:\n"
                              "<code>Данные товара...\n\n"
                              "Данные товара...\n\n"
                              "Данные товара...</code>", locale=lang), reply_markup=finish_load_rep)


# Завершение загрузки товаров
@rate_limit(0)
@dp.message_handler(IsAdminorShopAdmin(), text="📥 Закончить загрузку товаров", state="*")
async def product_item_load_finish(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    get_all_items = 0
    try:
        async with state.proxy() as data:
            get_all_items = data['here_count_add_items']
    except Exception:
        pass

    await state.finish()
    user_id = message.from_user.id
    ur = get_userx(user_id=user_id)['user_role']
    if ur == 'Admin':
        if lang == "ru":
            await message.answer("<b>📥 Загрузка товаров была успешно завершена ✅\n"
                                 f"▶ Загружено товаров: <code>{get_all_items}шт</code></b>", reply_markup=items_frep(lang))
        if lang == "en":
            await message.answer("<b>📥 Loading of items has been finished succesfully ✅\n"
                                 f"▶ Items Uploaded: <code>{get_all_items}шт</code></b>", reply_markup=items_frep(lang))
    if ur == 'ShopAdmin':
        if lang == "ru":
            await message.answer("<b>📥 Загрузка товаров была успешно завершена ✅\n"
                                 f"▶ Загружено товаров: <code>{get_all_items}шт</code></b>", reply_markup=items_sh_frep(lang))
        if lang == "en":
            await message.answer("<b>📥 Loading of items has been finished succesfully ✅\n"
                                 f"▶ Items Uploaded: <code>{get_all_items}шт</code></b>", reply_markup=items_sh_frep(lang))


# Принятие данных товара
@rate_limit(0)
@dp.message_handler(IsAdminorShopAdmin(), state="here_add_items")
async def product_item_load_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    cache_msg = await message.answer(_("<b>⌛ Ждите, товары добавляются...</b>", locale=lang))

    count_add = get_all_items = 0
    get_all_items = clear_list(message.text.split("\n\n"))

    for check_item in get_all_items:
        if not check_item.isspace() and check_item != "":
            count_add += 1

    async with state.proxy() as data:
        category_id = data['here_cache_add_item_category_id']
        position_id = data['here_cache_add_item_position_id']
        data['here_count_add_items'] += count_add

    get_user = get_userx(user_id=message.from_user.id)
    add_itemx(category_id, position_id, get_all_items, get_user['user_id'], get_user['user_name'])
    if lang == "ru":
        await cache_msg.edit_text(f"<b>📥 Товары в кол-ве</b> <u>{count_add}шт</u> <b>были успешно добавлены ✅</b>")
    if lang == "en":
        await cache_msg.edit_text(f"<b>📥 Items quantity</b> <u>{count_add}шт</u> <b>has been add succesfully ✅</b>")



################################################################################################
####################################### УДАЛЕНИЕ ТОВАРОВ ######################################
# Принятие айди товаров для их удаления
@dp.message_handler(IsAdmin(), state="here_items_delete")
async def product_item_delete_get(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    await state.finish()

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
        check_item = get_itemx(item_id=item_id)
        if check_item is not None:
            remove_itemx(item_id=item_id)
            remove_ids.append(item_id)
        else:
            cancel_ids.append(item_id)

    remove_ids = ", ".join(remove_ids)
    cancel_ids = ", ".join(cancel_ids)

    if lang == "ru":
        await message.answer(f"<b>✅ Успешно удалённые товары:\n"
                             f"▶ <code>{remove_ids}</code>\n"
                             f"➖➖➖➖➖➖➖➖➖➖\n"
                             f"❌ Ненайденные товары:\n"
                             f"▶ <code>{cancel_ids}</code></b>")
    if lang == "en":
        await message.answer(f"<b>✅ Successfully deleted items:\n"
                         f"▶ <code>{remove_ids}</code>\n"
                         f"➖➖➖➖➖➖➖➖➖➖\n"
                         f"❌ Undiscovered goods:\n"
                         f"▶ <code>{cancel_ids}</code></b>")


################################################################################################
##################################### УДАЛЕНИЕ ВСЕХ ТОВАРОВ ####################################
# Согласие на удаление всех товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_remove_item:", state="*")
async def product_item_remove(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = get_userx(user_id=user_id)['user_lang']
    get_action = call.data.split(":")[1]

    if get_action == "yes":
        get_items = len(get_all_itemsx())
        clear_itemx()
        if lang == "ru":
            await call.message.edit_text(f"<b>🎁 Вы удалили все товары<code>({get_items}шт)</code> ☑</b>")
        if lang == "en":
            await call.message.edit_text(f"<b>🎁 You have deleted all the products<code>({get_items}pcs)</code> ☑</b>")
    else:
            await call.message.edit_text(_("<b>🎁 Вы отменили удаление всех товаров ✅</b>", locale=lang))