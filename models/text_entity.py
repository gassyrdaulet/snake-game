from models.simple_game_entity import SimpleGameEntity
from constants.colors import *
from constants.text_constants import *
from constants.config_keys import *
from config import game_config

class TextEntity(SimpleGameEntity):
    def __init__(self, text: str, position=(0,0), color=COLOR_WHITE, align=ALIGN_CENTER, font_weight=FONT_WEIGHT_NORMAL, font=game_config[CONFIG_KEY_DEFAULT_FONT], font_size=game_config[CONFIG_KEY_DEFAULT_FONT_SIZE]):
        SimpleGameEntity.__init__(self)
        self.text = text
        self.position = position
        self.align = align
        self.font_weight = font_weight
        self.font = font
        self.font_size = font_size
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.goto(position)
        self.turtle.color(color)
        self.turtle.write(text, align, font=(font, font_size, font_weight))

    def draw(self):
        self.update_text()
        self.hidden = False

    def update_text(self):
        self.turtle.clear()
        self.turtle.write(self.text, align=self.align, font=(self.font, self.font_size, self.font_weight))