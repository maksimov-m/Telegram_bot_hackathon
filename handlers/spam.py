from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import db, bot
import keyboards.markups

ADMIN = "821204845" #id_user  Админа

class dialog(StatesGroup):
    spam = State()


async def cm_start(message : types.Message):
    print(message.from_user.id, ADMIN)
    if str(message.from_user.id) != ADMIN:
        await bot.send_message(message.from_user.id, "Я не знаю такой команды.", reply_markup=keyboards.markups.mainMenu)
    else:
        await dialog.spam.set()
        await message.answer('Напиши текст рассылки')

async def start_spam(message: types.Message, state: FSMContext):
  if message.text == 'отмена':
    await message.answer('Главное меню', reply_markup=keyboards.markups.mainMenu)
    await state.finish()
  else:
      mass = db.get_user_ud()
      for i in mass:
        await bot.send_message(i[0], message.text)
      await message.answer('Рассылка завершена', reply_markup=keyboards.markups.mainMenu)
      await state.finish()


async def cancel_handler(message : types.Message, state : FSMContext):
    await message.reply("Отменено", reply_markup=keyboards.markups.mainMenu)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()

def register_handlers_spam(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['spam'], state=None)
    dp.register_message_handler(cm_start, Text(equals='Рассылка', ignore_case=True), state=None)
    dp.register_message_handler(start_spam, state=dialog.spam)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
