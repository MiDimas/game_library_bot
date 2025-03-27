from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from app.events.menu.states import MenuStates
from app.events.add_game import start_add_game, add_game, approve_game
from app.events.menu.menu import menu
from app.events.check_games.check_my_games import check_my_games
from app.events.check_games.check_games import check_games
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
            CallbackQueryHandler(start_add_game, pattern="^add_game$"),
            CallbackQueryHandler(check_my_games, pattern="^check_my_games$"),
            CallbackQueryHandler(check_games, pattern="^admin_check_games$")
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
        MenuStates.ADMIN_LIST_GAMES: [
            CallbackQueryHandler(check_games, pattern="^\d+$"),
            CallbackQueryHandler(menu, pattern="^cancel$"),
        ]
    },
    fallbacks=menu_handlers,
    conversation_timeout=600
)