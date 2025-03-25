from functools import wraps
from typing import Callable, Any, Coroutine

from telegram import Update
from telegram.ext import ContextTypes


def async_event_error_handler(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]]):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Coroutine[Any, Any, None]:
        try:
            return await func(update, context)
        except Exception as e:
            print(e)
            return await update.message.reply_text("Я сломался, скажи администратору если можешь и попробуй позже")
    return wrapper