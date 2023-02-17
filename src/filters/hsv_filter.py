from typing import Dict, Optional
import numpy as np
import cv2 as cv


class HSVFilter:
    def __init__(self, parameters: Dict[str, Optional[int]]):
        self._parameters = parameters

    def apply(self, screenshot: np.ndarray) -> np.ndarray:
        hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, self._parameters["sAdd"])
        s = self.shift_channel(s, -self._parameters["sSub"])
        v = self.shift_channel(v, self._parameters["vAdd"])
        v = self.shift_channel(v, -self._parameters["vSub"])
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
