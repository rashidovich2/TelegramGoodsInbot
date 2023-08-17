# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.api_sqlite import get_paymentx


# Выбор способов пополнения
def refill_choice_finl():
    keyboard = InlineKeyboardMarkup()

    get_payments = get_paymentx()
    active_kb = []

    if get_payments['way_form'] == "True":
        active_kb.append(InlineKeyboardButton("📋 QIWI форма", callback_data="refill_choice:Form"))
    if get_payments['way_number'] == "True":
        active_kb.append(InlineKeyboardButton("📞 QIWI номер", callback_data="refill_choice:Number"))
    if get_payments['way_nickname'] == "True":
        active_kb.append(InlineKeyboardButton("Ⓜ QIWI никнейм", callback_data="refill_choice:Nickname"))

    if len(active_kb) == 3:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2])
    elif len(active_kb) == 2:
        keyboard.add(active_kb[0], active_kb[1])
    elif len(active_kb) == 1:
        keyboard.add(active_kb[0])
    else:
        keyboard = None

    if active_kb:
        keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩", callback_data="user_profile"))

    return keyboard

# Проверка киви платежа
def refill_bill_finl(send_requests, get_receipt, get_way):
    return (
        InlineKeyboardMarkup()
        .add(InlineKeyboardButton("🌀 Перейти к оплате", url=send_requests))
        .add(
            InlineKeyboardButton(
                "🔄 Проверить оплату",
                callback_data=f"Pay:{get_way}:{get_receipt}",
            )
        )
    )


# Кнопки при открытии самого товара
def products_open_finl(position_id, remover, category_id):
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                "💰 Купить товар",
                callback_data=f"buy_item_select:{position_id}",
            )
        )
        .add(
            InlineKeyboardButton(
                "⬅ Вернуться ↩",
                callback_data=f"buy_position_return:{remover}:{category_id}",
            )
        )
    )

# Способы пополнения
def payment_as_choice_finl():
    keyboard = InlineKeyboardMarkup()
    get_payments = get_paymentx()

    if get_payments['way_form'] == "True":
        status_form_kb = InlineKeyboardButton("✅", callback_data="change_payment:Form:False")
    else:
        status_form_kb = InlineKeyboardButton("❌", callback_data="change_payment:Form:True")

    if get_payments['way_number'] == "True":
        status_number_kb = InlineKeyboardButton("✅", callback_data="change_payment:Number:False")
    else:
        status_number_kb = InlineKeyboardButton("❌", callback_data="change_payment:Number:True")

    if get_payments['way_nickname'] == "True":
        status_nickname_kb = InlineKeyboardButton("✅", callback_data="change_payment:Nickname:False")
    else:
        status_nickname_kb = InlineKeyboardButton("❌", callback_data="change_payment:Nickname:True")

    keyboard.add(InlineKeyboardButton("📋 По форме", url="https://vk.cc/bYjKGM"), status_form_kb)
    keyboard.add(InlineKeyboardButton("📞 По номеру", url="https://vk.cc/bYjKEy"), status_number_kb)
    keyboard.add(InlineKeyboardButton("Ⓜ По никнейму", url="https://vk.cc/c8s66X"), status_nickname_kb)

    return keyboard

    

# Подтверждение покупки товара
def products_confirm_finl(position_id, get_count):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "✅ Подтвердить",
            callback_data=f"xbuy_item:yes:{position_id}:{get_count}",
        ),
        InlineKeyboardButton(
            "❌ Отменить",
            callback_data=f"xbuy_item:not:{position_id}:{get_count}",
        ),
    )


# Ссылка на поддержку
def user_support_finl(user_name):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "💌 Написать в поддержку", url=f"https://t.me/{user_name}"
        ),
    )
