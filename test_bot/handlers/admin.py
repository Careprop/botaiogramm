from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
import settings


class FSMAdmin(StatesGroup):
    login = State()
    password = State()
    name = State()
    age = State()
    life = State()


# @dp.message_handler(commands=['start'], state=None)
async def cm_start(message: types.Message, state: FSMContext):
    await FSMAdmin.login.set()
    async with state.proxy() as data:
        if 'login' in data:
            if message.from_user.id in data['login']:
                await message.answer('Вы уже авторизованы!')
                await message.answer('ФИО:')
                await FSMAdmin.name.set()
            else:
                await message.answer('Введите логин (test)')
                data['login'] = []
        else:
            await message.answer('Введите логин (test)')
            async with state.proxy() as data:
                data['login'] = []
    # --- Проверка авторизации ---


# @dp.message_handler(commands=['login'], state=FSMAdmin.login)
async def write_login(message: types.Message, state: FSMContext):
    x = message
    if x.text == settings.reference['login']:
        async with state.proxy() as data:
            data['login'] = [x.from_user.id]
        await FSMAdmin.next()
        await message.answer('Введите пароль (test)')
    else:
        await message.answer('Логин не совпадает с эталоном (test)')


# @dp.message_handler(state=FSMAdmin.password)
async def write_password(message: types.Message, state: FSMContext):
    x = message
    if x.text == settings.reference['password']:
        await FSMAdmin.next()
        await message.answer('Авторизация прошла успешно!')
        await message.answer('ФИО:')
    else:
        await message.answer('Пароль не совпадает с эталоном (test)')


# @dp.message_handler(state=FSMAdmin.name)
async def write_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Возраст:')


# @dp.message_handler(state=FSMAdmin.age)
async def write_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await FSMAdmin.next()
    async with state.proxy() as data:
        if int(data['age']) < 18:
            await message.answer('Введите место учебы:')
            async with state.proxy() as data:
                data['life'] = ['Место учебы:']
        else:
            await message.answer('Введите место работы:')
            async with state.proxy() as data:
                data['life'] = ['Место работы:']


async def life(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['life'].append(message.text)
    await FSMAdmin.next()
    await message.answer(f'ФИО: {data["name"]}\nВозраст: {data["age"]}\n{" ".join(data["life"])}')
    # await message.answer(str(data))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['start'], state=None)
    dp.register_message_handler(write_login, state=FSMAdmin.login)
    dp.register_message_handler(write_password, state=FSMAdmin.password)
    dp.register_message_handler(write_name, state=FSMAdmin.name)
    dp.register_message_handler(write_age, state=FSMAdmin.age)
    dp.register_message_handler(life, state=FSMAdmin.life)

