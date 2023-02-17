from processors.image_processor import ImageProcessor
from screen_capturers.window_screen_capturer import WindowScreenCapturer
from filters.hsv_filter import HSVFilter
from bots.bot_killer import BotKiller
from utils import load_yaml_document

from cv2 import (
    TM_CCOEFF,
    TM_CCOEFF_NORMED,
    TM_CCORR,
    TM_CCORR_NORMED,
    TM_SQDIFF,
    TM_SQDIFF_NORMED,
)

if __name__ == "__main__":
    window_name = "Steam"
    target_image_path = ""
    probability_threshold = 0.65
    max_results = 5
    detection_method = TM_CCOEFF_NORMED
    hsv_filter_parameters = load_yaml_document("filters/hsv_filter_parameters.yaml")

    window_screen_capturer = WindowScreenCapturer(window_name, offsets=(0, 0, 0, 0))
    image_processor = ImageProcessor(
        target_image_path, probability_threshold, max_results, detection_method
    )
    hsv_filter = HSVFilter(hsv_filter_parameters)
    killing_bot = BotKiller()

    while True:
        raw_screenshot = window_screen_capturer.make_screenshot()
        filtered_screenshot = hsv_filter.apply(raw_screenshot)
        processed_screenshot = image_processor.process(filtered_screenshot)
