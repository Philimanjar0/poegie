import math

from PyQt5.QtCore import QSettings, Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QSizeGrip, QMainWindow, QApplication

class BenchWindow(QMainWindow):
    def __init__(self):
        self.settings = QSettings('PoE', 'Hoagie')
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.oldPos = None
        label = QLabel(self)
        pixmap = QPixmap('resources\menu3.png')
        label.setPixmap(pixmap)
        self.label = label
        self.setGeometry(0, 0, 255, 458)

        self.init_window_settings()

        self.bench_craft_rect = self.updateCraftWindowRectangle()
        self.bench_button_rect = self.updateCraftButtonRectangle()
        self.window_hitbox = self.updateWindowHitbox()

        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)
        
        self.ignore_next_resize = True

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)
        pixmap1 = pixmap = QPixmap('resources\menu3.png')
        self.pixmap = pixmap1.scaled(self.width(), self.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.width(), self.height())
        self.bench_craft_rect = self.updateCraftWindowRectangle()
        self.bench_button_rect = self.updateCraftButtonRectangle()
        self.window_hitbox = self.updateWindowHitbox()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            delta = event.globalPos() - self.oldPos
            if not(self.pos().x() + delta.x() < 0 or self.pos().y() + delta.y() < 0):
                self.move(self.pos() + delta)
                self.oldPos = event.globalPos()
                self.bench_craft_rect = self.updateCraftWindowRectangle()
                self.bench_button_rect = self.updateCraftButtonRectangle()
                self.window_hitbox = self.updateWindowHitbox()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def updateCraftButtonRectangle(self):
        return QRect(
            math.floor(self.size().width() * 0.17 + self.pos().x()),
            math.floor(self.size().height() * 0.79 + self.pos().y()), 
            math.floor(self.size().width() * (0.84 - 0.17)),
            math.floor(self.size().height() * (0.90 - 0.79)))

    def updateCraftWindowRectangle(self):
        return QRect(
            math.floor(self.size().width() * 0.29 + self.pos().x()),
            math.floor(self.size().height() * 0.15 + self.pos().y()), 
            math.floor(self.size().width() * (0.71 - 0.29)),
            math.floor(self.size().height() * (0.67 - 0.15)))

    def updateWindowHitbox(self):
        size_mult_x = 0.007
        size_mult_y = 0.015
        if (self.bench_craft_rect == None):
            return None
        return self.bench_craft_rect.adjusted(
            math.floor((self.bench_craft_rect.left() * (1.0 - size_mult_x)) - self.bench_craft_rect.left()),
            math.floor((self.bench_craft_rect.top() * (1.0 - size_mult_y)) - self.bench_craft_rect.top()),
            math.floor((self.bench_craft_rect.right() * (1.0 + size_mult_x)) - self.bench_craft_rect.right()),
            math.floor((self.bench_craft_rect.bottom() * (1.0 + size_mult_y)) - self.bench_craft_rect.bottom()))

    def init_window_settings(self):
        screen_size =  QApplication.primaryScreen().availableGeometry()
        self.resize(self.settings.value("bench.size", QSize(self.width(), self.height())))
        self.move(self.settings.value("bench.pos", QPoint(50, 50)))
