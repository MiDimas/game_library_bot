from telegram.ext import ContextTypes
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.helpers.decorators.event_error_handler import async_event_error_handler
from app.events.menu.states import MenuStates
from app.repositories.user_repo import UserRepo
@async_event_error_handler      
async def start_add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text('Введите название игры, низкую цену на которую вы ждете. \n\n'
                                                   'Или нажмите "Отмена" чтобы вернуться в главное меню', 
                                                   reply_markup=reply_markup)

    return MenuStates.ADD_GAME

async def add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await UserRepo().get_user_by_telegram_id(update.effective_user.id)
    if not user:
        await update.message.reply_text('Пожалуйста, сначала используйте команду /start')
        return MenuStates.UNDEFINED
    
    game_name = update.message.text.strip()
    print(game_name)

    keyboard = [
        [InlineKeyboardButton("🎮 Добавить еще одну игру", callback_data="add_game")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Игра успешно добавлена в список ожидания! \n\n'
                                    'Чтобы добавить еще одну игру, нажмите "🎮 Добавить еще одну игру" \n\n'
                                    'Чтобы вернуться в главное меню, нажмите "🏠 Главное меню"',
                                    reply_markup=reply_markup
                                    )

    return MenuStates.MENU
