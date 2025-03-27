from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.helpers.decorators import async_event_error_handler
from app.events.menu.states import MenuStates

@async_event_error_handler
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_callback = bool(update.callback_query)
    message = update.effective_message
    keyboard = [
        [InlineKeyboardButton("🎮 Добавить игру", callback_data="add_game")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text("Выберите действие:", reply_markup=reply_markup)
        return MenuStates.MENU

    await message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return MenuStates.MENU