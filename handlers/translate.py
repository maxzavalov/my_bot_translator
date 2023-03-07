from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from create_bot import dp, bot
from data_base.common.models import Profile
from data_base.common.models import db
from aiogram.dispatcher.filters import Text
from keyboards import default_kb, menu_kb, create_kb, ask_to_continue
from site_api import translate_text


class FSMTranslate(StatesGroup):
    choice = State()
    working = State()
    cancel = State()


@dp.message_handler(commands=['перевод'], state=None)
async def cmd_translate(message: types.Message) -> None:
    await FSMTranslate.choice.set()
    await message.answer('Выберите нужный язык.', reply_markup=create_kb(
        Profile.select().where(Profile.user_id == message.from_user.id)[0].langs.split()))


@dp.callback_query_handler(state=FSMTranslate.choice)
async def current_lang(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['choice'] = call.data
    await FSMTranslate.next()
    await call.answer('Что нужно перевести?')
    await call.message.delete()


@dp.message_handler(commands=['продолжить'], state=FSMTranslate.working)
async def cmd_continue(message: types.Message) -> None:
    await message.answer(text='Что ещё перевести?')


@dp.message_handler(commands=['закончить'], state=FSMTranslate.working)
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(text='Добро пожаловать в главное меню', reply_markup=menu_kb)
    await message.delete()


@dp.message_handler(state=FSMTranslate.working)
async def translate_message(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        cur_lang = data.get('choice')
    await message.answer(text=translate_text(message.text, 'ru', cur_lang), reply_markup=ask_to_continue)


def register_handler_translate(dp: Dispatcher):
    dp.register_message_handler(cmd_translate, commands=['translate'], state=None)
    dp.register_callback_query_handler(current_lang, state=FSMTranslate.choice)
    dp.register_message_handler(cmd_continue, commands=['продолжить'], state=FSMTranslate.working)
    dp.register_message_handler(cmd_cancel, commands=['закончить'], state=FSMTranslate.working)
    dp.register_message_handler(translate_message, state=FSMTranslate.working)
