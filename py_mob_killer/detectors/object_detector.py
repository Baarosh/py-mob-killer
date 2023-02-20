import cv2 as cv
import numpy as np
from py_mob_killer.utils import dump_yaml_document, load_yaml_document


class ObjectDetector:
    def __init__(self, object_path, params_path):
        self._object_path = object_path
        self._params_path = params_path
        self._object = cv.imread(object_path, cv.IMREAD_UNCHANGED)
        self._params = self._load_params_from_document()
        self._object_height = self._object.shape[0]
        self._object_width = self._object.shape[1]

    def _detect_objects_on_image(self, image):
        objects = cv.matchTemplate(
            image, self._object, self._params["detection_method"]
        )
        objects = list(
            zip(*np.where(objects >= self._params["detection_threshold"])[::-1])
        )
        if not objects:
            return np.array([], dtype=np.int32).reshape(0, 4)
        return objects

    def _get_rectangles_position_over_targets(self, targets):
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

    def _draw_rectangles(self, screenshot, rectangles):
        for x, y, width, height in rectangles:
            top_left = (x, y)
            bottom_right = (x + width, y + height)
            cv.rectangle(
                screenshot, top_left, bottom_right, self._line_color, self._line_type
            )
        return screenshot

    def _get_center_points_from_rectangles(rectangles):
        points = []
        for x, y, width, height in rectangles:
            center_x = x + int(width / 2)
            center_y = y + int(height / 2)
            points.append((center_x, center_y))
        return points

    def dump_params_to_document(self):
        dump_yaml_document(self._params, self._params_path)

    def _load_params_from_document(self):
        return load_yaml_document(self._params_path)
