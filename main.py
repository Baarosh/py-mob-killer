import win32gui

a = win32gui.EnumWindows(lambda x,_: print(hex(x), win32gui.GetWindowText(x)), None)
print(a)