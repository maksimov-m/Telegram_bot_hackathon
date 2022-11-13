from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#---------CLIENT---------------
btnProfile = KeyboardButton('Мой профиль')
btnChange = KeyboardButton('Изменить информацию')
btnHistory = KeyboardButton('История записей')
btnRecord= KeyboardButton('Запись к специалисту')
btnRecordUpcoming = KeyboardButton('Актуальные записи')
btnRecordDel= KeyboardButton('Отменить запись')
btnFAQ= KeyboardButton('Часто задаваемые вопросы')
btnQuestAdmin= KeyboardButton('Задать свой вопрос')
btnLinks = KeyboardButton('Полезные ссылки')

mainMenu = ReplyKeyboardMarkup(resize_keyboard= True)
mainMenu.add(btnProfile, btnChange)
mainMenu.add(btnRecord, btnHistory)
mainMenu.add(btnRecordUpcoming)
mainMenu.add(btnRecordDel)
mainMenu.add(btnFAQ)
mainMenu.add(btnQuestAdmin)
mainMenu.add(btnLinks)


btnSite = InlineKeyboardButton('🟢Сайт клиники', url="https://norismed.ru/")
btnPrice = InlineKeyboardButton('🏷️Прайс лист клиники', url="https://norismed.ru/wp-content/uploads/2021/08/%D0%9F%D1%80%D0%B0%D0%B9%D1%81-%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0-%D0%9D%D0%BE%D1%80%D0%B8%D1%81-01.02.2022.pdf")
btnTG = InlineKeyboardButton('💬Телеграм группа', url="https://t.me/mednoris")
btnYoutube = InlineKeyboardButton('📍Ютуб канал', url="https://www.youtube.com/channel/UCI0k0sLbWqnwLbgtCyRuK6w")
btnVK = InlineKeyboardButton('🔹ВК группа', url="https://vk.com/mednoris")
btnWatsApp = InlineKeyboardButton("❇WhatsApp", url="https://wa.me/79173774289")

linkMenu = InlineKeyboardMarkup(row_width=6)

linkMenu.add(btnSite)
linkMenu.add(btnPrice)
linkMenu.add(btnTG)
linkMenu.add(btnYoutube)
linkMenu.add(btnVK)
linkMenu.add(btnWatsApp)

#----------ADMIN----------------
btnSpam = KeyboardButton('Рассылка')
btnStat = KeyboardButton('Статистика')
btnQuest = KeyboardButton('Вопросы клиентов')

adminMenu = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenu.add(btnSpam)
adminMenu.add(btnStat)
adminMenu.add(btnQuest)
