from turtle import Turtle
from models.simple_game_entity import SimpleGameEntity
from constants.config_keys import *
from config import game_config

class Scoreboard(SimpleGameEntity):
    def __init__(self, font_size = 14):
        SimpleGameEntity.__init__(self) 

        self.score_count = 0
        self.font_size = font_size

        w, h = game_config[CONFIG_KEY_SCREEN_SIZE]
        step = game_config[CONFIG_KEY_GRID_STEP]
        screen_size = (w - step, h - step)
        
        turtle = Turtle()
        turtle.penup()
        turtle.color("white")
        half_width = screen_size[0] // 2
        half_height = screen_size[1] // 2
        turtle.goto(-half_width + 10, half_height - font_size * 2)
        turtle.hideturtle()
        self.turtle = turtle
        self.draw()

        self.update_score()
    
    def draw(self):
        self.update_score()
        self.hidden = False

    def add_score_points(self, amount):
        self.score_count += amount
        self.update_score()

    def reset_score(self):
        self.score_count = 0
        self.update_score()

    def update_score(self):
        self.turtle.clear()
        self.turtle.write(f"Score: {self.score_count}", font=("Arial", self.font_size, "normal"))
