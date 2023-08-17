# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.api_sqlite import get_settingsx
#from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR

settings = get_settingsx()
type_trade = settings['type_trade']
print(type_trade)

# Рассылка
ad_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Отправить", callback_data="confirm_ad:yes"),
    InlineKeyboardButton("❌ Отменить", callback_data="confirm_ad:not")
)

# Рассылка
ad_add_to_plan_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Включить", callback_data="plan_once_ad:yes"),
    InlineKeyboardButton("❌ Отправить только один раз", callback_data="plan_once_ad:not")
)

# Кнопки при поиске профиля через админ-меню
refill_open_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("💰 Пополнить", callback_data="user_refill")
)

partners_list_open_inl = InlineKeyboardMarkup(row_width=2
).add(
    InlineKeyboardButton("Обновить", callback_data="open_partners_list"),
    InlineKeyboardButton("Разместить ссылку в каталоге", callback_data="partner_submit")
)

# Кнопки при поиске профиля через админ-меню
profile_open_inl = (InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
    InlineKeyboardButton("🎁 Мои покупки", callback_data="user_history")
)
.add(
#    InlineKeyboardButton("💰 Адрес BTC BEP20", callback_data="change_bep20"),
    InlineKeyboardButton("💰 Адрес USDT TRC20", callback_data="change_trc20"),
)
)

if(type_trade != 'digital'):
    profile_open_inl = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
        InlineKeyboardButton("🎁 Мои покупки", callback_data="user_history"),
        InlineKeyboardButton("➰ Ввести промокод", callback_data="enter_promocode"),
        InlineKeyboardButton("📡 Изменить город", callback_data="edit_location"),
        InlineKeyboardButton("💰 Адрес BTC BEP20", callback_data="change_bep20"),
        InlineKeyboardButton("💰 Адрес TRC20", callback_data="change_trc20"),
    )

profile_seller_open_inl = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("💰 Пополнить", callback_data="user_refill"),
        InlineKeyboardButton("🎁 Мои покупки", callback_data="user_history"),
#        InlineKeyboardButton("➰ Ввести промокод", callback_data="enter_promocode"),
        InlineKeyboardButton("📡 Изменить город", callback_data="edit_location"),
#        InlineKeyboardButton("🚛 Изменить настройки доставки", callback_data="edit_delivery_settings"),
#        InlineKeyboardButton("💰 Адрес BTC BEP20", callback_data="change_bep20"),
        InlineKeyboardButton("💰 Адрес USDT TRC20", callback_data="change_trc20"),
    )

give_number_inl = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("Поделиться номером", callback_data="enter_phone_auto_fin")
    )

# Удаление сообщения
close_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Закрыть", callback_data="close_this"),
)

# Открытие корзины
cart_open_created_inl = InlineKeyboardMarkup(
    ).add(InlineKeyboardButton("🏢 Ввести адрес", callback_data="enter_address_manualy"),
        InlineKeyboardButton("📱 Ввести телефон", callback_data="enter_phone_manualy"),
        InlineKeyboardButton(" ! Оформить заказ", callback_data="checkout_start"),
    ).add(
        InlineKeyboardButton("📱 Поделиться номером", callback_data="enter_phone_auto" ),
        InlineKeyboardButton("💰 Пополнить счет", callback_data="user_refill"),
        InlineKeyboardButton("❓ Спросить продавца", callback_data="enter_message_manualy"),
    ).add(
        InlineKeyboardButton(" Удалить корзину", callback_data="del_user_cart")
    )


cart_open_delivery_inl = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("📱 Подтвердить получение", callback_data="submit_order"),
        InlineKeyboardButton("❓ Задать вопрос продавцу",callback_data="enter_message_manualy")
    )

# Удаление корзина
confirm_delete_user_cart_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить корзину", callback_data="confirm_del_user_cart"),
    InlineKeyboardButton("✅ Нет, вернуться в корзину", callback_data="user_cart")
)

######################################## ТОВАРЫ ########################################
# Удаление категорий
category_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_category:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_category:not")
)

# Подтверждение оформления заказа
checkout_step2_accept = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("✅ Да, оформить", callback_data="checkout_finish"),
    InlineKeyboardButton("❌ Вернуться в Корзину", callback_data="user_cart")
)

# Подтверждение полполнения счета
order_user_refill = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("✅ Да, пополнить баланс", callback_data="user_refill"),
        InlineKeyboardButton("❌ Вернуться в Корзину", callback_data="user_cart")
    )

# Удаление позиций
position_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_position:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_position:not")
)

partners_list_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("Психологическая помощь PsyBorBot", url="https://t.me/PsyBorBot")
).add(
    InlineKeyboardButton("Юридический сервис \"Спроси Юриста\"", url="https://t.me/SprosiYuristaRBot")
)

# Удаление товаров
item_remove_confirm_inl = InlineKeyboardMarkup(
).add(
    InlineKeyboardButton("❌ Да, удалить все", callback_data="confirm_remove_item:yes"),
    InlineKeyboardButton("✅ Нет, отменить", callback_data="confirm_remove_item:not")
)
