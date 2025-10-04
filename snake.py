from models.scene_manager import SceneManager
from constants.scene_codes import *
from scenes.game import Game
from scenes.main_menu import MainMenu

scenes: dict[int, type] = {
    SCENE_CODE_MAIN_MENU: MainMenu,
    SCENE_CODE_GAME: Game,
}

SceneManager(scenes).render()