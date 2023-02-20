from pathlib import Path
from cv2 import (
    LINE_4,
    LINE_8,
    LINE_AA,
    TM_CCOEFF,
    TM_CCOEFF_NORMED,
    TM_CCORR,
    TM_CCORR_NORMED,
    TM_SQDIFF,
    TM_SQDIFF_NORMED,
)

calibration_mode = True
bot_active = True
window_name = "Ghost FlyFF - Mandarynka"
window_offsets = (10, 30, -10, -10)
probability_threshold = 0.65
max_results = None
detection_method = TM_CCOEFF_NORMED
group_threshold = 1
group_eps = 0.5
hsv_filter_parameters_path = Path().joinpath(
    "py_mob_killer", "filters", "hsv_filter_parameters.yaml"
)
monster_image_path = Path().joinpath(
    "py_mob_killer", "targets", "monster_augu_nickname.jpg"
)
monster_line_color = (255, 0, 255)
monster_line_type = LINE_4
player_image_path = Path().joinpath("py_mob_killer", "targets", "player_nickname.jpg")
player_line_color = (255, 255, 0)
player_line_type = LINE_4
