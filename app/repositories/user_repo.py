from sqlalchemy import select

from app.models.User import User
from app.repositories.base_repo import BaseRepo
from app.database import async_session
from app.types.user_types.user import User as UserType, FullUser as FullUserType

class UserRepo(BaseRepo):
    model = User

    @classmethod
    async def get_or_create(cls, telegram_id: int, username: str) -> UserType:
        async with async_session() as session:
            query = select(User).filter(User.telegram_id == telegram_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            created_now = False
            if not user: 
                user = User(
                    telegram_id=telegram_id,
                    username=username
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                created_now = True
            user_obj = UserType.model_validate(user)
            print(user_obj)
            user_obj.created_now = created_now
            return user_obj
    
    @classmethod
    async def __get_user_by_telegram_id(cls, telegram_id: int) -> User|None:
        async with async_session() as session:
            query = select(User).filter(User.telegram_id == telegram_id)
            result = await session.execute(query)
            data = result.scalar_one_or_none()
            if not data:
                return None
            return data

    @classmethod
    async def get_user_by_telegram_id(cls, telegram_id: int) -> UserType|None:
        user = await cls.__get_user_by_telegram_id(telegram_id)
        if not user:
            return None
        return UserType.model_validate(user)
    
    @classmethod
    async def get_full_user_by_telegram_id(cls, telegram_id: int) -> FullUserType|None:
        user = await cls.__get_user_by_telegram_id(telegram_id)
        if not user:
            return None
        return FullUserType.model_validate(user)
