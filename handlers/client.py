from aiogram import types, Dispatcher
from create_bot import db

#@dp.message_handler(commands=['Account'])
async def commands_account(message: types.Message):
    await message.reply(db.get_name(message.from_user.id))


#@dp.message_handler(text=['text'])


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_account, commands=['myprofile'])
