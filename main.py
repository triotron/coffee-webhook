import os
import telebot
from telebot import types, custom_filters
from flask import Flask, request
import time, datetime
import string, json
import logging
import psycopg2


TOKEN = '5057433410:AAEldf2_IXqPOeh32iPT3L0zHLmjO7Xw8aU'
APP_URL = f'https://coffeefal.herokuapp.com/{TOKEN}'
DB_URI ='postgres://mpwjzqjhqkrpbj:4cd378ff533f757d8cec6810422ba6f29093418abd717d1bf85ff2e114985764@ec2-63-33-239-176.eu-west-1.compute.amazonaws.com:5432/dd7jqblphtggds'
bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

server = Flask(__name__)


@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.first_name

    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    markup_inline.add(item_yes,  item_no)

    #db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    #result = db_object.fetchone()


    #if not result:
    db_object.execute("INSERT INTO users(id, username, time, messages) VALUES (%s, %s, %s, %s)", (user_id, username, datetime.datetime.now(), message.text))
    db_connection.commit()

    bot.send_message(message.chat.id, f'Привет,️ {message.from_user.first_name} \nХочешь узнать о себе больше?', reply_markup=markup_inline)



@bot.callback_query_handler(func = lambda call:True)
def answer(call):
    if call.data == 'yes':
        markup_reply=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id=types.KeyboardButton('Мой ID')
        item_username=types.KeyboardButton('Мой ник')

        markup_reply.add(item_id, item_username)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ну что же, начнем!!!!")
        bot.send_message(call.message.chat.id, text='Нажмите на одну из кнопок', reply_markup=markup_reply)
        bot.answer_callback_query(call.id) #убираем загрузку

    elif call.data == 'no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Но почему!!!!")
        bot.send_message(call.message.chat.id, 'Ну нет, так нет', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.answer_callback_query(call.id)  #убираем загрузку


    user_id = message.from_user.id
    username = message.from_user.first_name
    db_object.execute("INSERT INTO users(id, username, time, messages) VALUES (%s, %s, %s, %s)", (user_id, username, datetime.datetime.now(), message.text))
    db_connection.commit()

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
    elif {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        bot.send_message(message.chat.id, 'Мат запрещен')
        bot.delete_message(message.chat.id, message.message_id)
#    elif message.text == "мат" or message.text == "мат мат" :
#        bot.delete_message(message.chat.id, message.message_id)
    else:
        bot.send_message(message.chat.id, message.text)

    user_id = message.from_user.id
    username = message.from_user.first_name
    db_object.execute("INSERT INTO users(id, username, time, messages) VALUES (%s, %s, %s, %s)", (user_id, username, datetime.datetime.now(), message.text))
    db_connection.commit()




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
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))