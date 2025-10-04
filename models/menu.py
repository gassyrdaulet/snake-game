from typing import List
from models.menu_storage import MenuStorage
from models.scene_manager import SceneManager
from models.scene import Scene
from models.menu_option import MenuOption
from models.menu_option_template import MenuOptionTemplate
from constants.keyboard import *
from constants.colors import *
from constants.text_constants import *

class Menu(Scene):
    def __init__(self, scene_manager: SceneManager, menu_screens: dict[int, List[MenuOptionTemplate]], menu_x_start: int = -100, menu_y_start: int = 100, v_margin: int = 50, font_size: int = 14, color: str = COLOR_WHITE, color_highlighted: str = COLOR_YELLOW):
        Scene.__init__(self)
        self.scene_manager = scene_manager

        storage = MenuStorage()
        storage.menu_screens = menu_screens
        menu_screens_keys_sorted = sorted(storage.menu_screens.keys())
        self.menu_screens_keys_sorted = menu_screens_keys_sorted
        storage.screen = menu_screens_keys_sorted[0]
        storage.selected_option = 0
        for s in menu_screens.values():
            for mot in s:
                if mot.swipable and mot.swipable_values is not None:
                    swipable_values_keys_sorted = sorted(mot.swipable_values.keys())
                    value = swipable_values_keys_sorted[0] if mot.default_swipable_value is None else mot.default_swipable_value
                    if storage.all_swipable_values is None:
                        storage.all_swipable_values = {mot.id: value}
                    else:
                        storage.all_swipable_values[mot.id] = value
        storage.menu_x_start = menu_x_start
        storage.menu_y_start = menu_y_start
        storage.v_margin = v_margin
        storage.font_size = font_size
        storage.color = color
        storage.color_highlighted = color_highlighted
        self.storage = storage

        self.build_menu()

    def build_menu(self):
        self.delete_all_objects()
        storage: MenuStorage = self.storage
        for s in self.menu_screens_keys_sorted:
            if s == storage.screen:
                x = storage.menu_x_start
                y = storage.menu_y_start
                for index, mot in enumerate(storage.menu_screens[s]):
                    converted: MenuOptionTemplate = mot
                    color = storage.color_highlighted if index == storage.selected_option else storage.color
                    swipable = converted.swipable_values[storage.all_swipable_values[converted.id]] if converted.swipable else None
                    option = MenuOption(
                        id=converted.id, 
                        swipable=swipable,
                        text=converted.name,
                        position=(x, y),
                        color=color,
                        align=ALIGN_RIGHT,
                        font_weight=FONT_WEIGHT_BOLD,
                        font_size=storage.font_size
                    )
                    storage.objects.add(option)
                    if hasattr(option, "swipable") and option.swipable is not None: storage.objects.add(option.swipable)
                    y -= storage.v_margin

    def additional_build(self):
        pass
    
    def process_horizontal_press(self, _, __):
        return False

    def process_enter(self, _) -> bool:
        return False

    def process_key_press(self, key: str):
        dontrebuild = False
        storage: MenuStorage = self.storage
        mot: MenuOptionTemplate = storage.menu_screens[storage.screen][storage.selected_option]
        if key in (KEYBOARD_UP, KEYBOARD_DOWN):
            items = storage.menu_screens[storage.screen]
            change = 1 if key == KEYBOARD_DOWN else -1
            i = storage.selected_option
            if i + change < len(items) and i + change >= 0:
                storage.selected_option = i + change
            else:
                storage.selected_option = 0 if key == KEYBOARD_DOWN else len(items) - 1
        elif key in (KEYBOARD_LEFT, KEYBOARD_RIGHT):
            if mot.swipable:
                items = sorted(mot.swipable_values.keys())
                change = -1 if key == KEYBOARD_LEFT else 1
                i = items.index(storage.all_swipable_values[mot.id])
                if i + change < len(items) and i + change >= 0:
                    storage.all_swipable_values[mot.id] = items[i + change]
                else:
                    storage.all_swipable_values[mot.id] = items[0] if key == KEYBOARD_RIGHT else items[len(items) - 1]
                dontrebuild = self.process_horizontal_press(mot.id, storage.all_swipable_values[mot.id])
        elif key == KEYBOARD_ENTER:
            if mot.change_screen is not None:
                storage.screen = mot.change_screen
                storage.selected_option = 0
            dontrebuild = self.process_enter(mot.id)
        if not dontrebuild:
            self.build_menu()
            self.additional_build()