from datetime import datetime

from pydantic import BaseModel

class Game(BaseModel):
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class GameWithUsername(Game):
    username: str

class GameFull(Game):
    id: int
    user_id: int
    
    