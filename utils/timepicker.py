import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram_timepicker.panel import FullTimePicker, full_timep_callback, full_timep_default, \
    HourTimePicker, hour_timep_callback, MinuteTimePicker, minute_timep_callback, \
    SecondTimePicker, second_timep_callback, \
    MinSecTimePicker, minsec_timep_callback, minsec_timep_default
from aiogram_timepicker import result, carousel, clock


# insert your telegram bot API key here
API_TOKEN = '6324003418:AAF3e_smE49fyIrnCuY_L_44syzb1Q7SrUs' or os.getenv('token')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, )
start_kb.row('Full TimePicker', 'Full Carousel TimePicker')
start_kb.row('Hour TimePicker', 'Minute Timepicker', 'Second Timepicker')
start_kb.row('Minute & Second')
start_kb.row('Clock Hour 1', 'Clock Hour 2', 'Clock Minutes', 'Clock Minutes 2')


# starting bot when user sends `/start` command, answering with inline timepicker
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.reply('Pick a timepicker', reply_markup=start_kb)


@dp.message_handler(Text(equals=['Full TimePicker'], ignore_case=True))
async def full_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await FullTimePicker().start_picker()
    )


# full timepicker usage
@dp.callback_query_handler(full_timep_callback.filter())
async def process_full_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await FullTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()


@dp.message_handler(Text(equals=['Hour TimePicker'], ignore_case=True))
async def hour_picker_handler(message: Message):
    await message.answer(
        "Please select a hour: ",
        reply_markup=await HourTimePicker().start_picker()
    )


@dp.callback_query_handler(hour_timep_callback.filter())
async def process_hour_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await HourTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.edit_text(
            f'You selected {r.hours}h.',
        )


@dp.message_handler(Text(equals=['Minute TimePicker'], ignore_case=True))
async def minute_picker_handler(message: Message):
    await message.answer(
        "Please select a minute: ",
        reply_markup=await MinuteTimePicker(5, group_inside_count=10).start_picker()
    )


@dp.callback_query_handler(minute_timep_callback.filter())
async def process_minute_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await MinuteTimePicker(2, group_inside_count=10).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.edit_text(
            f'You selected {r.minutes}m.',
        )


@dp.message_handler(Text(equals=['Second TimePicker'], ignore_case=True))
async def second_picker_handler(message: Message):
    await message.answer(
        "Please select a second: ",
        reply_markup=await SecondTimePicker(5, group_inside_count=10).start_picker()
    )


@dp.callback_query_handler(second_timep_callback.filter())
async def process_second_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await SecondTimePicker(5, group_inside_count=10).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.edit_text(
            f'You selected {r.seconds}s.',
        )


@dp.message_handler(Text(equals=['Minute & Second'], ignore_case=True))
async def second_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await MinSecTimePicker(5).start_picker()
    )


@dp.callback_query_handler(minsec_timep_callback.filter())
async def process_second_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await MinSecTimePicker(5).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.edit_text(
            'You selected {time}.'.format(time=r.time.strftime('%M:%S')),
        )


@dp.message_handler(Text(equals=['Full Carousel TimePicker'], ignore_case=True))
async def full2_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await carousel.FullTimePicker().start_picker()
    )


# carousel full timepicker usage
@dp.callback_query_handler(carousel.full_timep_callback.filter())
async def process_full2_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await carousel.FullTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()


@dp.message_handler(Text(equals=['Clock Hour 1'], ignore_case=True))
async def clock_hour_1_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await clock.single.c24.TimePicker(select_button_needed=True).start_picker(6)
    )


# clock hour 1st timepicker usage
@dp.callback_query_handler(clock.single.c24.timepicker_callback.filter())
async def process_clock_hour_1_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await clock.single.c24.TimePicker(
        select_button_needed=True).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()
    elif r.status == result.Status.CANCELED:
        await callback_query.message.delete()


@dp.message_handler(Text(equals=['Clock Hour 2'], ignore_case=True))
async def clock_hour_2_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await clock.single.c24_ts3.TimePicker(select_button_needed=True).start_picker(6)
    )


# clock hour 2nd timepicker usage
@dp.callback_query_handler(clock.single.c24_ts3.timepicker_callback.filter())
async def process_clock_hour_2_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await clock.single.c24_ts3.TimePicker(select_button_needed=True).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()
    elif r.status == result.Status.CANCELED:
        await callback_query.message.delete()


@dp.message_handler(Text(equals=['Clock Minutes'], ignore_case=True))
async def clock_minute_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await clock.single.c60_ts5.TimePicker(
            select_button_needed=True,
            cancel_button_needed=True,
        ).start_picker()
    )


# clock minute timepicker usage
@dp.callback_query_handler(clock.single.c60_ts5.timepicker_callback.filter())
async def process_clock_minute_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await clock.single.c60_ts5.TimePicker(
        select_button_needed=True,
        cancel_button_needed=True,
    ).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()
    elif r.status == result.Status.CANCELED:
        await callback_query.message.delete()

@dp.message_handler(Text(equals=['Clock Minutes 2'], ignore_case=True))
async def clock_minute_2_picker_handler(message: Message):
    await message.answer(
        "Please select a time: ",
        reply_markup=await clock.single.c60_ts3.TimePicker(
            select_button_needed=True,
            cancel_button_needed=True,
        ).start_picker()
    )


# clock minute 2nd timepicker usage
'''@dp.callback_query_handler(clock.single.c60_ts3.timepicker_callback.filter())
async def process_clock_minute_2_timepicker(callback_query: CallbackQuery, callback_data: dict):
    r = await clock.single.c60_ts3.TimePicker(
        select_button_needed=True,
        cancel_button_needed=True,
    ).process_selection(callback_query, callback_data)
    if r.selected:
        await callback_query.message.answer(
            f'You selected {r.time.strftime("%H:%M:%S")}',
            reply_markup=start_kb
        )
        await callback_query.message.delete_reply_markup()
    elif r.status == result.Status.CANCELED:
        await callback_query.message.delete()'''


if __name__ == '__main__':
    full_timep_default(
        # default labels
        label_up='⇪', label_down='⇓',
        hour_format='{0:02}h', minute_format='{0:02}m', second_format='{0:02}s'
    )
    minsec_timep_default(
        hour_format='{0:02}h', minute_format='{0:02}m', second_format='{0:02}s'
    )
    carousel.full_timep_default(
        hour_current_format='{0:02}h',
        minute_current_format='{0:02}m',
        second_current_format='{0:02}s',
    )
    clock.single.c24.utils.default(
        time_current_format='⦾',
    )
    executor.start_polling(dp, skip_updates=True)