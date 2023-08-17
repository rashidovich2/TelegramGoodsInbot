from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from tgbot.loader import dp

from tgbot.data.config import DEFAULT_LANGUAGE
from tgbot.services.location_stat import geo_choice
from tgbot.keyboards.location_keyboards import *
from tgbot.services.location_function import search_address, add_address, search_city, add_geocode, add_city, get_city, update_position_city
from tgbot.services.api_sqlite import get_userx
from tgbot.keyboards.reply_z_all import menu_frep


@dp.callback_query_handler(text="edit_location", state='*')
async def geo_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await geo_choice.location.set()
    await call.message.answer('Отправьте локацию или выберите город из списка', reply_markup=geo_11_kb())

# приём локации
@dp.message_handler(content_types=['location'], state=geo_choice.location)
async def geo_2(message: types.Message, state: FSMContext):
    await message.delete()
    lat = message.location.latitude
    long = message.location.longitude
    city = 0
    city = search_city(lat, long)
    lang = get_userx(user_id=message.from_user.id)['user_lang']

    print(lang, city)
    address = search_address(lat, long)
    add_geocode(lat, long, message.from_user.id)
    add_address(address, message.from_user.id)
    print("geo_choice:")

    if city == False:
        await message.answer('Ваш город не определён. Выберите город из списка', reply_markup=geo_3_kb())
    else:
        await message.answer(f'Ваш город: {city[0]}?', reply_markup=geo_2_kb(city[1], city[0]))


@dp.message_handler(text = "📋 Выбрать город из списка", state="*") #geo_choice.location
async def geo_3(message: types.Message, state: FSMContext):
    await message.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())


@dp.callback_query_handler(text_startswith = "geo_first_letter", state="*") #geo_choice.location
async def geo_4(call: types.CallbackQuery):
    city_letter = str(call.data).split(':')[1]
    await call.message.edit_text('Выберите город', reply_markup=geo_4_kb(city_letter))


@dp.callback_query_handler(text_startswith = "geo_chosen_cities", state="*") #geo_choice.location
async def geo_5(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    city_id = int(call.data.split(":")[1])
    city_name = call.data.split(":")[2]
    lang = DEFAULT_LANGUAGE
    print("IIII")

    user_id = call.from_user.id
    print(city_id, lang, user_id)
    add_city(city_id, city_name, user_id)
    await call.message.answer(f"🔸 Выбран город: {city_name}.\n"
                              "🔸 Бот готов к использованию.\n"
                              "🔸 Если не появились вспомогательные кнопки\n"
                              "Наберите /start",
                              reply_markup=menu_frep(user_id, lang))

# ==============================================================================================================
# ================================  Локация для позицци (для магазина в будующем)   =============================

# приём локации
@dp.message_handler(content_types=['location'], state='here_change_city')
async def geo_position_1(message: types.Message, state: FSMContext):
    await message.delete()
    lat = message.location.latitude
    long = message.location.longitude
    city = 0
    city = search_city(lat, long)
    #lang = get_userx(user_id=message.from_user.id)['user_lang']
    lang = DEFAULT_LANGUAGE
    print(lang, city)

    if city == False:
        await message.answer('Город не определён. Выберите город из списка', reply_markup=geo_3_kb())
    else:
        await state.update_data({'city': city[0], 'city_id': city[1]})
        await message.answer(f'Ваш город: {city[0]}?', reply_markup=geo_2_kb(city[1], city[0]))

# выбор буквы города при нажатии кнопки
@dp.message_handler(text = "📋 Выбрать из списка", state='here_change_city')
async def geo_3(message: types.Message, state: FSMContext):
    #lang = get_userx(user_id=message.from_user.id)['user_lang']
    #lang = DEFAULT_LANGUAGE
    await message.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())


# выбор буквы города при ошибке геокода
@dp.callback_query_handler(text_startswith='choice_city_list', state='here_change_city')
async def geo_position_2(call: types.CallbackQuery, state: FSMContext):
    #lang = get_userx(user_id=call.from_user.id)['user_lang']
    #lang = DEFAULT_LANGUAGE
    await call.message.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())


# выбор города по букве
@dp.callback_query_handler(text_startswith='geo_first_letter', state='here_change_city')
async def geo_4(call: types.CallbackQuery):
    letter = str(call.data).split(':')[1]
    print(letter)
    await call.message.edit_text('Выберите город', reply_markup=geo_4_kb(letter))

# приём локации
@dp.message_handler(content_types=['location'], state='here_change_city_artist')
async def geo_position_1(message: types.Message, state: FSMContext):
    await message.delete()
    lat = message.location.latitude
    long = message.location.longitude
    city = 0
    city = search_city(lat, long)
    lang = get_userx(user_id=message.from_user.id)['user_lang']
    if city == False:
        await message.answer('Город не определён. Выберите город из списка', reply_markup=geo_3_kb(lang))
    else:
        await state.update_data({'city': city[0], 'city_id': city[1]})
        await message.answer(f'Ваш город: {city[0]}?', reply_markup=geo_2_kb(city[1]))

# выбор буквы города при нажатии кнопки
@dp.message_handler(text = "📋 Выбрать из списка", state='here_change_city_artist')
async def geo_3(message: types.Message, state: FSMContext):
    #lang = get_userx(user_id=message.from_user.id)['user_lang']
    await message.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())

# выбор буквы города при ошибке геокода
@dp.callback_query_handler(text_startswith='choice_city_list', state='here_change_city_artist')
async def geo_position_2(call: types.CallbackQuery, state: FSMContext):
    lang = get_userx(user_id=message.from_user.id)['user_lang']
    await call.message.answer('Первая буква названия вашего города', reply_markup=geo_3_kb())

# выбор города по букве
@dp.callback_query_handler(text_startswith='geo_first_letter', state='here_change_city_artist')
async def geo_4(call: types.CallbackQuery):
    info = str(call.data).split(':')[1]
    await call.message.edit_text('Выберите город', reply_markup=geo_4_kb(info))