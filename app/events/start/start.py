from telegram import Update
from telegram.ext import ContextTypes

from app.helpers.decorators import async_event_error_handler
from app.repositories.user_repo import UserRepo
from app.events.menu.main_menu import main_menu
from app.events.menu.states import MenuStates
from app.helpers.checks import check_is_admin_channel
from app.config.main_conf import settings
@async_event_error_handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    is_admin = await check_is_admin_channel(context, settings.CHANNEL_ID, tg_user.id)
    user = await UserRepo.get_or_create(tg_user.id, update.effective_user.username)
    print(user)
    print(update)
    print(context)
    if user.created_now:
        await update.message.reply_text(
            f'Добро пожаловать {update.effective_user.first_name}! Я бот для сбора информации об ожидаемых играх. \n\n'
            'Чтобы попасть в главное меню, нажми "🏠 Главное меню"',
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text(
            f'С возвращением, {update.effective_user.first_name}! Я бот для сбора информации об ожидаемых играх. \n\n'
            'Чтобы попасть в главное меню, нажми "🏠 Главное меню"',
            reply_markup=main_menu()
        )
        
    return MenuStates.START