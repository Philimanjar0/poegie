from PyQt5 import QtCore
settings = QtCore.QSettings('PoE', 'Hoagie')
settings.remove("data")