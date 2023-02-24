import numpy as np
import cv2 as cv
from mob_killer.utils import dump_yaml_document, load_yaml_document


class HSVFilter:
    GUI_WINDOW_NAME = "Trackbar"

    def __init__(self, params_path):
        self._params_path = params_path
        self._params = self._load_params_from_file()
        self._gui_window_name = self.GUI_WINDOW_NAME

    def apply(self, screenshot):
        hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        s = self._shift_channel(s, self._params["sAdd"])
        s = self._shift_channel(s, -self._params["sSub"])
        v = self._shift_channel(v, self._params["vAdd"])
        v = self._shift_channel(v, -self._params["vSub"])
        hsv = cv.merge([h, s, v])
        lower = np.array(
            [
                self._params["hMin"],
                self._params["sMin"],
                self._params["vMin"],
            ]
        )
        upper = np.array(
            [
                self._params["hMax"],
                self._params["sMax"],
                self._params["vMax"],
            ]
        )
        mask = cv.inRange(hsv, lower, upper)
        img = cv.bitwise_and(hsv, hsv, mask=mask)
        img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
        return img

    # apply adjustments to an HSV channel
    @staticmethod
    def _shift_channel(c, amount):
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

    def init_calibration_gui(self):
        cv.namedWindow(self._gui_window_name, cv.WINDOW_NORMAL)
        cv.resizeWindow(self._gui_window_name, 350, 700)
        for param in self._params:
            if self._params[param] in ("hMin", "hMax"):
                cv.createTrackbar(param, self._gui_window_name, 0, 179, lambda x: None)
            else:
                cv.createTrackbar(param, self._gui_window_name, 0, 255, lambda x: None)
            cv.setTrackbarPos(param, self._gui_window_name, self._params[param])

    def update_params_from_gui(self):
        for param in self._params:
            self._params[param] = cv.getTrackbarPos(param, self._gui_window_name)

    def dump_params_to_file(self):
        dump_yaml_document(self._params, self._params_path)

    def _load_params_from_file(self):
        return load_yaml_document(self._params_path)
