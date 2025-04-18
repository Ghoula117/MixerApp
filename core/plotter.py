import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core import settings

class Plotter:
    def __init__(self, parent_frame):
        self.figures, self.axes, self.canvases = {}, {}, {}
        self.parent_frame = parent_frame

        for name in settings.GRAPH:
            fig, ax = plt.subplots(figsize=(6, 2))
            self.figures[name] = fig
            self.axes[name] = ax
            canvas = FigureCanvasTkAgg(fig, master=self.parent_frame)
            canvas.get_tk_widget().pack(padx=5, pady=5, fill="both", expand=True)
            ax.set_title(name)
            self.canvases[name] = canvas

    def update_plot(self, signal_name, x_data, y_data):
        ax = self.axes[signal_name]
        ax.clear()

        ax.set_title(signal_name)
        ax.grid(True)
        ax.stem(x_data, y_data, use_line_collection=True)

        self.canvases[signal_name].draw()


class ProcessedSignalPlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 2))
        self.ax.set_title("Processed Signal")

    def show(self, root, x_data, y_data, fs=None):
        from tkinter import Toplevel
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        new_window = Toplevel(root)
        new_window.title("Processed Signal")
        new_window.geometry("700x250")

        self.ax.clear()

        if fs:
            x_data = x_data / fs
            self.ax.set_xlabel("Tiempo [s]")
        else:
            self.ax.set_xlabel("Muestras")

        self.ax.stem(x_data, y_data, use_line_collection=True)
        self.ax.set_title("Processed Signal")
        self.ax.grid(True)
        self.ax.set_xlim([min(x_data), max(x_data)])

        if min(x_data) < 0 < max(x_data):
            self.ax.axvline(0, color='gray', linestyle='--')

        canvas = FigureCanvasTkAgg(self.fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)