from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from create_bot import dp, bot
from data_base.common.models import Profile
from data_base.common.models import db
from aiogram.dispatcher.filters import Text
from keyboards import default_kb, menu_kb, create_kb


class FSMprofile(StatesGroup):
    add_lang = State()
    del_lang = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer(text='Привет! Я Бот-переводчик. Выбери нужное действие.', reply_markup=menu_kb)


@dp.message_handler(commands=['добавить_язык'], state=None)
async def cmd_add_lang(message: types.Message) -> None:
    await message.answer(text='Добавьте в избранное нужные языки', reply_markup=default_kb)
    await FSMprofile.add_lang.set()


@dp.message_handler(commands=['удалить_язык'], state=None)
async def cmd_delete_lang(message: types.Message) -> None:
    with db.atomic():
        cur_langs = Profile.select().where(Profile.user_id == message.from_user.id)[0].langs.split()
        print(cur_langs)
        await message.answer(text='Какой язык удалить из избранных?', reply_markup=create_kb(cur_langs))
        await FSMprofile.del_lang.set()


@dp.callback_query_handler(state=FSMprofile.del_lang)
async def delete_call(call: types.CallbackQuery, state: FSMContext) -> None:
    with db.atomic():
        cur_langs = Profile.select().where(Profile.user_id == call.from_user.id)[0].langs.split()
        cur_langs.remove(call.data)
        query = Profile.update(langs=' '.join(cur_langs)).where(
            Profile.user_id == call.from_user.id)
        query.execute()
        await call.message.edit_reply_markup()
        await call.answer()
    await bot.send_message(chat_id=call.from_user.id, text='Выбери нужное действие.', reply_markup=menu_kb)




@dp.callback_query_handler(Text(contains='cancel'), state=FSMprofile.add_lang)
async def cmd_cancel(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer(text='Языки добавлены в избранные!', show_alert=True)
    await bot.send_message(chat_id=call.from_user.id, text='Выберите действие:',
                           reply_markup=menu_kb)
    await state.finish()
    await call.message.edit_reply_markup()


@dp.callback_query_handler(state=FSMprofile.add_lang)
async def add_select_lang(call: types.CallbackQuery, state: FSMContext) -> None:
    with db.atomic():
        base_users = [user.user_id for user in Profile.select()]
        if str(call.from_user.id) not in base_users:
            new_user = Profile.create(user_id=call.from_user.id, langs=call.data, cur_lang='')
            new_user.save()
            await call.answer()
        else:
            cur_langs = Profile.select().where(Profile.user_id == call.from_user.id)[0].langs.split()
            if call.data in cur_langs:
                await call.answer(text='язык уже в списке')
            else:
                query = Profile.update(langs=Profile.langs + ' ' + call.data).where(
                    Profile.user_id == call.from_user.id)
                query.execute()
                await call.answer(text='язык добавлен')


def register_handler_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_add_lang, commands=['добавить_язык'], state=None)
    dp.register_message_handler(cmd_delete_lang, commands=['удалить язык'], state=None)
    dp.register_callback_query_handler(delete_call, state=FSMprofile.del_lang)
    dp.register_callback_query_handler(cmd_cancel, Text(contains='cancel'), state=FSMprofile.add_lang)
    dp.register_callback_query_handler(add_select_lang, state=FSMprofile.add_lang)
