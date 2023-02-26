import cv2 as cv
import numpy as np


class ObjectDetector:
    _detection_treshold = 0.45
    _detection_method = cv.TM_CCOEFF_NORMED
    _detection_max_results = None
    _grouping_treshold = 1
    _grouping_eps = 0.5

    def __init__(self, object_path):
        self._object_path = str(object_path)
        self._object = cv.imread(self._object_path, cv.IMREAD_UNCHANGED)
        self._object_height = self._object.shape[0]
        self._object_width = self._object.shape[1]

    def detect_all(self, image):
        objects = cv.matchTemplate(
            image,
            self._object,
            self._detection_method,
        )
        objects = list(
            zip(*np.where(objects >= self._detection_treshold)[::-1]),
        )
        if not objects:
            return ()
        rects = []
        for obj in objects:
            rect = [
                int(obj[0]),
                int(obj[1]),
                self._object_width,
                self._object_height,
            ]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rects.append(rect)
            rects.append(rect)
        grouped_rects, _weights = cv.groupRectangles(
            rects,
            self._grouping_treshold,
            self._grouping_eps,
        )
        return tuple(grouped_rects[: self._detection_max_results])
