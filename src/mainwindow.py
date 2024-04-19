import math
import numpy as np

from benchwindow import BenchWindow
from calcstab import CalcsTab
from common import reference_enum
from compare import ImageProcessor
from configtab import ConfigTab
from data import DataTab
from debugtab import DebugTab
from markov_mat import DataTableTab
from errorpopup import ErrorPopup
from hotkey import InputOutputManager
from mss import mss
from PyQt5.QtCore import QSize, QPoint, QSettings, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTabWidget
from togglebuttons import TargetWindowButton, FeatureEnableToggle

# Some TODO items (1h)
#  [ ] Clean up first tab. Button for enable/disable tracking, and a button for just input blocking
#  [ ] less naive weights for profit tab?
#  [x] export and clear buttons for table
#  [ ] make another release
#  [ ] re-record a video with script

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
        self.tableTab = DataTableTab()
        self.button_pressed_last = False
        self.imageProcessor = ImageProcessor()
        self.hotkeys_manager = InputOutputManager(input_passthrough_condition=lambda pos : self.trigger_check(pos))  
        
        tabs.addTab(self.configTab, "config")
        tabs.addTab(self.calcsTab, "calculator")
        tabs.addTab(self.tableTab, "table")

        # [ ] TODO dep, remove this tab
        # tabs.addTab(self.dataTab, "data")

        # Uncomment the following to debug the openCV stuff
        # tabs.addTab(self.debugTab, "debug")

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
        self.tableTab.close()

        self.hotkeys_manager.stop()

    def handle_selection_change(self, value, index):
        if (value == 2):
            self.selected_for_stop[index] = True
        else:
            self.selected_for_stop[index] = False

    def trigger_check(self, mouse_position):
        if (not self.configTab.target_window.isVisible()
                and self.configTab.enable_button.toggle_state):
            if (self.configTab.target_window.bench_button_rect.contains(mouse_position[0], mouse_position[1])):
                print("button pressed")
                imageFound = self.categorize_image()
                if imageFound == -1:
                    return True
                elif self.configTab.should_stop_on_index(imageFound):
                    print("Found a desired item, blocking reroll")
                    return False
                elif imageFound == self.last_seen:
                    print("duplicate duplicate item, blocking reroll")
                    return False
                # This is just a normal reroll, increment and unblock the input.
                if (self.button_pressed_last == True):
                    print(f"incrementing {imageFound}")
                    self.tableTab.increment(self.last_seen, imageFound)
                    self.dataTab.increment(imageFound)
                self.button_pressed_last = True
                self.last_seen = imageFound
                return True
            elif (self.configTab.target_window.window_hitbox.contains(mouse_position[0], mouse_position[1])):
                # Press was in the crafting window
                print("window clicked")
                if (self.button_pressed_last == True):
                    itemInWindow = self.parseText()
                    if not itemInWindow == self.last_seen:
                        self.tableTab.increment(self.last_seen, itemInWindow)
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
            return index
        except Exception as e:
            print(f"Could not parse text {copiedText}. Skipping increment step.")
        return -1

    def init_window_settings(self):
        screen_size =  QApplication.primaryScreen().availableGeometry()
        self.resize(self.settings.value("main.size", QSize(self.width(), 120)))
        self.move(self.settings.value("main.pos", 
            QPoint(math.floor(screen_size.width()/2 - math.floor(self.width()/2)), math.floor(screen_size.height()/5 * 4))))