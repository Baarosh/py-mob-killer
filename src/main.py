from processors.image_processor import ImageProcessor
from screen_capturers.window_screen_capturer import WindowScreenCapturer
from bots.bot_killer import BotKiller
from utils import get_windows_names

if __name__ == "__main__":
    window_name = "Norbert — Forecast Data Services Ltd \u200e- OneNote for Windows 10"
    target_image_path = ""
    threshold = 0.65
    max_results = 5

    window_screen_capturer = WindowScreenCapturer(window_name, offsets=(0, 0, 0, 0))
    image_processor = ImageProcessor(target_image_path, threshold, max_results)
    killing_bot = BotKiller()


