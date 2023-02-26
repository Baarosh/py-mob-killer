from pathlib import Path

from cv2 import destroyAllWindows, waitKey

from mob_killer.bots.bot import Bot
from mob_killer.detectors.object_detector import ObjectDetector
from mob_killer.filters.hsv_filter import HSVFilter
from mob_killer.screen_capturers.window_screen_capturer import \
    WindowScreenCapturer
from mob_killer.utils import draw_rectangles, get_center_points, show_image

CALIBRATION_MODE = True
WINDOW_NAME = "Ghost Flyff - Mandarynka"
FILTER_PARAMS_PATH = Path().joinpath("mob_killer", "filters", "hsv_filter_params.yaml")
MONSTER_IMG_PATH = Path().joinpath("mob_killer", "targets", "monster_augu_nickname.jpg")


def run(
    window_screen_capturer,
    hsv_filter,
    object_detector,
    player_processor,
    killing_bot,
):
    ...


def run_debug(
    window_screen_capturer,
    hsv_filter,
    object_detector,
    player_processor,
    killing_bot,
):
    ...


if __name__ == "__main__":
    window_screen_capturer = WindowScreenCapturer(WINDOW_NAME)
    hsv_filter = HSVFilter(FILTER_PARAMS_PATH)
    object_detector = ObjectDetector(MONSTER_IMG_PATH)
    bot = Bot(window_screen_capturer.coordinates)

    hsv_filter.init_calibration_gui()
    print("Window coords: ", window_screen_capturer.coordinates)

    while True:
        raw_image = window_screen_capturer.make_screenshot()
        filtered_image = hsv_filter.apply(raw_image)
        hsv_filter.update_params_from_gui()
        objects_positions = object_detector.detect_all(raw_image)
        draw_rectangles(filtered_image, objects_positions)
        show_image("Eyes of bot", filtered_image)

        objects_points = get_center_points(objects_positions)
        bot.make_action(objects_points)

        if waitKey(1) == ord("q"):
            destroyAllWindows()
            break

    hsv_filter.dump_params_to_file()
