from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from app.events.menu.states import MenuStates
from app.events.add_game import start_add_game, add_game, approve_game
from app.events.menu.menu import menu

menu_handlers = [
            CommandHandler('menu', menu),
            CallbackQueryHandler(menu, pattern="^menu$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"^🏠 Главное меню$"), menu)
        ]

conversation_handler = ConversationHandler(
    entry_points=menu_handlers,
    states={
        MenuStates.UNDEFINED: [],
        MenuStates.START: [],
        MenuStates.MENU: [
            CallbackQueryHandler(start_add_game, pattern="^add_game$")
        ],
        MenuStates.ADD_GAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(r"^🏠 Главное меню$"), add_game)
        ],
        MenuStates.APPROVE_GAME: [
            CallbackQueryHandler(approve_game, pattern="^approve_game$"),
            CallbackQueryHandler(menu, pattern="^cancel$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r"^Да$"), approve_game),
            MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(r"^Да$"), add_game),
        ],
    },
    fallbacks=menu_handlers,
    conversation_timeout=600
)