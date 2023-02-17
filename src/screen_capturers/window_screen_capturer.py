from typing import Dict, Tuple

import numpy as np
import win32con
import win32gui
import win32ui


class WindowScreenCapturer:
    def __init__(self, window_name: str, offsets: Tuple[int, int, int, int]) -> None:
        self._window_handler = self._get_window_handler(window_name)
        self._window_size_initial = self._get_window_size()
        self._offsets = self._get_offsets(offsets)
        self._window_size_calculated = self._calculate_window_size(
            self._window_size_initial, self._offsets
        )

        self._window_width_calculated = (
            self._window_size_calculated["right"] - self._window_size_calculated["left"]
        )
        self._window_height_calculated = (
            self._window_size_calculated["bottom"] - self._window_size_calculated["top"]
        )

    def make_screenshot(self) -> np.ndarray:
        wDC = win32gui.GetWindowDC(self._window_handler)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(
            dcObj, self._window_width_calculated, self._window_height_calculated
        )
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt(
            (0, 0),
            (self._window_width_calculated, self._window_height_calculated),
            dcObj,
            (self._offsets["left"], self._offsets["top"]),
            win32con.SRCCOPY,
        )
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self._window_height_calculated, self._window_width_calculated, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self._window_handler, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

    def _get_window_size(self) -> Dict[str, int]:
        try:
            window_size = win32gui.GetWindowRect(self._window_handler)
            return {
                "left": window_size[0],
                "top": window_size[1],
                "right": window_size[2],
                "bottom": window_size[3],
            }
        except Exception as e:
            raise Exception(f"Window coordinates cannot be found. Traceback: {e}")

    @property  # alternative: set separately getter, setter, deleter -> @property.setter
    def window_size(self):
        return self._window_size_calculated

    @staticmethod
    def _calculate_window_size(
        window_size: Dict[str, int], offsets: Dict[str, int]
    ) -> Dict[str, int]:
        return {
            "left": window_size["left"] + offsets["left"],
            "top": window_size["top"] + offsets["top"],
            "right": window_size["right"] - offsets["right"],
            "bottom": window_size["bottom"] - offsets["bottom"],
        }

    @staticmethod
    def _get_window_handler(window_name: str) -> int:
        try:
            window_handler = win32gui.FindWindow(None, window_name)
            return window_handler
        except Exception as e:
            raise Exception(f"Window with given name cannot be found. Traceback: {e}")

    @staticmethod
    def _get_offsets(offsets) -> Dict[str, int]:
        return {
            "left": offsets[0],
            "top": offsets[1],
            "right": offsets[2],
            "bottom": offsets[3],
        }
