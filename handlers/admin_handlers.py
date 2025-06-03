from aiogram import Bot
from config_loader import ADMIN_ID, MESSAGES

async def startup_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, MESSAGES['startup_admin'])
    