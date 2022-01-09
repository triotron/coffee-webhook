# - *- coding: utf- 8 - *-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token

import os
storage=MemoryStorage()

bot = Bot(token=token)
#bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)