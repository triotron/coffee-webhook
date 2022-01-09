from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую, я бот-ГСМ', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\n https://t.me/Coffee_FaLbot')


#@dp.message_handler(commands=['День_выплаты'])
async def command_payday(message : types.Message):
    await bot.send_message(message.from_user.id, 'Последний день выплаты в этом месяце', reply_markup = ReplyKeyboardRemove())


#@dp.message_handler(commands=['Последний_день_сдачи'])
async def command_lastday(message : types.Message):
    await bot.send_message(message.from_user.id, 'Последний день сдачи в этом месяце', reply_markup = ReplyKeyboardRemove())


#dp.message_handler(commands=['Меню'])
async def command_menu(message: types.Message):
    await sqlite_db.sql_read(message)

#    for ret in cur.execute('SELECT * FROM menu').fetchall():
#       await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена:{ret[-1]}')



def register_handler_client(dp : Dispatcher):

    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_payday, commands=['День_выплаты'])
    dp.register_message_handler(command_lastday, commands=['Последний_день_сдачи'])
    dp.register_message_handler(command_menu, commands=['Меню'])

