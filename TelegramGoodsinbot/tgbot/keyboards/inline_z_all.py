# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.api_sqlite import get_settingsx

settings = get_settingsx()
type_trade = settings['type_trade']
print(type_trade)

# Рассылка
ad_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Отправить", callback_data="confirm_ad:yes"),
    InlineKeyboardButton("❌ Отменить", callback_data="confirm_ad:not")
)

# Кнопки при поиске профиля через админ-меню
refill_open_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("💰 Пополнить", callback_data="user_refill")
)

# Кнопки при поиске профиля через админ-меню
profile_open_inl = InlineKeyboardMarkup(row_width=2
                                        ).add(
    InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
    InlineKeyboardButton("🎁 Мои покупки", callback_data="user_history")
)
if(type_trade != 'digital'):
    profile_open_inl = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
        InlineKeyboardButton("🎁 Мои покупки", callback_data="user_history"),
        #InlineKeyboardButton("📡 Изменить город", callback_data="edit_locatoin")
    )

give_number_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("Поделиться номером",
                         callback_data="enter_phone_auto_fin")
    #InlineKeyboardButton("Поделиться номером", request_contact=True)
)

# Удаление сообщения
close_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Закрыть", callback_data="close_this"),
)

# Открытие корзины
cart_open_created_inl = InlineKeyboardMarkup(
).add(
    # InlineKeyboardButton(
    #    "🏢 Ввести адрес", callback_data=f"enter_address_manualy"),
    # InlineKeyboardButton("📱 Ввести телефон",
    #                      callback_data=f"enter_phone_manualy"),
    InlineKeyboardButton(" ! Оформить заказ",
                         callback_data=f"checkout_start"),
).add(
    # InlineKeyboardButton("📱 Поделиться номером",
    #                      callback_data=f"enter_phone_auto"),
    InlineKeyboardButton("💰 Пополнить счет", callback_data=f"user_refill"),
    InlineKeyboardButton("❓ Спросить продавца",
                         callback_data=f"enter_message_manualy"),
).add(
    InlineKeyboardButton(" Удалить корзину",
                         callback_data=f"del_user_cart"),
)


cart_open_delivery_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("📱 Подтвердить получение",
                         callback_data=f"submit_order"),
).add(
    #    InlineKeyboardButton("📱 Открыть спор", callback_data=f"open_debate"),
    InlineKeyboardButton("❓ Задать вопрос продавцу",
                         callback_data=f"enter_message_manualy"),
)

# Удаление корзина
confirm_delete_user_cart_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить корзину",
                         callback_data="confirm_del_user_cart"),
    InlineKeyboardButton("✅ Нет, вернуться в корзину",
                         callback_data="user_cart")
)

######################################## ТОВАРЫ ########################################
# Удаление категорий
category_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все",
                         callback_data="confirm_remove_category:yes"),
    InlineKeyboardButton(
        "✅ Нет, отменить", callback_data="confirm_remove_category:not")
)

# Подтверждение полполнения счета
checkout_step2_accept = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Да, оформить", callback_data="checkout_finish"),
    InlineKeyboardButton("❌ Вернуться в Корзину", callback_data="user_cart")
)

# Подтверждение полполнения счета
order_user_refill = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Да, пополнить баланс",
                         callback_data="user_refill"),
    InlineKeyboardButton("❌ Вернуться в Корзину",
                         callback_data="user_cart")
)

# Удаление позиций
position_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все",
                         callback_data="confirm_remove_position:yes"),
    InlineKeyboardButton(
        "✅ Нет, отменить", callback_data="confirm_remove_position:not")
)

# Удаление товаров
item_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все",
                         callback_data="confirm_remove_item:yes"),
    InlineKeyboardButton(
        "✅ Нет, отменить", callback_data="confirm_remove_item:not")
)
