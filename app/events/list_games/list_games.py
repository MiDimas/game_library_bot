from app.database import async_session
from app.models.Game import Game
from app.models.User import User
from telegram.ext import ContextTypes
from telegram import Update
from app.config.main_conf import settings



async def list_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != settings.ADMIN_ID:
        await update.message.reply_text('У вас нет доступа к этой команде.')
        return
    
    async with async_session() as session:
        games = await session.query(Game).all()
        
        if not games:
            await update.message.reply_text('Список ожидаемых игр пуст.')
        else:
            message = 'Список ожидаемых игр:\n\n'
            for game in games:
                user = await session.query(User).filter_by(id=game.user_id).first()
                message += f'• {game.game_name} (от @{user.username})\n'
            
            await update.message.reply_text(message)