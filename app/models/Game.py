from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Game(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(400), nullable=False)

    user: Mapped["User"] = relationship(back_populates="games")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_game'),
    )