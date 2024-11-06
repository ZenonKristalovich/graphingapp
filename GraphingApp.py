import tkinter as tk
import graphviewer
import graphviewerV2
from tkinter import messagebox

#pyinstaller --onefile --noconsole --icon=Gamma.jpg --hidden-import=matplotlib.backends.backend_pdf GraphingApp.py


# Function to handle graph generation
def make_graph():
    csv_file_name = csv_file_input.get()
    component_names = component_names_input.get()
    temperatures = temperatures_input.get()
    colours = colours_input.get()
    font_size = font_input.get()
    font_style = font_style_input.get()
    font_family = font_family_input.get()

    if csv_file_name:
        global app
        app = graphviewer.GraphViewer(csv_file_name, component_names, temperatures, colours, font_size, font_style, font_family)
        app.mainloop()
    else:
        messagebox.showerror("Input Error", "Please enter a valid CSV file name.")

def make_graphv2():
    csv_multiple_names = csv_multiple_input.get()
    component_names = component_names_input.get()
    temperatures = temperature_multiple_input.get()
    colours = colours_input.get()
    font_size = font_input.get()
    font_style = font_style_input.get()
    font_family = font_family_input.get()
    sizes = size_input.get()
    shapes = shape_input.get()
    title = title_input.get()

    if csv_multiple_names:
        global app
        app = graphviewerV2.GraphViewerV2(csv_multiple_names, component_names, temperatures, colours, font_size, font_style, font_family, sizes, shapes, title)
        app.mainloop()
    else:
        messagebox.showerror("Input Error", "Please enter a valid CSV file name.")

# Create the main window
root = tk.Tk()
root.title("Graphing Application")
root.geometry("600x560")

# CSV File input
file_label = tk.Label(root, text="CSV File Name:")
file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
csv_file_input = tk.Entry(root, width=40)
csv_file_input.grid(row=0, column=1, padx=10, pady=10)

# Component Names input
component_label = tk.Label(root, text="Component Names:")
component_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
component_names_input = tk.Entry(root, width=40)
component_names_input.grid(row=1, column=1, padx=10, pady=10)

# Colours input
colour_label = tk.Label(root, text="Colours:")
colour_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
colours_input = tk.Entry(root, width=40)
colours_input.grid(row=2, column=1, padx=10, pady=10)

# Temperatures input
temperature_label = tk.Label(root, text="Temperatures:")
temperature_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
temperatures_input = tk.Entry(root, width=40)
temperatures_input.grid(row=3, column=1, padx=10, pady=10)

# Font info inputs (all on the same row)
font_label = tk.Label(root, text="Font Size:")
font_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
font_input = tk.Entry(root, width=40)
font_input.grid(row=4, column=1, padx=10, pady=10, sticky="w")

font_style_label = tk.Label(root, text="Font Style:")
font_style_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
font_style_input = tk.Entry(root, width=40)
font_style_input.grid(row=5, column=1, padx=10, pady=10, sticky="w")

font_family_label = tk.Label(root, text="Font Family:")
font_family_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
font_family_input = tk.Entry(root, width=40)
font_family_input.grid(row=6, column=1, padx=10, pady=10, sticky='w')

# Inputs for multiple CSVs and other details
csv_multiple_label = tk.Label(root, text="Multiple CSV File Names (e.g. 'file1.csv,file2.csv'):")
csv_multiple_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
csv_multiple_input = tk.Entry(root, width=40)
csv_multiple_input.grid(row=7, column=1, padx=10, pady=10, sticky='w')

size_label = tk.Label(root, text="Enter Sizes (e.g. '12nm,16nm'):")
size_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
size_input = tk.Entry(root, width=40)
size_input.grid(row=8, column=1, padx=10, pady=10, sticky='w')

temperature_multiple_label = tk.Label(root, text="Enter Temperatures (e.g. '10,100,200|10,100,200,300'):")
temperature_multiple_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")
temperature_multiple_input = tk.Entry(root, width=40)
temperature_multiple_input.grid(row=9, column=1, padx=10, pady=10, sticky = 'w')

shape_label = tk.Label(root, text="Enter Dot Shapes (e.g. 'o,s'):")
shape_label.grid(row=10, column=0, padx=10, pady=10, sticky="w")
shape_input = tk.Entry(root, width=40)
shape_input.grid(row=10, column=1, padx=10, pady=10, sticky="w")

title_label = tk.Label(root, text="Enter Base Title: (e.g. 'Title1,Title2')")
title_label.grid(row=11, column=0, padx=10, pady=10, sticky="w")
title_input = tk.Entry(root, width=40)
title_input.grid(row=11, column=1, padx=10, pady=10, sticky="w")

# Button for making the graph
graph_button = tk.Button(root, text="Make Graph", command=make_graph)
graph_button.grid(row=12, column=0, pady=20)

# Button for making graph v2
graphv2_button = tk.Button(root, text="Make GraphV2", command=make_graphv2)
graphv2_button.grid(row=12, column=1, pady=20)

# Set default values for the inputs
component_names_input.insert(0, "A,B0,B1")  # Default value inserted here
temperatures_input.insert(0, '10,100,200,300')
colours_input.insert(0, 'deeppink,blueviolet,lightseagreen')
font_input.insert(0, '20')
font_style_input.insert(0, 'Arial')
font_family_input.insert(0, 'sans-serif')
title_input.insert(0,'Fe3+ (Td),Fe2+ (Oh),Fe3+ (Oh)')

# Run the application
root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()

