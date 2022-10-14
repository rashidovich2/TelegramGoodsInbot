# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Рассылка
mail_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Отправить", callback_data="confirm_mail:yes"),
    InlineKeyboardButton("❌ Отменить", callback_data="confirm_mail:not")
)

# Кнопки при поиске профиля через админ-меню
profile_open_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
    InlineKeyboardButton("🎁 Мои покупки", callback_data="user_history")
)

# Удаление сообщения
close_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Закрыть", callback_data="close_this"),
)

# Подтверждение покупки товара
cart_open_inl = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🏢 Ввести адрес доставки", callback_data=f"enter_address_manualy"),
        InlineKeyboardButton("📱 Ввести номер телефона", callback_data=f"enter_phone_manualy")
    ).add(
        InlineKeyboardButton("💰 Пополнить счет", callback_data=f"user_refill"),
        #InlineKeyboardButton("❓ Задать вопрос продавцу", callback_data=f"enter_message_manualy")
    )

######################################## ТОВАРЫ ########################################
# Удаление категорий
category_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_category:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_category:not")
)

# Удаление позиций
position_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_position:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_position:not")
)

# Удаление товаров
item_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_item:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_item:not")
)
