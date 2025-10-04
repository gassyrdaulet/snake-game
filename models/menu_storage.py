from models.storage import Storage

class MenuStorage(Storage):
    def __init__(self):
        super().__init__()
        self.all_swipable_values: dict[str, str] = None
        self.selected_option: str
        self.screen: str
        self.menu_screens: dict[str, list[object]]
        self.menu_x_start: int
        self.menu_y_start: int
        self.v_margin: int
        self.font_size: int
        self.color: str
        self.color_highlighted: str