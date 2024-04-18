from PyQt5.QtCore import QAbstractTableModel, Qt, QSettings
from PyQt5.QtWidgets import QTableView, QLabel, QGroupBox, QGridLayout, QHeaderView, QTableView, QWidget
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
        self.setLayout(self.main_layout)

    def increment(self, from_index, to_index):
        previous_value = self.table.model.underlying_data[from_index][to_index]
        self.table.model.underlying_data[from_index][to_index] = previous_value + 1

    def close(self):
        print("CLOSING TABLE")
        self.table.model.saveSettings()

