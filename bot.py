import os
import asyncio

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.events import start
from app.config.main_conf import settings
from app.database import init_db
from app.conversation.conversation_handler import conversation_handler
# Загрузка переменных окружения
load_dotenv()



# def init():
    # Инициализация базы данных
    # asyncio.run(init_db())

async def main():
    # Инициализация базы данных
    await init_db()

    # Получаем токен бота из переменных окружения
    token = settings.TELEGRAM_TOKEN
    # Создаем приложение
    application = Application.builder().token(token).build()
    


    # Добавляем обработчики команд
    application.add_handler(CommandHandler('start', start))
    # application.add_handler(MessageHandler(filters.Regex(r"^🏠 Главное меню$"), menu))
    # application.add_handler(CommandHandler('list', list_games))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_game))
    application.add_handler(conversation_handler)

    # Запускаем бота
    print('Starting bot...')
    await application.initialize()
    await application.updater.start_polling()

    try:
        await application.start()
        await asyncio.Event().wait()
    finally:
        print('Stopping bot...')
        await application.stop()


if __name__ == '__main__':
    # init()
    asyncio.run(main())