from sqlalchemy import select

from app.models.User import User
from app.repositories.base_repo import BaseRepo
from app.database import async_session
from app.types.user_types.user import User as UserType

class UserRepo(BaseRepo):
    model = User

    async def get_or_create(self, telegram_id: int, username: str) -> User:
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
        
    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        async with async_session() as session:
            query = select(User).filter(User.telegram_id == telegram_id)
            result = await session.execute(query)
            data = result.scalar_one_or_none()
            if not data:
                return None
            return UserType.model_validate(data)
