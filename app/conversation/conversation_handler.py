from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from app.events.menu.states import MenuStates
from app.events.add_game import start_add_game, add_game
from app.events.menu.menu import menu

conversation_handler = ConversationHandler(
    entry_points=[
            CommandHandler('menu', menu),
            CallbackQueryHandler(menu, pattern="^menu$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"^🏠 Главное меню$"), menu)
        ],
    states={
        MenuStates.MENU: [
            CallbackQueryHandler(start_add_game, pattern="^add_game$")
        ],
        MenuStates.ADD_GAME: [
            CallbackQueryHandler(menu, pattern="^menu$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_game)
        ],
        MenuStates.UNDEFINED: [
            CommandHandler('menu', menu),
            CallbackQueryHandler(menu, pattern="^menu$"),
        ]
    },
    fallbacks=[CommandHandler('cancel', menu)]
)