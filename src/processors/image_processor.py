from typing import List

import cv2 as cv
import numpy as np


class ImageProcessor:
    def __init__(
        self, target_image_path: str, probability_treshold: float, max_results: int, method: int, group_treshold: int, group_eps: int,
    ) -> None:
        self._target_image = cv.imread(target_image_path, cv.IMREAD_UNCHANGED)
        self._target_image_height, self._target_image_width = self._target_image.shape
        self._screenshot = None
        self._probability_treshold = probability_treshold
        self._max_results = max_results
        self._method = method
        self._group_treshold = group_treshold
        self._group_eps = group_eps

    def process(screenshot: np.ndarray) -> np.ndarray:
        ...

    def _find_targets(self, screenshot: np.ndarray) -> np.ndarray:
        processing_result = cv.matchTemplate(
            screenshot, self._target_image, self._method
        )
        found_targets = list(zip(*np.where(processing_result >= self._probability_treshold[::-1])))
        if not found_targets:
            return np.array([], dtype=np.int32).reshape(0,4)
        return found_targets

    def _get_rectangles_position_over_targets(self, targets: np.ndarray) -> List[List[int]]:
        rectangles = []
        for target in targets:
            rectangle = [int(target[0]), int(target[1]), self._target_image_width, self._target_image_height]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rectangle)
            rectangles.append(rectangle)
        grouped_rectangles = cv.groupRectangles(rectangles, self._group_treshold, self._group_eps)[0]
        return grouped_rectangles[:self._max_results]





