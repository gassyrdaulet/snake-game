from models.text_entity import TextEntity
from constants.colors import *

class MenuOption(TextEntity):
    def __init__(self, id: str, swipable: str, **kwargs):
        TextEntity.__init__(self, **kwargs)
        
        self.id = id
        if swipable is not None:
            position = kwargs.get("position", (0, 0))
            kwargs.pop("text", None)
            kwargs.pop("position", None)
            self.swipable = TextEntity(text=f"< {swipable} >", position=(70, position[1]), **kwargs)