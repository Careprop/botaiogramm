from aiogram import types, Dispatcher
from create_bot import dp, bot


#@dp.message_handler(commands=['help'])
async def command_start(message: types.message):
    pass


def register_handlers_client(dp: Dispatcher):
     dp.register_message_handler(command_start, commands=['help'])
