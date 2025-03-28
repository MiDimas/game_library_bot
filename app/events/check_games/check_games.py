from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton 
from telegram.ext import ContextTypes

from app.helpers.decorators import async_event_error_handler
from app.repositories.game_repo import GameRepo
from app.events.menu.states import MenuStates
from app.helpers.checks import check_is_admin_channel
from app.config.main_conf import settings

keyboard_in_menu = [
    [InlineKeyboardButton('Назад в меню', callback_data='menu')]
]
reply_markup_in_menu = InlineKeyboardMarkup(keyboard_in_menu)

@async_event_error_handler
async def check_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await check_is_admin_channel(context, settings.CHANNEL_ID, user.id):
        await message.edit_text("Вы не являетесь администратором канала!", reply_markup=reply_markup_in_menu)
        return MenuStates.MENU
    message = update.effective_message
    is_callback = bool(update.callback_query)
    if is_callback:
        await update.callback_query.answer()
    games = await GameRepo.get_all_games()
    if not games:
        await message.edit_text("Нет игр")
        return
    prepare_message = "Все игры:\n"
    count = 1
    for game in games:
        prepare_message += f"{count}. {game.name} ({game.created_at.strftime('%d.%m.%Y')}) {game.username}\n"
        count += 1
    await message.edit_text(prepare_message, reply_markup=reply_markup_in_menu)
    return MenuStates.ADMIN_LIST_GAMES