from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnProfile = KeyboardButton('Мой профиль')
btsChange = KeyboardButton('Изменить информацию')

mainMenu = ReplyKeyboardMarkup(resize_keyboard= True)
mainMenu.add(btnProfile, btsChange)