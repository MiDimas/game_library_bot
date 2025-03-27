from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.database import async_session
from app.repositories.base_repo import BaseRepo
from app.models.Game import Game
from app.types.game_types import Game as GameType, GameWithUsername
from app.helpers.exceptions.game_exceptions import GameAlreadyExistsError


class GameRepo(BaseRepo):
    model = Game

    @classmethod
    async def count_games_added_in_period(cls, user_id: int, start_time: datetime, end_time: datetime) -> int:
        async with async_session() as session:
            query = select(func.count()).filter(Game.user_id == user_id, Game.created_at.between(start_time, end_time))
            result = await session.execute(query)
            count = result.scalar_one_or_none()
            return count or 0
        
    @classmethod
    async def count_games_added_today(cls, user_id: int) -> int:
        async with async_session() as session:
            query = select(func.count()).filter(Game.user_id == user_id, Game.created_at.between(datetime.now().date(), datetime.now()))
            result = await session.execute(query)
            count = result.scalar_one_or_none()
            return count or 0

    @classmethod
    async def add_game(cls, user_id: int, game_name: str) -> GameType:
        try:
            async with async_session() as session:
                game = Game(user_id=user_id, name=game_name)
                session.add(game)
                await session.commit()
                await session.refresh(game)
                print(game)
                return GameType.model_validate(game)
        except IntegrityError as e:
            print(e)
            raise GameAlreadyExistsError(f"Игра {game_name} уже в списке ожидания")


    @classmethod
    async def get_games_by_user_telegram_id(cls, user_id: int, limit: int = 10, offset: int = 0) -> list[GameType]:
        async with async_session() as session:
            from app.models.User import User
            query = select(Game.name, Game.created_at, User.username.label('username'))\
                    .join(User, Game.user_id == User.id)\
                    .filter(User.telegram_id == user_id)\
                    .order_by(Game.created_at.desc()).limit(limit).offset(offset)
            result = await session.execute(query)
            games = result.all()

            return [GameType.model_validate(game) for game in games]


    @classmethod
    async def get_all_games(cls, limit: int = 10, offset: int = 0) -> list[GameWithUsername]:
        async with async_session() as session:
            from app.models.User import User
            query = select(Game.name, Game.created_at, User.username\
                    .label('username')).join(User, Game.user_id == User.id)\
                    .order_by(Game.created_at.desc()).limit(limit).offset(offset)
            
            result = await session.execute(query)
            games = result.all()
            return [GameWithUsername.model_validate(game) for game in games]
