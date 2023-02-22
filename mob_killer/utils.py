from yaml import safe_load as yaml_safe_load, safe_dump as yaml_safe_dump, YAMLError
from cv2 import (
    waitKey as cv_waitKey,
    imshow as cv_imshow,
    destroyAllWindows as cv_destroyAllWindows,
)


def load_yaml_document(path):
    with open(path, "r") as stream:
        try:
            return yaml_safe_load(stream)
        except YAMLError as exc:
            # log instead
            print(f"Failed to load yaml document. Traceback: {exc}")


def dump_yaml_document(data, path):
    with open(path, "w") as stream:
        try:
            yaml_safe_dump(data, stream)
        except YAMLError as exc:
            # log instead
            print(f"Failed to dump yaml document. Traceback: {exc}")


def run(
    window_screen_capturer,
    hsv_filter,
    monster_processor,
    player_processor,
    killing_bot,
):
    while True:
        raw_screenshot = window_screen_capturer.make_screenshot()
        filtered_screenshot = hsv_filter.apply(raw_screenshot)
        monsters_position = monster_processor.detect_objects(filtered_screenshot)
        player_position = player_processor.detect_objects(filtered_screenshot)

        if cv_waitKey(1) == ord("q"):
            cv_destroyAllWindows()
            break


def run_debug(
    window_screen_capturer,
    hsv_filter,
    monster_processor,
    player_processor,
    killing_bot,
):
    hsv_filter.init_calibration_gui()
    while True:
        raw_screenshot = window_screen_capturer.make_screenshot()
        filtered_screenshot = hsv_filter.apply(raw_screenshot)
        hsv_filter.update_params_from_gui()
        monsters_position = monster_processor.detect_objects(filtered_screenshot)
        player_position = player_processor.detect_objects(filtered_screenshot)
        image_staged = monster_processor.draw_rectangles(
            filtered_screenshot, monsters_position
        )
        image_ready = monster_processor.draw_rectangles(
            filtered_screenshot, image_staged
        )
        cv_imshow("Filtered", image_ready)
        if cv_waitKey(1) == ord("q"):
            cv_destroyAllWindows()
            break

    hsv_filter.dump_params_to_file()
