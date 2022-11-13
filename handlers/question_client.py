from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from create_bot import bot, db
import keyboards.markups
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
class question(StatesGroup):
    question = State()

async def cm_start(message : types.Message):
    if db.user_exists(message.from_user.id):
        await bot.send_message(message.from_user.id, text="Введите свой вопрос.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("отмена")))
        await question.question.set()
    else:
        await bot.send_message(message.from_user.id, text="Закончите регистрацию! (введите /start или /register)")


async def write_question(message : types.Message, state : FSMContext):
    if len(message.text) > 10:

        db.set_question(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, text="Вопрос успешно отправлен.\nОжидайте, в течении ближайшего времени Вам придем ответ", reply_markup=keyboards.markups.mainMenu)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, text="Проверьте корректность ввода.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("отмена")))

async def cancel_handler(message : types.Message, state : FSMContext):
    await message.reply("ok", reply_markup=keyboards.markups.mainMenu)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()

def register_handlers_question(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['myquestion'], state=None)
    dp.register_message_handler(cm_start, Text(equals='Задать свой вопрос', ignore_case=True), state=None)
    dp.register_message_handler(write_question, state=question.question)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
