import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import csv

class GraphApp(QWidget):
    def __init__(self, filenames=None, width=5, height=4, dpi=100):
        super().__init__()
        
        self.filenames = filenames if filenames is not None else []
        self.current_file_index = 0
        
        # Load data
        self.matrix, self.row_names = self.read_csv(self.filenames)
        print("Matrix length:", len(self.matrix))

        # Set up main layout and grid layout
        main_layout = QVBoxLayout()
        grid = QGridLayout()

        # Set up labels and input fields
        grid.addWidget(QLabel("Filters"), 0, 1)
        self.setup_labels(grid)
        self.setup_inputs(grid)
        self.setup_buttons(grid)
        self.setup_checkboxes(grid)
        
        # Titles and Adjustments
        graph_title = QLabel('Graph Image')
        graph_title.setFixedWidth(575)
        grid.addWidget(graph_title, 0, 5)

        # Set up Matplotlib canvas
        self.canvas = FigureCanvas(Figure(figsize=(width, height), dpi=dpi))
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        grid.addWidget(self.canvas, 1, 5, 12, 2)

        # Image Control Buttons
        previous_button = QPushButton("Previous")
        previous_button.clicked.connect(self.previous_file)
        grid.addWidget(previous_button, 13, 5, 2, 1)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_file)
        grid.addWidget(next_button, 13, 6, 2, 1)

        download_button = QPushButton("Download")
        grid.addWidget(download_button, 15, 6, 2, 2)

        # Add grid to main layout and set to window
        main_layout.addLayout(grid)
        self.setLayout(main_layout)
        self.setWindowTitle("PyQt Checkered Grid with Overlay")
        self.showMaximized()

        # Initial plot
        if self.matrix:
            self.draw_plot(0)

    def setup_labels(self, grid):
        labels = [
            "Font Size:", "Font Type:", "X-Bounds:", "Y-Bounds:", 
            "Add Dashed Line:", "Pointer Size:", "Pointer Shape:", 
            "Title:", "X-title:", "Y-title:"
        ]
        for i, label in enumerate(labels, start=1):
            lbl = QLabel(label)
            lbl.setFixedWidth(150)
            grid.addWidget(lbl, i, 1)

    def setup_inputs(self, grid):
        self.inputs = []
        for i in range(10):
            input_field = QLineEdit()
            input_field.setFixedWidth(250)
            grid.addWidget(input_field, i + 1, 2)
            self.inputs.append(input_field)

    def setup_buttons(self, grid):
        for i in range(10):
            button = QPushButton("Apply")
            button.setFixedWidth(150)
            grid.addWidget(button, i + 1, 3)

    def setup_checkboxes(self, grid):
        for i in range(10):
            checkbox = QCheckBox("No Reset")
            checkbox.setFixedWidth(150)
            grid.addWidget(checkbox, i + 1, 4)

    def draw_plot(self, plot_index):
        # Clear the canvas axes for a fresh plot
        self.canvas.axes.clear()

        components = 3
        component_names = ['Comp1', 'Comp2', 'Comp3']
        temperatures = [10, 100, 200, 300]

        # Retrieve data based on plot_index
        pos = 2 * plot_index
        if pos + 1 >= len(self.matrix):
            return  # Exit if index is out of range
        
        y_data = self.matrix[pos]
        uncertainty_data = self.matrix[pos + 1]

        # Split data for each temperature
        y_data_by_temp = [y_data[i:i + components] for i in range(0, len(y_data), components)]
        uncertainty_by_temp = [uncertainty_data[i:i + components] for i in range(0, len(uncertainty_data), components)]

        # Plot each component
        for j in range(components):
            values = [y_data_by_temp[i][j] for i in range(len(temperatures))]
            uncertainty_values = [uncertainty_by_temp[i][j] for i in range(len(temperatures))]
            self.canvas.axes.errorbar(temperatures, values, yerr=uncertainty_values,
                                      label=component_names[j], markersize=9, elinewidth=2, capsize=4, capthick=2)

        # Set labels, title, and grid
        self.canvas.axes.set_xlabel('Temperature [K]', labelpad=10)
        self.canvas.axes.set_ylabel(self.row_names[pos] if pos < len(self.row_names) else "")
        self.canvas.axes.set_title("Plot")
        self.canvas.axes.grid(True)
        self.canvas.axes.legend()

        # Draw the updated plot
        self.canvas.draw()

    def next_file(self):
        if self.filenames:
            self.current_file_index = (self.current_file_index + 1) % len(self.filenames)
            self.draw_plot(self.current_file_index)

    def previous_file(self):
        if self.filenames:
            self.current_file_index = (self.current_file_index - 1) % len(self.filenames)
            self.draw_plot(self.current_file_index)

    def read_csv(self, filename):
        matrix = []
        row_names = []

        try:
            with open(filename, mode='r', newline='') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row
                
                for row in csv_reader:
                    row_names.append(row[0])
                    matrix.append([float(item) for item in row[1:] if item.replace('.', '', 1).replace('-', '', 1).isdigit()])

            return matrix, row_names
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return [], []
        

def main(filenames=None):
    app = QApplication(sys.argv)
    graph_app = GraphApp(filenames)
    graph_app.show()  # Make sure to call show() here to display the window
    sys.exit(app.exec_())

if __name__ == '__main__':
    filenames = '12nm.csv'  # Example filenames, pass real files as needed
    main(filenames)

