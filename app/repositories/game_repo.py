from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.database import async_session
from app.repositories.base_repo import BaseRepo
from app.models.Game import Game
from app.types.game_types import Game as GameType
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

