from aiogram.utils import executor
from create_bot import dp

async def on_strup(_):
    print('Bot on!')

from handlers import client, registration, others, record

client.register_handlers_client(dp)
registration.register_handlers_reg(dp)
record.register_handlers_rec(dp)
others.register_handlers_others(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_strup)