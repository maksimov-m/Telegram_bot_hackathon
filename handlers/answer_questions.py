from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import keyboards.markups
from create_bot import bot, db

class answer(StatesGroup):
    select_answer = State()
    send_answer = State()

dict_q = {}
mass_id = []
mass_user_id = []
mass_answ = []
res_id_db = 0
res_id_userId = 0

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


async def cm_start(message : types.Message):
    global dict_q, mass_id, mass_user_id, mass_answ
    res = db.get_questions()
    if len(res) == 0:
        await bot.send_message(message.from_user.id, text="Пока вопросов нет.", reply_markup=keyboards.markups.mainMenu)
    else:
        flag = True
        for i in res:
            if i[4] == "waiting":
                flag = False
                break
        if not flag:
            await answer.select_answer.set()
            count = 1
            await bot.send_message(message.from_user.id, text="Список вопросов:")
            mass_it = []
            for i in res:
                if i[4] == "waiting":
                    await bot.send_message(message.from_user.id, text=f"{count}\n"
                                                                      f"ID пользователя: {i[1]}\n"
                                                                      f"Вопрос: {i[2]}")

                    dict_q[i[0]] = i[2]
                    mass_id.append(i[0])
                    mass_it.append(str(count))

                    count += 1
                    mass_user_id.append(i[1])
                mass_answ = mass_it
            await bot.send_message(message.from_user.id, text="Выберите вопрос, на который ответить",
                                   reply_markup=make_row_keyboard(mass_it))
        else:
            await bot.send_message(message.from_user.id, text="Пока вопросов нет.",
                                   reply_markup=keyboards.markups.mainMenu)


async def answer_q(message : types.Message, state : FSMContext):
    global mass_id, res_id_db, res_id_userId, mass_answ
    if message.text in mass_answ:
        res_id_db = mass_id[int(message.text) - 1]
        res_id_userId = int(message.text) - 1
        await bot.send_message(message.from_user.id, text="Вводите ответ:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("отмена")))
        await answer.next()
    else:
        await bot.send_message(message.from_user.id, text="Проверьте корректность введенных данных")


async def send_q(message : types.Message, state : FSMContext):
    global res_id_db, res_id_userId
    answ = message.text
    db.set_status_answer(answ, res_id_db)
    print(res_id_userId, answ, mass_user_id, mass_user_id[res_id_userId])
    await bot.send_message(mass_user_id[res_id_userId], text=("Ответ на Ваш вопрос: " + answ))
    await bot.send_message(message.from_user.id, text="Ответ успешно отправлен", reply_markup=keyboards.markups.mainMenu)
    await state.finish()


async def cancel_handler(message : types.Message, state : FSMContext):
    await message.reply("Отмена", reply_markup=keyboards.markups.mainMenu)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


def register_handlers_answ(dp: Dispatcher):
    dp.register_message_handler(cm_start, Text(equals='Вопросы клиентов', ignore_case=True), state=None)
    dp.register_message_handler(answer_q, state=answer.select_answer)
    dp.register_message_handler(send_q, state=answer.send_answer)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")


