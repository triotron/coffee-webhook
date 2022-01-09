from aiogram.utils import executor
import os
from create_bot import dp
from data_base import sqlite_db

async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()

from handlers import client, admin, others

admin.register_handler_admin(dp)
client.register_handler_client(dp)
others.register_handler_others(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)