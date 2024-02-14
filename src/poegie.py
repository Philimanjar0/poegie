import sys

from mainwindow import Main
from PyQt5.QtWidgets import QApplication

import sys

app = QApplication([])

def app_shutdown(event):
    app.quit()
    event.accept()

main = Main(app_shutdown)

# The big try catch to close the app gracefully if my stuff didnt work :peepoClap:
def excepthook(exctype, value, traceback):
    print(f"Unhandled exception caught: {exctype}, {value}")
    print(traceback.tb_frame)
    print("exiting immediately")
    main.close()
    sys.stdout.close()
    sys.exit()

sys.excepthook = excepthook

main.show()
app.exec_()