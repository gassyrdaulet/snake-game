import random
from models.complex_game_entity import ComplexGameEntity, ComplexGameEntitySegment
from constants.config_keys import *
from constants.segment_keys import *
from config import game_config

class Food(ComplexGameEntity):
    def __init__(self, storage):
        ComplexGameEntity.__init__(self, storage) 

        self.spawn()

    def go_somewhere(self):
        from game_entities.snake import Snake
        from game_entities.bonus_food import BonusFood

        snakes = list(self.storage.find_by_class(Snake))
        bonus_foods = list(self.storage.find_by_class(BonusFood))
        foods = list(self.storage.find_by_class(self.__class__))

        food = self.segments[SEGMENT_KEY_FOOD]
        step = game_config[CONFIG_KEY_GRID_STEP]
        width, height = game_config[CONFIG_KEY_SCREEN_SIZE]
        halfx = width // 2 - step
        halfy = height // 2 - step

        while True:
            x = random.randint(- halfx // step, halfx // step) * step
            y = random.randint(- halfy // step, halfy // step) * step

            food.goto(x, y)

            if not any(self != g and g.check_collision(self) for g in snakes + bonus_foods + foods):
                break

    def spawn(self):
        segment = ComplexGameEntitySegment()
        segment.shape("circle")
        segment.color("red")
        segment.penup()
        segment.shapesize(0.55)
        self.segments[SEGMENT_KEY_FOOD] = segment

        self.go_somewhere()

    