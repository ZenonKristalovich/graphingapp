import matplotlib.pyplot as plt

class GraphFunctions:
    def __init__(self, app_instance):
        self.app = app_instance  # Reference to the GraphApp instance

    def apply_font_size(self, font_size):

        size = int(font_size)
        self.app.font_size = size  # Update the font size in GraphApp
        plt.rcParams['font.size'] = size
        self.app.plot_data()  # Redraw the canvas if the font size affects it

    def apply_font_style(self, font_style):
        plt.rcParams['font.family'] = font_style
        self.app.plot_data()  # Redraw the canvas if the font size affects it

