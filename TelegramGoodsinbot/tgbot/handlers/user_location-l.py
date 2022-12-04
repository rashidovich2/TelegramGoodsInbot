from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from tgbot.loader import dp


from tgbot.services.location_stat import geo_choice
from tgbot.keyboards.location_keyboards import *
from tgbot.services.location_function import search_city, add_geocode, add_city, get_city, update_position_city

from tgbot.keyboards.reply_z_all import menu_frep


@dp.callback_query_handler(lambda cb: cb.data == 'edit_locatoin', state='*')
async def geo_1(cb: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await geo_choice.location.set()
    await cb.message.answer('Отправте локациюили выбирите город из списка', reply_markup=geo_11_kb())

# приём локации


@dp.message_handler(content_types=['location'], state=geo_choice.location)
async def geo_2(msg: types.Message, state: FSMContext):
    await msg.delete()
    lat = msg.location.latitude
    long = msg.location.longitude
    city = search_city(lat, long)[0]
    add_geocode(lat, long, msg.from_user.id)
    if city == False:
        await msg.answer('Ваш город не определён. Выберите город из списка', reply_markup=geo_3_kb())
    else:
        await msg.answer(f'Ваш город: {city}?', reply_markup=geo_2_kb(city))


@dp.message_handler(lambda msg: msg.text == '📋 Выбрать из списка', state=geo_choice.location)
async def geo_3(msg: types.Message, state: FSMContext):
    await msg.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())


@dp.callback_query_handler(lambda cb: cb.data[:16] == 'geo_first_letter', state=geo_choice.location)
async def geo_4(cb: types.CallbackQuery):
    info = str(cb.data).split('#')[1]
    await cb.message.edit_text('Выберите город', reply_markup=geo_4_kb(info))


@dp.callback_query_handler(lambda cb: cb.data[:17] == 'geo_chosen_cities', state=geo_choice.location)
async def geo_5(cb: types.CallbackQuery, state: FSMContext):
    await state.finish()
    info = str(cb.data).split('#')[1]
    if len(info) < 4:
        id = info
        info = get_city(id, cb.from_user.id)
    add_city(info[0], cb.from_user.id, info[3])
    await cb.message.answer("🔸 Покупай, продавай, арендуй игры из Steam по самой низкой цене.\n"
                            "🔸 Если не появились вспомогательные кнопки\n"
                            "▶ Введите /start",
                            reply_markup=menu_frep(cb.from_user.id))


# ==============================================================================================================
# ================================  Локация для позицци (для магазина в будующем)   =============================


# приём локации
@dp.message_handler(content_types=['location'], state='here_change_city')
async def geo_position_1(msg: types.Message, state: FSMContext):
    await msg.delete()
    lat = msg.location.latitude
    long = msg.location.longitude
    city = search_city(lat, long)
    if city == False:
        await msg.answer('Город не определён. Выберите город из списка', reply_markup=geo_3_kb())
    else:
        await state.update_data({'city': city[0], 'city_id': city[1]})
        await msg.answer(f'Ваш город: {city[0]}?', reply_markup=geo_2_kb(0))

# выбор буквы города при нажатии кнопки


@dp.message_handler(lambda msg: msg.text == '📋 Выбрать из списка', state='here_change_city')
async def geo_3(msg: types.Message, state: FSMContext):
    await msg.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())


# выбор буквы города при ошибке геокода
@dp.callback_query_handler(text_startswith='choice_city_list', state='here_change_city')
async def geo_position_2(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())


# выбор города по букве
@dp.callback_query_handler(text_startswith='geo_first_letter', state='here_change_city')
async def geo_4(cb: types.CallbackQuery):
    info = str(cb.data).split('#')[1]
    await cb.message.edit_text('Выберите город', reply_markup=geo_4_kb(info))
