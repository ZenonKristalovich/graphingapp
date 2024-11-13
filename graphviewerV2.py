import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import csv


class GraphViewerV2(tk.Tk):

    def __init__(self, filenames, component_names, temperatures, colours, font_size, font_style, font_family, sizes, shapes, title):
        super().__init__()
        self.title("Graph Viewer")
        self.geometry("800x650")
        
        # Convert strings to lists
        self.component_names = component_names.split(',')
        parts = temperatures.split('|')
        self.temperatures = [list(map(int, part.split(','))) for part in parts]

        #Variables
        self.components = len(self.component_names)
        self.colours = colours.split(',')
        self.font_size = int(font_size)
        self.font_style = font_style
        self.font_family = font_family
        self.sizes = sizes.split(',')
        self.shapes = shapes.split(',')
        self.original_titles = title.split(',')
        self.plot_index = 0

        if self.components != len(self.original_titles):
            temp = []
            for x in range(self.components):
                temp.append('')
            self.original_titles = temp

        #Setting Values
        self.dot_size = 9
        self.title = None
        self.xbound = None
        self.ybound = None
        self.line_pos = None
        self.dpi=80
        
        # Read CSV and store data
        self.matrix, self.row_names, self.shape_matrix = self.read_csv(filenames, self.shapes)
        self.current_plot = 0
        self.current_component = 0

        #Set Font
        plt.rcParams['font.family'] = self.font_family  # Change to your preferred font family
        plt.rcParams['font.'+f'{self.font_family}'] = [self.font_style]  # Specify a font available on your system
        plt.rcParams['font.size'] = self.font_size  # Change default font size


        # Variations
        self.variations = len(self.sizes)
        self.lines = len(self.matrix) // 2
        self.tables = self.variations * self.lines

        # Canvas for the graph
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = None  # Initialize the canvas as None
        self.current_fig = None  # Store the current figure

        # Draw the first plot
        self.draw_plot(self.current_plot, self.current_component)

        # Frame for the buttons at the bottom
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

        # Create buttons for navigation and download
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_plot)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.download_button = tk.Button(button_frame, text="Download", command=self.download_plot)
        self.download_button.pack(side=tk.LEFT, padx=10)

        # Add Title
        tk.Label(button_frame, text="Title Name:").pack(side=tk.LEFT)
        self.title_entry = tk.Entry(button_frame, width=15)
        self.title_entry.pack(side=tk.LEFT, padx=5)

        self.add_title_button = tk.Button(button_frame, text="Add Title", command=self.add_title)
        self.add_title_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_plot)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # Frame for x-bounds and y-bounds input
        bounds_frame = tk.Frame(self)
        bounds_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

        # X-Bounds input
        tk.Label(bounds_frame, text="X-Bounds (e.g., '0,10'):").pack(side=tk.LEFT)
        self.xbound_entry = tk.Entry(bounds_frame, width=10)
        self.xbound_entry.pack(side=tk.LEFT, padx=5)

        # Y-Bounds input
        tk.Label(bounds_frame, text="Y-Bounds (e.g., '0,100'):").pack(side=tk.LEFT)
        self.ybound_entry = tk.Entry(bounds_frame, width=10)
        self.ybound_entry.pack(side=tk.LEFT, padx=5)

        # Submit button for applying bounds
        self.submit_button = tk.Button(bounds_frame, text="Submit", command=self.apply_bounds)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        # Add Dash Line
        tk.Label(bounds_frame, text="Dash Line (e.g., '33'):").pack(side=tk.LEFT)
        self.dashspot_entry = tk.Entry(bounds_frame, width=10)
        self.dashspot_entry.pack(side=tk.LEFT, padx=5)
        
        self.add_dash_button = tk.Button(bounds_frame, text="Add line", command=self.add_dashed_line)
        self.add_dash_button.pack(side=tk.LEFT, padx=10)

        #Set Dot Size
        tk.Label(bounds_frame, text="Pointer Size:").pack(side=tk.LEFT)
        self.dot_entry = tk.Entry(bounds_frame, width=5)
        self.dot_entry.pack(side=tk.LEFT, padx=5)
        self.dot_entry.insert(0,self.dot_size)

        self.dot_button = tk.Button(bounds_frame, text="Change", command=self.change_dot)
        self.dot_button.pack(side=tk.LEFT, padx=5)

        #DPI control
        tk.Label(bounds_frame, text="Resolution:").pack(side=tk.LEFT)
        self.dpi_entry = tk.Entry(bounds_frame, width=10)
        self.dpi_entry.pack(side=tk.LEFT, padx=5)
        self.dpi_entry.insert(0,'80')
        
        self.submit_button = tk.Button(bounds_frame, text="Change", command=self.change_resolution)
        self.submit_button.pack(side=tk.LEFT, padx=10)

    def change_dot(self):
        self.dot_size = self.dot_entry.get()
        self.dot_entry.delete(0, 'end')  
        self.dot_entry.insert(0, self.dot_size) 
        self.draw_plot(self.plot_index, self.current_component)

    def change_resolution(self):
        self.dpi = int(self.dpi_entry.get())
        self.draw_plot(self.plot_index, self.current_component)

    def add_title(self):
        self.title = self.title_entry.get()
        self.draw_plot(self.plot_index, self.current_component)

    def add_dashed_line(self):
        self.line_pos = float(self.dashspot_entry.get())
        self.draw_plot(self.plot_index, self.current_component)

    def apply_bounds(self):
        """Applies the x and y bounds entered by the user."""
        try:
            xbound_text = self.xbound_entry.get()
            ybound_text = self.ybound_entry.get()

            # Parse xbound and ybound from the input fields
            self.xbound = [float(x) for x in xbound_text.split(',')] if xbound_text else None
            self.ybound = [float(y) for y in ybound_text.split(',')] if ybound_text else None
            
            # Redraw the plot with the new bounds
            self.draw_plot(self.plot_index, self.current_component)

        except ValueError:
            print("Invalid input for bounds. Please enter valid numbers in the format 'min,max'.")

    def read_csv(self, filenames, shapes):
        matrix = []
        row_names = []
        shape_matrix = []  # To store the corresponding shapes

        # Split the filenames string by commas to get individual file paths
        file_list = filenames.split(',')

        try:
            # Initialize matrix structure
            for file_idx, file_name in enumerate(file_list):
                with open(file_name.strip(), mode='r', newline='') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)  # Skip the first line (assume it's headers)
                    next(csv_reader)  # Skip the number line if needed

                    for row_idx, row in enumerate(csv_reader):
                        if file_idx == 0:
                            # For the first file, initialize rows in the matrix and shape_matrix
                            row_names.append(row[0])
                            matrix.append([[] for _ in range(self.components)])
                            shape_matrix.append([[] for _ in range(self.components)])

                        for component_index in range(self.components):
                            # Read the component values for the given row and component
                            component_values = [float(row[1 + j * self.components + component_index]) for j in range(len(row[1:]) // self.components)]
                            matrix[row_idx][component_index].append(component_values)

                            # Add the corresponding shape for this file
                            shape_matrix[row_idx][component_index].append(shapes[file_idx])

            return matrix, row_names, shape_matrix  # Return matrix, row_names, and shape_matrix

        except FileNotFoundError:
            print(f"Error: One of the files {filenames} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return [], [], []


    def draw_plot(self, plot_index, component_index):
        # Clear the previous plot (if any)
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()  # Remove previous canvas from window

        temp_title = ''
        if self.title == None:
            temp_title = self.component_names[component_index] + ': ' + self.original_titles[component_index] 
        else:
            temp_title = self.title


        fig, ax = plt.subplots(figsize=(5, 5), dpi=self.dpi)
        self.current_fig = fig  # Store the figure for later saving

        # Ensure the indices are within the range
        if plot_index >= len(self.row_names) // 2 or component_index >= self.components:
            print("Index out of range")
            return

        # Get data for the selected component and plot index
        y_data_by_temp = self.matrix[plot_index * 2][component_index]
        uncertainty_data = self.matrix[plot_index * 2 + 1][component_index]
        shape_data_by_temp = self.shape_matrix[plot_index * 2][component_index]  # Access shape data
        print(y_data_by_temp)
        print(uncertainty_data)
        # Plot the data for the selected component
        count = 0
        for file_idx, (y_values, uncertainty_values, shape) in enumerate(zip(y_data_by_temp, uncertainty_data, shape_data_by_temp)):
            temperatures_used = self.temperatures[count%len(self.temperatures)]
            count += 1
            ax.errorbar(
                temperatures_used,
                y_values,
                yerr=uncertainty_values,
                fmt=shape,  # Use the corresponding shape from shape_matrix
                color=self.colours[file_idx],
                label=f"{self.sizes[file_idx]}",
                markersize=self.dot_size,
                elinewidth=2,
                capsize=4,
                capthick=2
            )

        ax.set_xlabel('Temperature [K]', labelpad=10)
        ax.set_ylabel(self.row_names[plot_index * 2])  # Label based on row name
        ax.legend()
        ax.grid(True)
        ax.set_title(temp_title)

        # Customize bounds
        if self.xbound is not None:
            ax.set_xlim(min(self.xbound), max(self.xbound))
        if self.ybound is not None:
            ax.set_ylim(min(self.ybound), max(self.ybound))

        # Add a horizontal dashed line at dash_pos if provided
        if self.line_pos is not None:
            line = Line2D([0], [0], color='gray', linestyle='--', linewidth=2)
            ax.axhline(y=self.line_pos, color='gray', linestyle='--', linewidth=2)

            # Add the dashed line to the legend
            handles, labels = ax.get_legend_handles_labels()
            handles.append(line)
            labels.append('Bulk')
            ax.legend(handles=handles, labels=labels)

        # Embed the plot into the canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def download_plot(self):
        """Opens a dialog to save the current plot as an image file (PNG or PDF)."""
        if self.current_fig:
            # Open file dialog to save the file
            file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                    filetypes=[("PDF files", "*.pdf"), 
                                                                ("PNG files", "*.png"),
                                                                ("All files", "*.*")])
            
            if file_path:
            # If saving as a PDF, match the current DPI for consistent display
                if file_path.endswith(".pdf"):
                    self.current_fig.savefig(file_path, bbox_inches='tight', dpi=self.dpi)
                else:
                    self.current_fig.savefig(file_path, bbox_inches='tight')

    def next_plot(self):
        """Show the next plot for the current component or move to the next component."""

        if self.current_plot < ( (self.lines) * self.components - 1) :
            self.xbound = None
            self.ybound = None
            self.title = None
            self.line_pos = None

            self.current_plot += 1
            self.current_component = self.current_plot // self.lines
            self.plot_index = self.current_plot % self.lines
            self.draw_plot(self.plot_index, self.current_component)
        else:
            print("No more plots to display")

    def prev_plot(self):
        """Show the previous plot for the current component or move to the previous component."""
        if self.current_plot > 0:
            self.xbound = None
            self.ybound = None
            self.title = None
            self.line_pos = None

            self.current_plot -= 1
            self.current_component = self.current_plot // self.lines
            self.plot_index = self.current_plot % self.lines
            self.draw_plot(self.plot_index, self.current_component)
        else:
            print("No previous plots to display")

