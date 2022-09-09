# - *- coding: utf- 8 - *-
from contextlib import suppress

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import CantParseEntities, MessageCantBeDeleted

from tgbot.data.loader import dp
from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl, position_edit_cancel_finl, category_edit_cancel_finl
from tgbot.keyboards.inline_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl
from tgbot.keyboards.inline_page import *
from tgbot.keyboards.reply_all import finish_load_rep, items_frep
from tgbot.middlewares.throttling import rate_limit
from tgbot.services.api_sqlite import *
from tgbot.utils.const_functions import clear_list
from tgbot.utils.misc.bot_filters import IsAdmin
from tgbot.utils.misc_functions import get_position_admin, upload_text


# Создание новой категории
@dp.message_handler(IsAdmin(), text="🗃 Создать категорию ➕", state="*")
async def product_category_create(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_category_name")
    await message.answer("<b>🗃 Введите название для категории 🏷</b>")


# Открытие страниц выбора категорий для редактирования
@dp.message_handler(IsAdmin(), text="🗃 Изменить категорию 🖍", state="*")
async def product_category_edit(message: Message, state: FSMContext):
    await state.finish()

    if len(get_all_categoriesx()) >= 1:
        await message.answer("<b>🗃 Выберите категорию для изменения 🖍</b>",
                             reply_markup=category_edit_swipe_fp(0))
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения категорий</b>")


# Окно с уточнением удалить все категории (позиции и товары включительно)
@dp.message_handler(IsAdmin(), text="🗃 Удалить все категории ❌", state="*")
async def product_category_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🗃 Вы действительно хотите удалить все категории? ❌</b>\n"
                         "❗ Так же будут удалены все позиции и товары",
                         reply_markup=category_remove_confirm_inl)


# Создание новой позиции
@dp.message_handler(IsAdmin(), text="📁 Создать позицию ➕", state="*")
async def product_position_create(message: Message, state: FSMContext):
    await state.finish()

    if len(get_all_categoriesx()) >= 1:
        await message.answer("<b>📁 Выберите категорию для позиции</b>",
                             reply_markup=position_create_swipe_fp(0))
    else:
        await message.answer("<b>❌ Отсутствуют категории для создания позиции</b>")


# Начальные категории для изменения позиции
@dp.message_handler(IsAdmin(), text="📁 Изменить позицию 🖍", state="*")
async def product_position_edit(message: Message, state: FSMContext):
    await state.finish()

    if len(get_all_categoriesx()) >= 1:
        await message.answer("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                             reply_markup=position_edit_category_swipe_fp(0))
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")


# Подтверждение удаления всех позиций
@dp.message_handler(IsAdmin(), text="📁 Удалить все позиции ❌", state="*")
async def product_position_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>📁 Вы действительно хотите удалить все позиции? ❌</b>\n"
                         "❗ Так же будут удалены все товары",
                         reply_markup=position_remove_confirm_inl)


# Начальные категории для добавления товаров
@dp.message_handler(IsAdmin(), text="🎁 Добавить товары ➕", state="*")
async def product_item_create(message: Message, state: FSMContext):
    await state.finish()

    if len(get_all_positionsx()) >= 1:
        await message.answer("<b>🎁 Выберите категорию с нужной позицией</b>",
                             reply_markup=products_add_category_swipe_fp(0))
    else:
        await message.answer("<b>❌ Отсутствуют позиции для добавления товара</b>")


# Удаление определённых товаров
@dp.message_handler(IsAdmin(), text="🎁 Удалить товары 🖍", state="*")
async def product_item_delete(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_items_delete")
    await message.answer("<b>🖍 Вводите айди товаров, которые нужно удалить</b>\n"
                         "❕ Получить айди товаров можно при изменении позиции\n"
                         "❕ Если хотите удалить несколько товаров, отправьте ID товаров через запятую или пробел. Пример:\n"
                         "<code>▶ 123456,123456,123456</code>\n"
                         "<code>▶ 123456 123456 123456</code>")


# Кнопки с подтверждением удаления всех категорий
@dp.message_handler(IsAdmin(), text="🎁 Удалить все товары ❌", state="*")
async def product_item_remove(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🎁 Вы действительно хотите удалить все товары? ❌</b>\n",
                         reply_markup=item_remove_confirm_inl)


################################################################################################
####################################### СОЗДАНИЕ КАТЕГОРИЙ #####################################
# Принятие названия категории для её создания
@dp.message_handler(IsAdmin(), state="here_category_name")
async def product_category_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 50:
        category_id = get_unix()
        add_categoryx(category_id, clear_html(message.text))

        await state.finish()

        get_positions = len(get_positionsx(category_id=category_id))
        get_category = get_categoryx(category_id=category_id)

        await message.answer(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"📁 Кол-во позиций: <code>{get_positions}шт</code>",
                             reply_markup=category_edit_open_finl(category_id, 0))
    else:
        await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                             "🗃 Введите название для категории 🏷")


################################################################################################
####################################### ИЗМЕНЕНИЕ КАТЕГОРИИ ####################################
# Выбор текущей категории для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_open:", state="*")
async def product_category_edit_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.finish()

    get_positions = len(get_positionsx(category_id=category_id))
    get_category = get_categoryx(category_id=category_id)

    await call.message.edit_text(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                                 "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"📁 Кол-во позиций: <code>{get_positions}шт</code>",
                                 reply_markup=category_edit_open_finl(category_id, remover))


# Страница выбора категорий для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="catategory_edit_swipe:", state="*")
async def product_category_edit_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🗃 Выберите категорию для изменения 🖍</b>",
                                 reply_markup=category_edit_swipe_fp(remover))


######################################## САМО ИЗМЕНЕНИЕ КАТЕГОРИИ ########################################
# Изменение названия категории
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_name:", state="*")
async def product_category_edit_name(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_category_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("here_change_category_name")
    await call.message.answer("<b>🗃 Введите новое название для категории 🏷</b>",
                              reply_markup=category_edit_cancel_finl(category_id, remover))


# Принятие нового имени для категории
@dp.message_handler(IsAdmin(), state="here_change_category_name")
async def product_category_edit_name_get(message: Message, state: FSMContext):
    category_id = (await state.get_data())['here_cache_category_id']
    remover = (await state.get_data())['here_cache_category_remover']

    if len(message.text) <= 50:
        await state.finish()

        update_categoryx(category_id, category_name=clear_html(message.text))

        get_positions = get_positionsx(category_id=category_id)
        get_category = get_categoryx(category_id=category_id)

        await message.answer(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"📁 Кол-во позиций: <code>{len(get_positions)}шт</code>",
                             reply_markup=category_edit_open_finl(category_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                             "🗃 Введите новое название для категории 🏷",
                             reply_markup=category_edit_cancel_finl(category_id, remover))


# Окно с уточнением удалить категорию
@dp.callback_query_handler(IsAdmin(), text_startswith="category_edit_delete:", state="*")
async def product_category_edit_delete(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await call.message.edit_text("<b>❗ Вы действительно хотите удалить категорию и все её данные?</b>",
                                 reply_markup=category_edit_delete_finl(category_id, remover))


# Отмена удаления категории
@dp.callback_query_handler(IsAdmin(), text_startswith="category_delete:", state="*")
async def product_category_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    get_action = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    if get_action == "yes":
        remove_categoryx(category_id=category_id)
        remove_positionx(category_id=category_id)
        remove_itemx(category_id=category_id)

        await call.answer("🗃 Категория и все её данные были успешно удалены ✅")
        if len(get_all_categoriesx()) >= 1:
            await call.message.edit_text("<b>🗃 Выберите категорию для изменения 🖍</b>",
                                         reply_markup=category_edit_swipe_fp(remover))
        else:
            with suppress(MessageCantBeDeleted):
                await call.message.delete()
    else:
        get_fat_count = len(get_positionsx(category_id=category_id))
        get_category = get_categoryx(category_id=category_id)

        await call.message.edit_text(f"<b>🗃 Категория: <code>{get_category['category_name']}</code></b>\n"
                                     "➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                     f"📁 Кол-во позиций: <code>{get_fat_count}шт</code>",
                                     reply_markup=category_edit_open_finl(category_id, remover))


################################################################################################
#################################### УДАЛЕНИЕ ВСЕХ КАТЕГОРИЙ ###################################
# Подтверждение на удаление всех категорий (позиций и товаров включительно)
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_remove_category:", state="*")
async def product_category_remove_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

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
####################################### ДОБАВЛЕНИЕ ПОЗИЦИИ #####################################
# Следующая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsAdmin(), text_startswith="position_create_swipe:", state="*")
async def product_position_create_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию для позиции ➕</b>",
                                 reply_markup=position_create_swipe_fp(remover))


# Выбор категории для создания позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_create_open:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]

    await state.update_data(here_cache_change_category_id=category_id)

    await state.set_state("here_position_name")
    await call.message.edit_text("<b>📁 Введите название для позиции 🏷</b>")


# Принятие имени для создания позиции
@dp.message_handler(IsAdmin(), state="here_position_name")
async def product_position_create_name(message: Message, state: FSMContext):
    if len(message.text) <= 50:
        await state.update_data(here_position_name=clear_html(message.text))

        await state.set_state("here_position_price")
        await message.answer("<b>📁 Введите цену для позиции 💰</b>")
    else:
        await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")


# Принятие цены позиции для её создания
@dp.message_handler(IsAdmin(), state="here_position_price")
async def product_position_create_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.update_data(here_position_price=message.text)

            await state.set_state("here_position_description")
            await message.answer("<b>📁 Введите описание для позиции 📜</b>\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
        else:
            await message.answer("<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
                                 "📁 Введите цену для позиции 💰")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰")


# Принятие описания позиции для её создания
@dp.message_handler(IsAdmin(), state="here_position_description")
async def product_position_create_description(message: Message, state: FSMContext):
    try:
        if len(message.text) <= 600:
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
@dp.message_handler(IsAdmin(), content_types="photo", state="here_position_photo")
@dp.message_handler(IsAdmin(), text="0", state="here_position_photo")
async def product_position_create_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_name = clear_html(data['here_position_name'])
        position_price = data['here_position_price']
        category_id = data['here_cache_change_category_id']
        position_description = data['here_position_description']
    await state.finish()

    position_id, position_photo = get_unix(), ""

    if "text" not in message:
        position_photo = message.photo[-1].file_id

    add_positionx(position_id, position_name, position_price, position_description, position_photo, category_id)
    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message,
                                   reply_markup=position_edit_open_finl(position_id, category_id, 0))
    else:
        await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, 0))


################################################################################################
####################################### ИЗМЕНЕНИЕ ПОЗИЦИИ #####################################
# Выбор категории с нужной позицией
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_category_open:", state="*")
async def product_position_edit_category_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]

    get_category = get_categoryx(category_id=category_id)
    get_positions = get_positionsx(category_id=category_id)

    if len(get_positions) >= 1:
        await call.message.edit_text("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                     reply_markup=position_edit_swipe_fp(0, category_id))
    else:
        await call.answer(f"📁 Позиции в категории {get_category['category_name']} отсутствуют")


# Перемещение по страницам категорий для редактирования позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_category_swipe:", state="*")
async def product_position_edit_category_swipe(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_swipe_fp(remover))


# Выбор позиции для редактирования
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_open:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_message, get_photo = get_position_admin(position_id)
    await state.finish()

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if get_photo is not None:
        await call.message.answer_photo(get_photo, get_message,
                                        reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await call.message.answer(get_message,
                                  reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Перемещение по страницам позиций для редактирования позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_swipe:", state="*")
async def product_position_edit_swipe(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    await call.message.answer("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                              reply_markup=position_edit_swipe_fp(remover, category_id))


######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_name:", state="*")
async def product_position_edit_name(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("here_change_position_name")
    await call.message.answer("<b>📁 Введите новое название для позиции 🏷</b>",
                              reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Принятие имени позиции для её изменения
@dp.message_handler(IsAdmin(), state="here_change_position_name")
async def product_position_edit_name_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_position_id']
        category_id = data['here_cache_category_id']
        remover = data['here_cache_position_remover']

    if len(message.text) <= 50:
        await state.finish()

        update_positionx(position_id, position_name=clear_html(message.text))
        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await message.answer_photo(get_photo, get_message,
                                       reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await message.answer("<b>❌ Название не может превышать 50 символов.</b>\n"
                             "📁 Введите новое название для позиции 🏷",
                             reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Изменение цены позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_price:", state="*")
async def product_position_edit_price(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("here_change_position_price")
    await call.message.answer("<b>📁 Введите новую цену для позиции 💰</b>",
                              reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Принятие цены позиции для её изменения
@dp.message_handler(IsAdmin(), state="here_change_position_price")
async def product_position_edit_price_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_position_id']
        category_id = data['here_cache_category_id']
        remover = data['here_cache_position_remover']

    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
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
            await message.answer("<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
                                 "📁 Введите цену для позиции 💰",
                                 reply_markup=position_edit_cancel_finl(position_id, category_id, remover))
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰",
                             reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Изменение описания позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_description:", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("here_change_position_description")
    await call.message.answer("<b>📁 Введите новое описание для позиции 📜</b>\n"
                              "❕ Вы можете использовать HTML разметку\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.",
                              reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Принятие описания позиции для её изменения
@dp.message_handler(IsAdmin(), state="here_change_position_description")
async def product_position_edit_description_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        category_id = data['here_cache_category_id']
        position_id = data['here_cache_position_id']
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
                                 "❕ Отправьте <code>0</code> чтобы пропустить.",
                                 reply_markup=position_edit_cancel_finl(position_id, category_id, remover))
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "📁 Введите новое описание для позиции 📜\n"
                             "❕ Вы можете использовать HTML разметку\n"
                             "❕ Отправьте <code>0</code> чтобы пропустить.",
                             reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Изменение изображения позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_photo:", state="*")
async def product_position_edit_photo(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_remover=remover)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("here_change_position_photo")
    await call.message.answer("<b>📁 Отправьте новое изображение для позиции 📸</b>\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.",
                              reply_markup=position_edit_cancel_finl(position_id, category_id, remover))


# Принятие нового фото для позиции
@dp.message_handler(IsAdmin(), content_types="photo", state="here_change_position_photo")
@dp.message_handler(IsAdmin(), text="0", state="here_change_position_photo")
async def product_position_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_position_id']
        category_id = data['here_cache_category_id']
        remover = data['here_cache_position_remover']
    await state.finish()

    if "text" in message:
        position_photo = ""
    else:
        position_photo = message.photo[-1].file_id

    update_positionx(position_id, position_photo=position_photo)
    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await message.answer_photo(get_photo, get_message,
                                   reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await message.answer(get_message, reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Выгрузка товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_items:", state="*")
async def product_position_edit_items(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    save_items = ['АйдиТовара   -   Данные товара', "================================"]

    if len(get_items) >= 1:
        for item in get_items: save_items.append(f"{item['item_id']} - {item['item_data']}")
        save_items = "\n".join(save_items)

        save_items = await upload_text(call, save_items)
        await call.message.answer(f"<b>📥 Все товары позиции: <code>{get_position['position_name']}</code>\n"
                                  f"🔗 Ссылка: <a href='{save_items}'>кликабельно</a></b>",
                                  reply_markup=close_inl)
        await call.answer()
    else:
        await call.answer("❕ В данной позиции отсутствуют товары", True)


# Удаление позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_delete:", state="*")
async def product_position_edit_delete(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    await call.message.answer("<b>📁 Вы действительно хотите удалить позицию? ❌</b>",
                              reply_markup=position_edit_delete_finl(position_id, category_id, remover))


# Подтверждение удаления позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_delete:", state="*")
async def product_position_edit_delete_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = call.data.split(":")[2]
    category_id = call.data.split(":")[3]
    remover = int(call.data.split(":")[4])

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        remove_positionx(position_id=position_id)

        await call.answer("📁 Вы успешно удалили позицию и её товары ✅")

        if len(get_positionsx(category_id=category_id)) >= 1:
            await call.message.edit_text("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                         reply_markup=position_edit_swipe_fp(remover, category_id))
        else:
            with suppress(MessageCantBeDeleted):
                await call.message.delete()
    else:
        get_message, get_photo = get_position_admin(position_id)

        with suppress(MessageCantBeDeleted):
            await call.message.delete()

        if get_photo is not None:
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await call.message.answer(get_message,
                                      reply_markup=position_edit_open_finl(position_id, category_id, remover))


# Очистка позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_edit_clear:", state="*")
async def product_position_edit_clear(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    with suppress(MessageCantBeDeleted):
        await call.message.delete()
    await call.message.answer("<b>📁 Вы хотите удалить все товары позиции?</b>",
                              reply_markup=position_edit_clear_finl(position_id, category_id, remover))


# Согласие очистики позиции
@dp.callback_query_handler(IsAdmin(), text_startswith="position_clear:", state="*")
async def product_position_edit_clear_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = call.data.split(":")[2]
    category_id = call.data.split(":")[3]
    remover = int(call.data.split(":")[4])

    if get_action == "yes":
        remove_itemx(position_id=position_id)
        await call.answer("📁 Вы успешно удалили все товары позиции ✅")

    get_message, get_photo = get_position_admin(position_id)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if get_photo is not None:
        await call.message.answer_photo(get_photo, get_message,
                                        reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await call.message.answer(get_message,
                                     reply_markup=position_edit_open_finl(position_id, category_id, remover))


################################################################################################
###################################### УДАЛЕНИЕ ВСЕХ ПОЗИЦИЙ ###################################
# Согласие на удаление всех позиций и товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_remove_position:", state="*")
async def product_position_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

    if get_action == "yes":
        get_positions = len(get_all_positionsx())
        get_items = len(get_all_itemsx())

        clear_positionx()
        clear_itemx()

        await call.message.edit_text(
            f"<b>📁 Вы удалили все позиции<code>({get_positions}шт)</code> и товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>📁 Вы отменили удаление всех позиций ✅</b>")


################################################################################################
####################################### ДОБАВЛЕНИЕ ТОВАРОВ #####################################
# Выбор категории с нужной позицией
@dp.callback_query_handler(IsAdmin(), text_startswith="products_add_category_open:", state="*")
async def product_item_category_open(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = get_categoryx(category_id=category_id)
    get_positions = get_positionsx(category_id=category_id)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    if len(get_positions) >= 1:
        await call.message.answer("<b>🎁 Выберите нужную вам позицию</b>",
                                  reply_markup=products_add_position_swipe_fp(0, category_id))
    else:
        await call.answer(f"🎁 Позиции в категории {get_category['category_name']} отсутствуют")


# Перемещение по страницам категорий для добавления товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="products_add_category_swipe:", state="*")
async def product_item_category_swipe(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите категорию с нужной позицией</b>",
                                 reply_markup=products_add_category_swipe_fp(remover))


# Перемещение по страницам позиций для добавления товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="products_add_position_swipe:", state="*")
async def product_item_position_swipe(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужную вам позицию</b>",
                                 reply_markup=products_add_position_swipe_fp(remover, category_id))


# Выбор позиции для добавления товаров
@rate_limit(0)
@dp.callback_query_handler(IsAdmin(), text_startswith="products_add_position_open:", state="*")
async def product_item_position_open(call: CallbackQuery, state: FSMContext):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]

    await state.update_data(here_cache_add_item_category_id=category_id)
    await state.update_data(here_cache_add_item_position_id=position_id)
    await state.update_data(here_count_add_items=0)

    with suppress(MessageCantBeDeleted):
        await call.message.delete()

    await state.set_state("here_add_items")
    await call.message.answer("<b>📤 Отправьте данные товаров.</b>\n"
                              "❗ Товары разделяются одной пустой строчкой. Пример:\n"
                              "<code>Данные товара...\n\n"
                              "Данные товара...\n\n"
                              "Данные товара...</code>",
                              reply_markup=finish_load_rep)


# Завершение загрузки товаров
@rate_limit(0)
@dp.message_handler(IsAdmin(), text="📥 Закончить загрузку товаров", state="*")
async def product_item_load_finish(message: Message, state: FSMContext):
    get_all_items = 0
    try:
        async with state.proxy() as data:
            get_all_items = data['here_count_add_items']
    except:
        pass

    await state.finish()
    await message.answer("<b>📥 Загрузка товаров была успешно завершена ✅\n"
                         f"▶ Загружено товаров: <code>{get_all_items}шт</code></b>",
                         reply_markup=items_frep())


# Принятие данных товара
@rate_limit(0)
@dp.message_handler(IsAdmin(), state="here_add_items")
async def product_item_load_get(message: Message, state: FSMContext):
    cache_msg = await message.answer("<b>⌛ Ждите, товары добавляются...</b>")

    count_add = 0
    get_all_items = clear_list(message.text.split("\n\n"))

    for check_item in get_all_items:
        if not check_item.isspace() and check_item != "": count_add += 1

    async with state.proxy() as data:
        category_id = data['here_cache_add_item_category_id']
        position_id = data['here_cache_add_item_position_id']
        data['here_count_add_items'] += count_add

    get_user = get_userx(user_id=message.from_user.id)
    add_itemx(category_id, position_id, get_all_items, get_user['user_id'], get_user['user_name'])

    await cache_msg.edit_text(f"<b>📥 Товары в кол-ве</b> <u>{count_add}шт</u> <b>были успешно добавлены ✅</b>")


################################################################################################
####################################### УДАЛЕНИЕ ТОВАРОВ ######################################
# Принятие айди товаров для их удаления
@dp.message_handler(IsAdmin(), state="here_items_delete")
async def product_item_delete_get(message: Message, state: FSMContext):
    await state.finish()

    remove_ids, cancel_ids = [], []  # Айди удалённых и ненайденных товаров
    get_item_ids_one, get_item_ids_two = [], [[]]
    save_ids = []

    if "," in message.text:
        get_item_ids_one = clear_list(message.text.split(","))
    else:
        get_item_ids_one = clear_list([message.text])

    for item in get_item_ids_one:
        if " " in item:
            get_item_ids_two.append(item.split(" "))

    if len(get_item_ids_two) == 1:
        get_item_ids_two.append(get_item_ids_one)

    for check_item in get_item_ids_two:
        for item in clear_list(check_item):
            save_ids.append(item)

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

    await message.answer(f"<b>✅ Успешно удалённые товары:\n"
                         f"▶ <code>{remove_ids}</code>\n"
                         f"➖➖➖➖➖➖➖➖➖➖\n"
                         f"❌ Ненайденные товары:\n"
                         f"▶ <code>{cancel_ids}</code></b>")


################################################################################################
##################################### УДАЛЕНИЕ ВСЕХ ТОВАРОВ ####################################
# Согласие на удаление всех товаров
@dp.callback_query_handler(IsAdmin(), text_startswith="confirm_remove_item:", state="*")
async def product_item_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

    if get_action == "yes":
        get_items = len(get_all_itemsx())
        clear_itemx()

        await call.message.edit_text(f"<b>🎁 Вы удалили все товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>🎁 Вы отменили удаление всех товаров ✅</b>")
