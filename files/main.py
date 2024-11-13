import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from file_input import File_Input 
from graph_app import GraphApp
from multi_graph import MultiGraphApp
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the stacked widget
        self.stacked_widget = QStackedWidget(self)
        
        # Create the File_Input widget
        self.file_input_page = File_Input(self)  # Pass the main window to the File_Input widget
        
        # Connect the signal from File_Input to a method in MainWindow
        self.file_input_page.switch_to_graphing_page.connect(self.switch_to_graphing_page)

        # Add the File_Input page to the stacked widget
        self.stacked_widget.addWidget(self.file_input_page)

        # Create the Graphing page (empty for now)
        self.graphing_page = QWidget()  # Placeholder for your graphing page

        # Add the Graphing page to the stacked widget
        self.stacked_widget.addWidget(self.graphing_page)

        # Set up the layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        
        # Create the central widget and set the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Window setup
        self.setWindowTitle("Graphing Application")
        self.showMaximized()

    def switch_to_graphing_page(self, files):

        # Create the Graphing page and pass the files to it
        if len(files) == 1:
            self.graphing_page = GraphApp(files[0])#.setFont(QFont("Arial", 18))
        else:
            self.graphing_page = MultiGraphApp(files)
        self.graphing_page.switch_to_select_page.connect(self.switch_to_select_page)
        
        # Add the Graphing page to the stacked widget
        self.stacked_widget.addWidget(self.graphing_page)

        # Switch to the graphing page
        self.stacked_widget.setCurrentWidget(self.graphing_page)

        # Now remove the File_Input page
        self.stacked_widget.removeWidget(self.file_input_page)
        self.file_input_page.deleteLater()  # Free the memory of the File_Input page
        
        # Optionally, if you no longer need the `file_input_page`, you can set it to None
        self.file_input_page = None
    
    def switch_to_select_page(self):
        # Add the Graphing page to the stacked widget
        self.file_input_page = File_Input(self)
        self.file_input_page.switch_to_graphing_page.connect(self.switch_to_graphing_page)
        self.stacked_widget.addWidget(self.file_input_page)
        self.stacked_widget.setCurrentWidget(self.file_input_page)
        self.stacked_widget.removeWidget(self.graphing_page)
        self.graphing_page.deleteLater() 

    def paintEvent(self, event):
        # Create a QPainter object
        painter = QPainter(self)

        # Load the background image
        background = QPixmap('files/base_background.png')

        # Draw the background image scaled to the widget's size
        painter.drawPixmap(self.rect(), background)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set a general font for the entire application
    general_font = QFont("Arial", 8)  # Customize the font and size as needed
    app.setFont(general_font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
