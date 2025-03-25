from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Game(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    game_name: Mapped[str] = mapped_column(String(400), nullable=False)

    user: Mapped["User"] = relationship(back_populates="games")