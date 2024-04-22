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

        # Catch both l-click and ctrl+l-click
        self.ahk.add_hotkey('LButton up', callback=lambda : self.callback_up())
        self.ahk.add_hotkey('LButton', callback=lambda : self.callback_down())
        self.ahk.add_hotkey('^LButton up', callback=lambda : self.callback_up())
        self.ahk.add_hotkey('^LButton', callback=lambda : self.callback_down())

        self.input_passthrough_condition = input_passthrough_condition
        self.start()

        # Sometimes an inputs can come in too fast. Need to block the LButton UP until LButton DOWN completes
        # This can happen especially if using something external to send clicks (X-Mouse)
        self.processing_click_down = False
        self.need_to_immediately_release = True

    def callback_down(self):
        # Set focus on the top visible window, this could cause some performance issues as it needs to be a blocking call.
        # [ ] TODO (1.0) Optimize to change focus only if needed (if top isnt already focused, or only to copy text)
        self.processing_click_down = True
        window = self.ahk.win_get_from_mouse_position(blocking=True)
        if (not (window.get_title() == "" and window.get_process_name() == "Explorer.EXE")):
            # If not over the taskbar change focus.
            # This is hacky? There has to be a better way to get the taskbar "window"
            window.activate(blocking=False)
        if (self.input_passthrough_condition(self.ahk.get_mouse_position(coord_mode='Screen', blocking=True))):
            if (self.ahk.key_state(key_name='Control', mode='P', blocking=True)):
                self.ahk.key_down("Control")
                self.ahk.key_down("LButton")
            else:
                self.ahk.key_down("LButton")
        self.processing_click_down = False
        if (self.need_to_immediately_release):
            self.callback_up()

    def callback_up(self):
        if (self.processing_click_down):
            self.need_to_immediately_release = True
            return
        elif (self.ahk.key_state(key_name='Control', mode='P')):
            self.ahk.key_down("Control")
            self.ahk.key_up("LButton")
        else:
            self.ahk.key_up("LButton")
        self.need_to_immediately_release = False

    def copyToClipboard(self):
        # [ ] TODO can use AHK for clipboard management
        lastClipboard = clipboard.paste()
        data=''
        clipboard.copy(data)
        ctrl=False
        # If the user is holding down ctrl, need to re-press control after the copy (ctrl+c) keypress as it will 
        # also release the control key.
        if (self.ahk.key_state(key_name='Control', mode='P')):
            ctrl=True
        self.ahk.send_input("^c")
        if (ctrl):
            self.ahk.key_down("Control")
        try:
            # block and wait for the clipboard to be updated with new text, this can be slow on windows for some reason?
            # 0.5 second timeout.
            self.ahk.clip_wait(timeout=0.5, blocking=True, wait_for_any_data=True)
            data = clipboard.paste()
        except TimeoutError: print(f"timed out waiting for clipboard data, returning {data}")
        clipboard.copy(lastClipboard)
        return data

    def stop(self):
        self.ahk.stop_hotkeys()

    def start(self):
        self.ahk.start_hotkeys()
