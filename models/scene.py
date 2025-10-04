from turtle import Screen
from models.storage import Storage
from models.complex_game_entity import ComplexGameEntity
from models.simple_game_entity import SimpleGameEntity
from constants.keyboard import *

class Scene:
    def __init__(self):
        self.set_control_keys()
        self.storage = Storage()

    def delete_all_objects(self):
        for o in self.storage.objects:
            if isinstance(o, (ComplexGameEntity, SimpleGameEntity)):
                o.make_hidden()
        self.storage.objects.clear()

    def process_key_press(self):
        pass
                    
    def set_control_keys(self):
        screen = self.screen
        for key in self.listening_keys:
            screen.onkey(lambda k=key: self.process_key_press(k), key)

    def render(self):
        pass

    def __del__(self):
        try:
            self.delete_all_objects()
            screen = self.screen
            for key in self.listening_keys:
                screen.onkey(None, key)
        except: pass

    screen = Screen()
    storage: Storage
    listening_keys = (
        KEYBOARD_UP, KEYBOARD_DOWN, KEYBOARD_LEFT, KEYBOARD_RIGHT, KEYBOARD_ENTER, KEYBOARD_ESC, KEYBOARD_SPACE,
        KEYBOARD_P, KEYBOARD_G, KEYBOARD_R, KEYBOARD_M
    )