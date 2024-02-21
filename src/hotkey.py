from ahk import AHK
from ahk.directives import MaxHotkeysPerInterval, NoTrayIcon
import clipboard

class InputOutputManager:
    def __init__(self, input_passthrough_condition):
        directives = [
            MaxHotkeysPerInterval(value=1000, apply_to_hotkeys_process=True),
            NoTrayIcon(apply_to_hotkeys_process=True)
        ]
        try:
            self.ahk = AHK(directives=directives)
        except EnvironmentError as e:
            ErrorPopup("Could not start AutoHotKey. It is likely not installed. \nPlease click \"Show Details\" for an automatic download link", "https://www.autohotkey.com/download/ahk-install.exe", True)

        self.ahk.add_hotkey('*LButton up', callback=lambda : self.callback_up())
        self.ahk.add_hotkey('*LButton', callback=lambda : self.callback_down())

        self.input_passthrough_condition = input_passthrough_condition
        self.start()

    def callback_down(self):
        if (self.input_passthrough_condition(self.ahk.get_mouse_position(coord_mode='Screen'))):
            if (self.ahk.key_state('Control')):
                self.ahk.key_down("Control")
                self.ahk.key_down("LButton")
            else:
                self.ahk.key_down("LButton")

    def callback_up(self):
        if (self.ahk.key_state('Control')):
            self.ahk.key_down("Control")
            self.ahk.key_up("LButton")
        else:
            self.ahk.key_up("LButton")

    def copyToClipboard(self):
        lastClipboard = clipboard.paste()
        clipboard.copy('')
        self.ahk.send_input('^c')
        # block and wait for the clipboard to be updated with new text, this can be slow on windows for some reason?
        # 0.25 second timeout.
        self.ahk.clip_wait(timeout=0.1, blocking=True, wait_for_any_data=True)
        data = clipboard.paste()
        clipboard.copy(lastClipboard)
        return data

    def stop(self):
        self.ahk.stop_hotkeys()

    def start(self):
        self.ahk.start_hotkeys()
