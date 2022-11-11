from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import db, bot
import keyboards.markups
from keyboards import markups as nav

class registration(StatesGroup):
    name = State()
    secondname = State()
    patronimyc = State()
    data_birth = State()
    sex = State()
    number = State()


#@dp.message_handler(commands='register', state=None)
async def cm_start(message : types.Message):
    if (not db.user_exists(message.from_user.id) or db.get_signup(message.from_user.id) == "change"):
        if(not db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id,
                               "Привет!\nЗаполним данные.\nДавай начнем.\n")
        await registration.name.set()
        await message.reply('Напиши имя')
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегестрированы.", reply_markup=nav.mainMenu)


#@dp.message_handler(state=registration.name)
async def load_name(message: types.Message, state: FSMContext):
    if 15 > len(message.text) > 1:
        print(len(message.text))
        async with state.proxy() as data:
            data['name'] = message.text
        await registration.next()
        await message.reply("Теперь фамилию")

    else:
        await message.reply(
            text="Не верный формат. Повтори попытку"
        )


#@dp.message_handler(state=registration.secondname)
async def load_secondname(message: types.Message, state: FSMContext):
    if 15 > len(message.text) > 1:
        async with state.proxy() as data:
            data['secondname'] = message.text
        await registration.next()
        await message.reply("Теперь отчество")
    else:
        await message.reply(
            text="Не верный формат. Повтори попытку")

#@dp.message_handler(state=registration.patronimyc)
async def load_patronymic(message: types.Message, state: FSMContext):
    if 15 > len(message.text) > 1:
        async with state.proxy() as data:
            data['patronymic'] = message.text
        await registration.next()
        await message.reply("Теперь дату рождения СТРОГО в формате YYYY-MM-DD")
    else:
        await message.reply(
            text="Не верный формат. Повтори попытку")

# @dp.message_handler(state=registration.secondname)
async def load_data_birth(message: types.Message, state: FSMContext):
    if len(message.text) == 10:
        async with state.proxy() as data:
            data['data_birth'] = message.text
        await registration.next()
        await message.reply("Теперь свой пол(male - муж, female - жен)")
    else:
        await message.reply(
            text="Не верный формат. Повтори попытку")

# @dp.message_handler(state=registration.patronimyc)
async def load_sex(message: types.Message, state: FSMContext):
    if message.text == "male" or message.text == "female":
        async with state.proxy() as data:
            data['sex'] = message.text
        await registration.next()
        await message.reply("Теперь номер телефона")
    else:
        await message.reply(
            text="Не верный формат. Повтори попытку")

# @dp.message_handler(state=registration.secondname)
async def load_number(message: types.Message, state: FSMContext):
    if len(message.text) == 11:
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

        await message.reply("Регистрация прошла успешно", reply_markup=keyboards.markups.mainMenu)
    else:
        await message.reply(
            text="Не верный формат. Повтори попытку")

def register_handlers_reg(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['register', 'start'], state=None)
    dp.register_message_handler(load_name, state=registration.name)
    dp.register_message_handler(load_secondname, state=registration.secondname)
    dp.register_message_handler(load_patronymic, state=registration.patronimyc)
    dp.register_message_handler(load_data_birth, state=registration.data_birth)
    dp.register_message_handler(load_sex, state=registration.sex)
    dp.register_message_handler(load_number, state=registration.number)
