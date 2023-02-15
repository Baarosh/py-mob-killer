import numpy as np
import win32con
import win32gui
import win32ui
from typing import Tuple


class WindowScreenMaker:
    def __init__(
        self,
        window_name: str,
        offset_left: int,
        offset_right: int,
        offset_top: int,
        offset_bottom: int,
    ) -> None:
        try:
            self._window_handler = win32gui.FindWindow(None, window_name)
            self._window_size = win32gui.GetWindowRect(self._window_handler)
        except Exception:
            raise Exception("Window with given name cannot be found.")

        self._offset_left = offset_left
        self._offset_right = offset_right
        self._offset_top = offset_top
        self._offset_bottom = offset_bottom

        self._window_left = self._window_size[0] + self._offset_left
        self._window_top = self._window_size[1] + self._offset_top
        self._window_right = self._window_size[2] - self._offset_right
        self._window_bottom = self._window_size[3] - self._offset_bottom
        self._window_width = self._window_right - self._window_left
        self._window_height = self._window_bottom - self._window_top

    def make_screenshot(self) -> np.ndarray:
        wDC = win32gui.GetWindowDC(self._window_handler)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(
            dcObj, self._window_width, self._window_height
        )
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt(
            (0, 0),
            (self._window_width, self._window_height),
            dcObj,
            (self._offset_left, self._offset_top),
            win32con.SRCCOPY,
        )
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self._window_height, self._window_width, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self._window_handler, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

    def get_window_position(self) -> Tuple:
        return (
            self._window_left,
            self._window_top,
            self._window_right,
            self._window_bottom,
        )

    @staticmethod
    def get_windows_names() -> set[str]:
        windows_names = set()
        win32gui.EnumWindows(
            lambda window_handler, _: windows_names.add(
                win32gui.GetWindowText(window_handler)
            )
            if win32gui.IsWindowVisible(window_handler)
            else None
        )
        return windows_names
