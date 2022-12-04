# - *- coding: utf- 8 - *-
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.data.config import BOT_DESCRIPTION
from tgbot.keyboards.inline_user import user_support_finl, products_open_finl, products_confirm_finl, payment_as_choice_finl
from tgbot.keyboards.inline_z_all import profile_open_inl
from tgbot.keyboards.inline_z_page import *
from tgbot.keyboards.reply_z_all import menu_frep, items_sh_frep
from tgbot.keyboards.inline_admin import category_edit_open_finl, position_edit_open_finl, category_edit_delete_finl, \
    position_edit_clear_finl, position_edit_delete_finl, payment_choice_finl
from tgbot.keyboards.inline_z_all import category_remove_confirm_inl, position_remove_confirm_inl, \
    item_remove_confirm_inl, close_inl
from tgbot.keyboards.inline_z_page import *
from tgbot.keyboards.reply_z_all import finish_load_rep
from tgbot.utils.misc.bot_filters import IsShopAdmin
from tgbot.utils.misc_functions import get_position_admin, upload_text
from tgbot.loader import dp
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_sqlite import *
from tgbot.utils.const_functions import get_date, split_messages, get_unix
from tgbot.utils.misc_functions import open_profile_my, upload_text, get_faq, send_admins

################################################################################################
# Заявка на продавца магазина
# Открытие товаров


@dp.message_handler(text="Хочу продавать", state="*")
async def user_seller_request(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>Подтвердите заявку:</b>",
                         reply_markup=request_seller_role(message.from_user.id))

# Управление товарами


@dp.message_handler(IsShopAdmin(), text="🎁 Управление товарами дмаг.🖍", state="*")
async def shopadmin_products(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🎁 Редактирование товаров дмаг.</b>", reply_markup=items_sh_frep())


@dp.message_handler(text="🗃 Создать категорию ➕", state="*")
async def product_category_create(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_category_name")
    await message.answer("<b>🗃 Введите название для категории 🏷</b>")

# Начальные категории для изменения позиции


# !!!!!!!   Изменить позицию
@dp.message_handler(IsShopAdmin(), text="📁 Изменить позицию 🖍", state="*")
async def product_position_edit(message: Message, state: FSMContext):
    print(f'📁 Изменить позицию 🖍  user_menu.py 73')
    await state.finish()

    await message.answer("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                         reply_markup=position_edit_category_open_fp(0))

# Открытие товаров


@dp.message_handler(text="🎁 Игры в аренду", state="*")
async def user_shop(message: Message, state: FSMContext):
    print(f'Открытие категорий товаров  user_menu.py 39')
    await state.finish()

    city_id = get_city_user(message.from_user.id)[2]
    # get_categories = get_category_in_city(city_id)

    if len(get_category_in_city(city_id)) >= 1:
        await message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                             reply_markup=products_item_category_open_fp(0, city_id))
    else:
        await message.answer("<b>🎁 В вашем городе товаров нет,выбирите другой город</b>\n\n"
                             "🏙 Изменить город вы можете в личном кабинете")


# Открытие профиля
@dp.message_handler(text="👤 Профиль", state="*")
async def user_profile(message: Message, state: FSMContext):
    await state.finish()

    await message.answer(open_profile_my(message.from_user.id), reply_markup=profile_open_inl)


# Открытие FAQ
@dp.message_handler(text=["ℹ FAQ", "/faq"], state="*")
async def user_faq(message: Message, state: FSMContext):
    await state.finish()

    send_message = get_settingsx()['misc_faq']
    if send_message == "None":
        send_message = f"ℹ Информация. Измените её в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}"

    await message.answer(get_faq(message.from_user.id, send_message), disable_web_page_preview=True)


# Открытие сообщения с ссылкой на поддержку
@dp.message_handler(text=["☎ Поддержка/FAQ", "/support"], state="*")
async def user_support(message: Message, state: FSMContext):
    await state.finish()

    user_support = get_settingsx()['misc_support']
    if str(user_support).isdigit():
        get_user = get_userx(user_id=user_support)

        if len(get_user['user_login']) >= 1:
            await message.answer("<b>☎ Нажмите кнопку ниже для связи с Администратором.</b>",
                                 reply_markup=user_support_finl(get_user['user_login']))
            return
        else:
            update_settingsx(misc_support="None")

    await message.answer(f"☎ Поддержка/FAQ.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{BOT_DESCRIPTION}",
                         disable_web_page_preview=True)


# Просмотр истории покупок
@dp.callback_query_handler(text="create_seller_request", state="*")
async def user_seller(call: CallbackQuery, state: FSMContext):
    seller_request = create_seller_request(call.from_user.id)
    await call.answer("🎁 Запрос успешно создан")
    await send_admins(f"Поступил новый запрос продавца!", markup='check_seller_requests')
    # await bot.send_message(get_admins(), "ntcnnnnnn")

# Удаление позиции


@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_delete", state="*")
async def product_position_edit_delete(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await call.message.delete()
    await call.message.answer("<b>📁 Вы действительно хотите удалить позицию? ❌</b>",
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
            await call.message.edit_text("<b>📁 Выберите нужную вам позицию 🖍</b>",
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
@dp.message_handler(IsShopAdmin(), text="🖲 Способы пополнения", state="*")
async def payment_systems(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🖲 Выберите способ пополнения</b>", reply_markup=payment_as_choice_finl())


# Включение/выключение самих способов пополнения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="change_payment:")
async def payment_systems_edit(call: CallbackQuery):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]
    print("Админ магазина")
    # print(call.data.split(":")[0])
    print(call.message.from_user.id)
    get_payment = get_paymentx()

    if get_payment['qiwi_login'] != "None" and get_payment['qiwi_token'] != "None" or way_status == "False":
        if way_pay == "Form":
            if get_payment['qiwi_secret'] != "None" or way_status == "False":
                update_upaymentx(way_form=way_status)
            else:
                await call.answer(
                    "❗ Приватный ключ отсутствует. Измените киви и добавьте приватный ключ для включения оплаты по Форме",
                    True)
        elif way_pay == "Number":
            update_upaymentx(way_number=way_status)
        elif way_pay == "Nickname":
            status, response = await (await QiwiAPI(call)).get_nickname()
            if status:
                update_upaymentx(way_nickname=way_status,
                                 qiwi_nickname=response)
            else:
                await call.answer(response, True)
    else:
        await call.answer("❗ Добавьте киви кошелёк перед включением Способов пополнений.", True)

    try:
        await call.message.edit_text("<b>🖲 Выберите способ пополнения</b>", reply_markup=payment_as_choice_finl())
    except:
        pass


####################################### QIWI ######################################
# Изменение QIWI кошелька
@dp.message_handler(IsShopAdmin(), text="🥝 Изменить QIWI 🖍", state="*")
async def payment_qiwi_edit(message: Message, state: FSMContext):
    await state.finish()

    await state.set_state("here_qiwi_login")
    await message.answer("<b>🥝 Введите <code>номер (через +7, +380)</code> QIWI кошелька 🖍</b>")


# Проверка работоспособности QIWI
@dp.message_handler(IsShopAdmin(), text="🥝 Проверить QIWI ♻", state="*")
async def payment_qiwi_check(message: Message, state: FSMContext):
    print("Проверка КИВИ админом магазина")
    await state.finish()

    await (await QiwiAPI(message, check_pass=True)).pre_checker()


# Баланс QIWI
@dp.message_handler(IsShopAdmin(), text="🥝 Баланс QIWI 👁", state="*")
async def payment_qiwi_balance(message: Message, state: FSMContext):
    await state.finish()

    await (await QiwiAPI(message)).get_balance()


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
@dp.message_handler(IsShopAdmin(), state="here_qiwi_secret")
async def payment_qiwi_edit_secret(message: Message, state: FSMContext):
    async with state.proxy() as data:
        qiwi_login = data['here_qiwi_login']
        qiwi_token = data['here_qiwi_token']
        if message.text == "0":
            qiwi_secret = "None"
        if message.text != "0":
            qiwi_secret = message.text

    await state.finish()

    cache_message = await message.answer("<b>🥝 Проверка введённых QIWI данных... 🔄</b>")
    await asyncio.sleep(0.5)

    await (await QiwiAPI(cache_message, qiwi_login, qiwi_token, qiwi_secret, True)).pre_checker()

################################################################################################
###################################### УДАЛЕНИЕ ВСЕХ ПОЗИЦИЙ ###################################
# Согласие на удаление всех позиций и товаров


@dp.callback_query_handler(IsShopAdmin(), text_startswith="confirm_remove_position:", state="*")
async def product_position_remove(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]

    if get_action == "yes":
        get_positions = len(get_all_positionsx())
        get_items = len(get_all_my_itemsx())

        clear_positionx()
        clear_itemx()

        await call.message.edit_text(
            f"<b>📁 Вы удалили все позиции<code>({get_positions}шт)</code> и товары<code>({get_items}шт)</code> ☑</b>")
    else:
        await call.message.edit_text("<b>📁 Вы отменили удаление всех позиций ✅</b>")


###############################################################################################
################################################################################################
####################################### ДОБАВЛЕНИЕ ПОЗИЦИЙ #####################################
# Следующая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_create_nextp:", state="*")
async def product_position_create_next(call: CallbackQuery, state: FSMContext):
    print(f'выбора категорий для создания позиций  user_menu.py 126')
    remover = int(call.data.split(":")[1])
    print(remover)

    await call.message.edit_text("<b>📁 Выберите категорию для позиции ➕</b>",
                                 reply_markup=position_create_next_page_fp(remover))


# Предыдущая страница выбора категорий для создания позиций
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_create_backp:", state="*")
async def product_position_create_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию для позиции ➕</b>",
                                 reply_markup=position_create_back_page_fp(remover))


@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_shop_create_here:", state="*")
async def product_position_create(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])

    await state.update_data(here_cache_change_shop_id=category_id)

    if len(get_all_categoriesx()) >= 1:
        await call.message.answer("<b>📁 Выберите категорию для позиции</b>",
                                  reply_markup=position_create_open_fp(0))
    else:
        await call.message.answer("<b>❌ Отсутствуют категории для создания позиции.</b>")


# Выбор категории для создания позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_create_here:", state="*")
async def product_position_create_select_category(call: CallbackQuery, state: FSMContext):
    print('position_create_here - user_menu 160')
    category_id = int(call.data.split(":")[1])

    await state.update_data(here_cache_change_category_id=category_id)

    await state.set_state("here_position_name")
    await call.message.edit_text("<b>📁 Введите название для позиции 🏷</b>")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Заготовка под принятие города магазином
# Принятие города для создания позиции
# @dp.message_handler(IsShopAdmin(), state="here_position_city")
# async def product_position_create_name(message: Message, state: FSMContext):
#     print(f'Принятие города для создания позиции  admin_products_shop.py 344')
#     city_user = get_city_user(message.from_user.id)
# Принятие имени для создания позиции
@dp.message_handler(IsShopAdmin(), state="here_position_name")
async def product_position_create_name(message: Message, state: FSMContext):
    print(f'Принятие имени для создания позиции  admin_products.py 355')
    if len(message.text) <= 100:
        await state.update_data(here_position_name=clear_html(message.text), here_position_city=get_city_user(message.from_user.id)[0], position_city_id=get_city_user(message.from_user.id)[2])

        await state.set_state("here_position_price")
        await message.answer("<b>📁 Введите цену для позиции 💰</b>")
    else:
        await message.answer("<b>❌ Название не может превышать 100 символов.</b>\n"
                             "📁 Введите название для позиции 🏷")


# Принятие цены позиции для её создания
@dp.message_handler(IsShopAdmin(), state="here_position_price")
async def product_position_create_price(message: Message, state: FSMContext):
    print(f'Принятие цены позиции  admin_products.py 366')
    if message.text.isdigit():
        if 0 <= int(message.text) <= 10000000:
            await state.update_data(here_position_price=message.text)

            await state.set_state("here_position_description")
            await message.answer("<b>📁 Введите описание для позиции 📜</b>\n"
                                 "❕ Вы можете использовать HTML разметку\n"
                                 "❕ Отправьте <code>0</code> чтобы пропустить.")
        else:
            await message.answer("<b>❌ Цена не может быть меньше 0 или больше 10 000 000.</b>\n"
                                 "📁 Введите цену для позиции 💰")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "📁 Введите цену для позиции 💰")


# Принятие описания позиции для её создания
@dp.message_handler(IsShopAdmin(), state="here_position_description")
async def product_position_create_description(message: Message, state: FSMContext):
    print(f'Принятие описания позиции  admin_products.py 386')

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
@dp.message_handler(IsShopAdmin(), content_types="photo", state="here_position_photo")
@dp.message_handler(IsShopAdmin(), text="0", state="here_position_photo")
async def product_position_create_photo(message: Message, state: FSMContext):
    print(f'Принятие изображения позиции  admin_products.py 418')
    async with state.proxy() as data:
        position_user_id = message.from_user.id
        position_city = data['here_position_city']
        position_city_id = data['position_city_id']
        position_name = clear_html(data['here_position_name'])
        position_price = data['here_position_price']
        catategory_id = data['here_cache_change_category_id']
        position_description = data['here_position_description']
    await state.finish()

    if "text" in message:
        position_photo = ""
    else:
        position_photo = message.photo[-1].file_id

    add_positionx(position_city, position_city_id, position_name, position_price,
                  position_description, position_photo, catategory_id, position_user_id)

    await message.answer("<b>📁 Позиция была успешно создана ✅</b>")


################################################################################################
####################################### ИЗМЕНЕНИЕ ПОЗИЦИЙ #####################################
# Возвращение к начальным категориям для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_open_fp(0))


# Следующая страница категорий для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_nextp:", state="*")
async def product_position_edit_category_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_next_page_fp(remover))


# Предыдущая страница категорий для редактирования позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category_backp:", state="*")
async def product_position_edit_category_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_category_back_page_fp(remover))


# Выбор категории с нужной позицией
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_category:", state="*")
async def product_position_edit_category_open(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.edit_text("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                     reply_markup=position_edit_open_fp(0, category_id))
    else:
        await call.answer("📁 Позиции в данной категории отсутствуют")


# Следующая страница позиций для их изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_nextp:", state="*")
async def product_position_edit_next(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_next_page_fp(remover, category_id))


# Предыдущая страница позиций для их изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_backp:", state="*")
async def product_position_edit_back(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>📁 Выберите категорию с нужной позицией 🖍</b>",
                                 reply_markup=position_edit_back_page_fp(remover, category_id))


# Выбор позиции для редактирования
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit:", state="*")
async def product_position_edit_open(call: CallbackQuery, state: FSMContext):
    print(f'Выбор позиции для редактирования api_sqlite.py 496')
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])
    user_id = call.from_user.id

    # IsProductShopAdmin()
    adminspos = check_position_owner(user_id, position_id)
    if adminspos is True:

        get_message, get_photo = get_position_admin(position_id)

        if get_photo is not None:
            await call.message.delete()
            await call.message.answer_photo(get_photo, get_message,
                                            reply_markup=position_edit_open_finl(position_id, category_id, remover))
        else:
            await call.message.edit_text(get_message,
                                         reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await call.answer("<b>❗ У Вас нет прав редактировать данную позицию.</b>")


# Возвращение к выбору позиции для изменения
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_return", state="*")
async def product_position_edit_return(call: CallbackQuery, state: FSMContext):
    category_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])

    if len(get_positionsx(category_id=category_id)) >= 1:
        await call.message.delete()
        await call.message.answer("<b>📁 Выберите нужную вам позицию 🖍</b>",
                                  reply_markup=position_edit_open_fp(remover, category_id))
    else:
        await call.answer("<b>❗ Позиции в данной категории отсутствуют</b>")


######################################## САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ########################################
# Изменение имени позиции
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_name", state="*")
async def product_position_edit_name(call: CallbackQuery, state: FSMContext):
    print(f'Изменение имени позиции api_sqlite.py 529')
    category_id = int(call.data.split(":")[1])
    position_id = int(call.data.split(":")[2])
    remover = int(call.data.split(":")[3])

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_name")
    await call.message.delete()
    await call.message.answer("<b>📁 Введите новое название для позиции 🏷</b>")


# Принятие имени позиции для её изменения
@dp.message_handler(IsShopAdmin(), state="here_change_position_name")
async def product_position_edit_name_get(message: Message, state: FSMContext):
    if len(message.text) <= 100:
        async with state.proxy() as data:
            position_id = data['here_cache_category_id']
            category_id = data['here_cache_position_id']
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
    await call.message.answer("<b>📁 Введите новую цену для позиции 💰</b>")


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

    await state.update_data(here_cache_category_id=category_id)
    await state.update_data(here_cache_position_id=position_id)
    await state.update_data(here_cache_position_remover=remover)

    await state.set_state("here_change_position_photo")
    await call.message.delete()
    await call.message.answer("<b>📁 Отправьте новое изображение для позиции 📸</b>\n"
                              "❕ Отправьте <code>0</code> чтобы пропустить.")


# Принятие нового фото для позиции
@dp.message_handler(IsShopAdmin(), content_types="photo", state="here_change_position_photo")
@dp.message_handler(IsShopAdmin(), text="0", state="here_change_position_photo")
async def product_position_edit_photo_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        position_id = data['here_cache_category_id']
        category_id = data['here_cache_position_id']
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


# ---------------------------  Добавлено 12.08.22 ------------------------------------------

# Изменение города продукта
@dp.callback_query_handler(IsShopAdmin(), text_startswith="position_edit_city", state="*")
async def product_position_edit_description(call: CallbackQuery, state: FSMContext):
    print(f'Изменение города продукта  admin_products.py 715')
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
    await call.message.answer("<b>📁 Выбирите другой город 🏙</b>\n"
                              "❕ Вы можете использовать геолокацию или выбрать город из списка\n"
                              f"❕  Город товара: <code>{current_city}</code>", reply_markup=geo_1_kb())


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
    update_position_city(city[0], city_id, position_id)

    # update_positionx(position_id)
    get_message, get_photo = get_position_admin(position_id)

    if get_photo is not None:
        await cb.message.answer_photo(get_photo, get_message,
                                      reply_markup=position_edit_open_finl(position_id, category_id, remover))
    else:
        await cb.message.answer(get_message,
                                reply_markup=position_edit_open_finl(position_id, category_id, remover))


################################################################################################
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
                                      f"🎁 Аренда: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}шт | {purchases['purchase_price']}₽</code>\n"
                                      f"🕰 Дата покупки: <code>{purchases['purchase_date']}</code>\n"
                                      f"🔗 Товары: <a href='{link_items}'>кликабельно</a>")

        await call.message.answer(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)
    else:
        await call.answer("❗ У вас отсутствуют покупки", True)


# Возвращение к профилю
@dp.callback_query_handler(text="user_profile", state="*")
async def user_profile_return(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)


################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
########################################### КАТЕГОРИИ ##########################################
# Открытие категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_open", state="*")
async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
    print(f'Открытие категорий для покупки user_menu.py 133')
    category_id = int(call.data.split(":")[1])

    get_category = get_categoryx(category_id=category_id)
    city = get_city_user(call.from_user.id)
    # get_positionsx(category_id=category_id)
    get_positions = get_position_on_city(category_id, city[2])

    if len(get_positions) >= 1:
        await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=products_item_position_open_fp(0, category_id, city[2]))
    else:
        await call.answer(f"❕ Товары в категории {get_category['category_name']} отсутствуют")


# Вернуться к категориям для покупки
@dp.callback_query_handler(text_startswith="buy_category_return", state="*")
async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
    get_categories = get_all_categoriesx()

    city = get_city_user(call.from_user.id)

    if len(get_categories) >= 1:
        await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                     reply_markup=products_item_category_open_fp(0, city[2]))
    else:
        await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
        await call.answer("❗ Категории были изменены или удалены")


# Следующая страница категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_next_page_fp(remover))


# Предыдущая страница категорий для покупки
@dp.callback_query_handler(text_startswith="buy_category_backp", state="*")
async def user_purchase_category_prev_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_category_back_page_fp(remover))


########################################### ПОЗИЦИИ ##########################################
# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_position_open", state="*")
async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
    print(f'🎁 Покупка товара:   user_menu.py  152')
    position_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])
    category_id = int(call.data.split(":")[3])

    get_position = get_positionx(position_id=position_id)
    get_category = get_categoryx(category_id=category_id)
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_description'] == "0":
        text_description = ""
    else:
        text_description = f"\n📜 Описание:\n" \
                           f"{get_position['position_description']}"

    send_msg = f"<b>🎁 Покупка товара:</b>\n" \
               f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
               f"🏷 Название: <code>{get_position['position_name']}</code>\n" \
               f"🏙 Город: <code>{get_position['position_city']}</code>\n" \
               f"🗃 Категория: <code>{get_category['category_name']}</code>\n" \
               f"💰 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
               f"📦 Количество: <code>{len(get_items)}шт</code>" \
               f"{text_description}"

    if len(get_position['position_photo']) >= 5:
        await call.message.delete()
        await call.message.answer_photo(get_position['position_photo'],
                                        send_msg, reply_markup=products_open_finl(position_id, remover, category_id))
    else:
        await call.message.edit_text(send_msg,
                                     reply_markup=products_open_finl(position_id, remover, category_id))


# Вернуться к позициям для покупки
@dp.callback_query_handler(text_startswith="buy_position_return", state="*")
async def user_purchase_position_return(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_positions = get_all_positionsx()
    city = get_city_user(call.from_user.id)

    if len(get_positions) >= 1:
        await call.message.delete()
        await call.message.answer("<b>🎁 Выберите нужный вам товар:</b>",
                                  reply_markup=products_item_position_open_fp(remover, category_id, city[2]))
    else:
        await call.message.edit_text("<b>🎁 Товары в данное время отсутствуют.</b>")
        await call.answer("❗ Позиции были изменены или удалены")


# Следующая страница позиций для покупки
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=products_item_position_next_page_fp(remover, category_id))


# Предыдущая страница позиций для покупки
@dp.callback_query_handler(text_startswith="buy_position_backp", state="*")
async def user_purchase_position_prev_page(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                 reply_markup=buy_position_return_page_fp(remover, category_id))


########################################### ПОКУПКА ##########################################
# Выбор количества товаров для покупки
@dp.callback_query_handler(text_startswith="buy_item_select", state="*")
async def user_purchase_select(call: CallbackQuery, state: FSMContext):
    position_id = int(call.data.split(":")[1])

    get_position = get_positionx(position_id=position_id)
    get_items = get_itemsx(position_id=position_id)
    get_user = get_userx(user_id=call.from_user.id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] /
                        get_position['position_price'])
        if get_count > len(get_items):
            get_count = len(get_items)
    else:
        get_count = len(get_items)

    if int(get_user['user_balance']) >= int(get_position['position_price']):
        if get_count == 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.finish()

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Срок аренды: <code>{get_position['position_name']}</code>\n"
                                      f"📦 Количество: <code>1шт</code>\n"
                                      f"💰 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
                                      reply_markup=products_confirm_finl(position_id, 1))
        elif get_count >= 1:
            await state.update_data(here_cache_position_id=position_id)
            await state.set_state("here_item_count")

            await call.message.delete()
            await call.message.answer(f"<b>🎁 Введите количество аккаунтов которое хотите купить</b>\n"
                                      f"▶ От <code>1</code> до <code>{get_count}</code>\n"
                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                      f"🎁 Аренда: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
                                      f"💰 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
        else:
            await call.answer("🎁 Товаров нет в наличии")
    else:
        await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)


# Принятие количества товаров для покупки
@dp.message_handler(state="here_item_count")
async def user_purchase_select_count(message: Message, state: FSMContext):
    position_id = (await state.get_data())['here_cache_position_id']

    get_position = get_positionx(position_id=position_id)
    get_user = get_userx(user_id=message.from_user.id)
    get_items = get_itemsx(position_id=position_id)

    if get_position['position_price'] != 0:
        get_count = int(get_user['user_balance'] /
                        get_position['position_price'])
        if get_count > len(get_items):
            get_count = len(get_items)
    else:
        get_count = len(get_items)

    send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"🎁 Введите количество аккаунтов которое хотите купить\n" \
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
                                         f"🎁 Срок аренды: <code>{get_position['position_name']}</code>\n"
                                         f"📦 Количество: <code>{get_count}шт</code>\n"
                                         f"💰 Сумма к покупке: <code>{amount_pay}₽</code>",
                                         reply_markup=products_confirm_finl(position_id, get_count))
                else:
                    await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n" + send_message)
            else:
                await message.answer(f"<b>❌ Неверное количество товаров.</b>\n" + send_message)
        else:
            await state.finish()
            await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>")
    else:
        await message.answer(f"<b>❌ Данные были введены неверно.</b>\n" + send_message)


# Подтверждение покупки товара
@dp.callback_query_handler(text_startswith="xbuy_item", state="*")
async def user_purchase_confirm(call: CallbackQuery, state: FSMContext):
    get_action = call.data.split(":")[1]
    position_id = int(call.data.split(":")[2])
    get_count = int(call.data.split(":")[3])

    if get_action == "yes":
        await call.message.edit_text("<b>🔄 Ждите, товары подготавливаются</b>")

        get_position = get_positionx(position_id=position_id)
        get_items = get_itemsx(position_id=position_id)
        get_user = get_userx(user_id=call.from_user.id)

        amount_pay = int(get_position['position_price'] * get_count)

        if 1 <= int(get_count) <= len(get_items):
            if int(get_user['user_balance']) >= amount_pay:
                save_items, send_count, split_len = buy_itemx(
                    get_items, get_count)

                if get_count != send_count:
                    amount_pay = int(
                        get_position['position_price'] * send_count)
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

                update_userx(
                    get_user['user_id'], user_balance=get_user['user_balance'] - amount_pay)
                add_purchasex(get_user['user_id'], get_user['user_login'], get_user['user_name'], receipt, get_count,
                              amount_pay, get_position['position_price'], get_position['position_id'],
                              get_position['position_name'], "\n".join(
                                  save_items), buy_time, receipt,
                              get_user['user_balance'], int(get_user['user_balance'] - amount_pay))

                await call.message.answer(f"<b>✅ Вы успешно купили товар(ы)</b>\n"
                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                          f"🧾 Чек: <code>#{receipt}</code>\n"
                                          f"🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>\n"
                                          f"🕰 Дата покупки: <code>{buy_time}</code>",
                                          reply_markup=menu_frep(call.from_user.id))
            else:
                await call.message.answer("<b>❗ На вашем счёте недостаточно средств</b>")
        else:
            await call.message.answer("<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                                      reply_markup=menu_frep(call.from_user.id))
    else:
        if len(get_all_categoriesx()) >= 1:
            await call.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                         reply_markup=products_item_category_open_fp(0))
        else:
            await call.message.edit_text("<b>✅ Вы отменили покупку товаров.</b>")
