import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

class DropAreaWidget(QWidget):
    def __init__(self, parent=None):
        super(DropAreaWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.parent = parent

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.isLocalFile() and url.toLocalFile().endswith('.csv') for url in urls):  # Accept only .csv files
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            csv_files = [url.toLocalFile() for url in urls if url.toLocalFile().endswith('.csv')]  # Accept only .csv files
            if csv_files:
                for file_path in csv_files:
                    self.parent.files.append(file_path)
                    self.parent.file_list.addItem(os.path.basename(file_path))  # Add the base name of each file
                event.acceptProposedAction()
            else:
                event.ignore()