from aiogram import executor, types
from create_bot import dp
from handlers import translate, cmd_handlers
from data_base.models import db, Profile

db.connect()
db.create_tables([Profile])


async def on_startup(_):
    print('Bot is online!')


cmd_handlers.register_handler_cmd(dp)
translate.register_handler_translate(dp)


@dp.message_handler()
async def catch_start_messages(message: types.Message) -> None:
    await message.answer(text='Для начала работы напиши: /start ')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
