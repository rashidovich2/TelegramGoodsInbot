# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as ikb

from tgbot.services.api_sqlite import get_paymentx, get_settingsx, get_userx, update_settingsx


# Поиск профиля
def profile_search_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("💰 Изменить баланс", callback_data=f"admin_user_balance_set:{user_id}"),
        ikb("💰 Выдать баланс", callback_data=f"admin_user_balance_add:{user_id}")
    ).add(
        ikb("🎁 Покупки", callback_data=f"admin_user_purchases:{user_id}"),
        ikb("💌 Отправить СМС", callback_data=f"admin_user_message:{user_id}")
    ).add(
        ikb("🔄 Обновить", callback_data=f"admin_user_refresh:{user_id}")
    )

    return keyboard


# Возвращение к профилю
def profile_search_return_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Отменить", callback_data=f"admin_user_refresh:{user_id}"),
    )

    return keyboard

# Способы пополнения
def payment_choice_finl():
    keyboard = InlineKeyboardMarkup()
    get_payments = get_paymentx()

    status_form_kb = ikb("✅", callback_data="change_payment:Form:False")
    status_number_kb = ikb("✅", callback_data="change_payment:Number:False")
    status_nickname_kb = ikb("✅", callback_data="change_payment:Nickname:False")

    if get_payments['way_form'] == "False":
        status_form_kb = ikb("❌", callback_data="change_payment:Form:True")
    if get_payments['way_number'] == "False":
        status_number_kb = ikb("❌", callback_data="change_payment:Number:True")
    if get_payments['way_nickname'] == "False":
        status_nickname_kb = ikb("❌", callback_data="change_payment:Nickname:True")

    keyboard.add(
        ikb("📋 По форме", url="https://vk.cc/bYjKGM"), status_form_kb
    ).row(
        ikb("📞 По номеру", url="https://vk.cc/bYjKEy"), status_number_kb
    ).row(
        ikb("Ⓜ По никнейму", url="https://vk.cc/c8s66X"), status_nickname_kb
    )

    return keyboard


# Кнопки с настройками
def settings_open_finl():
    keyboard = InlineKeyboardMarkup()

    get_settings = get_settingsx()

    if get_settings['misc_support'].isdigit():
        get_user = get_userx(user_id=get_settings['misc_support'])

        if get_user is not None:
            support_kb = ikb(f"@{get_user['user_login']} ✅", callback_data="settings_edit_support")
        else:
            support_kb = ikb("Не установлены ❌", callback_data="settings_edit_support")
            update_settingsx(misc_support="None")
    else:
        support_kb = ikb("Не установлены ❌", callback_data="settings_edit_support")

    if "None" == get_settings['misc_faq']:
        faq_kb = ikb("Не установлено ❌", callback_data="settings_edit_faq")
    else:
        faq_kb = ikb(f"{get_settings['misc_faq'][:15]}... ✅", callback_data="settings_edit_faq")

    keyboard.add(
        ikb("ℹ FAQ", callback_data="..."), faq_kb
    ).add(
        ikb("☎ Поддержка", callback_data="..."), support_kb
    )

    return keyboard


# Выключатели
def turn_open_finl():
    keyboard = InlineKeyboardMarkup()

    get_settings = get_settingsx()

    status_buy_kb = ikb("Включены ✅", callback_data="turn_buy:False")
    status_work_kb = ikb("Включены ✅", callback_data="turn_work:False")
    status_pay_kb = ikb("Включены ✅", callback_data="turn_pay:False")

    if get_settings['status_buy'] == "False":
        status_buy_kb = ikb("Выключены ❌", callback_data="turn_buy:True")
    if get_settings['status_work'] == "False":
        status_work_kb = ikb("Выключены ❌", callback_data="turn_work:True")
    if get_settings['status_refill'] == "False":
        status_pay_kb = ikb("Выключены ❌", callback_data="turn_pay:True")

    keyboard.row(
        ikb("⛔ Тех. работы", callback_data="..."), status_work_kb
    ).row(
        ikb("💰 Пополнения", callback_data="..."), status_pay_kb
    ).row(
        ikb("🎁 Покупки", callback_data="..."), status_buy_kb
    )

    return keyboard


######################################## ТОВАРЫ ########################################
# Изменение категории
def category_edit_open_finl(category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("🏷 Изм. название", callback_data=f"category_edit_name:{category_id}:{remover}"),
        ikb("📁 Добавить позицию", callback_data=f"position_create_open:{category_id}"),
    ).add(
        ikb("⬅ Вернуться ↩", callback_data=f"catategory_edit_swipe:{remover}"),
        ikb("❌ Удалить", callback_data=f"category_edit_delete:{category_id}:{remover}")
    )

    return keyboard


# Кнопки с удалением категории
def category_edit_delete_finl(category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Да, удалить", callback_data=f"category_delete:{category_id}:yes:{remover}"),
        ikb("✅ Нет, отменить", callback_data=f"category_delete:{category_id}:not:{remover}")
    )

    return keyboard


# Отмена изменения категории и возвращение
def category_edit_cancel_finl(category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Отменить", callback_data=f"category_edit_open:{category_id}:{remover}"),
    )

    return keyboard


# Кнопки при открытии позиции для изменения
def position_edit_open_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("🏷 Изм. название", callback_data=f"position_edit_name:{position_id}:{category_id}:{remover}"),
        ikb("💰 Изм. цену", callback_data=f"position_edit_price:{position_id}:{category_id}:{remover}"),
    ).add(
        ikb("📜 Изм. описание", callback_data=f"position_edit_description:{position_id}:{category_id}:{remover}"),
        ikb("📸 Изм. фото", callback_data=f"position_edit_photo:{position_id}:{category_id}:{remover}"),
    ).add(
        ikb("🗑 Очистить", callback_data=f"position_edit_clear:{position_id}:{category_id}:{remover}"),
        ikb("🎁 Добавить товары", callback_data=f"products_add_position_open:{position_id}:{category_id}"),
    ).add(
        ikb("📥 Товары", callback_data=f"position_edit_items:{position_id}:{category_id}:{remover}"),
        ikb("❌ Удалить", callback_data=f"position_edit_delete:{position_id}:{category_id}:{remover}"),
    ).add(
        ikb("⬅ Вернуться ↩", callback_data=f"position_edit_swipe:{category_id}:{remover}"),
    )

    return keyboard


# Подтверждение удаления позиции
def position_edit_delete_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Да, удалить", callback_data=f"position_delete:yes:{position_id}:{category_id}:{remover}"),
        ikb("✅ Нет, отменить", callback_data=f"position_delete:not:{position_id}:{category_id}:{remover}")
    )

    return keyboard


# Подтверждение очистики позиции
def position_edit_clear_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Да, очистить", callback_data=f"position_clear:yes:{position_id}:{category_id}:{remover}"),
        ikb("✅ Нет, отменить", callback_data=f"position_clear:not:{position_id}:{category_id}:{remover}")
    )

    return keyboard


# Отмена изменения позиции и возвращение
def position_edit_cancel_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        ikb("❌ Отменить", callback_data=f"position_edit_open:{position_id}:{category_id}:{remover}"),
    )

    return keyboard
