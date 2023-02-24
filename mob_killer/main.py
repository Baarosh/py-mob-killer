from mob_killer.detectors.object_detector import ObjectDetector
from mob_killer.screen_capturers.window_screen_capturer import WindowScreenCapturer
from mob_killer.filters.hsv_filter import HSVFilter
from mob_killer.bots.bot import Bot
from pathlib import Path
from mob_killer.utils import run, run_debug

CALIBRATION_MODE = True
BOT_ACTIVE = True
WINDOW_NAME = "Ghost Flyff - Mandarynka"
FILTER_PARAMS_PATH = Path().joinpath("mob_killer", "filters", "hsv_filter_params.yaml")
MONSTER_IMG_PATH = Path().joinpath("mob_killer", "targets", "monster_augu_nickname.jpg")
PLAYER_IMG_PATH = Path().joinpath("mob_killer", "targets", "player_nickname.jpg")

if __name__ == "__main__":
    window_screen_capturer = WindowScreenCapturer(WINDOW_NAME)
    hsv_filter = HSVFilter(FILTER_PARAMS_PATH)
    monster_processor = ObjectDetector(MONSTER_IMG_PATH)
    player_processor = ObjectDetector(PLAYER_IMG_PATH)
    killing_bot = Bot()

    if CALIBRATION_MODE:
        run_debug(
            window_screen_capturer,
            hsv_filter,
            monster_processor,
            player_processor,
            killing_bot,
        )
    else:
        run(
            window_screen_capturer,
            hsv_filter,
            monster_processor,
            player_processor,
            killing_bot,
        )
