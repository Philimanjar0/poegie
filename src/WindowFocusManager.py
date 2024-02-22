import pygetwindow as gw
import win32gui
import win32api

# [ ] TODO Deprecated, remove dependencies
class WindowFocusManager():
    def getVisibleWindowsAtCursor(self):
        tup = win32api.GetCursorPos()
        windowsAtLocation = gw.getWindowsAt(tup[0], tup[1])
        visibleWindows = []
        for window in windowsAtLocation:
            # Need the handle, dont care that its a "protected" field, its not exposed by a getter.
            if (win32gui.IsWindowVisible(window._hWnd)):
                visibleWindows.append(window._hWnd)
        return visibleWindows
    
    def shouldPoeBeInFocus(self):
        windows = gw.getWindowsWithTitle("Path of Exile")
        if len(windows) < 1:
            return False
        else:
            poe_win_hwnd = windows[0]._hWnd
            processed_windows = self.getVisibleWindowsAtCursor()
            if processed_windows[0] == poe_win_hwnd:
                return True
        return False

    def putPoeInFocus(self):
        win32gui.SetForegroundWindow(gw.getWindowsWithTitle("Path of Exile")[0]._hWnd)