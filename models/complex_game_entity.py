from turtle import Turtle
from typing import Deque
from collections import deque
from models.game_entity import GameEntity
from constants.config_keys import *
from constants.config_keys import *
from config import game_config
from models.storage import Storage

class ComplexGameEntity(GameEntity):
    def __init__(self, storage):
        GameEntity.__init__(self)

        self.storage: Storage = storage

        self.segments: dict[str, ComplexGameEntitySegment] = {}
        self.segments_deque: Deque[ComplexGameEntitySegment] = deque([])

    def check_collision(self, target: 'ComplexGameEntity') -> bool:
        for segment in self.segments_deque:
            if any(segment.check_collision(t) for t in target.segments.values()):
                return True
            if any(segment.check_collision(t) for t in target.segments_deque):
                return True
        for segment in self.segments.values():
            if any(segment.check_collision(t) for t in target.segments.values()):
                return True
            if any(segment.check_collision(t) for t in target.segments_deque):
                return True
        return False
    
    def draw(self):
        for s in list(self.segments.values()) + list(self.segments_deque):
            s.showturtle()
            
        self.hidden = False
    
    def make_hidden(self):
        if self.hidden != True:
            self.hidden = True

            for segment in self.segments_deque:
                segment.make_hidden()
            for segment in self.segments.values():
                segment.make_hidden()
        
class ComplexGameEntitySegment(Turtle):
    def __init__(self, collision_width = game_config[CONFIG_KEY_GRID_STEP]):
        Turtle.__init__(self)
        self.collsion_width = collision_width

    def check_collision(self, target: 'ComplexGameEntitySegment') -> bool:
        return self.distance(target) < (self.collsion_width + target.collsion_width) / 2
    
    def make_hidden(self):
        try:
            self.clear()
            self.hideturtle()
        except:
            pass