import json
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from requests.auth import HTTPBasicAuth
from aiogram import types, Dispatcher

import keyboards.markups
from create_bot import bot, db


mass_spec = []

class record(StatesGroup):
    uid_emp = State()
    uid_uslugi = State()
    time = State()
    data_b_1 = State()
    data_b_2 = State()
    rec = State()

dict_uid = {}
usl = []
date_usl = []

urlAdress = "https://norisapi.ru:12345/"
pasword = "rjvfy433"
login = "team1"

mass_date1 = []

def setBookanappointment(data ):
    servList = "bookanappointment"
    print("Set post request to Server with url\"" + urlAdress + servList + "\"")
    response = requests.post(url=(urlAdress + servList),
                            auth=HTTPBasicAuth(login, pasword),
                            json=data)
    return response


def getServiceList():
    r = (requests.get('https://norisapi.ru:12345/servicelist', auth=HTTPBasicAuth('team1', 'rjvfy433'))).json()['Services']
    return r


def getSchedule(uidDoctor : str, data : str ) -> json :
    servList = "getschedule"
    print("Set get request to Server with url\"" + urlAdress + servList + "\"")
    response = requests.get(url=(urlAdress + servList),
                            params={ "uid" : uidDoctor,
                                     "date" : data},
                            auth=HTTPBasicAuth(login, pasword),
                            verify=False)
    return response.json()


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



#@dp.message_handler(commands='record')
async def record_emp(message : types.Message):
    global mass_spec

    if db.get_signup(message.from_user.id) == "done":
        try:
            r = getServiceList()
            await record.uid_emp.set()
            await bot.send_message(message.from_user.id, "Список специалистов: ")
            mass = []
            mass_uid = {}
            for i in r:
                mass.append(i['ФИО'])
                mass_uid[i['ФИО']] = i['uid врача']
            mass_spec = mass
            for i in mass:
                await bot.send_message(message.from_user.id, text=i)
            await record.next()
            mass.append("отмена")
            await message.answer(text="Выберите специалиста(нажмите на нужную кнпоку)",
                reply_markup=make_row_keyboard(mass)
                )

        except:
            await bot.send_message(message.from_user.id, text="Извините. Сервер не отвечает.", reply_markup=keyboards.markups.mainMenu)
    else:
        await bot.send_message(message.from_user.id, text="Закончите регистрацию! (введите /start или /register)")



async def record_usl(message : types.Message, state : FSMContext):
    global usl, dict_uid, mass_spec

    if message.text in mass_spec:
        r = getServiceList()
        usl = []
        for i in r:
            if i['ФИО'] == message.text:
                dict_uid['uid_emp'] = i['uid врача']
                dict_uid['name_doctor'] = i['ФИО']
                usl = i['Услуги']
                break

        await bot.send_message(message.from_user.id, "Список услуг данного специалиста: ")
        for i in usl:
            await bot.send_message(message.from_user.id, text=f"Название услуги: {i['Наименование']}\n"
                                                                f"Стоимость: {i['Стоимость']}\n"
                                                                f"Длительность: {i['Длительность']}")
        mass = []
        for i in usl:
            mass.append(i['Наименование'])
        await record.next()
        mass.append("отмена")
        await bot.send_message(message.from_user.id, text = "Выберите услугу: ", reply_markup=make_row_keyboard(mass))
    else:
        await bot.send_message(message.from_user.id, text="Проверьте корректность введеных данных")


async def record_data(message : types.Message, state : FSMContext):
    global usl, dict_uid
    flag = False
    for i in usl:
        if message.text == i['Наименование']:
            dict_uid['uid_usl'] = i['uid']
            dict_uid['name_usl'] = i['Наименование']
            flag = True

    if flag:
        mass = ["2022-11-14", "2022-11-15", "2022-11-16"]
        mass.append("отмена")
        await bot.send_message(message.from_user.id, text="Выберите дату", reply_markup=make_row_keyboard(mass))
        await record.next()
    else:
        await bot.send_message(message.from_user.id, text="Проверьте корректность введенных дат")

async def record_data_b_1(message : types.Message, state : FSMContext):
    global dict_uid, date_usl, mass_date1
    dict_uid['data'] = message.text
    print(dict_uid['uid_emp'], message.text)
    r = getSchedule(dict_uid['uid_emp'], message.text)
    print(r)
    mass_date = r['Свободное время']

    count = 1
    if mass_date == None:
        await bot.send_message(message.from_user.id, text="У этого специалиста нет свободных мест")
        await state.finish()
        await record_emp(message)
    else:
        await bot.send_message(message.from_user.id, text="Cвободные даты")
        mass = []
        for i in mass_date:
            mass.append(f"{count}.\n"
                        f"Начало: {i['Начало']}\n"
                        f"Конец: {i['Конец']}")
            """await bot.send_message(message.from_user.id, text=f"{count}.\n"
                                                              f"Начало: {i['Начало']}\n"
                                                              f"Конец: {i['Конец']}")"""

            mass_date1.append(count)
            count += 1
        await bot.send_message(message.from_user.id, text=str.join('\n', mass))

        mass_btn = [str(i) for i in range(1, len(mass_date) + 1)]
        mass_btn.append("отмена")
        date_usl = mass_date

        await record.next()
        await bot.send_message(message.from_user.id, text="Выберите свободную дату", reply_markup=make_row_keyboard(mass_btn))


async def record_data_b_2(message: types.Message, state: FSMContext):
    global dict_uid, date_usl, mass_date1

    try:
        print(int(message.text), len(date_usl))
        if int(message.text) - 1 < len(date_usl) and int(message.text) > 0:
            date = date_usl[int(message.text) - 1]
            dict_uid['time_b'] = date['Начало']
            dict_uid['time_e'] = date['Конец']
            """await bot.send_message(message.from_user.id, text=f"uid_emp: {dict_uid['uid_emp']}\n"
                                                              f"uid_uslugi: {dict_uid['uid_usl']}\n"
                                                              f"timebegin: {dict_uid['time_b']}\n"
                                                              f"timeend: {dict_uid['time_e']}\n"
                                                              f"fio: {db.get_name(message.from_user.id) + ' ' + db.get_secondname(message.from_user.id)+ ' ' + db.get_patronymic(message.from_user.id)}\n"
                                                              f"datebirth : {db.get_birth_day(message.from_user.id)}\n"
                                                              f"sex: {db.get_sex(message.from_user.id)}\n"
                                                              f"phone: {db.get_number(message.from_user.id)}")"""

            data_res =  {}
            data_res['uid_emp'] = dict_uid['uid_emp']
            data_res['uid_uslugi'] = dict_uid['uid_usl']
            data_res['timebegin'] = dict_uid['time_b']
            data_res['timeend'] = dict_uid['time_e']
            data_res['fio'] = db.get_name(message.from_user.id) + ' ' + db.get_secondname(message.from_user.id)+ ' ' + db.get_patronymic(message.from_user.id)
            data_res['datebirth'] = db.get_birth_day(message.from_user.id)
            data_res['sex'] = db.get_sex(message.from_user.id)
            data_res['phone'] = db.get_number(message.from_user.id)
            #data_res['phone1'] = db.get_number(message.from_user.id)


            try:
                r  = setBookanappointment(data_res)
                print(r, r.json())
                await bot.send_message(message.from_user.id, text=f"Вы записаны на {dict_uid['time_b']}", reply_markup=keyboards.markups.mainMenu)
                db.add_history(message.from_user.id, r.json()['id'],
                                dict_uid['name_doctor'], dict_uid['name_usl'], dict_uid['time_b'])
                await state.finish()
            except:
                await bot.send_message(message.from_user.id, text="Извините, произошла ошибка сервера. Повторите попытку позже.", reply_markup=keyboards.markups.mainMenu)
                await state.finish()
        else:
            await bot.send_message(message.from_user.id, text="Проверьте корректность введеных данных")
    except:
        await bot.send_message(message.from_user.id, text="Проверьте корректность введеных данных")


#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message : types.Message, state : FSMContext):
    await message.reply("Запись отменена", reply_markup=keyboards.markups.mainMenu)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


def register_handlers_rec(dp : Dispatcher):
    dp.register_message_handler(record_emp, Text(equals='Запись к специалисту', ignore_case=True), state=None)
    dp.register_message_handler(record_usl, state=record.uid_uslugi)
    dp.register_message_handler(record_data, state=record.time)
    dp.register_message_handler(record_data_b_1, state=record.data_b_1)
    dp.register_message_handler(record_data_b_2, state=record.data_b_2)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")