import random
import time
from models.complex_game_entity import ComplexGameEntity, ComplexGameEntitySegment
from constants.counter_keys import *
from constants.config_keys import *
from constants.segment_keys import *
from config import game_config

class BonusFood(ComplexGameEntity):
    def __init__(self, storage):
        ComplexGameEntity.__init__(self, storage) 

        self.scale = 1.3
        self.growing = False
        self.min_scale = 0.7
        self.max_scale = 1
        self.animation_step = 0.01
        self.last_processed_count = None
        self.eatable = False
        self.spawned_date = None
        self.last_update = None

        self.spawn()

    def get_eaten(self) -> float:
        bonus_score_factor = (time.time() - self.spawned_date) / game_config[CONFIG_KEY_BONUS_FOOD_LIFETIME_IN_SECONDS] if self.spawned_date else 0
        self.eatable = False
        self.spawned_date = None
        return bonus_score_factor

    def go_somewhere(self):
        from game_entities.snake import Snake
        from game_entities.food import Food

        snakes = list(self.storage.find_by_class(Snake))
        foods = list(self.storage.find_by_class(Food))
        bonus_foods = list(self.storage.find_by_class(self.__class__))

        bonus_food = self.segments[SEGMENT_KEY_BONUS_FOOD]
        step = game_config[CONFIG_KEY_GRID_STEP]
        width, height = game_config[CONFIG_KEY_SCREEN_SIZE]
        halfx = width // 2 - step
        halfy = height // 2 - step

        while True:
            x = random.randint(- halfx // step, halfx // step) * step
            y = random.randint(- halfy // step, halfy // step) * step
            bonus_food.goto(x, y)
            
            if not any(self != g and g.check_collision(self) for g in snakes + foods + bonus_foods):
                break
    
    def spawn(self):
        bonus_food = ComplexGameEntitySegment()
        bonus_food.shape("circle")
        bonus_food.color("red")
        bonus_food.penup()
        self.segments[SEGMENT_KEY_BONUS_FOOD] = bonus_food

    def render(self):
        food_counter = self.storage.food_counter
        width, height = game_config[CONFIG_KEY_SCREEN_SIZE]

        if food_counter[COUNTER_KEY_FOOD_COUNT] > game_config[CONFIG_KEY_BONUS_FOOD_ONLY_AFTER_X_FOODS] and self.last_processed_count != food_counter[COUNTER_KEY_FOOD_COUNT] and not self.eatable:
            if random.random() < game_config[CONFIG_KEY_BONUS_FOOD_CHANCE]:  
                self.go_somewhere()
                self.eatable = True
                self.spawned_date = time.time()
            self.last_processed_count = food_counter[COUNTER_KEY_FOOD_COUNT]
        
        if self.eatable:
            self.last_processed_count = food_counter[COUNTER_KEY_FOOD_COUNT]
        else:
            self.segments[SEGMENT_KEY_BONUS_FOOD].goto(width * 10, height * 10)
            return
        
        now = time.time()

        if self.storage.is_game_paused and self.last_update is not None:
            self.spawned_date += now - self.last_update
        else: 
            if now - self.spawned_date > game_config[CONFIG_KEY_BONUS_FOOD_LIFETIME_IN_SECONDS]:
                self.eatable = False
                self.spawned_date = None
                self.segments[SEGMENT_KEY_BONUS_FOOD].goto(width * 10, height * 10)
        
        self.last_update = now

        if self.growing:
            self.scale += self.animation_step
            if self.scale >= self.max_scale:
                self.growing = False
        else:
            self.scale -= self.animation_step
            if self.scale <= self.min_scale:
                self.growing = True

        self.segments[SEGMENT_KEY_BONUS_FOOD].shapesize(self.scale)
