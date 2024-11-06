import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from newfrontend import GraphApp

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
                self.parent.file_names.extend(csv_files)
                self.parent.display_files()
                event.acceptProposedAction()
            else:
                event.ignore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 700, 700)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Maker")
        self.setWindowIcon(QIcon("pot.png"))
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("QWidget { background-color: rgba(200, 160, 255, 1); }")

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Graph Maker")
        font = QFont("Arial", 30, QFont.Bold)
        title.setFont(font)
        title.setStyleSheet("color: #4B0082;")
        title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(title)
        layout.addSpacing(20)

        self.upload_button = QPushButton("Upload Files")
        self.set_button_style(self.upload_button)
        self.upload_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.upload_button)
        layout.addSpacing(10)

        self.drop_area = DropAreaWidget(self)
        self.drop_area.setMinimumHeight(100)
        self.drop_area.setStyleSheet("background-color: rgba(200, 160, 255, 1);")

        self.drop_label = QLabel("Drag and Drop Here")
        self.drop_label.setFont(QFont("Arial", 14))
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("color: #4B0082; border: 2px dashed #4B0082; padding: 20px;")
        self.drop_label.setFixedHeight(100)
        self.drop_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        drop_area_layout = QVBoxLayout(self.drop_area)
        drop_area_layout.addWidget(self.drop_area)
        drop_area_layout.addWidget(self.drop_label)
        drop_area_layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.drop_area)

        self.file_display = QLabel("")
        self.file_display.setStyleSheet("color: #4B0082; padding: 10px; font-size: 20px;")
        layout.addWidget(self.file_display)
        layout.addStretch(1)

        clear_button = QPushButton("Clear Files")
        self.set_button_style(clear_button)
        clear_button.clicked.connect(self.clear_files)
        layout.addWidget(clear_button)

        convert_button = QPushButton("Make Graph")
        self.set_button_style(convert_button)
        convert_button.clicked.connect(self.convert_files)
        layout.addWidget(convert_button)

        layout.addStretch(1)
        self.file_names = []

    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if files:
            self.file_names.extend(files)
            self.display_files()

    def display_files(self):
        file_names_only = [os.path.basename(file) for file in self.file_names]
        self.file_display.setText('\n'.join(file_names_only))

    def clear_files(self):
        self.file_names = []
        self.file_display.setText("")

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #4B0082; 
                color: white; 
                font-size: 20px; 
                padding: 10px; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5C0094;
            }
            QPushButton:pressed {
                background-color: #3D0071;
                padding-left: 12px;
                padding-top: 12px;
            }
        """)

    def convert_files(self):
        if len(self.file_names) <= 0:
            QMessageBox.information(self, "Error", "Must provide at least 1 file", QMessageBox.Ok)
            return

        try:
            global app
            app = GraphApp(self.file_names)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to graph files:\n{str(e)}", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
