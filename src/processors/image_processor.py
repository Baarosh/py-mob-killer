from typing import List, Tuple

import cv2 as cv
import numpy as np
from utils import Mat


class ImageProcessor:
    def __init__(
        self,
        target_image_path: str,
        probability_treshold: float,
        max_results: int,
        method: int,
        group_treshold: int,
        group_eps: int,
        line_color: Tuple[int],
        line_type: int,
    ) -> None:
        self._target_image = cv.imread(target_image_path, cv.IMREAD_UNCHANGED)
        self._target_image_height = self._target_image.shape[0]
        self._target_image_width = self._target_image.shape[1]
        self._probability_treshold = probability_treshold
        self._max_results = max_results
        self._method = method
        self._group_treshold = group_treshold
        self._group_eps = group_eps
        self._line_color = line_color
        self._line_type = line_type

    def process(self, screenshot: Mat) -> Mat:
        found_targets = self._find_targets(screenshot)
        targets_rectangles = self._get_rectangles_position_over_targets(found_targets)
        screenshot_with_rectangles = self._draw_rectangles(
            screenshot, targets_rectangles
        )
        return screenshot_with_rectangles

    def _find_targets(self, screenshot: Mat) -> List[Tuple[int]]:
        processing_result = cv.matchTemplate(
            screenshot, self._target_image, self._method
        )
        found_targets = list(
            zip(*np.where(processing_result >= self._probability_treshold)[::-1])
        )
        if not found_targets:
            return np.array([], dtype=np.int32).reshape(0, 4)
        return found_targets

    def _get_rectangles_position_over_targets(self, targets: List[Tuple[int]]) -> List[List[int]]:
        rectangles = []
        for target in targets:
            rectangle = [
                int(target[0]),
                int(target[1]),
                self._target_image_width,
                self._target_image_height,
            ]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rectangle)
            rectangles.append(rectangle)
        grouped_rectangles = cv.groupRectangles(
            rectangles, self._group_treshold, self._group_eps
        )[0]
        return grouped_rectangles[: self._max_results]

    def _draw_rectangles(self, screenshot: Mat, rectangles: List[List[int]]) -> Mat:
        for x, y, width, height in rectangles:
            top_left = (x, y)
            bottom_right = (x + width, y + height)
            cv.rectangle(
                screenshot, top_left, bottom_right, self._line_color, self._line_type
            )
        return screenshot
