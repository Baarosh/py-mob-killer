from typing import Set

import win32gui


def get_windows_names() -> Set[str]:
    windows_names = set()
    win32gui.EnumWindows(
        lambda window_handler, y: windows_names.add(
            win32gui.GetWindowText(window_handler)
        )
        if win32gui.IsWindowVisible(window_handler)
        else None,
        None,
    )
    return windows_names

print(get_windows_names())