import os
import telebot
from telebot import types, custom_filters
from flask import Flask, request
import time
import string, json
import sqlite3

TOKEN = '5057433410:AAEldf2_IXqPOeh32iPT3L0zHLmjO7Xw8aU'
APP_URL = f'https://coffeefal.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

class FSMAdmin:
    photo = 1
    name = 2
    description = 3
    price = 4
#State()

@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    #######################################
    connect = sqlite3.connect('coffeeFaL.db')
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS menu (img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)")
    connect.commit()
    ######################################


    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    markup_inline.add(item_yes,  item_no)

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


################################################################################
@bot.message_handler(commands=['load'])
def add_new(message):
    bot.set_state(message.from_user.id, FSMAdmin.photo)
    bot.send_message(message.chat.id, 'Загрузить фото')

@bot.message_handler(state=FSMAdmin.photo)
def load_photo(message):
    bot.send_message(message.chat.id, f'Теперь введите название')
    bot.set_state(message.chat.id, FSMAdmin.name)
    with bot.retrieve_data(message.from_user.id) as data:
        data['photo'] = message.text

@bot.message_handler(state=FSMAdmin.name)
def load_name(message):
    bot.send_message(message.chat.id, f'Теперь введите описание')
    bot.set_state(message.chat.id, FSMAdmin.description)
    with bot.retrieve_data(message.from_user.id) as data:
        data['name'] = message.text

@bot.message_handler(state=FSMAdmin.description)
def load_description(message):
    bot.send_message(message.chat.id, f'Теперь введите цену')
    bot.set_state(message.chat.id, FSMAdmin.price)
    with bot.retrieve_data(message.from_user.id) as data:
        data['description'] = message.text

@bot.message_handler(state=FSMAdmin.price, is_digit=True)
def load_price(message):
    bot.send_message(message.chat.id, f'Все данные внесены')
    with bot.retrieve_data(message.from_user.id) as data:
        data['price'] = message.text
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(message.chat.id,
                         "Ready, take a look:\n<b>photo: {photo}\nname: {name}\ndescription: {description}\nprice: {price}</b>".format(
                             photo=data['photo'], name=data['name'], description=data['description'], price=['price']), parse_mode="html")

    cursor.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
    connect.commit()
    state.finish()

@bot.message_handler(commands=['menu'])
def sql_read(message):
    for ret in cursor.execute('SELECT * FROM menu').fetchall():
        bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание:{ret[2]}\nЦена:{ret[-1]}')
######################################################################################



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