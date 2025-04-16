import tkinter as tk
from ui.ui import SignalProcessingApp 

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()