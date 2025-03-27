from telegram.ext import ContextTypes
from telegram.error import TelegramError
async def check_subscription (context: ContextTypes.DEFAULT_TYPE, chat_id: str|int, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except TelegramError as e:
        print(e)
        print("проверка не удалась")
        return False
    except Exception as e:
        print(e)
        print("Произошла ошибка при проверке подписки")
        return False