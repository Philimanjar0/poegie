import math

from benchwindow import BenchWindow
from common import reference_enum
from mss import mss
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QCheckBox, QHBoxLayout, QGridLayout, QGroupBox
from togglebuttons import TargetWindowButton, FeatureEnableToggle

class ConfigTab(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.settings = QSettings('PoE', 'Hoagie')

        layout = QHBoxLayout()
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
        costsGroup = QGroupBox("block reroll for:")
        selection_layout = QGridLayout()
        costsGroup.setLayout(selection_layout)
        
        num_rows = 4
        for c in range(math.ceil(len(reference_enum)/num_rows)):
            for r in range(num_rows):
                single_index = c * num_rows + r
                if (single_index >= len(reference_enum)):
                    # If the number of elements does not evenly fit, early exit
                    break
                checkbox = QCheckBox(reference_enum[single_index])
                if (len(self.selected_for_stop) <= single_index):
                    self.selected_for_stop.insert(single_index, False)
                elif (self.selected_for_stop[single_index]):
                    checkbox.setChecked(2)
                checkbox.stateChanged.connect(lambda value, index=single_index : self.handle_selection_change(value, index))
                selection_layout.addWidget(checkbox, r, c)
        # return the widget containing the checkboxes
        return costsGroup

    def should_stop_on_index(self, index):
        return self.selected_for_stop[index]

    def close(self):
        print("CLOSING CONFIG TAB")
        self.settings.setValue("bench.size", self.target_window.size())
        self.settings.setValue("bench.pos", self.target_window.pos())
        self.settings.setValue("selection", self.selected_for_stop)

    def handle_selection_change(self, value, index):
        if (value == 2):
            self.selected_for_stop[index] = True
        else:
            self.selected_for_stop[index] = False
