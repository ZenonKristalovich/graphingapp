from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect, Qt

class ImageWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)