from datetime import datetime

from pydantic import BaseModel

class User(BaseModel):
    username: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    created_now: bool | None = None

    class Config:
        from_attributes = True

class FullUser(User):
    id: int
    telegram_id: int
