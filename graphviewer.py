import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import csv


class GraphViewer(tk.Tk):

    def __init__(self, filename, component_names, temperatures, colours, font_size, font_style, font_family):
        super().__init__()
        self.title("Graph Viewer")
        self.geometry("800x650")
        
        # Convert strings to lists
        self.component_names = component_names.split(',')
        self.temperatures = [int(item) for item in temperatures.split(',')]
        self.components = len(self.component_names)
        self.colours = colours.split(',')
        self.font_size = int(font_size)
        self.font_style = font_style
        self.font_family = font_family

        #Setting Values
        self.title = ''
        self.dot_size = 9
        self.pointer = 'o','o','o','o','o','o','o','o','o','o'
        self.xbound = None
        self.ybound = None
        self.line_pos = None
        self.dpi = 80

        #Set Font
        plt.rcParams['font.family'] = self.font_family  # Change to your preferred font family
        plt.rcParams['font.'+f'{self.font_family}'] = [self.font_style]  # Specify a font available on your system
        plt.rcParams['font.size'] = self.font_size  # Change default font size

        
        # Read CSV and store data
        self.matrix, self.row_names = self.read_csv(filename)
        
        self.current_plot = 0

        # Canvas for the graph
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = None  # Initialize the canvas as None
        self.current_fig = None  # Store the current figure

        # Draw the first plot
        self.draw_plot(self.current_plot)

        # Frame for the buttons at the bottom
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

        # Create buttons for navigation and download
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_plot)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.download_button = tk.Button(button_frame, text="Download", command=self.download_plot)
        self.download_button.pack(side=tk.LEFT, padx=10)

        #Add Title
        tk.Label(button_frame, text="Title Name:").pack(side=tk.LEFT)
        self.title_entry = tk.Entry(button_frame, width=15)
        self.title_entry.pack(side=tk.LEFT, padx=5)

        self.AddTitle_button = tk.Button(button_frame, text="Add Title", command=self.add_title)
        self.AddTitle_button.pack(side=tk.LEFT, padx=10)

        #Set Pointer
        tk.Label(button_frame, text="Custom Pointer:").pack(side=tk.LEFT)
        self.pointer_entry = tk.Entry(button_frame, width=10)
        self.pointer_entry.pack(side=tk.LEFT, padx=5)

        self.AddTitle_button = tk.Button(button_frame, text="Change Pointer", command=self.change_pointer)
        self.AddTitle_button.pack(side=tk.LEFT, padx=10)

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

        #Add Dash Line
        tk.Label(bounds_frame, text="Dash Line (e.g., '33'):").pack(side=tk.LEFT)
        self.dashspot_entry = tk.Entry(bounds_frame, width=10)
        self.dashspot_entry.pack(side=tk.LEFT, padx=5)
        
        self.submit_button = tk.Button(bounds_frame, text="Add line", command=self.add_dashed_line)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        #Set Dot Size
        tk.Label(bounds_frame, text="Pointer Size:").pack(side=tk.LEFT)
        self.dot_entry = tk.Entry(bounds_frame, width=5)
        self.dot_entry.pack(side=tk.LEFT, padx=5)
        self.dot_entry.insert(0,self.dot_size)

        self.dot_button = tk.Button(bounds_frame, text="Change", command=self.change_dot)
        self.dot_button.pack(side=tk.LEFT, padx=5)

        #DPI control
        tk.Label(bounds_frame, text="Resolution:").pack(side=tk.LEFT)
        self.dpi_entry = tk.Entry(bounds_frame, width=5)
        self.dpi_entry.pack(side=tk.LEFT, padx=5)
        self.dpi_entry.insert(0,'80')
        
        self.submit_button = tk.Button(bounds_frame, text="Change", command=self.change_resolution)
        self.submit_button.pack(side=tk.LEFT, padx=10)
    
    def change_dot(self):
        self.dot_size = self.dot_entry.get()
        self.dot_entry.delete(0, 'end')  
        self.dot_entry.insert(0, self.dot_size) 
        self.draw_plot(self.current_plot)

    def change_resolution(self):
        self.dpi = int(self.dpi_entry.get())
        self.draw_plot(self.current_plot)


    def change_pointer(self):
        self.pointer = (self.pointer_entry.get()).split(',')
        self.draw_plot(self.current_plot)

    def add_title(self):
        self.title = self.title_entry.get()
        self.draw_plot(self.current_plot)

    def add_dashed_line(self):
        self.line_pos = float(self.dashspot_entry.get())
        self.draw_plot(self.current_plot)

    def apply_bounds(self):
        """Applies the x and y bounds entered by the user."""
        try:
            xbound_text = self.xbound_entry.get()
            ybound_text = self.ybound_entry.get()

            # Parse xbound and ybound from the input fields
            self.xbound = [float(x) for x in xbound_text.split(',')] if xbound_text else None
            self.ybound = [float(y) for y in ybound_text.split(',')] if ybound_text else None
            
            # Redraw the plot with the new bounds
            self.draw_plot(self.current_plot)

        except ValueError:
            print("Invalid input for bounds. Please enter valid numbers in the format 'min,max'.")

    def read_csv(self, filename):
        matrix = []
        row_names = []

        try:
            with open(filename, mode='r', newline='') as file:
                csv_reader = csv.reader(file)
                first_line = next(csv_reader)  # Read the first line
                
                # Skip the number line
                next(csv_reader)

                # Populate matrix and row_names
                for row in csv_reader:
                    row_names.append(row[0])
                    # Convert row elements to float and append to the matrix
                    matrix.append([float(item) for item in row[1:] if item and (item.replace('.', '', 1).replace('-', '', 1).isdigit())])

            return matrix, row_names
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return [], []

    def draw_plot(self, plot_index):
        # Clear the previous plot (if any)
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()  # Remove previous canvas from window

        fig, ax = plt.subplots(figsize=(5, 5), dpi=self.dpi)
        self.current_fig = fig  # Store the figure for later saving

        pos = 2 * plot_index
        y_data = self.matrix[pos]
        uncertainty_data = self.matrix[pos + 1]

        # Split data for each temperature
        y_data_by_temp = [y_data[i:i + self.components] for i in range(0, len(y_data), self.components)]
        uncertainty_by_temp = [uncertainty_data[i:i + self.components] for i in range(0, len(uncertainty_data), self.components)]
        
        # Colors for the components
        colors = self.colours
        pointers = self.pointer  # Assuming this is a list of marker types

        # Plot the data for each component
        for j in range(self.components):
            values = [y_data_by_temp[i][j] for i in range(len(self.temperatures))]
            uncertainty_values = [uncertainty_by_temp[i][j] for i in range(len(self.temperatures))]
            # Use the corresponding pointer for each component
            ax.errorbar(self.temperatures, values, yerr=uncertainty_values, fmt=pointers[j], color=colors[j], 
                        label=str(self.component_names[j]), markersize=self.dot_size, elinewidth=2, capsize=4, capthick=2)
        
        ax.set_xlabel('Temperature [K]', labelpad=10)
        ax.set_ylabel(self.row_names[pos])
        ax.legend()
        ax.grid(True)
        ax.set_title(self.title)

        # Customize Bounds
        if self.xbound is not None:
            ax.set_xlim(min(self.xbound), max(self.xbound))
        if self.ybound is not None:
            ax.set_ylim(min(self.ybound), max(self.ybound))

        # Add a horizontal dashed line at dash_pos if provided
        if self.line_pos is not None:
            # Create the dashed line
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
        self.title = ''
        self.pointer = 'o','o','o','o','o','o','o','o','o','o'
        self.xbound = None
        self.ybound = None
        self.line_pos = None
        if self.current_plot < int(len(self.matrix) / 2) - 1:
            self.current_plot += 1
            self.draw_plot(self.current_plot)

    def prev_plot(self):
        self.title = ''
        self.pointer = 'o','o','o','o','o','o','o','o','o','o'
        self.xbound = None
        self.ybound = None
        self.line_pos = None
        if self.current_plot > 0:
            self.current_plot -= 1
            self.draw_plot(self.current_plot)




