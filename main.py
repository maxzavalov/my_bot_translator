from aiogram import executor
from create_bot import dp
from handlers import translate, cmd_handlers


async def on_startup(_):
    print('Bot is online!')


cmd_handlers.register_handler_cmd(dp)
translate.register_handler_translate(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
