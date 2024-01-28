from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSizeGrip, QCheckBox, QMainWindow, QTabWidget, QFileDialog 
from PyQt5.QtGui import QIcon, QPixmap
import math
from common import reference_enum
from hotkey import InputOutputManager
from benchwindow import BenchWindow
from togglebuttons import TargetWindowButton, FeatureEnableToggle
from mss import mss
import numpy as np

class DataTab(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.settings = QtCore.QSettings('PoE', 'Hoagie')

        self.data = []
        self.gridWidgets = []
        self.parent = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.parent)
        self.initFields()
        self.readSettings()
        self.parent.addLayout(self.button_layout)
        self.addResetButton()
        self.addSaveButton()
        print(self.data)
        print(type(self.data[7]))

    def initFields(self):   
        group = QtWidgets.QGroupBox("times rolled")
        gridLayout = QtWidgets.QGridLayout()
        group.setLayout(gridLayout)
        self.parent.addWidget(group)
        num_rows = 4
        for c in range(math.ceil(len(reference_enum)/num_rows)):
            for r in range(num_rows):
                single_index = c * num_rows + r
                if (single_index >= len(reference_enum)):
                    # If the number of elements does not evenly fit, early exit
                    break
                self.data.insert(single_index, 0)
                label = QtWidgets.QLabel(reference_enum[single_index] + ": 0")
                gridLayout.addWidget(label, r, c)
                self.gridWidgets.insert(single_index, label)

    def addResetButton(self):
        button = QtWidgets.QPushButton("reset data")
        button.clicked.connect(self.reset)
        self.button_layout.addWidget(button)

    def addSaveButton(self):
        button = button = QtWidgets.QPushButton("export to csv")
        button.clicked.connect(self.openFileDialog)
        self.button_layout.addWidget(button)

    def openFileDialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter(str("CSV *.csv"))
        fileNames = []
        dialog.exec_()
        fileNames = dialog.selectedFiles()
        fileName = fileNames[0]
        if not len(fileNames) == 1:
            print("too many files selected")
            return
        if not fileName.endswith(".csv"):
            fileName += ".csv"
        print(','.join(reference_enum))
        np.savetxt(fileName, np.array(self.data).reshape(1, len(reference_enum)).astype(np.uint8), delimiter=",", header=','.join(reference_enum), fmt='%1.0f', comments='')

    def reset(self):
        for i, name in enumerate(reference_enum):
            print("reseting " + name)
            self.setValue(i, 0)

    def increment(self, index):
        print(index)
        newValue = self.data[index] + 1
        self.setValue(index, newValue)

    def setValue(self, index, value):
        self.data[index] = value
        self.gridWidgets[index].setText(reference_enum[index] + ": " + str(value))

    def readSettings(self):
        persisted_data = self.settings.value("data", [])
        if not len(persisted_data) == len(reference_enum):
            print("Invalid settings upon initialization: " + str(persisted_data))
            print("reseting data")
            self.settings.remove("data")
            return
        for i, value in enumerate(persisted_data):
            self.setValue(i, int(value))

    def saveSettings(self):
        self.settings.setValue("data", self.data)

    def close(self):
        print("CLOSING DATA")
        self.saveSettings()