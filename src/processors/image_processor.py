from typing import Tuple

import cv2 as cv
import numpy as np


class ImageProcessor:
    def __init__(
        self, target_image_path: str, threshold: float, max_results: int, method: int
    ) -> None:
        self._target_image = cv.imread(target_image_path, cv.IMREAD_UNCHANGED)
        self._target_image_height, self._target_image_width = self._target_image.shape
        self._screenshot = None
        self._treshold = threshold
        self._max_results = max_results
        self._method = method

    # def find(self, screenshot: np.ndarray) -> Tuple:
    #     processing_result = cv.matchTemplate(
    #         screenshot, self._target_image, self._method
    #     )
    #     locations_of_found_instances = zip(
    #         *np.where(processing_result >= self._threshold[::-1])
    #     )

