import aiogram.types
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os
TOKEN ='5084358491:AAElx-kTIpc7CAy_ocdgP8eis6ogJ7toLCc'
APP_URL= f'https://telegcoffee.herokuapp.com/{TOKEN}'
storage=MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)



