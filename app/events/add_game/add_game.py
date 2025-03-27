from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from app.helpers.decorators.event_error_handler import async_event_error_handler
from app.events.menu.states import MenuStates
from app.repositories.user_repo import UserRepo
from app.repositories.game_repo import GameRepo
from app.helpers.checks import check_subscription
from app.config.main_conf import settings
from app.helpers.exceptions.game_exceptions import GameAlreadyExistsError

keyboard_cancel = [
    [InlineKeyboardButton("Отмена", callback_data="menu")]
]
reply_markup_cancel = InlineKeyboardMarkup(keyboard_cancel)

keyboard_in_menu = [
    [InlineKeyboardButton("Назад к главному меню", callback_data="menu")]
]
reply_markup_in_menu = InlineKeyboardMarkup(keyboard_in_menu)

@async_event_error_handler      
async def start_add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Начало добавления игры'''

    print(update)
    await update.callback_query.answer()
    if not await check_subscription(context, settings.CHANNEL_ID, update.effective_user.id):
        await update.callback_query.message.edit_text('Вы не подписаны на канал. \n\n'
                                                       f'Пожалуйста, подпишитесь на канал {settings.CHANNEL_ID} и попробуйте снова.')
        return MenuStates.MENU
    
    user = await UserRepo.get_full_user_by_telegram_id(update.effective_user.id)
    if not user:
        await update.callback_query.message.edit_text('Пожалуйста, сначала используйте команду /start')
        return MenuStates.UNDEFINED
    
    context.user_data['user_id'] = user.id

    
    count_games_added_today = await GameRepo.count_games_added_today(user.id) 

    if settings.MAX_GAMES_PER_DAY and count_games_added_today >= settings.MAX_GAMES_PER_DAY:
        await update.callback_query.message.edit_text('Вы достигли максимального количества игр для добавления в день. \n\n'\
                                        'Попробуйте добавить игру завтра.', reply_markup=reply_markup_in_menu)
        return MenuStates.MENU


    await update.callback_query.message.edit_text('Введите название игры, низкую цену на которую вы ждете. \n\n'
                                                   'Или нажмите "Отмена" чтобы вернуться в главное меню', 
                                                   reply_markup=reply_markup_cancel)

    return MenuStates.ADD_GAME

async def add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Добавление названия игры'''
    
    game_name = update.message.text.strip()
    if len(game_name) < 3 or len(game_name) > 300: 
        await update.message.reply_text('Название игры должно быть от 3 до 300 символов.', reply_markup=reply_markup_cancel)
        return MenuStates.ADD_GAME
    
    game_name = game_name.lower()

    print(game_name)

    context.user_data['pending_game'] = game_name

    keyboard = [
        [InlineKeyboardButton("✅ Добавить игру", callback_data="approve_game")],
        [InlineKeyboardButton("🚫 Отменить", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Вы хотите добавить игру {game_name} в список ожидания? \n\n'
                                    'Чтобы подтвердить, нажмите "✅ Добавить игру" \n\n'
                                    'Чтобы отменить добавление, нажмите "🚫 Отменить" \n\n'
                                    'Чтобы изменить название, напишите новое название игры',
                                    reply_markup=reply_markup
                                    )

    return MenuStates.APPROVE_GAME

async def approve_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Подтверждение добавления игры'''
    is_callback = update.callback_query is not None
    message = update.effective_message

    if is_callback:
        await update.callback_query.answer()

    game_name = context.user_data.get('pending_game', '')
    user_id = context.user_data.get('user_id', None)
    if not game_name:
        result = 'Ничего не добавлено. \n\n'\
                'Чтобы добавить игру, нажмите "🎮 Добавить еще одну игру" \n\n'\
                'Чтобы вернуться в главное меню, нажмите "🏠 Главное меню"'
        if is_callback: await message.edit_text(result, reply_markup=reply_markup_in_menu)
        else: await message.reply_text(result, reply_markup=reply_markup_in_menu)
        return MenuStates.UNDEFINED
    
    if not user_id:
        result = 'Произошла ошибка. \n\n'\
                'Пожалуйста, попробуйте снова.'
        if is_callback: await message.edit_text(result, reply_markup=reply_markup_in_menu)
        else: await message.reply_text(result, reply_markup=reply_markup_in_menu)
        return MenuStates.UNDEFINED
    
    if 'pending_game' in context.user_data:
        del context.user_data['pending_game']
    try:
        game = await GameRepo.add_game(user_id, game_name)
    except GameAlreadyExistsError as e:
        result = str(e)
        if is_callback: await message.edit_text(result, reply_markup=reply_markup_cancel)
        else: await message.reply_text(result, reply_markup=reply_markup_cancel)
        return MenuStates.ADD_GAME

    keyboard = [
        [InlineKeyboardButton("🎮 Добавить еще одну игру", callback_data="add_game")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    result = f'Игра {game.name} успешно добавлена в список ожидания! \n\n'\
            'Чтобы добавить еще одну игру, нажмите "🎮 Добавить еще одну игру" \n\n'\
            'Чтобы вернуться в главное меню, нажмите "🏠 Главное меню"'
    if is_callback: await message.edit_text(result, reply_markup=reply_markup)
    else: await update.message.reply_text(result,reply_markup=reply_markup)

    return MenuStates.MENU