from app.repositories.base_repo import BaseRepo
from app.models.Game import Game

class GameRepo(BaseRepo):
    model = Game
