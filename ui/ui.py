import tkinter as tk
from tkinter import ttk, simpledialog
from core.plotter import Plotter, ProcessedSignalPlot
from core import generation, signal_utils, settings

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
            values=settings.source_select,
            state="readonly",
            width=10
        )
        self.signal_selection.pack(side="left", padx=5)
        self.signal_selection.bind("<<ComboboxSelected>>", self.configure_signal)

        ttk.Label(self.top_frame, text="Control:").pack(side="left", padx=5)
        self.control_selection = ttk.Combobox(
            self.top_frame,
            values=settings.control_select,
            state="readonly",
            width=7
        )
        self.control_selection.pack(side="left", padx=5)
        self.control_selection.bind("<<ComboboxSelected>>", self.execute_control)

        ttk.Label(self.top_frame, text="Operation:").pack(side="left", padx=5)
        self.operation_selection = ttk.Combobox(
            self.top_frame,
            values=settings.operation_select,
            state="readonly",
            width=20
        )
        self.operation_selection.pack(side="left", padx=5)
        self.operation_selection.bind("<<ComboboxSelected>>", self.execute_control)

        ttk.Button(self.top_frame, text="Show Result", command=self.generate_result).pack(side="right", pady=10)
        ttk.Button(self.top_frame, text="Generate", command=self.generate_synthetic).pack(side="right", pady=10)


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
            values=settings.GRAPH,
            state="readonly",
            width=5
        )
        self.signal_selector.pack(padx=5, pady=(0, 10))

        ttk.Label(self.left_fixed_panel, text="Operations in amplitude:").pack(pady=(0, 5))
        self.amp_selector = ttk.Combobox(
            self.left_fixed_panel,
            values=settings.opera_amp,
            state="readonly",
            width=10
        )
        self.amp_selector.pack(padx=5, pady=(0, 10))
        self.amp_selector.bind("<<ComboboxSelected>>")

        def create_labeled_entry(parent, label_text, default_value):
            var = tk.DoubleVar(value=default_value)
            ttk.Label(parent, text=label_text).pack(pady=(0, 5))
            ttk.Entry(parent, textvariable=var, width=10).pack(padx=5, pady=(0, 10))
            return var

        self.fa_var = create_labeled_entry(self.left_fixed_panel, "Analog Freq (Hz):", 60.0)
        self.fs_var = create_labeled_entry(self.left_fixed_panel, "Sampling Freq (Hz):", 180.0)
        self.gain_var = create_labeled_entry(self.left_fixed_panel, "Gain:", 1.0)
        self.start_var = create_labeled_entry(self.left_fixed_panel, "start:", -4)
        self.duration_var = create_labeled_entry(self.left_fixed_panel, "Duration: (s)", 1.5)
        self.t_shift_var = create_labeled_entry(self.left_fixed_panel, "Time Shift:", 0)
        self.sampling_var = create_labeled_entry(self.left_fixed_panel, "Sampling:", 0)

        
        # Panel dinámico contenedor
        self.left_dynamic_panel = ttk.Frame(self.left_panel_container)
        self.left_dynamic_panel.pack(fill="both", expand=True)

        # Subpaneles independientes
        self.left_dynamic_signal_panel = ttk.Frame(self.left_dynamic_panel)
        self.left_dynamic_signal_panel.pack(fill="x")

        self.left_dynamic_op_panel = ttk.Frame(self.left_dynamic_panel)
        self.left_dynamic_op_panel.pack(fill="x")

        # === Área de gráficas ===
        self.plot_frame = ttk.LabelFrame(self.main_frame, text="Graph")
        self.plot_frame.pack(side="left", fill="both", expand=True)

        self.plotter = Plotter(self.plot_frame)
        self.processed_plot = ProcessedSignalPlot()
      
   
    def configure_signal(self, event=None):
        for widget in self.left_dynamic_signal_panel.winfo_children():
            widget.destroy()

        signal_type = self.signal_selection.get()

        if signal_type == "Microphone":
            pass

        elif signal_type == "Audio File":
            ttk.Button(self.left_dynamic_signal_panel, text="Cargar archivo de audio", command=self.load_audio_file).pack(pady=20)

        elif signal_type == "Synthetic":
            ttk.Label(self.left_dynamic_signal_panel, text="Synthetic: ").pack(pady=(0, 10))
            self.signal_synthetic = ttk.Combobox(
                self.left_dynamic_signal_panel,
                values=settings.signalSelector,
                state="readonly",
                width=10
            )
            self.signal_synthetic.pack(padx=10, pady=(0, 10))

        elif signal_type == "Board":
            ttk.Label(self.left_dynamic_signal_panel, text="Puerto serial:").pack()
            ttk.Entry(self.left_dynamic_signal_panel).pack()
            ttk.Label(self.left_dynamic_signal_panel, text="Baudrate:").pack(pady=(10, 0))
            baud = ttk.Combobox(self.left_dynamic_signal_panel, values=["9600", "115200", "250000"], state="readonly")
            baud.current(1)
            baud.pack()
            ttk.Button(self.left_dynamic_signal_panel, text="Conectar", command=lambda: print("Conectando...")).pack(pady=10)

    def generate_synthetic(self):
        signal = self.signal_selector.get()
        amp = self.amp_selector.get()
        synthetic = self.signal_synthetic.get()
        fa = self.fa_var.get()
        fs = self.fs_var.get()
        gain = self.gain_var.get()
        n0 = self.start_var.get()
        duration = self.duration_var.get()
        shift = self.t_shift_var.get()
        try:
            self.n, self.y = generation.signal_selector(synthetic, fa, fs, gain, n0, duration, shift)
            self.y = signal_utils.amplitud_selector(amp, self.y)
        except:
            print("Error generating signal")

        self.plotter.update_plot(signal, self.n, self.y)

    def generate_result(self):
        fs = self.fa_var.get()
        self.processed_plot.show(self.root, self.n, self.y, fs)

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