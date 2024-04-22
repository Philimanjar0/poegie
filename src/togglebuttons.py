from PyQt5.QtWidgets import QPushButton

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
        super(FeatureEnableToggle, self).__init__("allow input blocking")
        self.toggle_state = False
        self.setMaximumWidth(200)
        self.clicked.connect(self.handle_button_update)
        self.callback = callback
        self.setStyleSheet("background-color : red")
    
    def handle_button_update(self):
        self.callback()
        if (self.toggle_state):
            self.setText("allow input blocking")
            self.setStyleSheet("background-color : red")
        else:
            self.setText("disable input blocking")
            self.setStyleSheet("background-color : green")
        self.toggle_state = not(self.toggle_state)

class TrackingEnableToggle(QPushButton):
    def __init__(self, callback):
        super(TrackingEnableToggle, self).__init__("allow tracking")
        self.toggle_state = False
        self.setMaximumWidth(200)
        self.clicked.connect(self.handle_button_update)
        self.callback = callback
        self.setStyleSheet("background-color : red")
    
    def handle_button_update(self):
        self.callback()
        if (self.toggle_state):
            self.setText("allow data tracking")
            self.setStyleSheet("background-color : red")
        else:
            self.setText("disable data tracking")
            self.setStyleSheet("background-color : green")
        self.toggle_state = not(self.toggle_state)