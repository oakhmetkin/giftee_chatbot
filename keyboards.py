from aiogram.types import *


# none keyboard
none = ReplyKeyboardRemove()


# start keyboard
start_buttons = [
    'Подобрать подарок',
]

start_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
for a in start_buttons:
    start_markup.add(a)


# check keyboard
check_buttons = [
    'OK',
    'Начать заново',
]

check_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
for a in check_buttons:
    check_markup.add(a)
