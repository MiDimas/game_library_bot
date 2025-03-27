from functools import wraps
from typing import Callable, Any, Coroutine

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


from app.events.menu.states import MenuStates
def async_event_error_handler(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Coroutine[Any, Any, None]:
        try:
            return await func(update, context)
        except Exception as e:
            message = update.effective_message
            keyboard = [
                [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            print(e)
            await message.reply_text("Я сломался, скажи администратору если можешь и попробуй позже \n\n"
                                     "Чтобы вернуться в главное меню, нажми '🏠 Главное меню'",
                                     reply_markup=reply_markup
                                     )
            return MenuStates.UNDEFINED
    return wrapper