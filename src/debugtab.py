from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLineEdit
from mss import mss
from compare import ImageProcessor
import cv2 as cv2
import numpy as np


class DebugTab(QWidget):
    def __init__(self, target_window):
        QWidget.__init__(self)
        
        self.image_processor = ImageProcessor()
        self.target_window = target_window

        layout = QHBoxLayout()

        button_raw = QPushButton("raw")
        button_raw.clicked.connect(lambda event : self.show(self.grab(), "raw"))
        layout.addWidget(button_raw)

        button_thresh = QPushButton("thresh")
        button_thresh.clicked.connect(lambda event : self.show(self.threshold()[1], "threshold"))
        layout.addWidget(button_thresh)

        button_key = QPushButton("keypoints")
        button_key.clicked.connect(lambda event : self.show(self.keypoints()[1], "keypoints"))
        layout.addWidget(button_key)

        button_icon = QPushButton("icon")
        button_icon.clicked.connect(lambda event : self.show(self.icon(), "crop"))
        layout.addWidget(button_icon)

        button_histo = QPushButton("hist")
        button_histo.clicked.connect(lambda event : self.histogram())
        layout.addWidget(button_histo)

        button_save = QPushButton("save")
        button_save.clicked.connect(lambda event : self.save())
        layout.addWidget(button_save)

        self.text = QLineEdit()
        layout.addWidget(self.text)

        button_class = QPushButton("classify")
        button_class.clicked.connect(lambda event : self.classify())
        layout.addWidget(button_class)

        self.setLayout(layout)

    
    def show(self, img, title):
        cv2.imshow(title, img)
        cv2.waitKey(0)

    def threshold(self):
        raw = self.grab()
        threshold, combined_mask = self.image_processor.find_mask(raw)
        return threshold, combined_mask
    
    def keypoints(self):
        raw = self.grab()
        threshold, combined_mask = self.image_processor.find_mask(raw)
        keypoints, combined_keypoints = self.image_processor.find_keypoints(threshold, raw)
        return keypoints, combined_keypoints

    def icon(self):
        raw = self.grab()
        keypoints = self.keypoints()[0]
        return self.image_processor.crop_to_icon(raw, keypoints)

    def histogram(self):
       img = self.icon()
       hist = self.image_processor.generate_histogram(img)

    def save(self):
        img = self.icon()
        if not cv2.imwrite(".\\resources\\images_icons\\" + self.text.text() + ".jpg", img):
            print("could not save")

    def classify(self):
        raw = self.grab()
        print(self.image_processor.classify_raw_image(raw))

    def grab(self):
        bounding_box = {'top': self.target_window.bench_craft_rect.top(), 
                'left': self.target_window.bench_craft_rect.left(),
                'width': self.target_window.bench_craft_rect.width(),
                'height': self.target_window.bench_craft_rect.height()}

        img = None
        with mss() as sct:
            img = sct.grab(bounding_box)
        return np.array(img)