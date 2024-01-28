from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSizeGrip, QCheckBox, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon, QPixmap
import math
from common import reference_enum
from hotkey import InputOutputManager
from benchwindow import BenchWindow
from togglebuttons import TargetWindowButton, FeatureEnableToggle
from mss import mss

class ConfigTab(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.settings = QtCore.QSettings('PoE', 'Hoagie')

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.selected_for_stop = []

        # show bench button
        self.show_target_button = TargetWindowButton(self.target_button_callback)
        layout.addWidget(self.show_target_button)
        self.target_window = BenchWindow()

        # enable button
        self.enable_button = FeatureEnableToggle(lambda : None) # No callback. TODO dis/enable ahk scripts?
        layout.addWidget(self.enable_button)
        # selection checkboxes
        self.init_selection_settings()
        layout.addWidget(self.generate_selection_buttons())

    def target_button_callback(self):
        if (self.show_target_button.toggle_state):
            self.target_window.hide()
        else:
            self.target_window.show()

    def init_selection_settings(self):
        read_in_selection = self.settings.value("selection", [])
        # Need to deserialize
        for i in range(len(read_in_selection)):
            if (read_in_selection[i] == 'false'):
                self.selected_for_stop.insert(i, False)
            else:
                self.selected_for_stop.insert(i, True)

    def generate_selection_buttons(self):
        selection_layout = QtWidgets.QGridLayout()
        sel_wid = QtWidgets.QWidget(self)
        sel_wid.setLayout(selection_layout)
        
        num_rows = 4
        for c in range(math.ceil(len(reference_enum)/num_rows)):
            for r in range(num_rows):
                single_index = c * num_rows + r
                if (single_index >= len(reference_enum)):
                    # If the number of elements does not evenly fit, early exit
                    break
                checkbox = QCheckBox(reference_enum[single_index])
                if (len(self.selected_for_stop) <= single_index):
                    print("inserting default")
                    self.selected_for_stop.insert(single_index, False)
                elif (self.selected_for_stop[single_index]):
                    checkbox.setChecked(2)
                checkbox.stateChanged.connect(lambda value, index=single_index : self.handle_selection_change(value, index))
                selection_layout.addWidget(checkbox, r, c)
        # return the widget containing the checkboxes
        return sel_wid

    def should_stop_on_index(self, index):
        return self.selected_for_stop[index]

    def close(self):
        print("CLOSING CONFIG TAB")
        # self.settings.setValue("main.size", self.size())
        # self.settings.setValue("main.pos", self.pos())

        self.settings.setValue("bench.size", self.target_window.size())
        self.settings.setValue("bench.pos", self.target_window.pos())

        self.settings.setValue("selection", self.selected_for_stop)

        # self.hotkeys_manager.stop()
        # self.close_callback(event)

    def handle_selection_change(self, value, index):
        if (value == 2):
            self.selected_for_stop[index] = True
        else:
            self.selected_for_stop[index] = False
        print(self.selected_for_stop)
