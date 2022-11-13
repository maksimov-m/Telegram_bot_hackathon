from aiogram.utils import executor
from create_bot import dp

async def on_strup(_):
    print('Bot on!')

from handlers import client, registration, others, record, delete, spam, statistics, question_client, answer_questions


registration.register_handlers_reg(dp)
client.register_handlers_client(dp)
spam.register_handlers_spam(dp)
answer_questions.register_handlers_answ(dp)
statistics.register_handlers_stat(dp)
question_client.register_handlers_question(dp)
record.register_handlers_rec(dp)
delete.register_handlers_del(dp)
others.register_handlers_others(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_strup)