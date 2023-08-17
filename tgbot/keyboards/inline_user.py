# - *- coding: utf- 8 - *-
import gettext
from pathlib import Path
from contextvars import ContextVar

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.api_sqlite import get_paymentx, get_upaymentx, get_upaycount, create_upayments_row

from babel import Locale
from tgbot.data.config import get_admins, BOT_DESCRIPTION, I18N_DOMAIN, LOCALES_DIR

from tgbot.middlewares.i18n import I18nMiddleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

print(i18n)
_ = i18n.gettext

# Кнопки при поиске профиля через админ-меню
def refill_open_finl(lang):
    keyboard = InlineKeyboardMarkup()

    k1 = InlineKeyboardButton(_("💰 Пополнить", locale=lang), callback_data="user_refill")
    keyboard.insert(k1)

    return keyboard

def profile_open_finl(lang):
    print(lang)
    print("buyerway")
    keyboard = InlineKeyboardMarkup()
    if lang == "ru":
        print("rumenu")
        topupbtn = "💰 Пополнить"
        mybuyes = "🎁 Мои покупки"
        pcbtn = "➰ Ввести промокод"
        chcbtn = "📡 Изменить город"
    if lang == "en":
        print("engmenu")
        topupbtn = "💰 Top Up"
        mybuyes = "🎁 My Purchases"
        pcbtn = "➰ Enter Promocode"
        chcbtn = "📡 Change City"

    k1 = InlineKeyboardButton(topupbtn, callback_data="user_refill"),
    k2 = InlineKeyboardButton(mybuyes, callback_data="user_history"),
    k3 = InlineKeyboardButton(pcbtn, callback_data="enter_promocode"),
    k4 = InlineKeyboardButton(chcbtn, callback_data="edit_location")
    keyboard.insert(k1)
    keyboard.insert(k2)
    keyboard.insert(k3)
    keyboard.insert(k4)

    return keyboard

def profile_seller_open_finl(lang):
    print(lang)
    print("sellway")
    keyboard = InlineKeyboardMarkup()
    if lang == 'ru':
        print("rumenu")
        topupbtn = "💰 Пополнить"
        mybuyes = "🎁 Мои покупки"
        pcbtn = "➰ Ввести промокод"
        chcbtn = "📡 Изменить город"
        chsdbtn = "🚛 Изменить настройки доставки"
        print("rumenu2")
    if lang == 'en':
        print("engmenu")
        topupbtn = "💰 Top Up"
        mybuyes = "🎁 My Purchases"
        pcbtn = "➰ Enter Promocode"
        chcbtn = "📡 Change City"
        chsdbtn = "🚛 Change Delivery Settings"

    print("rumenu3")
    k1 = InlineKeyboardButton(topupbtn, callback_data="user_refill"),
    k2 = InlineKeyboardButton(mybuyes, callback_data="user_history"),
    k3 = InlineKeyboardButton(pcbtn, callback_data="enter_promocode"),
    k4 = InlineKeyboardButton(chcbtn, callback_data="edit_locatoin"),
    k5 = InlineKeyboardButton(chsdbtn, callback_data="edit_delivery_settings")
    keyboard.insert(k1)
    keyboard.insert(k2)
    keyboard.insert(k3)
    keyboard.insert(k4)
    keyboard.insert(k5)
    print("rumenu4")

    return keyboard

# Проверка киви платежа
def confirm_cart_del_finl(order_id):
    keyboard = InlineKeyboardMarkup()

    k1 = InlineKeyboardButton(_("Да, удалите", locale=lang), callback_data="confirm_del_user_cart:{order_id}")
    k2 = InlineKeyboardButton(_("Нет, вернуться в корзину", locale=lang), callback_data="user_cart")
    keyboard.insert(k1)
    keyboard.insert(k2)

    return keyboard

# Проверка киви платежа
def lang_menu_finl(lang):
    keyboard = InlineKeyboardMarkup()
    if lang == "ru":
        rubtn = "🇷🇺 Русский"
        enbtn = "🇬🇧 Английский"
    if lang == "en":
        rubtn = "🇷🇺 Russian"
        enbtn = "🇬🇧 English"

    k1 = InlineKeyboardButton(rubtn, callback_data="lang:ru")
    k2 = InlineKeyboardButton(enbtn, callback_data="lang:en")
    keyboard.insert(k1)
    keyboard.insert(k2)

    return keyboard

def lang_menu_ext_finl():
    keyboard = InlineKeyboardMarkup()

    k1 = InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru")
    k2 = InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")
    k3 = InlineKeyboardButton("Продолжить", callback_data="continue")
    keyboard.insert(k1)
    keyboard.insert(k2)
    keyboard.insert(k3)

    return keyboard

# Проверка киви платежа
def lang_menu_finl2():
    keyboard = InlineKeyboardMarkup()
    ak = [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")]
    ak.append(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    keyboard.add(ak[0], ak[1])

    return keyboard

# Выбор способов пополнения
def refill_choice_finl(lang): #lang
    keyboard = InlineKeyboardMarkup()

    #print(lang)
    print(":::")
    get_payments = get_paymentx()
    print(get_payments)

    #currencies = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'TON', 'BNB']
    currencies = ["USDT", "BUSD", "USDC", "BTC", "ETH", "TON", "BNB"]
    active_kb = []

    if get_payments['way_form'] == "True":
        active_kb.append(InlineKeyboardButton(_("📋 QIWI форма", locale=lang), callback_data="refill_choice:Form"))
    if get_payments['way_number'] == "True":
        active_kb.append(InlineKeyboardButton(_("📞 QIWI номер", locale=lang), callback_data="refill_choice:Number"))
    if get_payments['way_nickname'] == "True":
        active_kb.append(InlineKeyboardButton(_("Ⓜ QIWI никнейм", locale=lang), callback_data="refill_choice:Nickname"))
    if get_payments['way_formy'] == "True":
        active_kb.append(InlineKeyboardButton(_("📋 Yoo форма", locale=lang), callback_data="refill_choice:ForYm"))
    if get_payments['way_coinbase'] == "True":
        active_kb.append(InlineKeyboardButton("USDT", callback_data="refill_choice:Tron:USDT"))
        active_kb.append(InlineKeyboardButton("TRX", callback_data="refill_choice:Tron:TRX"))
        active_kb.append(InlineKeyboardButton("BTC BEP20", callback_data="refill_choice:BTCB"))

    if len(active_kb) == 9:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
        keyboard.add(active_kb[4], active_kb[5])
        keyboard.add(active_kb[6], active_kb[7])
        keyboard.add(active_kb[8])
    if len(active_kb) == 8:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
        keyboard.add(active_kb[4], active_kb[5])
        keyboard.add(active_kb[6], active_kb[7])
    if len(active_kb) == 7:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
        keyboard.add(active_kb[4], active_kb[5])
        keyboard.add(active_kb[6])
    if len(active_kb) == 6:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
        keyboard.add(active_kb[4], active_kb[5])
    if len(active_kb) == 5:
        keyboard.add(active_kb[0], active_kb[1])
        keyboard.add(active_kb[2], active_kb[3])
        keyboard.add(active_kb[4])
    elif len(active_kb) == 4:
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

    if active_kb:
        keyboard.add(InlineKeyboardButton("⬅ Вернуться в профиль ↩", callback_data="user_profile"))
        keyboard.add(InlineKeyboardButton("⬅ Вернуться в корзину ↩", callback_data="user_cart"))

    return keyboard


# Проверка киви платежа
def position_select_type_finl(lang):
    if lang == "ru":
        realbtn = "✅ Реальная"
        digibtn = "❌ Цифровая"
    if lang == "en":
        realbtn = "✅ Real"
        digibtn = "❌ Digital"

    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                realbtn,
                callback_data="here_position_type:real",
            )
        )
        .add(
            InlineKeyboardButton(
                digibtn,
                callback_data="here_position_type:digital",
            )
        )
    )


# Проверка киви платежа
def open_deep_link_object_finl(object_id, category_id, remover, city_id):
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                _("✅ Открыть", locale=lang),
                callback_data=f"buy_position_open:{object_id}:{category_id}:{remover}:{city_id}",
            )
        )
        .add(
            InlineKeyboardButton(
                _("❌ Стартовать магазин", locale=lang), callback_data="start"
            )
        )
    )

# Проверка киви платежа
def refill_bill_crypto_finl(get_way, type_net, receipt, lang):
    print(get_way, type_net, receipt, lang)
    return (InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                _("🔄 Проверить оплату", locale=lang), callback_data=f"Pay:{get_way}:{type_net}:{receipt}",
            )
        )
    )



# Проверка киви платежа
def refill_bill_finl(send_requests, get_receipt, get_way, lang):
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                _("🌀 Перейти к оплате", locale=lang), url=send_requests
            )
        )
        .add(
            InlineKeyboardButton(
                _("🔄 Проверить оплату", locale=lang),
                callback_data=f"Pay:{get_way}:{get_receipt}",
            )
        )
    )

# Поделиться телефоном
def give_number_inl():
    return InlineKeyboardMarkup().add(
        # InlineKeyboardButton("Поделиться номером", callback_data="enter_phone_auto")
        InlineKeyboardButton(
            _("Поделиться номером", locale=lang), request_contact=True
        )
    )

# Кнопки при открытии самого товара
def event_open_finl(event_id, remover, place_id, city_id, lang):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton(_("💰 Забронировать столик", locale=lang), callback_data=f"book_event_ticket:{event_id}")
    )
    if place_id != 0:
        keyboard.add(
        InlineKeyboardButton(_("⬅ Вернуться в место ↩", locale=lang), callback_data=f"book_place_open:{place_id}")     #callback_data=f"events_place_swipe:{remover}:{place_id}:{city_id}")
        )
    if city_id != 0:
        keyboard.add(
        InlineKeyboardButton(_("⬅ Вернуться в город ↩", locale=lang), callback_data=f"events_city_swipe:{remover}:{city_id}")
        )

    return keyboard

# Кнопки при открытии самого товара
def shop_creation_request_finl(lang):
    if lang == "ru":
        csbtn = "🏪 Создать магазин ➕"
        wscbtn = "Продолжить без создания магазина"
    if lang == "en":
        csbtn = "🏪 Create shop ➕"
        wscbtn = "Continue without shop creation"

    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                csbtn, callback_data="product_shop_create"
            )
        )
        .add(
            InlineKeyboardButton(
                wscbtn,
                callback_data="here_position_addtoshop:NoCreate",
            )
        )
    )

# Кнопки при открытии самого товара
def edit_delivery_settings_finl():
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                _("⬅ Вернуться в профиль ↩", locale=lang),
                callback_data="user_profile",
            )
        )
        .add(
            InlineKeyboardButton(
                _("⬅ Ввести данные заново ↩", locale=lang),
                callback_data="edit_delivery_settings",
            )
        )
    )


# Кнопки при открытии самого товара c корзиной
def products_open_cart_finl2(position_id, remover, category_id):
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                _("🛒 Добавить в корзину", locale=lang),
                callback_data=f"add_item_cart:{position_id}",
            )
        )
        .add(
            InlineKeyboardButton(
                _("⬅ Вернуться ↩", locale=lang),
                callback_data=f"buy_position_return:{remover}:{category_id}",
            )
        )
    )

# Кнопки при открытии самого товара c корзиной
def products_open_finl(cart, position_id, remover, category_id, shop_id, lang):
    if lang == "ru":
        acbtn = "🛒 Добавить в корзину"
        bpbtn = "💰 Купить товар"
        bbtn = "⬅ Вернуться ↩"
    if lang == "en":
        acbtn = "🛒 Add to Cart"
        bpbtn = "💰 Buy Product"
        bbtn = "⬅ Back ↩"

    if cart == 1 and category_id != 0:
        keyboard = (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    acbtn,
                    callback_data=f"add_item_cart:{position_id}",
                )
            )
            .add(
                InlineKeyboardButton(
                    bbtn,
                    callback_data=f"buy_position_return:{remover}:{category_id}:0",
                )
            )
        )

    if cart == 1 and shop_id != 0:
        keyboard = (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    acbtn,
                    callback_data=f"add_item_cart:{position_id}",
                )
            )
            .add(
                InlineKeyboardButton(
                    bbtn,
                    callback_data=f"buy_position_return:{remover}:0:{shop_id}",
                )
            )
        )
    if cart == 0 and category_id != 0:
        keyboard = (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    bpbtn,
                    callback_data=f"buy_item_select:{position_id}",
                )
            )
            .add(
                InlineKeyboardButton(
                    bbtn,
                    callback_data=f"buy_position_return:{remover}:{category_id}:0",
                )
            )
        )
    if cart == 0 and shop_id != 0:
        keyboard = (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    bpbtn,
                    callback_data=f"buy_item_select:{position_id}",
                )
            )
            .add(
                InlineKeyboardButton(
                    bbtn,
                    callback_data=f"buy_position_return:{remover}:0:{shop_id}",
                )
            )
        )

    return keyboard

def switch_category_shop_finl():
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                _("🛒 Переключиться в категории", locale=lang),
                callback_data='products_item_category_open_fp:0:None',
            )
        )
        .add(
            InlineKeyboardButton(
                _("🛒 Переключиться в магазины", locale=lang),
                callback_data='products_item_shop_open_fp:0:None',
            )
        )
        .add(
            InlineKeyboardButton(
                _("⬅ Вернуться ↩", locale=lang),
                callback_data=f"buy_position_return:{remover}:{category_id}",
            )
        )
    )


# Возврат в профиль
def back_to_profile_finl(lang):
    return (
        InlineKeyboardMarkup()
            .add(
            InlineKeyboardButton(
                _("🌀 Вернуться в профиль", locale=lang),
                callback_data="user_profile",
            )
        )
    )

# Проверка киви платежа
def enter_promocode_finl():
    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(
                _("🌀 Вернуться в профиль", locale=lang),
                callback_data="user_profile",
            )
        )
        .add(
            InlineKeyboardButton(
                _("🔄 Повторить ввод промокода", locale=lang),
                callback_data="enter_promocode",
            )
        )
    )

#).add(
#InlineKeyboardButton("💰 Купить товар", callback_data=f"buy_item_select:{position_id}")

def charge_button_add(anull):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("💰 Пополнить", locale=lang), callback_data="user_refill"
        )
    )

#просмотр корзины
# Открытие корзины
def cart_open_created_finl(order_id, lang):
    print(lang)
    print(":::")
    if lang == "ru":
        enad = "🏢 Ввести адрес"
        entph = "📱 Ввести телефон"
        shtph = "📱 Поделиться номером"
        pap = "   Оплата при получении"
        pthacc = "💰 Пополнить счет"
        doord = f" ! Оформить заказ{order_id}"
        delcart = "   Удалить корзину"
        askseller = "❓ Спросить продавца"
    if lang == "en":
        enad = "🏢 Enter address"
        entph = "📱 Enter phone"
        shtph = "📱 Share phone"
        pap = "   Pay after get"
        pthacc = "💰 Charge account"
        doord = f" ! Make order: {order_id}"
        delcart = "   Delete cart"
        askseller = "❓ Ask seller"

    return (
        InlineKeyboardMarkup()
        .add(
            InlineKeyboardButton(enad, callback_data="enter_address_manualy"),
            InlineKeyboardButton(entph, callback_data="enter_phone_manualy"),
            InlineKeyboardButton(shtph, callback_data="enter_phone_auto"),
        )
        .add(
            InlineKeyboardButton(pap, callback_data=f"pay_after_delivery:{order_id}"),
            InlineKeyboardButton(pthacc, callback_data="user_refill"),
            InlineKeyboardButton(doord, callback_data=f"checkout_start:{order_id}"),
        )
        .add(
            InlineKeyboardButton(delcart, callback_data=f"del_user_cart:{order_id}"),
            InlineKeyboardButton(askseller, callback_data="enter_message_manualy"),
        )
    )


# Подтверждение оформления заказа
def checkout_step2_accept_finl(order_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Да, оформить", locale=lang),
            callback_data=f"checkout_finish:{order_id}",
        ),
        InlineKeyboardButton(
            _("❌ Вернуться в Корзину", locale=lang), callback_data="user_cart"
        ),
    )

#корзина - заказ в статусе доставка
def cart_open_delivery_finl(order_id, lang):
    print(lang)
    print("III")
    if lang == "ru":
        subm = "📱 Подтвердить получение"
        askseller = "❓ Задать вопрос продавцу"
    if lang == "en":
        subm = "📱 Submit Receiption"
        askseller = "❓ Ask Seller"

    return (
        InlineKeyboardMarkup()
        .add(InlineKeyboardButton(subm, callback_data=f"submit_order:{order_id}"),)
        .add(InlineKeyboardButton(askseller, callback_data="enter_message_manualy"),)
    )

# Корзина - заказ для администратора площадки
def cart_open_admin_finl(order_id, lang):
    print(lang)
    if lang == "ru":
        enad = "🏢 Ввести адрес"
        entph = "📱 Ввести телефон"
        shtph = "📱 Поделиться номером"
        pap = "   Оплата при получении"
        pthacc = "💰 Пополнить счет"
        doord = f" ! Оформить заказ{order_id}"
        delcart = "   Удалить корзину"
        askseller = "❓ Спросить продавца"
    if lang == "en":
        enad = "🏢 Enter address"
        entph = "📱 Enter phone"
        shtph = "📱 Share phone"
        pap = "   Pay after get"
        pthacc = "💰 Charge account"
        doord = f" ! Make order: {order_id}"
        delcart = "   Delete cart"
        askseller = "❓ Ask seller"

    return (
        InlineKeyboardMarkup()
            .add(
            InlineKeyboardButton(enad, callback_data="enter_address_manualy"),
            InlineKeyboardButton(entph, callback_data="enter_phone_manualy"),
            InlineKeyboardButton(shtph, callback_data="enter_phone_auto"),
        )
            .add(
            InlineKeyboardButton(pap, callback_data=f"pay_after_delivery:{order_id}"),
            InlineKeyboardButton(pthacc, callback_data="user_refill"),
            InlineKeyboardButton(doord, callback_data=f"checkout_start:{order_id}"),
        )
            .add(
            InlineKeyboardButton(delcart, callback_data=f"del_user_cart:{order_id}"),
            InlineKeyboardButton(askseller, callback_data="enter_message_manualy"),
        )
    )


# Способы пополнения
def payment_as_choice_finl(user_id):
    keyboard = InlineKeyboardMarkup()
    print("|||||")
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

    keyboard.add(InlineKeyboardButton(_("📋 По форме", locale=lang), url="https://vk.cc/bYjKGM"), status_form_kb)
    keyboard.add(InlineKeyboardButton(_("📞 По номеру", locale=lang), url="https://vk.cc/bYjKEy"), status_number_kb)
    keyboard.add(InlineKeyboardButton(_("Ⓜ По никнейму", locale=lang), url="https://vk.cc/c8s66X"), status_nickname_kb)
    keyboard.add(InlineKeyboardButton(_("📋 По форме Yoo", locale=lang), url="https://vk.cc/bYjKGM"), status_formy_kb)

    return keyboard

# Удаление корзины
def confirm_user_cart(user_id, ):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Подтвердить", locale=lang),
            callback_data=f"xaddcart_item:yes:{position_id}:{get_count}",
        ),
        InlineKeyboardButton(
            _("❌ Отменить", locale=lang),
            callback_data=f"xaddcart_item:not:{position_id}:{get_count}",
        ),
    )

# Подтверждение покупки товара
def products_addcart_confirm_finl(position_id, get_count, lang):
    if lang == "ru":
        sbmbtn = "✅ Подтвердить"
        clbtn = "❌ Отменить"
    if lang == "en":
        sbmbtn = "✅ Submit"
        clbtn = "❌ Cancel"
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            sbmbtn,
            callback_data=f"xaddcart_item:yes:{position_id}:{get_count}:{lang}",
        ),
        InlineKeyboardButton(
            clbtn,
            callback_data=f"xaddcart_item:not:{position_id}:{get_count}:{lang}",
        ),
    )

# Подтверждение покупки товара
def products_confirm_finl(position_id, get_count):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Подтвердить", locale=lang),
            callback_data=f"xbuy_item:yes:{position_id}:{get_count}",
        ),
        InlineKeyboardButton(
            _("❌ Отменить", locale=lang),
            callback_data=f"xbuy_item:not:{position_id}:{get_count}",
        ),
    )


# Подтверждение покупки товара
def products_confirm_finl(position_id, get_count):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Подтвердить", locale=lang),
            callback_data=f"xbuy_item:yes:{position_id}:{get_count}",
        ),
        InlineKeyboardButton(
            _("❌ Отменить", locale=lang),
            callback_data=f"xbuy_item:not:{position_id}:{get_count}",
        ),
    )


# Подтверждение сохранения адреса доставки
def accept_saved_adr(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Да, оставить текущий адрес", locale=lang),
            callback_data="user_cart",
        ),
        InlineKeyboardButton(
            _("❌ Ввести новый адрес", locale=lang),
            callback_data=f"enter_address_manualy:{user_id}",
        ),
    )



def accept_saved_phone(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Да, оставить текущий номер", locale=lang),
            callback_data="user_cart",
        ),
        InlineKeyboardButton(
            _("❌ Ввести новый номер", locale=lang),
            callback_data=f"enter_phone_manualy:{user_id}",
        ),
    )

# Подтверждение отправки сообщения продавцом
def order_reply_message_finl(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Вернуться в Корзину", locale=lang), callback_data="user_cart"
        ),
        InlineKeyboardButton(
            _("❌ Ввести новое сообщение", locale=lang),
            callback_data="reply_toorder_message",
        ),
    )

# Подтверждение отправки сообщения покупателем
def cart_enter_message_finl(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Ответить на сообщение", locale=lang),
            callback_data="enter_message_manualy",
        ),
        InlineKeyboardButton(
            _("❌ Остановить сделку", locale=lang),
            callback_data="stop_sale_process",
        ),
    )

# Ответ на сообщение продавца
def enter_cart_message_finl(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Вернуться в Корзину", locale=lang), callback_data="user_cart"
        ),
        InlineKeyboardButton(
            _("❌ Ввести новое сообщение", locale=lang),
            callback_data="enter_message_manualy",
        ),
    )


# Ответ на сообщение покупателя
def reply_order_message_finl(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("✅ Ответить на сообщение покупателя", locale=lang),
            callback_data="reply_toorder_message",
        ),
        InlineKeyboardButton(
            _("❌ Остановить сделку", locale=lang),
            callback_data="stop_sale_process",
        ),
    )

# Ссылка на поддержку
def user_support_finl(user_name):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            _("💌 Написать в поддержку", locale=lang),
            url=f"https://t.me/{user_name}",
        ),
    )
