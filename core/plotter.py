import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plotter:
    def __init__(self, parent_frame):
        self.figures, self.axes, self.canvases = {}, {}, {}
        self.parent_frame = parent_frame

        for name in ["x1(n)", "x2(n)"]:
            fig, ax = plt.subplots(figsize=(6, 2))
            self.figures[name] = fig
            self.axes[name] = ax
            canvas = FigureCanvasTkAgg(fig, master=self.parent_frame)
            canvas.get_tk_widget().pack(padx=5, pady=5, fill="both", expand=True)
            ax.set_title(f"{name} Signal")
            self.canvases[name] = canvas

    def update_plot(self, signal_name, x_data, y_data):
        ax = self.axes[signal_name]
        ax.clear()
        ax.plot(x_data, y_data)
        ax.set_title(f"{signal_name} Signal")
        self.canvases[signal_name].draw()

class ProcessedSignalPlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 2))
        self.ax.set_title("Processed Signal")

    def show(self, root, x_data, y_data):
        from tkinter import Toplevel
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        new_window = Toplevel(root)
        new_window.title("Processed Signal")
        new_window.geometry("700x250")

        self.ax.clear()
        self.ax.plot(x_data, y_data)
        self.ax.set_title("Processed Signal")

        canvas = FigureCanvasTkAgg(self.fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)