import numpy as np
import win32con
import win32gui
import win32ui


class WindowScreenCapturer:
    def __init__(self, window_name, offset):
        self._window_name = window_name
        self._offset = offset
        self._handler = self._get_window_handler()
        self._coordinates = self._get_window_coordinates()
        self._width = self._coordinates["right"] - self._coordinates["left"]
        self._height = self._coordinates["bottom"] - self._coordinates["top"]

    def make_screenshot(self):
        wDC = win32gui.GetWindowDC(self._handler)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self._width, self._height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt(
            (0, 0),
            (self._width, self._height),
            dcObj,
            (self._offset[0], self._offset[1]),
            win32con.SRCCOPY,
        )
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self._height, self._width, 4)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self._handler, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

    def _get_window_coordinates(self):
        try:
            window_size = win32gui.GetWindowRect(self._handler)
        except Exception as e:
            raise Exception(f"Window coordinates cannot be found. Traceback: {e}")
        else:
            return {
                "left": window_size[0] + self._offset[0],
                "top": window_size[1] + self._offset[1],
                "right": window_size[2] + self._offset[2],
                "bottom": window_size[3] + self._offset[3],
            }

    def _get_window_handler(self):
        try:
            window_handler = win32gui.FindWindow(None, self._window_name)
        except Exception as e:
            raise Exception(f"Window with given name cannot be found. Traceback: {e}")
        else:
            return window_handler
