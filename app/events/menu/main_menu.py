from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ReplyKeyboardMarkup


def main_menu():
    keyboard = [[KeyboardButton("🏠 Главное меню")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
