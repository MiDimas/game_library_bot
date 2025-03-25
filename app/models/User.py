from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base 

class User(Base):
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(400))
    is_admin: Mapped[bool] = mapped_column(default=False)

    games: Mapped[list["Game"]] = relationship(back_populates="user", cascade="all, delete-orphan")
