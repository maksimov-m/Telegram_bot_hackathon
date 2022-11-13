from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
#from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar
from create_bot import db, bot
import keyboards.markups
import validate

"""start_kb = ReplyKeyboardMarkup(resize_keyboard=True,)
start_kb.row('Navigation Calendar', 'Dialog Calendar')"""

class registration(StatesGroup):
    name = State()
    secondname = State()
    patronimyc = State()
    data_birth = State()
    sex = State()
    number = State()


#@dp.message_handler(commands='register', state=None)
async def cm_start(message : types.Message):
    if (not db.user_exists(message.from_user.id) or db.get_signup(message.from_user.id) == "change" or db.get_signup(message.from_user.id) == "reg"):
        if(not db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)
            db.set_signup(message.from_user.id, "reg")
        await bot.send_message(message.from_user.id,
                               "Привет!\nЗаполним данные.\nДавай начнем.\n")
        await registration.name.set()
        await bot.send_message(message.from_user.id, 'Напиши имя', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))
    elif message.text == "/register":
        await bot.send_message(message.from_user.id, "Вы уже зарегестрированы.", reply_markup=keyboards.markups.mainMenu)
    elif message.text  == "/start" and db.user_exists(message.from_user.id):
        mass = db.get_history(message.from_user.id)
        if len(mass) != 0:
            await bot.send_message(message.from_user.id, text="Акутальных записи", reply_markup=keyboards.markups.mainMenu)
            mass_res = []
            for i in mass:
                if validate.isNextDate(i[5]):
                    mass_res.append(i)

            for i in mass_res:
                await bot.send_message(message.from_user.id, text=f"Дата: {i[5]}\n"
                                                                  f"ФИО специалиста: {i[3]}\n"
                                                                  f"Услуга: {i[4]}")
        else:
            await bot.send_message(message.from_user.id, text="Акутальных записей нет", reply_markup=keyboards.markups.mainMenu)


#@dp.message_handler(state=registration.name)
async def load_name(message: types.Message, state: FSMContext):
    if 15 > len(message.text) > 1 and validate.isValidateLSP(message.text):
        print(len(message.text))
        async with state.proxy() as data:
            data['name'] = message.text
        await registration.next()
        await bot.send_message(message.from_user.id, "Теперь фамилию", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))

    else:
        await bot.send_message(message.from_user.id,
            text="Неверный формат. Повторите попытку", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена"))
        )


#@dp.message_handler(state=registration.secondname)
async def load_secondname(message: types.Message, state: FSMContext):
    if 15 > len(message.text) > 1 and validate.isValidateLSP(message.text):
        async with state.proxy() as data:
            data['secondname'] = message.text
        await registration.next()
        await bot.send_message(message.from_user.id,"Теперь отчество")
    else:
        await bot.send_message(message.from_user.id,
            text="Неверный формат. Повторите попытку", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))

#@dp.message_handler(state=registration.patronimyc)
async def load_patronymic(message: types.Message, state: FSMContext):
    if 15 > len(message.text) > 1 and validate.isValidateLSP(message.text):
        async with state.proxy() as data:
            data['patronymic'] = message.text
        await registration.next()
        await  bot.send_message(message.from_user.id,"Теперь дату рождения СТРОГО в формате ГГГГ-ММ-ДД (Пример 1999-05-12)", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))
    else:
        await bot.send_message(message.from_user.id,
            text="Неверный формат. Повторите попытку", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))

# @dp.message_handler(state=registration.secondname)
async def load_data_birth(message: types.Message, state: FSMContext):
    if len(message.text) == 10 and validate.isValidate(message.text):
        async with state.proxy() as data:
            data['data_birth'] = message.text
        await registration.next()
        await bot.send_message(message.from_user.id,"Теперь свой пол (СТРОГО в формате \"муж\" или \"жен\")", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))
    else:
        await bot.send_message(message.from_user.id,
            text="Неверный формат. Повторите попытку", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))

# @dp.message_handler(state=registration.patronimyc)
async def load_sex(message: types.Message, state: FSMContext):
    if validate.isSex(message.text) != None:
        async with state.proxy() as data:
            data['sex'] = validate.isSex(message.text)
        await registration.next()
        await bot.send_message(message.from_user.id,"Теперь номер телефона", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))
    else:
        await bot.send_message(message.from_user.id,
            text="Неверный формат. Повторите попытку", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))

# @dp.message_handler(state=registration.secondname)
async def load_number(message: types.Message, state: FSMContext):
    if validate.isValidatPhoneNumber(message.text):
        async with state.proxy() as data:
            data['number'] = message.text
        await registration.next()

        res = list(data.values())
        print(res)
        db.set_name(message.from_user.id, res[0])
        db.set_secondname(message.from_user.id, res[1])
        db.set_patronymic(message.from_user.id, res[2])
        db.set_data_birth(message.from_user.id, res[3])
        db.set_sex(message.from_user.id, res[4])
        db.set_number(message.from_user.id, res[5])
        db.set_signup(message.from_user.id, "done")

        await state.finish()

        await bot.send_message(message.from_user.id,"Регистрация прошла успешно", reply_markup=keyboards.markups.mainMenu)
    else:
        await bot.send_message(message.from_user.id,
            text="Не верный формат. Повтори попытку", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="отмена")))


async def cancel_handler(message: types.Message, state: FSMContext):
    if db.get_signup(message.from_user.id) == "change":
        db.set_signup(message.from_user.id, "done")
    await message.reply("Ввод данных отменен", reply_markup=keyboards.markups.mainMenu)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


def register_handlers_reg(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['register', 'start'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=registration.name)
    dp.register_message_handler(load_secondname, state=registration.secondname)
    dp.register_message_handler(load_patronymic, state=registration.patronimyc)
    dp.register_message_handler(load_data_birth, state=registration.data_birth)
    dp.register_message_handler(load_sex, state=registration.sex)
    dp.register_message_handler(load_number, state=registration.number)
