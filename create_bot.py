from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from DataBase.db import Database



TOKEN = "5743429635:AAFcQlpWeAHdGRByCVuRJWCP7xNYQzxYsJ8"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('DataBase/database.db')