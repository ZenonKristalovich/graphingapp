from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtWidgets import QComboBox, QLineEdit, QColorDialog, QSizePolicy
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_handler import read_multi_csv
from plotter import draw_multi_plot
from button_functions import GraphFunctions
import matplotlib.pyplot as plt
import re
from PyQt5.QtGui import QGuiApplication
import sys
import os
from PyQt5.QtGui import QIcon



class MultiGraphApp(QWidget):

    switch_to_select_page = pyqtSignal()

    def __init__(self, filenames=None, width=7, height=2, dpi=100):
        super().__init__()
        self.filenames = filenames if filenames else []
        self.file_names_short = [path.split('/')[-1].replace('.csv', '') for path in self.filenames]

        # Create an instance of GraphFunctions and pass self
        self.functions = GraphFunctions(self)
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()
        self.width = screen_width / 2256
        self.height = screen_height/ 1504

        if hasattr(sys, '_MEIPASS'):
            # If running as a bundled app (PyInstaller)
            base_image = os.path.join(sys._MEIPASS, 'base_background.png')
            white_image = os.path.join(sys._MEIPASS, 'white.png')
            blue_image = os.path.join(sys._MEIPASS, 'blue.png')
            icon = os.path.join(sys._MEIPASS, 'Gamma.jpg')
        else:
            # If running from the source directory
            base_image = 'base_background.png'
            white_image = 'white.png'
            blue_image = 'blue.png'
            icon = 'Gamma.jpg'

        self.setWindowIcon(QIcon(icon))

        #Data
        self.font_size = 24
        self.font_style = "Arial"
        self.x_bounds = None
        self.y_bounds = None
        self.dashed_lines = []
        self.title = None
        self.x_title = None
        self.y_title = None
        self.pointer_size = 12
        self.component_names =  ['A', 'B0', 'B1','XX','XX','XX']
        self.component_titles = ['A: Fe3+ (Td)','B0: Fe3+ (Oh)','B1:Fe3+ (Oh)','Unknown','Unknown']
        self.pointer_types = ['o','o','o','o','o','o','o','o']
        self.colours = ['#FF1493','#8A2BE2','#20B2AA','#ff0000','#ff0000','#ff0000']
        self.legend = "Inside"
        self.hollow = self.colours
        self.line_size = 3
        self.cap_size = 4

        # Load data
        self.matrix, self.row_names,self.temperatures,self.components = read_multi_csv(self.filenames)
        self.total_graphs = int(len(self.matrix)/2)
        self.current_file_index = 0
        self.current_component_index =0
        self.files = len(filenames)

        # Set up layout
        main_layout = QVBoxLayout()
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(int(5*self.height))

        #start up
        self.start_up()

        # Set up UI elements
        filter_title = QLabel("Filter Options")
        filter_title.setStyleSheet("font-weight: bold; font-size: 36px;")
        self.grid.addWidget(filter_title, 0, 1,1,2)

        label = QLabel(self)
        pixmap = QPixmap(white_image)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)  # Optional: to center the image in the label
        label.setScaledContents(True)
        self.grid.addWidget(label, 1, 1, 21, 5)

        #SetUp Rows
        for x in range(1,21):
            label = QLabel(self)
            if( x % 2 == 0):
                pixmap = QPixmap(blue_image)
            else:
                pixmap = QPixmap(white_image)
            label.setPixmap(pixmap)
            label.setScaledContents(True)
            self.grid.addWidget(label, x, 1, 1, 5)

        self.setup_labels(self.grid)
        self.setup_inputs(self.grid)
        self.setup_pointers(self.grid)
        self.setup_buttons(self.grid)
        self.setup_checkboxes(self.grid)
        self.add_blanks(self.grid)
        self.graph_title = QLabel(f'Graph Image {self.current_file_index + 1}/{self.total_graphs * self.components}')
        self.graph_title.setStyleSheet("font-weight: bold; font-size: 36px;")
        self.graph_title.setFixedWidth(int(600*self.width))
        self.grid.addWidget(self.graph_title, 0, 6)

        self.main_button = QPushButton("Back To Main")
        self.main_button.clicked.connect(self.go_main)
        self.main_button.setFixedHeight(int(60*self.height))
        self.main_button.setStyleSheet("font-weight: bold; font-size: 28px;")
        self.grid.addWidget(self.main_button, 0, 7)

        #Blanks
        blank = QLabel("")
        blank.setFixedWidth(int(600*self.width))
        self.grid.addWidget(blank, 0, 6)

        # Set up Matplotlib canvas
        self.canvas = FigureCanvas(Figure(figsize=(width, height), dpi=dpi))
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.setFixedHeight(int(700*self.height))
        self.grid.addWidget(self.canvas, 1, 6, 12, 2)

        # Image Control Buttons
        self.setup_navigation_buttons(self.grid)
        main_layout.addLayout(self.grid)
        self.setLayout(main_layout)
        self.setWindowTitle("Graphing Application")
        self.showMaximized()

        if self.matrix:
            self.plot_data()

    # Separate methods for UI setup and navigation
    def setup_labels(self, grid):
        labels = [
            "Font Size:", "Font Type:", "X-Bounds:", "Y-Bounds:", 
            "Dashed Line:", "Title:", "X-title:", "Y-title:","Pointer Size:", 
            "Pointer Shape:"
        ]
        for i, label in enumerate(labels, start=1):
            lbl = QLabel(label)
            lbl.setFixedWidth(int(150*self.width))
            lbl.setFixedHeight(int(40*self.height))
            grid.addWidget(lbl, i, 1)

        lbl = QLabel("Line Size:")
        lbl.setFixedWidth(int(150*self.width))
        lbl.setFixedHeight(int(45*self.height))
        grid.addWidget(lbl, 11 + self.files, 1)

        lbl = QLabel("Cap Size: ")
        lbl.setFixedWidth(int(150*self.width))
        lbl.setFixedHeight(int(45*self.height))
        grid.addWidget(lbl, 12 + self.files, 1)

        lbl = QLabel("Legend Position:")
        lbl.setFixedWidth(int(150*self.width))
        lbl.setFixedHeight(int(45*self.height))
        grid.addWidget(lbl, 13 + self.files, 1)

    def setup_inputs(self, grid):
        self.inputs = []

        # Create a QComboBox for the font size selection
        self.font_size_input = QComboBox()
        self.font_size_input.setEditable(True)  # Allow the user to type in an exact size
        self.font_size_input.setFixedWidth(int(150*self.width))
        self.font_size_input.setFixedHeight(int(40*self.height)) 
        common_font_sizes = ["8", "10", "12", "14", "16", "18", "20", "24", "28", "32", "36"]
        self.font_size_input.addItems(common_font_sizes)

        # Add the QComboBox to the grid, spanning 2 columns
        grid.addWidget(self.font_size_input, 1, 2, 1, 2)
        self.font_size_input.setCurrentText(str(self.font_size)) 
        self.inputs.append(self.font_size_input)

        # Font style selection (spanning 2 columns)
        self.font_style_input = QComboBox()
        self.font_style_input.setFixedWidth(int(300*self.width))  
        self.font_style_input.setFixedHeight(int(40*self.height)) 
        common_font_styles = ["Arial", "Times New Roman", "Courier New", "Comic Sans MS", "Verdana","Impact","Lucida Console","DejaVu Sans"]
        self.font_style_input.addItems(common_font_styles)

        grid.addWidget(self.font_style_input, 2, 2, 1, 2)  # Spanning 2 columns
        self.inputs.append(self.font_style_input)

        # X bounds (min and max) each taking 1 column
        self.x_min = QLineEdit()
        self.x_min.setFixedWidth(int(100*self.width))  # Set fixed width
        grid.addWidget(self.x_min, 3, 2)  # Min value in column 2
        self.x_max = QLineEdit()
        self.x_max.setFixedWidth(int(100*self.width))  # Set fixed width
        grid.addWidget(self.x_max, 3, 3)  # Max value in column 3

        # Y bounds (min and max) each taking 1 column
        self.y_min = QLineEdit()
        self.y_min.setFixedWidth(int(100*self.width))  # Set fixed width
        grid.addWidget(self.y_min, 4, 2)  # Min value in column 2
        self.y_max = QLineEdit()
        self.y_max.setFixedWidth(int(100*self.width))  # Set fixed width
        grid.addWidget(self.y_max, 4, 3)  # Max value in column 3

        # Create QLineEdit inputs for the rest, each will span 2 columns
        other_labels = [
            "Dashed Line:", "Title:", "X-title:", "Y-title:"
        ]
        
        for i, label in enumerate(other_labels, start=5):  # Start from row 5 onwards
            input_field = QLineEdit()
            input_field.setFixedWidth(int(300*self.width))  # Set fixed width
            grid.addWidget(input_field, i, 2, 1, 2)  # Spanning 2 columns
            self.inputs.append(input_field)
        
        # Create a QComboBox for the font size selection
        self.pointer_size_input = QComboBox()
        self.pointer_size_input.setEditable(True)  # Allow the user to type in an exact size
        self.pointer_size_input.setFixedWidth(int(150*self.width)) 
        self.pointer_size_input.setFixedHeight(int(40*self.height)) 
        common_pointer_sizes = ["5", "6", "8", "10", "12", "14", "16", "18", "20"]
        self.pointer_size_input.addItems(common_pointer_sizes)
        self.pointer_size_input.setCurrentText(str(self.pointer_size))
        grid.addWidget(self.pointer_size_input, 9, 2) 

        self.hollow_input = QComboBox()
        self.hollow_input.setFixedWidth(int(150*self.width)) 
        self.hollow_input.setFixedHeight(int(40*self.height)) 
        hollow_options = ["Full","Hollow"]
        self.hollow_input.addItems(hollow_options)
        grid.addWidget(self.hollow_input, 9, 3) 

        self.line_input = QComboBox()
        self.line_input.setEditable(True)
        self.line_input.setFixedWidth(int(150*self.width)) 
        self.line_input.setFixedHeight(int(40*self.height)) 
        line_options = ["2","3","4","6","8","10","12"]
        self.line_input.addItems(line_options)
        self.line_input.setCurrentText(str(self.line_size))
        grid.addWidget(self.line_input, 11 + self.files, 2) 

        self.cap_input = QComboBox()
        self.cap_input.setEditable(True)
        self.cap_input.setFixedWidth(int(150*self.width)) 
        self.cap_input.setFixedHeight(int(40*self.height)) 
        line_options = ["2","4","6","8","10","12"]
        self.cap_input.addItems(line_options)
        self.cap_input.setCurrentText(str(self.cap_size))
        grid.addWidget(self.cap_input, 12 + self.files, 2)

        self.legend_input = QComboBox()
        self.legend_input.setFixedWidth(int(200*self.width)) 
        self.legend_input.setFixedHeight(int(40*self.height)) 
        legend_pos = ["TopLeft","TopRight","BottomLeft","BottomRight","Inside","No Legend"]
        self.legend_input.addItems(legend_pos)
        self.legend_input.setCurrentText(self.legend)
        grid.addWidget(self.legend_input, 13 + self.files, 2, 1, 2) 

    def setup_pointers(self, grid):
        self.pointers = []
        self.alter_componenets = []
        self.color_buttons = []
        start = 11
        common_pointer_shapes = ["Point (.)", "Pixel (,)","Circle (o)","Triangle Down (v)",
                                "Triangle Up (^)","Triangle Left (<)","Triangle Right (>)",
                                "Square (s)", "Pentagon (p)", "Star (*)", "Hexagon1 (h)",
                                "Hexagon2 (H)", "Plus (+)", "Cross (x)", "Diamond (D)",
                                "Thin Diamond (d)", "Vertical Line (|)", "Horizontal Line (_)" 
                                ]

        for i in range(self.files):

            temp = QLabel("")
            temp.setFixedHeight(int(45*self.height))
            grid.addWidget(temp, i + start, 1)


            name = QLineEdit(self.file_names_short[i])
            name.setFixedWidth(int(100*self.width))
            grid.addWidget(name, i + start, 2)
            self.alter_componenets.append(name)
            
            selection = QComboBox()
            selection.setFixedWidth(int(250*self.width))
            selection.setFixedHeight(int(40*self.height))
            selection.addItems(common_pointer_shapes)
            selection.setCurrentText("Circle (o)")
            grid.addWidget(selection, i + start, 3,1,2)
            self.pointers.append(selection)

            # Create a square button
            button = QPushButton(self)
            button.setFixedWidth(int(30*self.width))
            button.setFixedHeight(int(30*self.width))
            button.setStyleSheet(f"background-color: {self.colours[i]};")  # Initial background color (white)
            grid.addWidget(button, i + start, 5)
            button.clicked.connect(lambda checked, i=i: self.show_color_dialog(i))
            self.color_buttons.append(button)


    def setup_buttons(self, grid):
        self.buttons = []
        for i in range(10):
            button = QPushButton("Apply")
            button.setFixedWidth(int(150*self.width))
            grid.addWidget(button, i + 1, 4)
            self.buttons.append(button)
        
        for i in range(3):
            button = QPushButton("Apply")
            button.setFixedWidth(int(150*self.width))
            self.grid.addWidget(button, 11 + self.files + i, 4)
            self.buttons.append(button)
        
        self.buttons[0].clicked.connect(self.apply_font_size)
        self.buttons[1].clicked.connect(self.apply_font_style)
        self.buttons[2].clicked.connect(self.apply_x_bounds)
        self.buttons[3].clicked.connect(self.apply_y_bounds)
        self.buttons[4].clicked.connect(self.add_dashed_line)
        self.buttons[5].clicked.connect(self.set_title)
        self.buttons[6].clicked.connect(self.set_xtitle)
        self.buttons[7].clicked.connect(self.set_ytitle)
        self.buttons[8].clicked.connect(self.apply_pointer_size)
        self.buttons[9].clicked.connect(self.apply_pointer_shapes)
        self.buttons[10].clicked.connect(self.set_line)
        self.buttons[11].clicked.connect(self.set_cap)
        self.buttons[12].clicked.connect(self.set_legend)

    def setup_checkboxes(self, grid):
        self.checkboxes = []
        for i in range(10):
            checkbox = QCheckBox("No Reset")
            checkbox.setFixedWidth(int(175*self.width))
            self.checkboxes.append(checkbox)
            grid.addWidget(checkbox, i + 1, 5)

        for i in range(3):
            checkbox = QCheckBox("No Reset")
            checkbox.setFixedWidth(int(175*self.width))
            self.checkboxes.append(checkbox)
            grid.addWidget(checkbox, 11 + self.files + i, 5)

        self.checkboxes[0].setChecked(True)
        self.checkboxes[1].setChecked(True)
        self.checkboxes[8].setChecked(True)
        self.checkboxes[9].setChecked(True)
        self.checkboxes[10].setChecked(True)
        self.checkboxes[11].setChecked(True)
        self.checkboxes[12].setChecked(True)

    def setup_navigation_buttons(self, grid):
        previous_button = QPushButton("Previous")
        previous_button.setFixedWidth(int(600*self.width))
        previous_button.setFixedHeight(int(80*self.height))
        previous_button.clicked.connect(self.previous_file)
        previous_button.setStyleSheet("font-weight: bold; font-size: 36px;")
        grid.addWidget(previous_button, 13, 6, 2, 1)

        next_button = QPushButton("Next")
        next_button.setFixedWidth(int(600*self.width))
        next_button.setFixedHeight(int(80*self.height))
        next_button.clicked.connect(self.next_file)
        next_button.setStyleSheet("font-weight: bold; font-size: 36px;")
        grid.addWidget(next_button, 13, 7, 2, 1)

        download_button = QPushButton("Download Image")
        download_button.setFixedWidth(int(1260*self.width))
        download_button.setFixedHeight(int(80*self.height))
        download_button.clicked.connect(self.download_plot)
        download_button.setStyleSheet("font-weight: bold; font-size: 36px;")
        grid.addWidget(download_button, 15, 6, 2,2)

    def add_blanks(self,grid):
        for x in range(13 - self.components):
            empty = QLabel("")
            empty.setFixedHeight(int(40*self.height))
            grid.addWidget(empty, 13 + self.components + x, 1)

    def plot_data(self):
        draw_multi_plot(self.canvas, self.matrix, self.row_names, self.current_file_index, 
                        self.current_component_index, self.files,
                  self.temperatures, self.components, self.x_bounds,self.y_bounds, 
                  self.dashed_lines, self.title, self.x_title,self.y_title, self.pointer_size,
                  self.component_names, self.pointer_types, self.legend, self.colours,
                  self.hollow, self.line_size, self.cap_size, self.file_names_short, self.component_titles)

    def next_file(self):
        self.filter_reset()
        self.current_file_index += 1
        self.current_component_index = self.current_file_index // self.total_graphs
        if self.current_file_index >= (self.total_graphs* self.components):
            self.current_file_index = 0
            self.current_component_index = 0
        print(self.current_file_index)
        self.graph_title.setText(f'Graph Image {self.current_file_index + 1}/{self.total_graphs * self.components}')
        self.plot_data()

    def previous_file(self):
        self.filter_reset()
        self.current_file_index -= 1
        if self.current_file_index < 0:
            self.current_file_index = self.total_graphs * self.components - 1
        self.current_component_index = self.current_file_index // self.total_graphs
        self.graph_title.setText(f'Graph Image {self.current_file_index + 1}/{self.total_graphs * self.components}')
        self.plot_data()
        
    def download_plot(self):
        """Opens a dialog to save the current plot as an image file (PNG or PDF)."""
        if self.canvas:
            # Open file dialog to save the file
            file_path = QFileDialog.getSaveFileName(
                                                self,
                                                "Save Plot",
                                                "",
                                                "PNG files (*.png);;PDF files (*.pdf);;All files (*)",
                                                "PNG files (*.png)"  # Set the default selected filter
                                            )[0]
            if file_path:
                # If saving as a PDF
                if file_path.endswith(".pdf"):
                    self.canvas.figure.savefig(file_path, bbox_inches='tight', dpi=100)
                else:
                    # Save as PNG or any other file
                    self.canvas.figure.savefig(file_path, bbox_inches='tight', dpi=100)

                self.show_success_alert()
#EXCESS FUNCTIONS===================================================================

    def apply_font_size(self):
        try:
            selected_font_size = self.font_size_input.currentText()
            self.functions.apply_font_size(selected_font_size)
        except ValueError:
            warning = "Invalid Font Size"
            self.show_warning(warning)

    def apply_font_style(self):
        try:
            selected_font_style = self.font_style_input.currentText()
            self.functions.apply_font_style(selected_font_style)
        except ValueError:
            warning = "Invalid Font Style"
            self.show_warning(warning)

    def apply_x_bounds(self):
        try:
            if self.x_min.text() == "" or self.x_max.text() == "":
                self.x_bounds = None
            else:
                if float(self.x_min.text()) < float(self.x_max.text()):
                    self.x_bounds = self.x_min.text() + '|' + self.x_max.text()
                else:
                    self.x_bounds = self.x_max.text() + '|' + self.x_min.text()
            self.plot_data()
        except ValueError:
            warning = "Invalid Input in X-Bounds"
            self.show_warning(warning)

    def apply_y_bounds(self):
        try:
            if self.y_min.text() == "" or self.y_max.text() == "":
                self.y_bounds = None
            else:
                if float(self.y_min.text()) < float(self.y_max.text()):
                    self.y_bounds = self.y_min.text() + '|' + self.y_max.text()
                else:
                    self.y_bounds = self.y_max.text() + '|' + self.y_min.text()
            self.plot_data()
        except ValueError:
            warning = "Invalid Input in Y-Bounds"
            self.show_warning(warning)

    def add_dashed_line(self):
        try:
            pos = self.inputs[2].text()
            self.dashed_lines.append(pos)
            self.plot_data()
        except ValueError:
            warning = "Invalid Dashed Line Position"
            self.show_warning(warning)
    
    def set_title(self):
        temp = self.inputs[3].text()
        self.title = temp
        self.plot_data()
    
    def set_xtitle(self):
        temp = self.inputs[4].text()
        if temp == '':
            self.x_title = None
        else:
            self.x_title = temp
        self.plot_data()
    
    def set_ytitle(self):
        temp = self.inputs[5].text()
        if temp == '':
            self.y_title = None
        else:
            self.y_title = temp
        self.plot_data()
    
    def apply_pointer_size(self):
        try:
            size = int(self.pointer_size_input.currentText())
            self.pointer_size = size
            if self.hollow_input.currentText() == "Hollow":
                self.hollow = ["white"] * self.components
            else:
                self.hollow = self.colours
            self.plot_data()
        except ValueError:
            warning = "Invalid Font Size"
            self.show_warning(warning)

    def apply_pointer_shapes(self):
        names = []
        pointers = []

        for x in range(len(self.alter_componenets)):
            if self.alter_componenets[x].text() == "":
                self.show_warning("Pointer Names should not be Empty")
                return
            names.append(self.alter_componenets[x].text())
        self.file_names_short = names

        for x in range(len(self.pointers)):
            string = self.pointers[x].currentText()
            type = (re.search(r'\((.*?)\)', string)).group(1)
            pointers.append(type)
        self.pointer_types = pointers

        self.plot_data()

    def set_legend(self):
        self.legend = self.legend_input.currentText()
        self.plot_data()

    def show_color_dialog(self,pos):
        color = QColorDialog.getColor()  # Open the color dialog
        if color.isValid():
            color_str = color.name()  # This will return something like '#FF0000'
            self.color_buttons[pos].setStyleSheet(f"background-color: {color_str};")
            self.colours[pos]=color_str
            
    def set_line(self):
        try:
            self.line_size = int(self.line_input.currentText())
            self.plot_data()
        except ValueError:
            warning = "Invalid Font Size"
            self.show_warning(warning)
    
    def set_cap(self):
        try:
            self.cap_size = int(self.cap_input.currentText())
            self.plot_data()
        except ValueError:
            warning = "Invalid Cap Size"
            self.show_warning(warning)

    def start_up(self):
        plt.rcParams['font.size'] = self.font_size

    def paintEvent(self, event):
        # Create a QPainter object
        painter = QPainter(self)
        
        # Load the background image
        background = QPixmap('files/base_background.png')

        # Draw the background image scaled to the widget's size
        painter.drawPixmap(self.rect(), background)


    def show_warning(self, message):
        # Create a message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)  # Set the icon to Warning
        msg.setWindowTitle("Warning")     # Set the window title
        msg.setText(message)              # Set the warning message
        msg.addButton("I'll do better", QMessageBox.AcceptRole)

        # Show the message box
        msg.exec_()

    def go_main(self):
        self.switch_to_select_page.emit()
    
    def show_success_alert(self):
        """Displays an alert indicating the file was saved successfully."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText("Your Graph has been saved successfully!")
        msg.addButton("Thank You!", QMessageBox.AcceptRole)
        msg.exec_()

    def filter_reset(self):
        if not self.checkboxes[0].isChecked():
            self.font_size = 24
            self.font_size_input.setCurrentText(str(self.font_size))
        if not self.checkboxes[1].isChecked():
            self.font_style = "Arial"
            self.font_style_input.setCurrentText("Arial")
        if not self.checkboxes[2].isChecked():
            self.x_bounds = None
            self.x_max.setText("")
            self.x_min.setText("")
        if not self.checkboxes[3].isChecked():
            self.y_bounds = None
            self.y_max.setText("")
            self.y_min.setText("")
        if not self.checkboxes[4].isChecked():
            self.dashed_lines = []
            self.inputs[2].setText("")
        if not self.checkboxes[5].isChecked():
            self.title = None
            self.inputs[3].setText("")
        if not self.checkboxes[6].isChecked():
            self.x_title = None
            self.inputs[4].setText("")
        if not self.checkboxes[7].isChecked():
            self.y_title = None
            self.inputs[5].setText("")
        if not self.checkboxes[8].isChecked():
            self.pointer_size = 12
            self.pointer_size_input.setCurrentText(str(self.pointer_size))
            self.hollow = ['#FF1493','#8A2BE2','#20B2AA','#ff0000','#ff0000','#ff0000']
            self.hollow_input.setCurrentText("Full")
        if not self.checkboxes[9].isChecked():
            self.component_names =  ['A1', 'B0', 'B1','XX','XX','XX']
            self.pointer_types = ['o','o','o','o','o','o','o','o']
            self.colours = ['#FF1493','#8A2BE2','#20B2AA','#ff0000','#ff0000','#ff0000']

            for i in range(self.components):
                self.alter_componenets[i].setText(self.component_names[i])
                self.pointers[i].setCurrentText("Circle (o)")
                self.color_buttons[i].setStyleSheet(f"background-color: {self.colours[i]};")
        if not self.checkboxes[10].isChecked():
            self.line_size = 3
            self.line_input.setCurrentText(str(self.line_size))
        if not self.checkboxes[11].isChecked():
            self.cap_size = 4
            self.cap_input.setCurrentText(str(self.cap_size))
        if not self.checkboxes[12].isChecked():
            self.legend = "Inside"
            self.legend_input.setCurrentText(self.legend)