import time
import math
from turtle import Turtle
from constants.directions import *
from constants.config_keys import *
from constants.counter_keys import *
from constants.keyboard import *
from constants.segment_keys import *
from models.complex_game_entity import ComplexGameEntity, ComplexGameEntitySegment
from game_entities.scoreboard import Scoreboard
from game_entities.food import Food
from game_entities.bonus_food import BonusFood
from collections import deque
from typing import Deque
from config import game_config

class Snake(ComplexGameEntity):
    def __init__(self, storage):
        ComplexGameEntity.__init__(self, storage)
        self.direction_movement_mappings = {
            DIRECTION_DOWN: (0,-1),
            DIRECTION_LEFT: (-1,0),
            DIRECTION_UP: (0,1),
            DIRECTION_RIGHT: (1,0),
            DIRECTION_STOP: (0,1),
        }
        self.control_step = game_config[CONFIG_KEY_GRID_STEP]
        self.last_moved_time = None
        self.speed = { 0: 0.12, 1: 0.08, 2: 0.06}[game_config[CONFIG_KEY_GAME_DIFFICULTY]]
        self.food_points_factor = { 0: 0.5, 1: 1, 2: 1.5}[game_config[CONFIG_KEY_GAME_DIFFICULTY]]
        self.calculated_common_food_eat_points = math.floor(self.food_points_factor * game_config[CONFIG_KEY_COMMON_FOOD_EAT_POINTS])
        self.spawn()

    def memorize_input(self, direction: str):
        if len(self.input_buffer) > game_config[CONFIG_KEY_SNAKE_INPUT_BUFFER_SIZE] or not self.alive:
            return
        self.input_buffer.append(direction)

    def move(self):
        head = self.segments[SEGMENT_KEY_SNAKE_HEAD]
        control_step = self.control_step
        if head.direction == DIRECTION_STOP: return
        self.move_segment(head)
        for index in range(len(self.segments_deque)-1, -1, -1):
            s = self.segments_deque[index]
            self.move_segment(s)
            if s.xcor() % control_step == 0 and s.ycor() % control_step == 0:
                if index == 0:
                    s.direction = head.direction
                else:
                    previos_segment = self.segments_deque[index - 1]
                    s.direction = previos_segment.direction

    def move_segment(self, segment):
        tr = game_config[CONFIG_KEY_TICKRATE]
        step = (self.control_step * tr) / self.speed
        width, height = game_config[CONFIG_KEY_SCREEN_SIZE]
        halfx = width // 2
        halfy = height // 2
        x = segment.xcor()
        y = segment.ycor()

        segment.setx(x + step * self.direction_movement_mappings[segment.direction][0])
        segment.sety(y + step * self.direction_movement_mappings[segment.direction][1])

        x = segment.xcor()
        y = segment.ycor()
        if x>=halfx:
            segment.setx(step - halfx)
        elif x<=-halfx:
            segment.setx(halfx - step)
        if y>=halfy:
            segment.sety(step - halfy)
        elif y<=-halfy:
            segment.sety(halfy - step)

    def apply_direction_change_from_buffer(self):
        head = self.segments[SEGMENT_KEY_SNAKE_HEAD] 
        x = head.xcor()
        y = head.ycor()
        step = game_config[CONFIG_KEY_GRID_STEP]

        if len(self.input_buffer) > 0 and x % step == 0 and y % step == 0:
            head = self.segments[SEGMENT_KEY_SNAKE_HEAD]
            new_direction = self.input_buffer.popleft()
            if (new_direction == DIRECTION_UP and head.direction != DIRECTION_DOWN) or \
            (new_direction == DIRECTION_DOWN and head.direction != DIRECTION_UP) or \
            (new_direction == DIRECTION_LEFT and head.direction != DIRECTION_RIGHT) or \
            (new_direction == DIRECTION_RIGHT and head.direction != DIRECTION_LEFT):
                head.direction = new_direction

    def grow(self):
        tail_last_segment = self.segments_deque[len(self.segments_deque) - 1] if self.segments_deque else self.segments[SEGMENT_KEY_SNAKE_HEAD]
        x = tail_last_segment.xcor() + self.control_step * -self.direction_movement_mappings[tail_last_segment.direction][0]
        y = tail_last_segment.ycor() + self.control_step * -self.direction_movement_mappings[tail_last_segment.direction][1]
        new_segment = SnakeTailPart(tail_last_segment.direction, (x, y))
        self.segments_deque.append(new_segment)

    def spawn(self):
        self.input_buffer = deque([])        
        head = SnakeHead()
        head.penup()
        head.goto(0, 0)
        self.segments: dict[str, SnakeHead] = { SEGMENT_KEY_SNAKE_HEAD: head }
        self.segments_deque: Deque[SnakeTailPart] = deque([])
        self.alive = True
        self.grow()
        self.draw()
    
    def render(self):
        if not self.alive: return

        self.apply_direction_change_from_buffer()
        
        storage = self.storage
        head = self.segments[SEGMENT_KEY_SNAKE_HEAD] 

        if any(head.check_collision(tail_part) for tail_part in self.segments_deque):
            time.sleep(game_config[CONFIG_KEY_FREEZE_TIME_AFTER_DEATH])
            self.alive = False
            storage.is_game_over = True

        for food in storage.find_by_class(Food):
            if head.check_collision(food.segments[SEGMENT_KEY_FOOD]):
                storage.food_counter[COUNTER_KEY_FOOD_COUNT] += 1
                storage.apply_to_class(Scoreboard, lambda o: o.add_score_points(self.calculated_common_food_eat_points))
                food.go_somewhere()
                self.grow()

        for bonus_food in storage.find_by_class(BonusFood):
            if bonus_food.eatable and head.check_collision(bonus_food.segments[SEGMENT_KEY_BONUS_FOOD]):
                storage.apply_to_class(Scoreboard, lambda o: o.add_score_points(math.floor(game_config[CONFIG_KEY_BONUS_FOOD_SCORE_POINTS] * bonus_food.get_eaten() * self.food_points_factor)))
                self.grow()

        if self.alive: self.move()

class SnakeHead(ComplexGameEntitySegment):
    def __init__(self):
        ComplexGameEntitySegment.__init__(self)
        self.collsion_width = game_config[CONFIG_KEY_GRID_STEP] // 2
        self.direction = DIRECTION_STOP
        self.shape("square")
        self.color("green") 
        self.shapesize(game_config[CONFIG_KEY_GRID_STEP] / 20)

class SnakeTailPart(ComplexGameEntitySegment):
    def __init__(self, direction: str, cords: tuple):
        ComplexGameEntitySegment.__init__(self)
        self.collsion_width = game_config[CONFIG_KEY_GRID_STEP] // 2
        self.direction = direction
        self.penup()
        self.shape("square")
        self.color("green")
        self.shapesize(game_config[CONFIG_KEY_GRID_STEP] / 20)
        self.goto(*cords)