from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv, find_dotenv
import os
from site_api import translate_text

load_dotenv(find_dotenv())


async def on_startup(_):
    print('Bot is online!')


bot = Bot(os.getenv('TOKEN_API'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer(text='Добро пожаловать в Бот-переводчик! Напишите сообщение и я переведу его на английский')


@dp.message_handler()
async def cmd_start(message: types.Message) -> None:
    await message.answer(text=translate_text(message.text, 'ru', 'en'))

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
