from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.helpers.decorators import async_event_error_handler
from app.helpers.checks import check_subscription
from app.repositories.game_repo import GameRepo
from app.config.main_conf import settings
from app.events.menu.states import MenuStates

keyboard_in_menu = [
    [InlineKeyboardButton('Назад в меню', callback_data='menu')]
]
reply_markup_in_menu = InlineKeyboardMarkup(keyboard_in_menu)

@async_event_error_handler
async def check_my_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message
    is_callback = bool(update.callback_query)
    if is_callback:
        await update.callback_query.answer()
    if not await check_subscription(context, settings.CHANNEL_ID, user.id):
        await message.edit_text(f'Вы не подписаны на канал {settings.CHANNEL_ID}', reply_markup=reply_markup_in_menu)
        return MenuStates.MENU
    games = await GameRepo.get_games_by_user_telegram_id(update.effective_user.id)
    if not games:
        await message.edit_text('Вы еще не добавили ни одной игры', reply_markup=reply_markup_in_menu)
        return MenuStates.MENU
    prepare_message = 'Ожидаемые вами игры:\n'
    count = 1
    for game in games:
        prepare_message += (f'{count}. {game.name} ({game.created_at.strftime("%d.%m.%Y")})\n')
        count += 1

    await message.edit_text(prepare_message, reply_markup=reply_markup_in_menu)
    return MenuStates.MENU