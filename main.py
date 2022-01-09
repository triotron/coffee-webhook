import os
import telebot
from flask import Flask, request

TOKEN = '5084358491:AAElx-kTIpc7CAy_ocdgP8eis6ogJ7toLCc'
APP_URL = f'https://coffeefal.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello ,️ " + message.from_user.first_name)

@bot.message_handler(content_types=['text'])
def start_message(message):
  bot.send_message(message.chat.id, message.text)
#bot.infinity_poling()

@bot.message_handler(content='привет')
def hihi(message):
  bot.send_message(message.chat.id, 'привет')

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