from processors.image_processor import ImageProcessor
from screen_capturers.window_screen_capturer import WindowScreenCapturer
from filters.hsv_filter import HSVFilter
from bots.bot_killer import BotKiller
from utils import load_yaml_document

import cv2 as cv

if __name__ == "__main__":
    calibration_mode = False

    window_name = "Ghost FlyFF - Mandarynka"
    offsets = (20, 20, -20, -20)
    target_image_path = "src/targets/game_nickname.jpg"
    probability_threshold = 0.65
    max_results = None
    detection_method = cv.TM_CCOEFF_NORMED
    group_threshold = 1
    group_eps = 0.5
    hsv_filter_parameters = load_yaml_document("src/filters/hsv_filter_parameters.yaml")
    line_color = (255, 0, 255)
    line_type = cv.LINE_4

    if not calibration_mode:
        window_screen_capturer = WindowScreenCapturer(window_name, offsets)
        hsv_filter = HSVFilter(hsv_filter_parameters)
        image_processor = ImageProcessor(
            target_image_path,
            probability_threshold,
            max_results,
            detection_method,
            group_threshold,
            group_eps,
            line_color,
            line_type,
        )
        killing_bot = BotKiller()

        while True:
            raw_screenshot = window_screen_capturer.make_screenshot()
            filtered_screenshot = hsv_filter.apply(raw_screenshot)
            processed_screenshot = image_processor.process(filtered_screenshot)

            cv.imshow("Raw", raw_screenshot)
            cv.imshow("Filtered", filtered_screenshot)
            cv.imshow("Processed", processed_screenshot)

            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                break

    if calibration_mode:
        window_screen_capturer = WindowScreenCapturer(window_name, offsets)
        hsv_filter = HSVFilter(hsv_filter_parameters)
        hsv_filter.initialize_calibration_gui()

        while True:
            raw_screenshot = window_screen_capturer.make_screenshot()
            filtered_screenshot = hsv_filter.apply(raw_screenshot)

            hsv_filter.update_parameters_from_calibration_gui()

            cv.imshow("Raw", raw_screenshot)
            cv.imshow("Filtered", filtered_screenshot)

            if cv.waitKey(1) == ord("q"):
                hsv_filter.dump_parameters_to_document(
                    "src/filters/hsv_filter_parameters.yaml"
                )
                cv.destroyAllWindows()
                break
