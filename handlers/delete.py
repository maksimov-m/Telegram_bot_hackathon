import types
from aiogram import types, Dispatcher
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from requests.auth import HTTPBasicAuth
import keyboards.markups
from create_bot import db, bot
import validate

class delete(StatesGroup):
    delete = State()


urlAdress = "https://norisapi.ru:12345/"
pasword = "rjvfy433"
login = "team1"


def cancelBookanappointment(id: str) -> str:
    servList = "cancelbookanappointment"
    print("delete get request to Server with url\"" + urlAdress + servList + "\"")
    response = requests.delete(url=(urlAdress + servList),
                               auth=HTTPBasicAuth(login, pasword),
                               verify=False,
                               json={"id": id})
    print(response.status_code)
    return response.text


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    btns = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in items:
        btns.add(KeyboardButton(i))
    row = [KeyboardButton(text=item) for item in items]
    return btns


async def cm_start(message: types.Message):
    print("--------")
    history = db.get_history(message.from_user.id)
    if len(history) != 0:
        try:

            await bot.send_message(message.from_user.id, text="Ваша история:")
            mass = []
            for i in history:
                if validate.isNextDate(i[5]):
                    await bot.send_message(message.from_user.id, text=f"ID записи: {i[2]}\n"
                                                                      f"Имя врача: {i[3]}\n"
                                                                      f"Наименование услуги {i[4]}\n"
                                                                      f"Дата: {i[5]}")
                    mass.append(i[2])

            if len(mass) != 0:
                await bot.send_message(message.from_user.id, text="Выберите историю, которую удалить",
                                       reply_markup=make_row_keyboard(mass))
                await delete.delete.set()
            else:
                await bot.send_message(message.from_user.id, text="Список пуст")
        except:
            await bot.send_message(message.from_user.id, text="Извините. Сервер не отвечает.",
                                   reply_markup=keyboards.markups.mainMenu)
    else:
        await bot.send_message(message.from_user.id, text="Список пуст", reply_markup=keyboards.markups.mainMenu)

async def delete_history(message: types.Message, state: FSMContext):
    try:
        r = cancelBookanappointment(message.text)
        print(r)
        await bot.send_message(message.from_user.id, text="Удаление прошло успешно", reply_markup=keyboards.markups.mainMenu)
        db.del_history(message.from_user.id, message.text)
    except:
        await bot.send_message(message.from_user.id, text="Произошла ошибка", reply_markup=keyboards.markups.mainMenu)

    await state.finish()


def register_handlers_del(dp: Dispatcher):
    dp.register_message_handler(cm_start, Text(equals='Отменить запись', ignore_case=True))
    dp.register_message_handler(delete_history, state=delete.delete)
