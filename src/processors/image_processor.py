
import numpy as np
import cv2 as cv
from typing import Tuple

class ImageProcessor:
    def __init__(self, target_image_path: str, threshold: float, max_results: int) -> None:
        self._target_image = cv.imread(target_image_path, cv.IMREAD_UNCHANGED)
        self._target_image_height, self._target_image_width = self._target_image.shape
        self._screenshot = None
        self._treshold = threshold
        self._max_results = max_results
        self._method = cv.TM_CCOEFF_NORMED

    def apply_hsv_filter(self) -> None:
        pass

    def find(self, screenshot: np.ndarray) -> Tuple:
        processing_result = cv.matchTemplate(screenshot, self._target_image, self._method)
        locations_of_found_instances = zip(*np.where(processing_result >= self._threshold[::-1]))


    @property.setter
    def set_method(self, method: int) -> None:
        self._method = method

    # apply adjustments to HSV channel
    @staticmethod
    def shift_hsv_channel(c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c