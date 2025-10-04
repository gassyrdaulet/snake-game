from turtle import Turtle
from models.complex_game_entity import GameEntity

class SimpleGameEntity(GameEntity):
    def __init__(self):
        GameEntity.__init__(self)
        self.turtle = Turtle()

    def draw(self):
        self.turtle.showturtle()
        self.hidden = False
    
    def make_hidden(self):
        try:
            if self.hidden != True:
                self.hidden = True
                self.turtle.clear()
                self.turtle.hideturtle()
        except:
            pass