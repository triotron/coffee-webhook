# - *- coding: utf- 8 - *-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

answ =dict()

urlkb = InlineKeyboardMarkup(row_width=2)
urlButton = InlineKeyboardButton(text='Ссылка', url='http://www.youtube.com')
urlButton2 = InlineKeyboardButton(text='Ссылка 2', url ='http://www.google.com')
x = InlineKeyboardButton(text='Ссылка 3', url='http://www.youtube.com'), InlineKeyboardButton(text='Ссылка 4', url ='http://www.google.com'),\
    InlineKeyboardButton(text='Ссылка 5', url ='http://www.google.com')
urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Ссылка 6', url ='http://www.google.com'))

@dp.message_handler(commands='ссылки')
async def url_command(messange : types.Message):
    await messange.answer('Ссылки:', reply_markup=urlkb)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Like', callback_data='like_1'),
                                             InlineKeyboardButton(text='DisLike', callback_data='like_-1'))

@dp.message_handler(commands='test')
async def url_command(messange : types.Message):
    await messange.answer('За бота', reply_markup=inkb)

@dp.callback_query_handler(Text(startswith='like_'))
async def www_call(callback : types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('Вы проголосовали')
    else:
        await callback.answer('Вы уже проголосовали', show_alert=True)

    #await callback.answer('Вы проголосовали')
    #await callback.answer('Нажата кнопка', show_alert=True)
    #await callback.message.answer('Нажата кнопка')
    #await callback.answer()

executor.start_polling(dp, skip_updates=True)

