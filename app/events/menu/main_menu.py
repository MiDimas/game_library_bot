from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = [[KeyboardButton("🏠 Главное меню")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
