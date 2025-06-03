from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import asyncio
import logging

from handlers.admin_handlers import startup_bot
from handlers.user_handlers import start, get, spy, spy_stop, spy_list, spy_stop_all

from env import BOT_TOKEN

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(startup_bot)
    dp.message.register(start, Command('start'))
    dp.message.register(get, Command('get'))
    dp.message.register(spy, Command('spy'))
    dp.message.register(spy_stop, Command('spy_stop'))
    dp.message.register(spy_list, Command('spy_list'))
    dp.message.register(spy_stop_all, Command('spy_stop_all'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())