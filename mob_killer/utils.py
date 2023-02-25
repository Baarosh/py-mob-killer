from yaml import safe_load as yaml_safe_load, safe_dump as yaml_safe_dump, YAMLError
from cv2 import (
    waitKey as cv_waitKey,
    imshow as cv_imshow,
    destroyAllWindows as cv_destroyAllWindows,
    rectangle as cv_rectangle,
    LINE_4 as cv_LINE_4,
)
from enum import IntEnum

LINE_COLOR = (255, 0, 255)
LINE_TYPE = cv_LINE_4


class State(IntEnum):
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    ATTACKING = 3


def load_yaml_document(path):
    with open(path, "r") as stream:
        try:
            return yaml_safe_load(stream)
        except YAMLError as exc:
            print(f"Failed to load yaml document. Traceback: {exc}")


def dump_yaml_document(data, path):
    with open(path, "w") as stream:
        try:
            yaml_safe_dump(data, stream)
        except YAMLError as exc:
            print(f"Failed to dump yaml document. Traceback: {exc}")


def draw_rectangles(image, rectangles):
    for x, y, width, height in rectangles:
        top_left = (x, y)
        bottom_right = (x + width, y + height)
        cv_rectangle(image, top_left, bottom_right, LINE_COLOR, LINE_TYPE)


def get_center_point_from_rect(rectangle):
    for x, y, width, height in rectangle:
        center_x = x + int(width / 2)
        center_y = y + int(height / 2)
    return (center_y, center_x)


def get_hit_points_coords(window_coords):
    return [
        [
            int(window_coords["width"] / 2) + 50,  # left
            30,  # top
            20,  # width
            20,  # height
        ]
    ]


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
    win_coords = window_screen_capturer.coordinates
    hit_points_coords = get_hit_points_coords(win_coords)
    last_hp_pixel_color = [255,255,255]
    while True:
        raw_screenshot = window_screen_capturer.make_screenshot()
        filtered_screenshot = hsv_filter.apply(raw_screenshot)
        hsv_filter.update_params_from_gui()
        monsters_position = monster_processor.detect_objects(raw_screenshot)
        player_position = player_processor.detect_objects(filtered_screenshot)
        hp_pixel = filtered_screenshot[
            get_center_point_from_rect(hit_points_coords)
        ]
        hp_pixel_color = [hp_pixel[0], hp_pixel[1], hp_pixel[2]]

        draw_rectangles(filtered_screenshot, monsters_position)
        draw_rectangles(filtered_screenshot, player_position)
        draw_rectangles(filtered_screenshot, hit_points_coords)

        if hp_pixel_color != last_hp_pixel_color:
            print('HP RGB Color: ', hp_pixel_color[::-1])
            last_hp_pixel_color = hp_pixel_color

        cv_imshow("Filtered", filtered_screenshot)

        if cv_waitKey(1) == ord("q"):
            cv_destroyAllWindows()
            break

    # hsv_filter.dump_params_to_file()
