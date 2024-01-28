from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSizeGrip, QCheckBox, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon, QPixmap
import math
from common import reference_enum
from hotkey import InputOutputManager
from benchwindow import BenchWindow
from togglebuttons import TargetWindowButton, FeatureEnableToggle
from mss import mss

class CalcsTab(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        # [ ] TODO use settings
        # self.settings = QtCore.QSettings('PoE', 'Hoagie')

        mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(mainLayout)

        entryLayout = QtWidgets.QVBoxLayout()
        self.layout().addLayout(entryLayout, 3)

        self.addedFieldOptions = []

        # Static costs fields
        # life force per divine and bulk orb per divine
        costsGroup = QtWidgets.QGroupBox("base costs (per divine)")
        statics = QtWidgets.QVBoxLayout()
        costsGroup.setLayout(statics)
        entryLayout.addWidget(costsGroup)
        self.lifeforceEntry = self.addStaticRow("lifeforce", statics)
        self.bulkEntry = self.addStaticRow("bulk orb", statics)

        # User input for returns
        revenueGroup = QtWidgets.QGroupBox("returns (per divine)")
        returns = QtWidgets.QVBoxLayout()
        self.returnsChild = QtWidgets.QVBoxLayout()
        returns.addLayout(self.returnsChild)
        revenueGroup.setLayout(returns)
        entryLayout.addWidget(revenueGroup)

        # output text
        outputGroup = QtWidgets.QGroupBox("profits (in divines)")
        output = QtWidgets.QVBoxLayout()
        outputGroup.setLayout(output)
        mainLayout.addWidget(outputGroup)
        self.outputText = QtWidgets.QLabel()
        self.outputText.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        output.addWidget(self.outputText)
        
        # add buttons and things
        mainLayout.addWidget(outputGroup, 7)
        returns.addLayout(self.addOutcomeSelection())
        calculateButton = QtWidgets.QPushButton("calc avg profit")
        calculateButton.clicked.connect(lambda event : self.calcAndDisplayProfits())
        entryLayout.addWidget(calculateButton)


    def calcAndDisplayProfits(self):
        returns = 0
        for hbox in self.returnsChild.layout().children():
            nextValue = self.readInputAsFloat(hbox.itemAt(1).widget())
            if nextValue == None:
                return
            returns = returns + nextValue
        
        numSuccess = len(self.returnsChild.layout().children())
        if numSuccess < 1:
            return
        
        lifeForcePerDiv = self.readInputAsFloat(self.lifeforceEntry)
        if lifeForcePerDiv == None:
            return
        lifeForcePerDiv = 1 / lifeForcePerDiv

        numRolls = 1/(numSuccess * 1/19)
        lifeForceCost = (numRolls * 30) * lifeForcePerDiv

        orbCost = self.readInputAsFloat(self.bulkEntry)
        if orbCost == None:
            return
        orbCost = 1/orbCost
        
        totalCost = lifeForceCost + orbCost
        profit = (1 / (returns/numSuccess)) - totalCost
        
        self.outputText.setText("per orb: " + str(round(profit, 4)) + "\n percent return: " + str(round((profit/totalCost) * 100, 0)) + " %")

    def addFormField(self, key):
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(QtWidgets.QLabel(key), 4)
        horizontalLayout.addWidget(QtWidgets.QLineEdit(), 6)
        button = QtWidgets.QPushButton("x")
        button.setMinimumWidth(7)
        button.setStyleSheet("background-color : red")

        button.clicked.connect(lambda event, toRemove=horizontalLayout, keyToRemove=key : self.removeRow(event, toRemove, key))
        horizontalLayout.addWidget(button, 1)
        return horizontalLayout

    def addOutcomeSelection(self):
        horizontalLayout = QtWidgets.QHBoxLayout()
        self.selectioncombo = QtWidgets.QComboBox()
        self.selectioncombo.addItems(reference_enum)
        button = QtWidgets.QPushButton("add")
        button.setMinimumWidth(20)
        button.clicked.connect(lambda event : self.addRow(event))
        horizontalLayout.addWidget(self.selectioncombo, 8)
        horizontalLayout.addWidget(button, 2)
        self.outcomeSelection = horizontalLayout
        return horizontalLayout

    def addStaticRow(self, key, parent):
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(QtWidgets.QLabel(key), 3)
        inputBox = QtWidgets.QLineEdit()
        horizontalLayout.addWidget(inputBox, 7)
        parent.addLayout(horizontalLayout)
        return inputBox

    def removeRow(self, signal, layout, key):
        self.deleteItemsOfLayout(layout)
        self.returnsChild.removeItem(layout)
        self.addedFieldOptions.remove(key)

    def addRow(self, event):
        optionToAdd = self.selectioncombo.currentText()
        if optionToAdd in self.addedFieldOptions:
            return
        self.returnsChild.addLayout(self.addFormField(optionToAdd))
        self.addedFieldOptions.append(optionToAdd)

    def readInputAsFloat(self, inputBox):
        text = inputBox.text()
        if text == "" :
            return None
        try:
            return float(text)
        except:
            return None

    def deleteItemsOfLayout(self, layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
             else:
                 self.deleteItemsOfLayout(item.layout())

    def close(self):
        print("CLOSING PROFITS")