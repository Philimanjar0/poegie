import sys
import os

from datetime import datetime
from mainwindow import Main
from PyQt5.QtWidgets import QApplication

import sys

# Set a log file
# if (not os.path.isdir('logs')):
#     os.mkdir('logs')

# time_affix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# sys.stdout = open(f'logs/log_{time_affix}.txt', 'w')

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