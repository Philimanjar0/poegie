from ahk import AHK
from ahk._sync.transport import AhkExecutableNotFoundError
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
        except AhkExecutableNotFoundError as e:
            ErrorPopup("Could not start AutoHotKey. It is likely not installed. \nPlease click \"Show Details\" for an automatic download link", "https://www.autohotkey.com/download/ahk-install.exe", True)

        # self.ahk.add_hotkey('LButton', callback=lambda : self.callback(input='LButton'))
        # [x] TODO change this back to LMouse
        self.ahk.add_hotkey('LButton up', callback=lambda : self.ahk.key_up('LButton'))
        # self.ahk.add_hotkey('^LButton up', callback=lambda : self.ahk.key_up('^LButton'))
        self.ahk.add_hotkey('LButton', callback=lambda : self.callback('LButton'))
        # self.ahk.add_hotkey('^LButton', callback=lambda : self.callback('^LButton'))
        self.input_passthrough_condition = input_passthrough_condition
        self.start()

    def callback(self, input):
        if (self.input_passthrough_condition(self.ahk.get_mouse_position(coord_mode='Screen'))):
            self.ahk.key_down(input)

    def copyToClipboard(self):
        lastClipboard = clipboard.paste()
        clipboard.copy('')
        self.ahk.send_input('^c')
        # block and wait for the clipboard to be updated with new text, this can be slow on windows.
        # 0.25 second timeout.
        # [ ] TODO fix this, timeout is failing
        self.ahk.clip_wait(timeout=0.1, blocking=True, wait_for_any_data=True)
        data = clipboard.paste()
        clipboard.copy(lastClipboard)
        return data

    def stop(self):
        self.ahk.stop_hotkeys()

    def start(self):
        self.ahk.start_hotkeys()
