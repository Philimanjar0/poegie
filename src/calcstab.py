from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QComboBox
from common import reference_enum

class CalcsTab(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # [ ] TODO use settings
        # self.settings = QtCore.QSettings('PoE', 'Hoagie')

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        entryLayout = QVBoxLayout()
        self.layout().addLayout(entryLayout, 3)

        self.addedFieldOptions = []

        # Static costs fields
        # life force per divine and bulk orb per divine
        costsGroup = QGroupBox("base costs (per divine)")
        statics = QVBoxLayout()
        costsGroup.setLayout(statics)
        entryLayout.addWidget(costsGroup)
        self.lifeforceEntry = self.addStaticRow("lifeforce", statics)
        self.bulkEntry = self.addStaticRow("bulk orb", statics)

        # User input for returns
        revenueGroup = QGroupBox("returns (per divine)")
        returns = QVBoxLayout()
        self.returnsChild = QVBoxLayout()
        returns.addLayout(self.returnsChild)
        revenueGroup.setLayout(returns)
        entryLayout.addWidget(revenueGroup)

        # output text
        outputGroup = QGroupBox("profits (in divines)")
        output = QVBoxLayout()
        outputGroup.setLayout(output)
        mainLayout.addWidget(outputGroup)
        self.outputText = QLabel()
        self.outputText.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        output.addWidget(self.outputText)
        
        # add buttons and things
        mainLayout.addWidget(outputGroup, 7)
        returns.addLayout(self.addOutcomeSelection())
        calculateButton = QPushButton("calc avg profit")
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
        if lifeForcePerDiv == None or lifeForcePerDiv < 1:
            return
        lifeForcePerDiv = 1 / lifeForcePerDiv

        numRolls = 1/(numSuccess * 1/16)
        lifeForceCost = (numRolls * 30) * lifeForcePerDiv

        orbCost = self.readInputAsFloat(self.bulkEntry)
        if orbCost == None or orbCost < 1:
            return
        orbCost = 1/orbCost
        
        totalCost = lifeForceCost + orbCost
        profit = (1 / (returns/numSuccess)) - totalCost
        
        self.outputText.setText("per orb: " + str(round(profit, 4)) + "\n percent return: " + str(round((profit/totalCost) * 100, 0)) + " %")

    def addFormField(self, key):
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(QLabel(key), 4)
        horizontalLayout.addWidget(QLineEdit(), 6)
        button = QPushButton("x")
        button.setMinimumWidth(7)
        button.setStyleSheet("background-color : red")

        button.clicked.connect(lambda event, toRemove=horizontalLayout, keyToRemove=key : self.removeRow(event, toRemove, key))
        horizontalLayout.addWidget(button, 1)
        return horizontalLayout

    def addOutcomeSelection(self):
        horizontalLayout = QHBoxLayout()
        self.selectioncombo = QComboBox()
        self.selectioncombo.addItems(reference_enum)
        button = QPushButton("add")
        button.setMinimumWidth(20)
        button.clicked.connect(lambda event : self.addRow(event))
        horizontalLayout.addWidget(self.selectioncombo, 8)
        horizontalLayout.addWidget(button, 2)
        self.outcomeSelection = horizontalLayout
        return horizontalLayout

    def addStaticRow(self, key, parent):
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(QLabel(key), 3)
        inputBox = QLineEdit()
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