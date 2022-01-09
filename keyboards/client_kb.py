# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/День_выплаты')
b2 = KeyboardButton('/Последний_день_сдачи')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('Поделиться номером', request_contact=True)
b5 = KeyboardButton('Где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
#one_time_keyboard=True
kb_client.add(b1).insert(b2).insert(b3).row(b4, b5)
#kb_client.add(b1).add(b2).add(b3)
#kb_client.row(b1,b2,b3)