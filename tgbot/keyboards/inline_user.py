# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.api_sqlite import get_paymentx, get_upaymentx, get_upaycount, create_upayments_row


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
    if get_payments['way_formy'] == "True":
        active_kb.append(InlineKeyboardButton("📋 Yoo форма", callback_data="refill_choice:ForYm"))

    if len(active_kb) == 4:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
    elif len(active_kb) == 3:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2])
    elif len(active_kb) == 2:
        keyboard.add(active_kb[0], active_kb[1])
    elif len(active_kb) == 1:
        keyboard.add(active_kb[0])
    else:
        keyboard = None

    if len(active_kb) >= 1:
        keyboard.add(InlineKeyboardButton("⬅ Вернуться в профиль ↩", callback_data="user_profile"))
        keyboard.add(InlineKeyboardButton("⬅ Вернуться в корзину ↩", callback_data="user_cart"))

    return keyboard

# Проверка киви платежа
def refill_bill_finl(send_requests, get_receipt, get_way):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🌀 Перейти к оплате", url=send_requests)
    ).add(
        InlineKeyboardButton("🔄 Проверить оплату", callback_data=f"Pay:{get_way}:{get_receipt}")
    )

    return keyboard

# Поделиться телефоном
def give_number_inl():
    keyboard = InlineKeyboardMarkup(
    ).add(
        #InlineKeyboardButton("Поделиться номером", callback_data="enter_phone_auto")
        InlineKeyboardButton("Поделиться номером", request_contact=True)
    )

    return keyboard

# Кнопки при открытии самого товара
def products_open_finl2(position_id, remover, category_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_select:{position_id}")
    ).add(
        InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{category_id}")
    )

    return keyboard

# Кнопки при открытии самого товара
def shop_creation_request_finl():
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🏪 Создать магазин ➕", callback_data=f"product_shop_create")
    ).add(
        InlineKeyboardButton("Продолжить без создания магазина", callback_data=f"here_position_addtoshop:NoCreate")
    )

    return keyboard


# Кнопки при открытии самого товара c корзиной
def products_open_cart_finl2(position_id, remover, category_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_item_cart:{position_id}")
    ).add(
        InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{category_id}")
    )

    return keyboard

# Кнопки при открытии самого товара c корзиной
def products_open_finl(cart, position_id, remover, category_id, shop_id):
    if cart == 1 and category_id != 0:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_item_cart:{position_id}")
        ).add(
            InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{category_id}:{0}")
        )
    if cart == 1 and shop_id != 0:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_item_cart:{position_id}")
        ).add(
            InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{0}:{shop_id}")
        )
    if cart == 0 and category_id != 0:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_select:{position_id}")
        ).add(
            InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{category_id}:{0}")
        )
    if cart == 0 and shop_id != 0:
        keyboard = InlineKeyboardMarkup(
        ).add(
            InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_select:{position_id}")
        ).add(
            InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{0}:{shop_id}")
        )

    return keyboard

def switch_category_shop_finl():
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🛒 Переключиться в категории", callback_data=f"products_item_category_open_fp:{0}:{None}")
    ).add(
        InlineKeyboardButton("🛒 Переключиться в магазины", callback_data=f"products_item_shop_open_fp:{0}:{None}")
    ).add(
        InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_position_return:{remover}:{category_id}")
    )

    return keyboard


#).add(
#InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_select:{position_id}")

def charge_button_add(anull):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("💰 Пополнить", callback_data="user_refill")
    )

    return keyboard

# Способы пополнения
def payment_as_choice_finl(user_id):
    keyboard = InlineKeyboardMarkup()
    #get_payments = get_paymentx()
    print(user_id)
    print("inline_user")
    count = get_upaycount(user_id)
    print(count['paycount'])
    if count['paycount'] == 0:
        cur = create_upayments_row(user_id)
    else:
        get_payments = get_upaymentx(user_id)

    if get_payments['way_form'] == "True":
        status_form_kb = InlineKeyboardButton("✅", callback_data=f"change_payment:Form:False:{user_id}")
    else:
        status_form_kb = InlineKeyboardButton("❌", callback_data=f"change_payment:Number:False:{user_id}")

    if get_payments['way_number'] == "True":
        status_number_kb = InlineKeyboardButton("✅", callback_data=f"change_payment:Nickname:False:{user_id}")
    else:
        status_number_kb = InlineKeyboardButton("❌", callback_data=f"change_payment:ForYm:False:{user_id}")

    if get_payments['way_nickname'] == "True":
        status_nickname_kb = InlineKeyboardButton("✅", callback_data=f"change_payment:Form:True:{user_id}")
    else:
        status_nickname_kb = InlineKeyboardButton("❌", callback_data=f"change_payment:Number:True:{user_id}")

    if get_payments['way_formy'] == "True":
        status_formy_kb = InlineKeyboardButton("✅", callback_data=f"change_payment:Nickname:True:{user_id}")
    else:
        status_formy_kb = InlineKeyboardButton("❌", callback_data=f"change_payment:ForYm:True:{user_id}")

    keyboard.add(InlineKeyboardButton("📋 По форме", url="https://vk.cc/bYjKGM"), status_form_kb)
    keyboard.add(InlineKeyboardButton("📞 По номеру", url="https://vk.cc/bYjKEy"), status_number_kb)
    keyboard.add(InlineKeyboardButton("Ⓜ По никнейму", url="https://vk.cc/c8s66X"), status_nickname_kb)
    keyboard.add(InlineKeyboardButton("📋 По форме Yoo", url="https://vk.cc/bYjKGM"), status_formy_kb)

    return keyboard

# Удаление корзины
def confirm_user_cart(user_id, ):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"xaddcart_item:yes:{position_id}:{get_count}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"xaddcart_item:not:{position_id}:{get_count}")
    )

    return keyboard

# Подтверждение покупки товара
def products_addcart_confirm_finl(position_id, get_count):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"xaddcart_item:yes:{position_id}:{get_count}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"xaddcart_item:not:{position_id}:{get_count}")
    )

    return keyboard
    

# Подтверждение покупки товара
def products_confirm_finl(position_id, get_count):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"xbuy_item:yes:{position_id}:{get_count}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"xbuy_item:not:{position_id}:{get_count}")
    )

    return keyboard


# Подтверждение сохранения адреса доставки
def accept_saved_adr(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Да, оставить текущий адрес", callback_data=f"user_cart"),
        InlineKeyboardButton("❌ Ввести новый адрес", callback_data=f"enter_address_manualy:{user_id}")
    )

    return keyboard



def accept_saved_phone(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Да, оставить текущий номер", callback_data=f"user_cart"),
        InlineKeyboardButton("❌ Ввести новый номер", callback_data=f"enter_phone_manualy:{user_id}")
    )

    return keyboard

# Подтверждение отправки сообщения продавцом
def order_reply_message_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Вернуться в Корзину", callback_data=f"user_cart"),
        InlineKeyboardButton("❌ Ввести новое сообщение", callback_data=f"reply_toorder_message")
    )

    return keyboard

# Подтверждение отправки сообщения покупателем
def cart_enter_message_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Ответить на сообщение продавца", callback_data=f"enter_message_manualy"),
        InlineKeyboardButton("❌ Остановить сделку", callback_data=f"stop_sale_process")
    )

    return keyboard

# Ответ на сообщение продавца
def enter_cart_message_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Вернуться в Корзину", callback_data=f"user_cart"),
        InlineKeyboardButton("❌ Ввести новое сообщение", callback_data=f"enter_message_manualy")
    )

    return keyboard


# Ответ на сообщение покупателя
def reply_order_message_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Ответить на сообщение покупателя", callback_data=f"reply_toorder_message"),
        InlineKeyboardButton("❌ Остановить сделку", callback_data=f"stop_sale_process")
    )

    return keyboard

# Ссылка на поддержку
def user_support_finl(user_name):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("💌 Написать в поддержку", url=f"https://t.me/{user_name}"),
    )

    return keyboard
