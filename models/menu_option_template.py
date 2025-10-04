
class MenuOptionTemplate:
    def __init__(self, id: str, name: str, swipable: bool = False, swipable_values: dict[int, str] = {}, default_swipable_value: str = None, change_screen: str = None):
        self.id = id
        self.name = name
        self.swipable = swipable
        self.swipable_values = swipable_values
        self.default_swipable_value = default_swipable_value
        self.change_screen = change_screen