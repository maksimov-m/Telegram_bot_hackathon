from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import db, bot
import keyboards.markups

async def stat(message : types.Message):
    res = db.get_user_ud()
    await bot.send_message(message.from_user.id, text=f'Людей которые когда либо заходили в бота: {len(res)}', reply_markup=keyboards.markups.mainMenu)



def register_handlers_stat(dp: Dispatcher):
    dp.register_message_handler(stat, commands=['statistics'], state=None)
    dp.register_message_handler(stat, Text(equals='Статистика', ignore_case=True), state=None)
    dp.register_message_handler(stat, Text(equals='отмена', ignore_case=True))
