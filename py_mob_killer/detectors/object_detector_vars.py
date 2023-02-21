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
from enum import Enum

class ObjectDetectorVars(Enum):
    probability_threshold = 0.65
    max_results = None
    detection_method = TM_CCOEFF_NORMED
    group_threshold = 1
    group_eps = 0.5
    monster_line_color = (255, 0, 255)
    monster_line_type = LINE_4
    player_line_color = (255, 255, 0)
    player_line_type = LINE_4