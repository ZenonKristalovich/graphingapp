from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QListWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPixmap
import os
from DropArea import DropAreaWidget
from graph_app import GraphApp

class File_Input(QWidget):
    # Define a signal that will be emitted when it's time to switch the page
    switch_to_graphing_page = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__()

        self.files = []

        # Outer layout to add padding around the grid layout
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(500, 100, 500, 300)  # Add margins (left, top, right, bottom)

        # Set up the main layout using QGridLayout
        main_layout = QGridLayout()
        main_layout.setSpacing(10)  # Add some spacing between widgets

        # Left Section: Current Files
        files_title = QLabel("Current Files")
        files_title.setStyleSheet("font-weight: bold; font-size: 36px;")
        main_layout.addWidget(files_title, 0, 0, 1, 2)  # Row 0, Column 0-1 (spans 2 columns)

        # List of Current Files
        self.file_list = QListWidget()
        self.file_list.setFixedWidth(600)
        self.file_list.setFixedHeight(800)
        self.file_list.setStyleSheet("font-size: 36px;")
        main_layout.addWidget(self.file_list, 1, 0, 3, 2)  # Row 1-4, Column 0-1 (spans 4 rows)

        # Clear Files Button
        clear_button = QPushButton("Clear Files")
        clear_button.setFixedWidth(600)
        clear_button.setFixedHeight(100)
        clear_button.clicked.connect(self.clear_files)
        clear_button.setStyleSheet("font-weight: bold; font-size: 36px;")
        main_layout.addWidget(clear_button, 4, 0, 1, 2)  # Row 5, Column 0-1 (spans 2 columns)

        # Right Section: Import Files and Drag-and-Drop
        import_button = QPushButton("Import Files")
        import_button.setFixedHeight(100)
        import_button.setFixedWidth(500)
        import_button.clicked.connect(self.open_file_dialog)
        import_button.setStyleSheet("font-weight: bold; font-size: 36px;")
        main_layout.addWidget(import_button, 1, 3)  # Row 1, Column 3

        # Drag and Drop Section
        self.drop_area = DropAreaWidget(self)
        self.drop_area.setFixedHeight(500)
        self.drop_area.setFixedWidth(500)

        self.drag_and_drop_label = QLabel("Drag and Drop Files Here")
        self.drag_and_drop_label.setFixedHeight(500)
        self.drag_and_drop_label.setFixedWidth(500)
        self.drag_and_drop_label.setStyleSheet("""
                                            border: 4px dashed black;
                                            font-size: 28px;
                                            padding: 10px; 
                                        """)
        self.drag_and_drop_label.setAlignment(Qt.AlignCenter)
        self.drag_and_drop_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        main_layout.addWidget(self.drop_area, 2, 3, 1, 1)  # Row 2, Column 3, spanning 2 rows
        main_layout.addWidget(self.drag_and_drop_label, 2, 3, 1, 1)  # Same position as drop area

        # Start Graphing Button
        start_graphing_button = QPushButton("Start Graphing")
        start_graphing_button.setFixedHeight(100)
        start_graphing_button.setFixedWidth(500)
        start_graphing_button.setStyleSheet("font-weight: bold; font-size: 36px;")
        start_graphing_button.clicked.connect(self.start_graphing)
        main_layout.addWidget(start_graphing_button, 3, 3)  # Row 4, Column 3

        # Add the main layout to the outer layout
        outer_layout.addLayout(main_layout)

        # Set the outer layout as the main layout
        self.setLayout(outer_layout)
        self.setWindowTitle("Graphing Application")
        self.showMaximized()

    def open_file_dialog(self):
        # Open file dialog to allow the user to select files
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "CSV Files (*.csv);;All Files (*)")
        if files:
            # Add files to the list
            for file in files:
                self.files.append(file)
                self.file_list.addItem(os.path.basename(file))

    def clear_files(self):
        # Clear all files from the list
        self.file_list.clear()

    def start_graphing(self):
        print("TEST")
        if len(self.files) == 0:
            self.show_warning("Must Have At Least One File")
        self.switch_to_graphing_page.emit(self.files)

    def show_warning(self, message):
        # Create a message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)  # Set the icon to Warning
        msg.setWindowTitle("Warning")     # Set the window title
        msg.setText(message)              # Set the warning message
        msg.addButton("I'll do better", QMessageBox.AcceptRole)

        # Show the message box
        msg.exec_()
