from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards.markups
import validate
from create_bot import db, bot, dp
from handlers.registration import cm_start
import requests
from requests.auth import HTTPBasicAuth

#@dp.message_handler(content_types=["text"])
from handlers.registration import register_handlers_reg

ADMIN = "821204845" #id_user  Админа


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объмект реплай-клавиатуры
    """
    btns = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in items:
        btns.add(KeyboardButton(i))
    row = [KeyboardButton(text=item) for item in items]
    return btns


async def admin_panel(message : types.Message):
    if str(message.from_user.id) != ADMIN:
        await bot.send_message(message.from_user.id, "Я не знаю такой команды.",
                               reply_markup=keyboards.markups.mainMenu)
    else:
        await bot.send_message(message.from_user.id, text="Добро пожаловать, админ!\nВыбери нужное действие:", reply_markup=keyboards.markups.adminMenu)


async def what_fun(message: types.Message):
    print(message.text)
    if message.chat.type == "private":
        if db.get_signup(message.from_user.id) == "done":
            if message.text == "Мой профиль":
                if db.get_sex(message.from_user.id) == "male":
                    sex = "муж"
                else:
                    sex = "жен"

                text = f"Имя: {db.get_name(message.from_user.id)}\n" \
                       f"Фамилия: {db.get_secondname(message.from_user.id)}\n" \
                       f"Отчество: {db.get_patronymic(message.from_user.id)}\n" \
                       f"Дата рождения: {db.get_birth_day(message.from_user.id)}\n" \
                       f"Пол: {sex}\n" \
                       f"Номер: {db.get_number(message.from_user.id)}\n"
                await bot.send_message(message.from_user.id, text)
            elif message.text == "Изменить информацию":
                db.set_signup(message.from_user.id, "change")
                await cm_start(message)
            elif message.text == "История записей":
                history = db.get_history(message.from_user.id)
                """keys = getServiceList()
                mass_usl = []
                doc = None
                usl = None
                date = None
                for i in history:
                    for j in keys:
                        if j['uid врача'] == i[3]:
                            doc = j['ФИО']"""
                if len(history) != 0:
                    count = 1
                    for i in history:

                        await bot.send_message(message.from_user.id, text=f"{count}.\n"
                                                                          f"Дата: {i[5]}\n"
                                                                          f"ФИО специалиста: {i[3]}\n"
                                                                          f"Наименование услуги: {i[4]}")
                        count += 1
                else:
                    await bot.send_message(message.from_user.id, text="Список пуст")
            elif message.text == "Актуальные записи":
                mass = db.get_history(message.from_user.id)
                if len(mass) != 0:
                    mass_res = []
                    for i in mass:
                        if validate.isNextDate(i[5]):
                            mass_res.append(i)

                    for i in mass_res:
                        await bot.send_message(message.from_user.id, text=f"Дата: {i[5]}\n"
                                                                          f"ФИО специалиста: {i[3]}\n"
                                                                          f"Услуга: {i[4]}")
                else:
                    await bot.send_message(message.from_user.id, text="Актуальных записей нет", reply_markup=keyboards.markups.mainMenu)
            elif message.text == "Часто задаваемые вопросы":
                mass = db.get_FAQ()
                count = 1
                for i in mass:
                    await bot.send_message(message.from_user.id, text=f"{count}.\n"
                                                                      f"{i[0]}:\n"
                                                                      f"{i[1]}")
                    count += 1
            elif message.text == "Полезные ссылки":
                await bot.send_message(message.from_user.id, text="Нажмите на интересующую ссылку", reply_markup=keyboards.markups.linkMenu)
            else:
                await bot.send_message(message.from_user.id, "Я не знаю такой команды.",
                                       reply_markup=keyboards.markups.mainMenu)

        elif db.get_signup(message.from_user.id) == "reg":
            await bot.send_message(message.from_user.id, text="Закончите регистрацию! (введите /start или /register)")




def register_handlers_others(dp : Dispatcher):
    dp.register_message_handler(admin_panel, commands=['admin'])
    dp.register_message_handler(what_fun)
