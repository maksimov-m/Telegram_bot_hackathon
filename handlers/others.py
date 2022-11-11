from aiogram import types, Dispatcher
import keyboards.markups
from create_bot import db, bot, dp
from handlers.registration import cm_start
import requests
from requests.auth import HTTPBasicAuth

#@dp.message_handler(content_types=["text"])
from handlers.registration import register_handlers_reg

async def what_fun(message: types.Message):
    print(message.text)
    if message.chat.type == "private":
        if message.text == "Account":
            text = f"Имя: {db.get_name(message.from_user.id)}\n" \
                   f"Фамилия: {db.get_secondname(message.from_user.id)}\n" \
                   f"Отчество: {db.get_patronymic(message.from_user.id)}\n" \
                   f"Дата рождения: {db.get_birth_day(message.from_user.id)}\n" \
                   f"Пол: {db.get_sex(message.from_user.id)}\n" \
                   f"Номер: {db.get_number(message.from_user.id)}\n"
            await bot.send_message(message.from_user.id, text)
        elif message.text == "Change info":
            db.set_signup(message.from_user.id, "change")
            await cm_start(message)
        else:
            await bot.send_message(message.from_user.id, "What?", reply_markup=keyboards.markups.mainMenu)



def register_handlers_others(dp : Dispatcher):
    dp.register_message_handler(what_fun)