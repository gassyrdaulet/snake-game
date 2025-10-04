from turtle import Turtle
from constants.config_keys import *
from config import game_config
from models.simple_game_entity import SimpleGameEntity

class Border(SimpleGameEntity):
    def __init__(self):        
        SimpleGameEntity.__init__(self) 
        
        border = Turtle()
        border.speed(0)
        border.color(game_config[CONFIG_KEY_GRID_COLOR])
        border.penup()
        border.hideturtle()
        self.turtle = border

        self.draw()

    def draw(self):
        w, h = game_config[CONFIG_KEY_SCREEN_SIZE]
        step = game_config[CONFIG_KEY_GRID_STEP]
        size = (w - step, h - step)
        
        halfx = size[0] // 2 
        halfy = size[1] // 2

        self.turtle.penup()
        self.turtle.goto(-halfx, -halfy)
        self.turtle.pendown()

        for _ in range(2):
            self.turtle.forward(size[0])
            self.turtle.left(90)
            self.turtle.forward(size[1])
            self.turtle.left(90)

        self.turtle.penup()

        self.hidden = False