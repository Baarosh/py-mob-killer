from py_mob_killer.detectors.image_processor import ImageProcessor
from py_mob_killer.screen_capturers.window_screen_capturer import WindowScreenCapturer
from py_mob_killer.filters.hsv_filter import HSVFilter
from py_mob_killer.bots.bot import Bot
import cv2 as cv
import py_mob_killer.config as cfg

if __name__ == "__main__":
    window_screen_capturer = WindowScreenCapturer(cfg.window_name, cfg.window_offsets)
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

    if not cfg.calibration_mode:
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
