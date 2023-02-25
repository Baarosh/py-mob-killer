import numpy as np
import win32con
import win32gui
import win32ui


class WindowScreenCapturer:
    BORDER_PIXELS = 8
    TOPBAR_PIXELS = 31

    def __init__(self, window_name):
        self._window_name = window_name
        self._border_pixels = self.BORDER_PIXELS
        self._topbar_pixels = self.TOPBAR_PIXELS
        self._handler = self._get_window_handler()
        self._coordinates = self._get_window_coordinates()  # left, top, width, height

    def make_screenshot(self):
        wDC = win32gui.GetWindowDC(self._handler)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(
            dcObj, self._coordinates["width"], self._coordinates["height"]
        )
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt(
            (0, 0),
            (self._coordinates["width"], self._coordinates["height"]),
            dcObj,
            (self._border_pixels, self._topbar_pixels),
            win32con.SRCCOPY,
        )
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self._coordinates["height"], self._coordinates["width"], 4)
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
                "left": window_size[0] + self._border_pixels,
                "top": window_size[1] + self._topbar_pixels,
                "width": (window_size[2] - window_size[0]) - (2 * self._border_pixels),
                "height": (window_size[3] - window_size[1])
                - self._border_pixels
                - self._topbar_pixels,
            }

    def _get_window_handler(self):
        try:
            return win32gui.FindWindow(None, self._window_name)
        except Exception as e:
            raise Exception(f"Window with given name cannot be found. Traceback: {e}")

    @property
    def coordinates(self):
        return self._coordinates
