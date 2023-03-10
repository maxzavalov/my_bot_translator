from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

lang_keys = ['ar', 'az', 'be', 'bg', 'ca', 'cs', 'el', 'en', 'eu', 'fi', 'fr', 'gn', 'he', 'hi', 'hr', 'hy', 'ja', 'ka',
             'kk', 'ko', 'la', 'pl', 'pt', 'es', 'sv', 'tr', 'uk', 'zh']


def create_kb(buttons: list) -> InlineKeyboardMarkup():
    lang_dict = {'ar': 'Арабский', 'az': 'Азербайджанский', 'be': 'Белорусский', 'bg': 'Болгарский',
                 'ca': 'Каталанский',
                 'cs': 'Чешский', 'el': 'Греческий', 'en': 'Английский', 'eu': 'Баскский', 'fi': 'Финский',
                 'fr': 'Французский',
                 'gn': 'Гуарани', 'he': 'Иврит', 'hi': 'Хинди', 'hr': 'Хорватский', 'hy': 'Армянский', 'ja': 'Японский',
                 'ka': 'Грузинский', 'kk': 'Казахский', 'ko': 'Корейский', 'la': 'Латинский', 'pl': 'Польский',
                 'pt': 'Португальский', 'es': 'Испанский', 'sv': 'Шведский', 'tr': 'Турецкий', 'uk': 'Украинский',
                 'zh': 'Китайский'}
    result = InlineKeyboardMarkup(row_width=3)
    for button in buttons:
        result.insert(InlineKeyboardButton(text=lang_dict[button], callback_data=button))

    return result


default_kb = create_kb(lang_keys).insert(InlineKeyboardButton(text='Закончить', callback_data='cancel'))

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_kb.add(KeyboardButton(
    text='/добавить_язык')).add(KeyboardButton(
    text='/перевод')).add(KeyboardButton(
    text='/удалить_язык'))

ask_to_continue = ReplyKeyboardMarkup(resize_keyboard=True)
ask_to_continue.add(KeyboardButton(text='/продолжить')).add(KeyboardButton(text='/закончить'))
