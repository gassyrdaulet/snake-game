from storages.game_storage import GameStorage
from models.scene_manager import SceneManager
from models.scene import Scene
from models.game_entity import GameEntity
from models.text_entity import TextEntity
from game_entities.scoreboard import Scoreboard
from game_entities.border import Border
from game_entities.grid import Grid
from game_entities.food import Food
from game_entities.bonus_food import BonusFood
from game_entities.snake import Snake
from constants.counter_keys import *
from constants.directions import *
from constants.keyboard import *
from constants.text_constants import *
from constants.scene_codes import *

class Game(Scene):
    def __init__(self, scene_manager: SceneManager):
        Scene.__init__(self)
        self.scene_manager = scene_manager
        self.start_new_game()

    def start_new_game(self):
        self.delete_all_objects()
        storage = GameStorage()
        self.storage = storage
        storage = self.storage
        storage.is_game_paused = False
        storage.is_game_over = False
        storage.food_counter[COUNTER_KEY_FOOD_COUNT] = 0
        storage.objects.add(Border())
        storage.objects.add(Grid())
        storage.objects.add(Scoreboard())
        storage.objects.add(Food(storage))
        storage.objects.add(BonusFood(storage))
        storage.objects.add(Snake(storage))
        self.pause_texts = {
            TextEntity("Game paused. Press SPACEBAR to resume.", (-180, 10), align=ALIGN_RIGHT),
            TextEntity("Press ESC to return to the Main Menu.", (-180, -20), align=ALIGN_RIGHT),
        }
        self.game_over_texts = {
            TextEntity("Game over. Press SPACEBAR to try again.", (-180, 10), align=ALIGN_RIGHT),
            TextEntity("Press ESC to return to the Main Menu.", (-180, -20), align=ALIGN_RIGHT),
        }
        for t in self.pause_texts | self.game_over_texts:
            t.make_hidden()
            storage.objects.add(t)
            
    def pause_game(self):
        new_value = not self.storage.is_game_paused
        self.storage.is_game_paused = new_value
        for t in self.pause_texts:
            if new_value: t.draw()
            else: t.make_hidden()

    def show_game_over_messages(self):
        for t in self.game_over_texts: t.draw()

    def process_key_press(self, key: str):
        if key in (KEYBOARD_UP, KEYBOARD_DOWN, KEYBOARD_LEFT, KEYBOARD_RIGHT):
            if not self.storage.is_game_paused:
                self.storage.apply_to_class(Snake, lambda o: o.memorize_input(self.directions_mapping[key]), True)
        elif key == KEYBOARD_ESC and (self.storage.is_game_paused or self.storage.is_game_over):
            self.scene_manager.switch_scene(SCENE_CODE_MAIN_MENU)
        elif key == KEYBOARD_ESC:
            self.pause_game()
        elif key == KEYBOARD_SPACE and self.storage.is_game_paused:
            self.pause_game()
        elif key == KEYBOARD_SPACE and self.storage.is_game_over:
            self.start_new_game()

    def render(self):
        if self.storage.is_game_over: self.show_game_over_messages()
        if not self.storage.is_game_paused:
            for item in self.storage.objects:
                if isinstance(item, GameEntity):
                    item.render()

    directions_mapping = {
        KEYBOARD_UP: DIRECTION_UP,
        KEYBOARD_DOWN: DIRECTION_DOWN,
        KEYBOARD_LEFT: DIRECTION_LEFT,
        KEYBOARD_RIGHT: DIRECTION_RIGHT,
    }