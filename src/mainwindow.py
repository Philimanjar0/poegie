import math
import numpy as np

from benchwindow import BenchWindow
from calcstab import CalcsTab
from common import reference_enum
from compare import ImageProcessor
from configtab import ConfigTab
from data import DataTab
from debugtab import DebugTab
from errorpopup import ErrorPopup
from hotkey import InputOutputManager
from mss import mss
from PyQt5.QtCore import QSize, QPoint, QSettings, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget
from togglebuttons import TargetWindowButton, FeatureEnableToggle
from WindowFocusManager import WindowFocusManager

# must do (0.1.0)
# [x] get the config tab working, finish the refactor
# [x] vision stuff for 3.23 (4 hours)
#   [x] take all references
#   [x] add a debug tab?
#   [x] edit the enum
#   [x] processing improvements
#       [x] better background color thresholding
#       [x] how many "bins"? (8 right now?)
#   [x] accuracy on all orbs
#      [x] armor doesnt work rn
#   [x] error handling, what happens on bad results?
#       [x] if keypoints != 1, do nothing
#   [x] img process when removing from the window
# [x] full flowchart for adding, removing, clicking button, etc. 
# [x] Data Tab
#   [x] update data dynamically
#   [x] Some sort of export, not even copy past works
#   [ ] "are you sure" pop up for clearing data 
# [ ] final test of all functionality
# [ ] release (2 hours)
#   [ ] clean up imports
#   [ ] documentation of methods
#   [ ] requirements.txt
#   [ ] logging https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module
#   [ ] remake git repo with good structure
#   [ ] readme
#   [ ] build executable
#   [ ] fully test executable
#   [ ] publish public git repo
# [ ] make known, video, discord, streamer?

# BUGS 
# [x] Investigate if not tabbed in messes with the flags and stuff
# [x] Changing settings, disabling/reenabling should reset the "last seen" flag to allow rolling on accident.
# [x] data did not save
# [x] data reset doesnt work, whispering has "1"
# [x] if the app crashes, AHK threads are still running eating left click
# [x] data export button should be horizontal
# [x] moving the window around changes where the icon ends up in the "icon" button
# [x] error in image stuff can crash the app
# [x] can roll over first orb put into window

# stretch goals
# [ ] scroll bar on calcs tab (1.0)
# [x] export data to CSV (0.1)
# [ ] reorganize config tab (TBD)
# [ ] save last inputs of config tab to settings (0.1.1)
# [ ] debug tab for prod (0.2.0)
#   [ ] sub tabs
#      [ ] finding logs
#      [ ] image stuff (what we already have but nicer?)
#      [ ] cached data (viewer maybe? button to clear)



class Main(QMainWindow):
    def __init__(self, close_callback):
        QMainWindow.__init__(self)
        
        ## declare variables
        self.last_seen = -1
        self.selected_for_stop = []
        self.settings = QSettings('PoE', 'Hoagie')
        self.close_callback = close_callback

        ## window setup
        tabs = QTabWidget()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setCentralWidget(tabs)
        self.configTab = ConfigTab()
        self.calcsTab = CalcsTab()
        self.dataTab = DataTab()
        self.debugTab = DebugTab(self.configTab.target_window)
        self.button_pressed_last = False
        self.imageProcessor = ImageProcessor()
        self.windowFocusManager = WindowFocusManager()
        self.hotkeys_manager = InputOutputManager(input_passthrough_condition=lambda pos : self.trigger_check(pos))  
        
        tabs.addTab(self.configTab, "config")
        tabs.addTab(self.calcsTab, "calculator")
        tabs.addTab(self.dataTab, "data")
        tabs.addTab(self.debugTab, "debug")

        self.init_window_settings()

    def target_button_callback(self):
        if (self.show_target_button.toggle_state):
            self.target_window.hide()
        else:
            self.target_window.show()
    
    def closeEvent(self, event):
        self.close()
        self.close_callback(event)

    def close(self):
        print("CLOSING")
        self.settings.setValue("main.size", self.size())
        self.settings.setValue("main.pos", self.pos())

        self.configTab.close()
        self.calcsTab.close()
        self.dataTab.close()

        self.hotkeys_manager.stop()

    def handle_selection_change(self, value, index):
        if (value == 2):
            self.selected_for_stop[index] = True
        else:
            self.selected_for_stop[index] = False

        """
        flag button = false

        if press button (successful orb result ie somethings in there)
            button = true
            item = classifyImage()
            if previous click was not button:
                do nothing
            else
                increment(item)

        if press in window
            if button == true
                increment
            else
                do nothing
            button = false
        """

    def trigger_check(self, mouse_position):
        # [x] TODO clean this up, to be better if nests. Flowchart is not right. Image processing and incrementing stored data needs to be seperate.
        if self.windowFocusManager.shouldPoeBeInFocus():
            # This is to solve, where the user has another window in focus (such as the app) in front of poe.
            # If they do, and they click on the item in the bench, then copying the item text does not work, because the keyboard focus is not POE.
            # This will check if poe can be in the foreground (mouse is within the window, and no visible windows are on top of it) and focus it.
            self.windowFocusManager.putPoeInFocus()
        
        if (not self.configTab.target_window.isVisible()
                and self.configTab.enable_button.toggle_state):
            if (self.configTab.target_window.bench_button_rect.contains(mouse_position[0], mouse_position[1])):
                print("button pressed")
                imageFound = self.categorize_image()
                if imageFound == -1:
                    return True
                elif self.configTab.should_stop_on_index(imageFound):
                    print("Found a desired item, blocking reroll")
                    self.last_seen = imageFound
                    self.button_pressed_last = True
                    return False
                elif imageFound == self.last_seen:
                    print("duplicate duplicate item, blocking reroll")
                    return False
                # This is just a normal reroll, increment and unblock the input.
                if (self.button_pressed_last == True):
                    print("incrementing {imageFound}")
                    self.dataTab.increment(imageFound)
                self.button_pressed_last = True
                self.last_seen = imageFound
                return True
            # Press was in the crafting window
            elif (self.configTab.target_window.bench_craft_rect.contains(mouse_position[0], mouse_position[1])):
                print("window clicked")
                if (self.button_pressed_last == True):
                    itemInWindow = self.parseText()
                    if not itemInWindow == self.last_seen:
                        self.dataTab.increment(itemInWindow)
                self.last_seen = -1 # Reset the last seen in case of starting with the same orb back to back.
                self.button_pressed_last = False
        return True

    def categorize_image(self):
        bounding_box = {'top': self.configTab.target_window.bench_craft_rect.top(), 
                'left': self.configTab.target_window.bench_craft_rect.left(),
                'width': self.configTab.target_window.bench_craft_rect.width(),
                'height': self.configTab.target_window.bench_craft_rect.height()}
        index_of_checked = -1
        with mss() as sct:
            frame_rgb = sct.grab(bounding_box)
            try:
                index_of_checked = self.imageProcessor.classify_raw_image(np.array(frame_rgb))
            except Exception as e:
                # If the image could not be classified for whatever reason, log the exception and return true to unblock inputs
                print("Encounter exception when processing image: " + str(e))
        return index_of_checked
    
    def parseText(self):
        copiedText = self.hotkeys_manager.copyToClipboard()
        try:
            name = ((copiedText.split("\n")[2]).split(" ")[0]).split("\'")[0]
            index = reference_enum.index(name)
            # print(f"index found from parsing text {index} resultant name {name}")
            return index
        except Exception as e:
            print(f"Could not parse text {copiedText}. Skipping increment step.")
        return -1


    def init_window_settings(self):
        screen_size =  QApplication.primaryScreen().availableGeometry()
        self.resize(self.settings.value("main.size", QSize(self.width(), 120)))
        self.move(self.settings.value("main.pos", 
            QPoint(math.floor(screen_size.width()/2 - math.floor(self.width()/2)), math.floor(screen_size.height()/5 * 4))))