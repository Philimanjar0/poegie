from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, Qt, QSettings, QModelIndex
from PyQt5.QtWidgets import QTableView, QLabel, QGroupBox, QGridLayout, QHeaderView, QTableView, QWidget, QHBoxLayout, QPushButton, QFileDialog
import numpy as np
from common import reference_enum

class SampleData(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('PoE', 'Hoagie')
        self.underlying_data = [[0 for i in range(len(reference_enum))] for j in range(len(reference_enum))]
        self.init_from_stored()

    def init_from_stored(self):
        persisted_data = self.settings.value("mat_data", [])
        if not len(persisted_data) == len(reference_enum):
            print("Invalid settings upon initialization: " + str(persisted_data))
            print("reseting data")
            self.settings.remove("mat_data")
            return
        for r, row in enumerate(persisted_data):
            for c, value in enumerate(row):
                self.underlying_data[r][c] = value
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.underlying_data[index.row()][index.column()]
            # return index.row() + index.column()
        else:
            return None

    def init_data(self):
        size = len(reference_enum)
        for r in range(size):
            for c in range(size):
                self.underlying_data[r][c] = 0
        self.refresh(0, 0, size, size)

    def saveSettings(self):
        self.settings.setValue("mat_data", self.underlying_data)

    def rowCount(self, parent):
        return len(reference_enum)
    
    def columnCount(self, parent):
        return len(reference_enum)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        return reference_enum[section]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def add_mapping(self, color, area):
        self.mapping[color] = area

    def clear_mapping(self):
        self.mapping = {}

    def refresh(self, index_t, index_l, index_b, index_r):
        size = len(reference_enum)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(size, size))

class DataMatrix(QTableView):
    def __init__(self):
        QTableView.__init__(self)

        self.model = SampleData()
        self.setModel(self.model)

        self.horizontalHeader().setMinimumSectionSize(90)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

class DataTableTab(QWidget):
    def __init__(self):
        super().__init__()
        self.table = DataMatrix()
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.table, 2, 1)
        self.main_layout.addWidget(QLabel("FROM:"), 2, 0, alignment=Qt.AlignTop)
        self.main_layout.addWidget(QLabel("TO:"), 1, 1)    
        group = QGroupBox("How to read this?")
        sub_layout = QGridLayout()
        group.setLayout(sub_layout)
        sub_layout.addWidget(QLabel("This is a transition matrix. Each cell represents how many times you have had some item in the FROM axis, and rolled it to the item in the TO axis."), 0, 0)
        self.main_layout.addWidget(group, 0, 1)

        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout, 3, 1)
        self.addSaveButton()
        self.addResetButton()
        self.setLayout(self.main_layout)

    def increment(self, from_index, to_index):
        previous_value = self.table.model.underlying_data[from_index][to_index]
        self.table.model.underlying_data[from_index][to_index] = previous_value + 1
        # Force a refresh of the table view in case the application is not in focus
        self.table.viewport().update()

    def close(self):
        print("CLOSING TABLE")
        self.table.model.saveSettings()

    def addResetButton(self):
        button = QPushButton("reset data")
        button.clicked.connect(self.reset_data)
        self.button_layout.addWidget(button)
    
    def reset_data(self):
        self.table.model.init_data()

    def addSaveButton(self):
        button = QPushButton("export to csv")
        button.clicked.connect(self.openFileDialog)
        self.button_layout.addWidget(button)

    def openFileDialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter(str("CSV *.csv"))
        fileNames = []
        dialog.exec_()
        fileNames = dialog.selectedFiles()
        if not len(fileNames) == 1:
            return
        fileName = fileNames[0]
        if not fileName.endswith(".csv"):
            fileName += ".csv"
        
        h_header = np.array(reference_enum).reshape(1, len(reference_enum))
        v_header = np.concatenate((np.array([" "]), np.array(reference_enum)))
        v_header = v_header.reshape(len(reference_enum) + 1, 1)
        display_data = np.array(self.table.model.underlying_data).reshape(len(reference_enum), len(reference_enum))
        with_h_header = np.vstack((h_header, display_data))
        np.savetxt(fileName, np.hstack((v_header, with_h_header)), delimiter=",", fmt='%s', comments='')
