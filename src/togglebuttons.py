from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSizeGrip, QCheckBox, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
import math
from common import reference_enum
from hotkey import InputOutputManager
from benchwindow import BenchWindow

class TargetWindowButton(QPushButton):
    def __init__(self, callback):
        super(TargetWindowButton, self).__init__("set bench location")
        self.toggle_state = False
        self.clicked.connect(self.handle_button_update)
        self.callback = callback

    def handle_button_update(self):
        self.callback()
        if (self.toggle_state):
            self.setText("set bench location")
        else:
            self.setText("done")
        self.toggle_state = not(self.toggle_state)

class FeatureEnableToggle(QPushButton):
    def __init__(self, callback):
        super(FeatureEnableToggle, self).__init__("enable stopping")
        self.toggle_state = False
        self.clicked.connect(self.handle_button_update)
        self.callback = callback
        self.setStyleSheet("background-color : green")
    
    def handle_button_update(self):
        self.callback()
        if (self.toggle_state):
            self.setText("ENABLE")
            self.setStyleSheet("background-color : green")
        else:
            self.setText("DISABLE")
            self.setStyleSheet("background-color : RED")
        self.toggle_state = not(self.toggle_state)