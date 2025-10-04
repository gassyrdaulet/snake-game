from collections import Counter
from models.storage import Storage
from config import game_config
from constants.config_keys import *

class GameStorage(Storage):
    def __init__(self):
        super().__init__()
        self.is_game_paused: bool = False
        self.is_game_over: bool = False
        self.food_counter = Counter()
        self.game_difficulty = game_config[CONFIG_KEY_GAME_DIFFICULTY]