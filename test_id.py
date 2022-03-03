from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor


import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import settings


bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def test(message: types.Message):
    print(message.message_id)
    await bot.send_message(message.chat.id, "Message")


if __name__ == '__main__':
    
    
    executor.start_polling(dp, skip_updates=True)
