import os
import telebot
from telebot import types
from flask import Flask, request
import sqlite3

TOKEN = '5057433410:AAEldf2_IXqPOeh32iPT3L0zHLmjO7Xw8aU'
APP_URL = f'https://coffeefal.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_message(message):
    connect=sqlite3.connect('mess.db')
    cursor=connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXIST log_id(name TEXT PRIMARY KEY, time TEXT, msgtext TEXT)""")
    connect.commit()
    user_name = [message.from_user.first_name, message.date, message.text]
    cursor.execute("INSERT INTO log_id VALUES(?,?,?);", user_name)
    connect.commit()

    bot.send_message(message.chat.id, "Hello,️ " + message.from_user.first_name)

@bot.message_handler(commands=['readsql'])
def read_sql():
    return cursor.execute('SELECT * FROM log_id').fetchall()

@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text=='привет':
        bot.send_message(message.chat.id, 'привет!!!')
    else:
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
    server.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))