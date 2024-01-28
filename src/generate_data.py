from compare import ImageProcessor
from common import file_format, reference_enum
# import cv2 as cv
import numpy as np
from ahk import AHK
from ahk.directives import MaxHotkeysPerInterval, NoTrayIcon
import clipboard
from PyQt5.QtWidgets import QFileDialog 
from PyQt5 import QtWidgets
import pygetwindow as gw
import win32gui
from WindowFocusManager import WindowFocusManager

focus = WindowFocusManager()

if focus.shouldPoeBeInFocus():
    focus.putPoeInFocus()
else:
    print("poe should not be in focus")


# def getVisibleWindowsInOrder():
#     tup = win32api.GetCursorPos()
#     windowsAtLocation = gw.getWindowsAt(tup[0], tup[1])
#     visibleWindows = []
#     for window in windowsAtLocation:
#         if (win32gui.IsWindowVisible(window._hWnd)):
#             visibleWindows.append(window._hWnd)
#             print(str(win32gui.GetWindowText(window._hWnd)))
#     return visibleWindows

# try:
#     poe_win_hwnd = gw.getWindowsWithTitle("Path of Exile")[0]._hWnd
# except:
#     print("no window found, poe might not be running")
# else:
#     processed_windows = getVisibleWindowsInOrder()
#     print(f"poe window is {poe_win_hwnd}")
#     if processed_windows[0] == poe_win_hwnd:
#         print("Top is poe")
#     else:
#         print("top is not poe")
#         print(f"top is: {str(win32gui.GetWindowText(processed_windows[0]))}")


# the problem is, there can be a window that is above the window of interest, but is not visible.
# solution: need to get ALL windows above the current one. If any are in region and visible, poe is not at the top.
# if isPoeInRegion():
#     windowAbove = win32gui.GetWindow(poe_win[0]._hWnd, win32con.GW_HWNDFIRST)
#     # print("is window above visible " + str(win32gui.IsWindowVisible(windowAbove)))
#     # print("window above: "+ str(win32gui.GetWindowText(windowAbove)))
#     # print("window above: "+ str(windowAbove))
#     # print("other windows:" + str(windows))
#     print("poe app: " + str(poe_win[0]._hWnd))
#     for window in windows:
#         if (win32gui.IsWindowVisible(window._hWnd)):
#             print(str(win32gui.GetWindowText(window._hWnd)))
#             # and str(win32gui.IsWindowVisible(windowAbove))
#     if windowAbove != 0 and isWindowInList(windowAbove):
#         print("not top window")
#     else:
#         print("top window")
# else:
#     print("not in region")



# print("poeWindow ", str(poe_win[0]._hWnd))
# print(win32gui.GetWindow(poe_win[0]._hWnd, win32con.GW_HWNDPREV))








# need explorer to get file name


# directives = [
#             MaxHotkeysPerInterval(value=1000, apply_to_hotkeys_process=True),
#             NoTrayIcon(apply_to_hotkeys_process=True)
#         ]
# ahk = AHK(directives=directives)

# def copyToClipboard():
#     ahk.send_input('^c')
#     text = clipboard.paste()
#     print("copied text")
#     print(text)

# ahk.add_hotkey('RButton', callback=lambda : copyToClipboard())
# ahk.start_hotkeys()
# while True:
#     pass

# processor = ImageProcessor()
# processor.generate_data_csv()

# naem = "abyssal"
# cv.imread(file_format.format(dname=naem))
# array = processor.generate_histogram(cv.imread(file_format.format(dname=naem)))
# print(array)
# flat = array.flatten().astype(np.float32)
# print(flat)
# print(flat.reshape(64,3))
# all_data =  np.array([], dtype=np.float32).reshape(0,64 * 3)
# all_data = np.vstack((all_data, flat))
# all_data = np.vstack((all_data, flat))
# print(all_data)

# processor.generate_data_csv()
# read_in = np.loadtxt("resources/histogram_icons_1.csv", dtype=float, delimiter=",").astype(np.float32)
# abyssal = read_in[0,:].reshape(64,3)
# for i, name in enumerate(reference_enum):
#     nextHist = read_in[i,:].reshape(64,3)
#     print(name + ": " + str(processor.compare_histograms(abyssal, nextHist)))