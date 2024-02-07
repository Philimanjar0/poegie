from PyQt5.QtWidgets import QMessageBox
import sys

class ErrorPopup(QMessageBox):
    def __init__(self, text, text_verbose, should_close):
        super(ErrorPopup, self).__init__()
        self.should_close = should_close
        self.setWindowTitle("Startup error")
        self.setText(text)
        self.setDetailedText(text_verbose)
        self.setStandardButtons(QMessageBox.StandardButton.Close)
        self.buttonClicked.connect(self.handleButton)
        self.exec_()

    def handleButton(self, event):
        if self.should_close:
            # Something is very wrong, kill the app.
            sys.exit()
