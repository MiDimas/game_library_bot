from telegram.ext import ContextTypes
from telegram import Update
from telegram.ext import ReplyKeyboardRemove

from app.database import async_session
from app.models.User import User
from app.models.Game import Game
from app.helpers.decorators.event_error_handler import async_event_error_handler
from app.events.menu.states import MenuStates

@async_event_error_handler      
async def start_add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите название игры, низкую цену на которую вы ждете', reply_markup=ReplyKeyboardRemove())

    return MenuStates.ADD_GAME

async def add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with async_session() as session:
        user = await session.query(User).filter_by(telegram_id=update.effective_user.id).first()
        
        if not user:
            await update.message.reply_text('Пожалуйста, сначала используйте команду /start')
            return
        
        game_name = update.message.text
        game = Game(user_id=user.id, game_name=game_name)
        session.add(game)
        await session.commit()
        
        await update.message.reply_text('Игра успешно добавлена в список ожидания!')

    return MenuStates.MENU
