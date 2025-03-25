from telegram import Update
from telegram.ext import ContextTypes

from app.helpers.decorators import async_event_error_handler
from app.repositories.user_repo import UserRepo
from app.events.menu.main_menu import main_menu


@async_event_error_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await UserRepo().get_or_create(update.effective_user.id, update.effective_user.username)
    print(user)
    print(update)
    print(context)
    if user.created_now:
        await update.message.reply_text(
            'Привет! Я бот для сбора информации об ожидаемых играх. '
            'Чтобы попасть в главное меню, нажми "🏠 Главное меню"',
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text(
            'С возвращением! Я бот для сбора информации об ожидаемых играх. '
            'Чтобы попасть в главное меню, нажми "🏠 Главное меню"',
            reply_markup=main_menu()
        )
        
