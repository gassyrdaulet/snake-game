from turtle import Turtle
from constants.config_keys import *
from config import game_config
from models.simple_game_entity import SimpleGameEntity

class Grid(SimpleGameEntity):
    def __init__(self):        
        SimpleGameEntity.__init__(self) 
        
        self.hidden: bool = not game_config[CONFIG_KEY_DRAW_GRID] if isinstance(game_config[CONFIG_KEY_DRAW_GRID], bool) else True
        
        grid = Turtle()
        grid.speed(0)
        grid.color(game_config[CONFIG_KEY_GRID_COLOR])
        grid.penup()
        grid.hideturtle()
        self.turtle = grid

        if not self.hidden:
            self.draw()

    def draw(self):
        w, h = game_config[CONFIG_KEY_SCREEN_SIZE]
        step = game_config[CONFIG_KEY_GRID_STEP]
        size = (w - step, h - step)
        halfx = size[0] // 2
        halfy = size[1] // 2

        for x in range(-halfx, halfx + 1, step):
            self.turtle.goto(x, -halfy)
            self.turtle.pendown()
            self.turtle.goto(x, halfy)
            self.turtle.penup()

        for y in range(-halfy, halfy + 1, step):
            self.turtle.goto(-halfx, y)
            self.turtle.pendown()
            self.turtle.goto(halfx, y)
            self.turtle.penup()

        self.hidden = False