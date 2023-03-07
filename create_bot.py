from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv(find_dotenv())

bot = Bot(os.getenv('TOKEN_API'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


