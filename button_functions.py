import matplotlib.pyplot as plt

class GraphFunctions:
    def __init__(self, app_instance):
        self.app = app_instance  # Reference to the GraphApp instance

    def apply_font_size(self, font_size):
        try:
            size = int(font_size)
            self.app.font_size = size  # Update the font size in GraphApp
            plt.rcParams['font.size'] = size
            self.app.plot_data()  # Redraw the canvas if the font size affects it
        except ValueError:
            print("Invalid font size. Please enter a number.")

    def apply_font_style(self, font_style):
        try:
            plt.rcParams['font.family'] = font_style
            self.app.plot_data()  # Redraw the canvas if the font size affects it
        except ValueError:
            print("Invalid font style")
