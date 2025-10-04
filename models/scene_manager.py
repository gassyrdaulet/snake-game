import time
from config import game_config
from turtle import Screen, Terminator
from constants.config_keys import *

class SceneManager():
    def __init__(self, all_scenes: dict[int, type], default_scene_id = None):
        for dim in game_config[CONFIG_KEY_SCREEN_SIZE]:
            if dim % (game_config[CONFIG_KEY_GRID_STEP] * 2) != 0:
                raise ValueError(f"Screen sizes must be divisible by {CONFIG_KEY_GRID_STEP} * 2 ({game_config[CONFIG_KEY_GRID_STEP]*2})")
        screen = Screen()
        screen.title(game_config[CONFIG_KEY_GAME_TITLE])
        screen.bgcolor(game_config[CONFIG_KEY_SCREEN_BACKGROUND_COLOR])
        screen.setup(*game_config[CONFIG_KEY_SCREEN_SIZE])
        screen.tracer(0) 
        screen.listen()
        self.screen = screen
        self.all_scenes = all_scenes
        scene_keys_sorted = sorted(all_scenes.keys())
        default_scene = all_scenes.get(default_scene_id, all_scenes[scene_keys_sorted[0]])
        self.active_scene = default_scene(self)

    def switch_scene(self, id: int):
        self.active_scene.delete_all_objects()
        for scene_key in self.all_scenes.keys():
            if scene_key == id:
                self.active_scene = self.all_scenes[id](self)

    def render(self):
        try:
            while True:
                self.active_scene.render()
                self.screen.update()
                time.sleep(game_config[CONFIG_KEY_TICKRATE])
        except Terminator: pass