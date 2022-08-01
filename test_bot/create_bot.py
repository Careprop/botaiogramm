from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

import settings

bot = Bot(settings.TOKEN)
dp = Dispatcher(bot, storage=storage)
