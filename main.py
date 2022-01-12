import os
import telebot
from telebot import types
from flask import Flask, request
import time
#import sqlite3

TOKEN = '5057433410:AAEldf2_IXqPOeh32iPT3L0zHLmjO7Xw8aU'
APP_URL = f'https://coffeefal.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
#    connect=sqlite3.connect('mess.db')
#    cursor=connect.cursor()
#    cursor.execute("""CREATE TABLE IF NOT EXIST log_id(name TEXT PRIMARY KEY, time TEXT, msgtext TEXT)""")
#    connect.commit()
#    user_name = [message.from_user.first_name, message.date, message.text]
#    cursor.execute("INSERT INTO log_id VALUES(?,?,?);", user_name)
#    connect.commit()

    markup_inline = types.InlineKeyboardMarkup()
    item_yes= types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no=types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    markup_inline.add(item_yes,  item_no)

    bot.send_message(message.chat.id, f'Привет,️ {message.from_user.first_name} \nХочешь узнать о себе больше?', reply_markup=markup_inline)

@bot.callback_query_handler(func = lambda call:True)
def answer(call):
    if call.data == 'yes':
        markup_reply=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id=types.KeyboardButton('Мой ID')
        item_username=types.KeyboardButton('Мой ник')

        markup_reply.add(item_id, item_username)
        bot.send_message(call.message.chat.id, 'Нажмите на одну из кнопок', reply_markup=markup_reply)
        #time.sleep(3)
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="тру-ту-ту")

        #bot.answer_inline_query(call.id)




    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Ну нет, так нет', reply_markup=telebot.types.ReplyKeyboardRemove())
        #bot.answer_inline_query(call.id)



@bot.message_handler(commands=['time'])
def whats_the_time(message):
    bot.send_message(message.chat.id, text='1')
    time.sleep(2)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="2")
    time.sleep(2)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="3")
    time.sleep(2)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="4")
    time.sleep(2)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="5")


@bot.message_handler(commands=['id'])
def whats_id(message):
    bot.reply_to(message, message.from_user.id)

#@bot.message_handler(commands=['readsql'])
#def read_sql():
#    return cursor.execute('SELECT * FROM log_id').fetchall()

@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == 'Мой ID':
        bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')
    elif message.text == 'Мой ник':
        bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower()=='привет':
        bot.send_message(message.chat.id, 'привет!!!')
    elif message.text == "мат":
        bot.delete_message(message.chat.id, message.message_id)
    else:
        #bot.edit_message_text(message.chat.id, message.text + ' так сказал - ' + message.from_user.first_name)
        bot.send_message(message.chat.id, message.text)


#bot.infinity_poling()

#@bot.message_handler(func=lambda message:True,content_types=['text'])
#def echo(message):
#    bot.send_message(message.chat.id, message.text)
    #bot.reply_to(message, message.text)

@server.route('/'+TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

    
@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200

if __name__ == '__main__':
    server.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))