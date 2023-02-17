from typing import Dict, Optional
import numpy as np
import cv2 as cv
from utils import dump_yaml_document, Mat
from utils import Mat

class HSVFilter:
    def __init__(self, parameters: Dict[str, int]) -> None:
        self._parameters = parameters
        self._gui_window_name = 'Trackbar'


    def apply(self, screenshot: Mat) -> Mat:
        hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        s = self._shift_channel(s, self._parameters["sAdd"])
        s = self._shift_channel(s, -self._parameters["sSub"])
        v = self._shift_channel(v, self._parameters["vAdd"])
        v = self._shift_channel(v, -self._parameters["vSub"])
        hsv = cv.merge([h, s, v])

        lower = np.array(
            [
                self._parameters["hMin"],
                self._parameters["sMin"],
                self._parameters["vMin"],
            ]
        )
        upper = np.array(
            [
                self._parameters["hMax"],
                self._parameters["sMax"],
                self._parameters["vMax"],
            ]
        )
        mask = cv.inRange(hsv, lower, upper)
        img = cv.bitwise_and(hsv, hsv, mask=mask)
        # img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
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

    def initialize_calibration_gui(self) -> None:
        # make better
        cv.namedWindow(self._gui_window_name, cv.WINDOW_NORMAL)
        cv.resizeWindow(self._gui_window_name, 350, 700)
        def nothing(position):
            ...
        cv.createTrackbar('hMin', self._gui_window_name, 0, 179, nothing)
        cv.createTrackbar('sMin', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('vMin', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('hMax', self._gui_window_name, 0, 179, nothing)
        cv.createTrackbar('sMax', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('vMax', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('sAdd', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('sSub', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('vAdd', self._gui_window_name, 0, 255, nothing)
        cv.createTrackbar('vSub', self._gui_window_name, 0, 255, nothing)

        cv.setTrackbarPos('hMin', self._gui_window_name, self._parameters['hMin'])
        cv.setTrackbarPos('sMin', self._gui_window_name, self._parameters['sMin'])
        cv.setTrackbarPos('vMin', self._gui_window_name, self._parameters['vMin'])
        cv.setTrackbarPos('hMax', self._gui_window_name, self._parameters['hMax'])
        cv.setTrackbarPos('sMax', self._gui_window_name, self._parameters['sMax'])
        cv.setTrackbarPos('vMax', self._gui_window_name, self._parameters['vMax'])
        cv.setTrackbarPos('sAdd', self._gui_window_name, self._parameters['sAdd'])
        cv.setTrackbarPos('sSub', self._gui_window_name, self._parameters['sSub'])
        cv.setTrackbarPos('vAdd', self._gui_window_name, self._parameters['vAdd'])
        cv.setTrackbarPos('vSub', self._gui_window_name, self._parameters['vSub'])


    def update_parameters_from_calibration_gui(self) -> None:
        self._parameters["hMin"] = cv.getTrackbarPos('hMin', self._gui_window_name)
        self._parameters["sMin"] = cv.getTrackbarPos('sMin', self._gui_window_name)
        self._parameters["vMin"] = cv.getTrackbarPos('vMin', self._gui_window_name)
        self._parameters["hMax"] = cv.getTrackbarPos('hMax', self._gui_window_name)
        self._parameters["sMax"] = cv.getTrackbarPos('sMax', self._gui_window_name)
        self._parameters["vMax"] = cv.getTrackbarPos('vMax', self._gui_window_name)
        self._parameters["sAdd"] = cv.getTrackbarPos('sAdd', self._gui_window_name)
        self._parameters["sSub"] = cv.getTrackbarPos('sSub', self._gui_window_name)
        self._parameters["vAdd"] = cv.getTrackbarPos('vAdd', self._gui_window_name)
        self._parameters["vSub"] = cv.getTrackbarPos('vSub', self._gui_window_name)

    def dump_parameters_to_document(self, path: str) -> None:
        dump_yaml_document(self._parameters, path)