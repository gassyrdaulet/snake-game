from turtle import bye
from game_entities.border import Border
from models.menu import Menu
from models.menu_option_template import MenuOptionTemplate
from constants.scene_codes import *
from constants.config_keys import *
from config import game_config

class MainMenu(Menu):
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        difficulty_options = {
            0: "Easy",
            1: "Normal",
            2: "Hard",
        }
        on_off_options = {
            0: "Off",
            1: "On"
        }
        is_grid_on_by_default = game_config[CONFIG_KEY_DRAW_GRID]
        default_game_difficulty = game_config[CONFIG_KEY_GAME_DIFFICULTY]
        menu_screens = {
            0: [
                MenuOptionTemplate("main_newgame", "Start new game"),
                MenuOptionTemplate("main_settings", "Settings", False, {}, None, 1),
                MenuOptionTemplate("main_exit", "Exit")
            ],
            1: [
                MenuOptionTemplate("settings_difficulty", "Difficulty", True, difficulty_options, default_game_difficulty),
                MenuOptionTemplate("settings_grid", "Draw grid", True, on_off_options, is_grid_on_by_default),
                MenuOptionTemplate("settings_back", "Back", False, {}, None, 0),
            ],
        }
        Menu.__init__(self, scene_manager, menu_screens) 
        self.storage.objects.add(Border())

    def additional_build(self):
        self.storage.objects.add(Border())

    def process_enter(self, option_id) -> bool:
        if option_id == "main_newgame":
            self.scene_manager.switch_scene(SCENE_CODE_GAME)
            return True
        if option_id == "main_exit":
            bye()
            return True
    
    def process_horizontal_press(self, option_id, selected_value) -> bool:
        if option_id == "settings_grid": game_config[CONFIG_KEY_DRAW_GRID] = selected_value
        elif option_id == "settings_difficulty": game_config[CONFIG_KEY_GAME_DIFFICULTY] = selected_value