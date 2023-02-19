from py_mob_killer.processors.image_processor import ImageProcessor
from py_mob_killer.screen_capturers.window_screen_capturer import WindowScreenCapturer
from py_mob_killer.filters.hsv_filter import HSVFilter
from py_mob_killer.bots.bot_killer import BotKiller
import cv2 as cv
import py_mob_killer.config as cfg

if __name__ == "__main__":
    if not cfg.calibration_mode:
        window_screen_capturer = WindowScreenCapturer(
            cfg.window_name, cfg.window_offsets
        )
        hsv_filter = HSVFilter(cfg.hsv_filter_parameters_path)
        image_processor_monster = ImageProcessor(
            str(cfg.monster_image_path),
            cfg.probability_threshold,
            cfg.max_results,
            cfg.detection_method,
            cfg.group_threshold,
            cfg.group_eps,
            cfg.monster_line_color,
            cfg.monster_line_type,
        )
        image_processor_player = ImageProcessor(
            str(cfg.player_image_path),
            cfg.probability_threshold,
            cfg.max_results,
            cfg.detection_method,
            cfg.group_threshold,
            cfg.group_eps,
            cfg.player_line_color,
            cfg.player_line_type,
        )
        killing_bot = BotKiller()

        while True:
            raw_screenshot = window_screen_capturer.make_screenshot()
            filtered_screenshot = hsv_filter.apply(raw_screenshot)
            processed_screenshot1 = image_processor_monster.process(filtered_screenshot)
            processed_screenshot2 = image_processor_player.process(
                processed_screenshot1
            )

            cv.imshow("Raw", raw_screenshot)
            cv.imshow("Processed", processed_screenshot2)
            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                break

    if cfg.calibration_mode:
        window_screen_capturer = WindowScreenCapturer(
            cfg.window_name, cfg.window_offsets
        )
        hsv_filter = HSVFilter(cfg.hsv_filter_parameters_path)
        hsv_filter.initialize_calibration_gui()

        while True:
            raw_screenshot = window_screen_capturer.make_screenshot()
            filtered_screenshot = hsv_filter.apply(raw_screenshot)
            hsv_filter.update_parameters_from_calibration_gui()

            cv.imshow("Raw", raw_screenshot)
            cv.imshow("Filtered", filtered_screenshot)
            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                break

        hsv_filter.dump_parameters_to_document(cfg.hsv_filter_parameters_path)
