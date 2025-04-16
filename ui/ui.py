import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from core.plotter import Plotter, ProcessedSignalPlot
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mixer Signal")
        self.root.geometry("1000x600")

        # === Frame superior ===
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(self.top_frame, text="Source:").pack(side="left", padx=5)
        self.signal_selection = ttk.Combobox(
            self.top_frame,
            values=["Microphone", "Audio File", "Synthetic", "Board"],
            state="readonly",
            width=12
        )
        self.signal_selection.pack(side="left", padx=5)
        self.signal_selection.bind("<<ComboboxSelected>>", self.configure_signal)

        ttk.Label(self.top_frame, text="Control:").pack(side="left", padx=5)
        self.control_selection = ttk.Combobox(
            self.top_frame,
            values=["Record", "Play", "Save", "Result"],
            state="readonly",
            width=10
        )
        self.control_selection.pack(side="left", padx=5)
        self.control_selection.bind("<<ComboboxSelected>>", self.execute_control)

        # === Frame principal ===
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # === Contenedor lateral izquierdo ===
        self.left_panel_container = ttk.Frame(self.main_frame)
        self.left_panel_container.pack(side="left", fill="y", padx=10, pady=10)

        # Panel fijo (parte superior del panel izquierdo)
        self.left_fixed_panel = ttk.Frame(self.left_panel_container)
        self.left_fixed_panel.pack(fill="x")

        ttk.Label(self.left_fixed_panel, text="Signal:").pack(pady=(0, 5))
        self.signal_selector = ttk.Combobox(
            self.left_fixed_panel,
            values=["x1(n)", "x2(n)"],
            state="readonly",
            width=5
        )
        self.signal_selector.pack(padx=5, pady=(0, 10))
        self.signal_selector.bind("<<ComboboxSelected>>", self.execute_control)

        # Panel dinámico (se borra y reconstruye con cada cambio)
        self.left_dynamic_panel = ttk.Frame(self.left_panel_container)
        self.left_dynamic_panel.pack(fill="both", expand=True)


        # === Área de gráficas ===
        self.plot_frame = ttk.LabelFrame(self.main_frame, text="Graph")
        self.plot_frame.pack(side="left", fill="both", expand=True)

        self.plotter = Plotter(self.plot_frame)
        self.processed_plot = ProcessedSignalPlot()

        self.n = np.arange(-5, 50 + 1)
        self.x = np.ones_like(self.n, dtype=float)
        self.x[self.n >= -5] = 1 * (0.9 ** (self.n[self.n >= -5] - 0))

        self.plotter.update_plot("x1(n)", self.n, self.x)
        self.plotter.update_plot("x2(n)", self.n, self.x * self.x * 0.5)
        self.processed_plot.show(self.root, self.n, self.x)

    def configure_signal(self, event=None):
        # Limpia solo el panel dinámico
        for widget in self.left_dynamic_panel.winfo_children():
            widget.destroy()

        signal_type = self.signal_selection.get()

        if signal_type == "Microphone":
            ttk.Label(self.left_dynamic_panel, text="Ganancia del micrófono:").pack(pady=(10, 0))
            self.mic_gain = tk.DoubleVar(value=1.0)
            ttk.Scale(self.left_dynamic_panel, from_=0.0, to=5.0, orient="horizontal", variable=self.mic_gain).pack()
            ttk.Button(self.left_dynamic_panel, text="Aplicar ganancia", command=lambda: print(f"Ganancia aplicada: {self.mic_gain.get():.2f}")).pack(pady=5)

        elif signal_type == "Audio File":
            ttk.Button(self.left_dynamic_panel, text="Cargar archivo de audio", command=self.load_audio_file).pack(pady=20)

        elif signal_type == "Synthetic":
            ttk.Label(self.left_dynamic_panel, text="Freq (Hz):").pack()
            self.freq_var = tk.DoubleVar(value=1000)
            ttk.Scale(self.left_dynamic_panel, from_=100, to=5000, variable=self.freq_var, orient="horizontal").pack()

            ttk.Label(self.left_dynamic_panel, text="Amplitud:").pack(pady=(10, 0))
            self.amp_var = tk.DoubleVar(value=1.0)
            ttk.Scale(self.left_dynamic_panel, from_=0.0, to=5.0, variable=self.amp_var, orient="horizontal").pack()

            ttk.Label(self.left_dynamic_panel, text="Synthetic: ").pack(pady=(0, 10))
            self.signal_synthetic = ttk.Combobox(
                self.left_dynamic_panel,
                values=["Impulse", "Step", "Ramp", "Triangular", "Sawtooth", "Sine", "Cosine", "SinC", "Chirp"],
                state="readonly",
                width=10
            )
            self.signal_synthetic.pack(padx=10, pady=(0, 10))
            self.signal_synthetic.bind("<<ComboboxSelected>>", self.execute_control)

            ttk.Button(self.left_dynamic_panel, text="Generar señal", command=self.generate_synthetic).pack(pady=10)

        elif signal_type == "Board":
            ttk.Label(self.left_dynamic_panel, text="Puerto serial:").pack()
            ttk.Entry(self.left_dynamic_panel).pack()

            ttk.Label(self.left_dynamic_panel, text="Baudrate:").pack(pady=(10, 0))
            baud = ttk.Combobox(self.left_dynamic_panel, values=["9600", "115200", "250000"], state="readonly")
            baud.current(1)
            baud.pack()

            ttk.Button(self.left_dynamic_panel, text="Conectar", command=lambda: print("Conectando...")).pack(pady=10)


    def generate_synthetic(self):
        signal = self.signal_selector.get()
        synthetic = self.signal_synthetic.get()
        f = self.freq_var.get()
        A = self.amp_var.get()
        print(f"Generando señal sintética con S1={signal} S1={synthetic} f={f} Hz y A={A}")

    def execute_control(self, event=None):
        action = self.control_selection.get()
        if action == "Result":
            self.processed_plot.show(self.root, self.n, self.x)
            print("Mostrar resultado final")
        elif action == "Record":
            print("Grabando...")
        elif action == "Play":
            print("Reproduciendo...")
        elif action == "Save":
            print("Guardando...")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()