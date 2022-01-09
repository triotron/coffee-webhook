
import string, json
from aiogram import types, Dispatcher
from flask import Flask, request
from create_bot import dp


#@dp.message_handler()
async def echo_send(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Мат запрещен')
        await message.delete()

def register_handler_others(dp : Dispatcher):
    dp.register_message_handler(echo_send)