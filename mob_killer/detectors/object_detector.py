import cv2 as cv
import numpy as np

DETECTION_THRESHOLD = 0.65
DETECTION_METHOD = cv.TM_CCOEFF_NORMED
DETECTION_MAX_RESULTS = None
GROUPING_TRESHOLD = 1
GROUPING_EPS = 0.5
LINE_COLOR = (255, 0, 255)
LINE_TYPE = cv.LINE_4


class ObjectDetector:
    def __init__(self, object_path):
        self._object_path = object_path
        self._object = cv.imread(object_path, cv.IMREAD_UNCHANGED)
        self._object_height = self._object.shape[0]
        self._object_width = self._object.shape[1]

    def detect_objects(self, image):
        objects = cv.matchTemplate(image, self._object, DETECTION_METHOD)
        objects = list(zip(*np.where(objects >= DETECTION_THRESHOLD)[::-1]))
        if not objects:
            return []
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
        grouped_rects = cv.groupRectangles(rects, GROUPING_TRESHOLD, GROUPING_EPS)[0]
        return grouped_rects[:DETECTION_MAX_RESULTS]

    @staticmethod
    def draw_rectangles(screenshot, rectangles):
        for x, y, width, height in rectangles:
            top_left = (x, y)
            bottom_right = (x + width, y + height)
            cv.rectangle(screenshot, top_left, bottom_right, LINE_COLOR, LINE_TYPE)

    @staticmethod
    def get_center_points(rectangles):
        points = []
        for x, y, width, height in rectangles:
            center_x = x + int(width / 2)
            center_y = y + int(height / 2)
            points.append((center_x, center_y))
        return points
