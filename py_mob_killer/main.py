from py_mob_killer.detectors.object_detector import ObjectDetector
from py_mob_killer.screen_capturers.window_screen_capturer import WindowScreenCapturer
from py_mob_killer.filters.hsv_filter import HSVFilter
from py_mob_killer.bots.bot import Bot
import cv2 as cv
from pathlib import Path

CALIBRATION_MODE = True
BOT_ACTIVE = True
WINDOW_NAME = "Ghost FlyFF - Mandarynka"
WINDOW_OFFSET = (10, 30, -10, -10)
FILTER_PARAMETERS_PATH = Path().joinpath(
    "py_mob_killer", "filters", "hsv_filter_parameters.yaml"
)
MONSTER_IMG_PATH = Path().joinpath(
    "py_mob_killer", "targets", "monster_augu_nickname.jpg"
)
PLAYER_IMG_PATH = Path().joinpath("py_mob_killer", "targets", "player_nickname.jpg")

if __name__ == "__main__":
    window_screen_capturer = WindowScreenCapturer(WINDOW_NAME, WINDOW_OFFSET)
    hsv_filter = HSVFilter(FILTER_PARAMETERS_PATH)
    monster_processor = ObjectDetector(MONSTER_IMG_PATH)
    player_processor = ObjectDetector(PLAYER_IMG_PATH)
    killing_bot = Bot()

    if not CALIBRATION_MODE:
        while True:
            raw_screenshot = window_screen_capturer.make_screenshot()
            filtered_screenshot = hsv_filter.apply(raw_screenshot)
            targets_position = image_processor_monster.find_targets_position(
                filtered_screenshot
            )
            player_position = image_processor_player.find_targets_position(
                filtered_screenshot
            )

            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                break

    else:
        hsv_filter.initialize_calibration_gui()
        while True:
            raw_screenshot = window_screen_capturer.make_screenshot()
            filtered_screenshot = hsv_filter.apply(raw_screenshot)
            hsv_filter.update_parameters_from_calibration_gui()
            processed_targets_screenshot = image_processor_monster.draw_targets(
                filtered_screenshot
            )
            processed_targets_and_player_screenshot = (
                image_processor_player.draw_targets(processed_targets_screenshot)
            )
            cv.imshow("Filtered", processed_targets_and_player_screenshot)
            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                break

        hsv_filter.dump_parameters_to_document(cfg.hsv_filter_parameters_path)
