import pygetwindow as gw
import win32gui
import win32api


class WindowFocusManager():
    def getVisibleWindowsAtCursor(self):
        tup = win32api.GetCursorPos()
        windowsAtLocation = gw.getWindowsAt(tup[0], tup[1])
        visibleWindows = []
        for window in windowsAtLocation:
            if (win32gui.IsWindowVisible(window._hWnd)):
                visibleWindows.append(window._hWnd)
                # print(str(win32gui.GetWindowText(window._hWnd)))
        return visibleWindows
    
    def shouldPoeBeInFocus(self):
        try:
            poe_win_hwnd = gw.getWindowsWithTitle("Path of Exile")[0]._hWnd
        except:
            print("no window found, poe might not be running")
        else:
            processed_windows = self.getVisibleWindowsAtCursor()
            # print(f"poe window is {poe_win_hwnd}")
            if processed_windows[0] == poe_win_hwnd:
                # print("Top is poe")
                return True
            # else:
            #     print("top is not poe")
            #     print(f"top is: {str(win32gui.GetWindowText(processed_windows[0]))}")
        return False

    def putPoeInFocus(self):
        win32gui.SetForegroundWindow(gw.getWindowsWithTitle("Path of Exile")[0]._hWnd)