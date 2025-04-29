import tkinter as tk
from tkinter import ttk, messagebox
from core.plotter import Plotter, ProcessedSignalPlot
from core import generation, signal_utils, audio_utils , file_manager, math, settings
from core.math import generate_result

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
        self.control_selection.bind("<<ComboboxSelected>>", self.configure_control)

        ttk.Label(self.top_frame, text="Operation:").pack(side="left", padx=5)
        self.operation_selection = ttk.Combobox(
            self.top_frame,
            values=settings.operation_select,
            state="readonly",
            width=20
        )
        self.operation_selection.pack(side="left", padx=5)
        self.operation_selection.bind("<<ComboboxSelected>>", self.configure_operations)

        ttk.Button(self.top_frame, text="Show Result", command=self.handle_operation).pack(side="right", pady=10)
        ttk.Button(self.top_frame, text="Show features", command=self.handle_features).pack(side="right", pady=10)

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
        self.signal_selector.set(settings.GRAPH[0])

        ttk.Label(self.left_fixed_panel, text="Amplitude:").pack(pady=(0, 5))
        self.amp_selector = ttk.Combobox(
            self.left_fixed_panel,
            values=settings.opera_amp,
            state="readonly",
            width=10
        )
        self.amp_selector.pack(padx=5, pady=(0, 10))
        self.amp_selector.set(settings.opera_amp[5])

        self.fa_var = self.create_labeled_entry(self.left_fixed_panel, "Analog Freq (Hz):", 5.0)
        self.fs_var = self.create_labeled_entry(self.left_fixed_panel, "Sampling Freq (Hz):", 180.0)
        self.gain_var = self.create_labeled_entry(self.left_fixed_panel, "Gain:", 1.0)
        self.start_var = self.create_labeled_entry(self.left_fixed_panel, "start: (s)", -4)
        self.duration_var = self.create_labeled_entry(self.left_fixed_panel, "Duration: (s)", 1.5)
        self.t_shift_var = self.create_labeled_entry(self.left_fixed_panel, "Time Shift: (s)", 0)

        ttk.Label(self.left_fixed_panel, text="Sampling").pack(pady=(0, 5))
        self.sampling_select = ttk.Combobox(
            self.left_fixed_panel,
            values=settings.sampling_method,
            state="readonly",
            width=10
        )
        self.sampling_select.pack(padx=5, pady=(0, 10))

        # Panel dinámico contenedor
        self.left_dynamic_panel = ttk.Frame(self.left_panel_container)
        self.left_dynamic_panel.pack(fill="both", expand=True)

        # Subpaneles independientes
        self.left_dynamic_signal_panel = ttk.Frame(self.left_dynamic_panel)
        self.left_dynamic_signal_panel.pack(fill="x")

        self.up_dynamic_op_panel = ttk.Frame(self.top_frame)
        self.up_dynamic_op_panel.pack(fill="x")

        # === Área de gráficas ===
        self.plot_frame = ttk.LabelFrame(self.main_frame, text="Graph")
        self.plot_frame.pack(side="left", fill="both", expand=True)

        self.plotter = Plotter(self.plot_frame)
        self.processed_plot = ProcessedSignalPlot()

    def create_labeled_entry(self, parent, label_text, default_value):
        ttk.Label(parent, text=label_text).pack(pady=(0, 5))

        entry = ttk.Entry(parent, width=10)
        entry.insert(0, str(default_value))
        entry.pack(padx=5, pady=(0, 10))

        return entry

    def configure_signal(self, event=None):
        for widget in self.left_dynamic_signal_panel.winfo_children():
            widget.destroy()

        signal_type = self.signal_selection.get()

        if signal_type == settings.source_select[0]:
            ttk.Button(self.left_dynamic_signal_panel, text="Record", command=self.record_audio).pack(padx=5, pady=(0, 10))

        elif signal_type == settings.source_select[1]:
            ttk.Button(self.left_dynamic_signal_panel, text="Load file", command=self.load_audio).pack(pady=20)

        elif signal_type == settings.source_select[2]:
            self.signal_synthetic = ttk.Combobox(
                self.left_dynamic_signal_panel,
                values=settings.signalSelector,
                state="readonly",
                width=10
            )
            self.signal_synthetic.pack(padx=10, pady=(0, 10))

            ttk.Button(self.left_dynamic_signal_panel, text="Generate", command=self.generate_synthetic).pack(padx=5, pady=(0, 10))

        elif signal_type == settings.source_select[3]:
            ttk.Label(self.left_dynamic_signal_panel, text="Puerto serial:").pack()
            ttk.Entry(self.left_dynamic_signal_panel).pack()
            ttk.Label(self.left_dynamic_signal_panel, text="Baudrate:").pack(pady=(10, 0))
            baud = ttk.Combobox(self.left_dynamic_signal_panel, values=["9600", "115200", "250000"], state="readonly")
            baud.current(1)
            baud.pack()
            ttk.Button(self.left_dynamic_signal_panel, text="Conectar", command=lambda: print("Conectando...")).pack(pady=10)

    def configure_control(self, event=None):
        action = self.control_selection.get()
        actions = {
            settings.control_select[0]: lambda: audio_utils.play_mono(settings.GRAPH[0], self.y1, self.fs1),
            settings.control_select[1]: lambda: audio_utils.play_mono(settings.GRAPH[1], self.y2, self.fs2),
            settings.control_select[2]: lambda: audio_utils.play_stereo(self.y3, self.fs1, self.y3, self.fs2),
            settings.control_select[3]: lambda: file_manager.save_signal(self.fs1, self.y1, self.n1, self.y2, self.n2, self.y3, self.n3)
        }
        actions[action]()

    def configure_operations(self, event=None):
        for widget in self.up_dynamic_op_panel.winfo_children():
            widget.destroy()

        operation_type = self.operation_selection.get()

        if operation_type == settings.operation_select[0]:
            self.basic_select = ttk.Combobox(
                self.up_dynamic_op_panel,
                values=settings.basic_operation,
                state="readonly",
                width=20
            )
            self.basic_select.pack(side="left", pady=15, padx=5)
            
        elif operation_type == settings.operation_select[1]:
            self.preprocessing_select = ttk.Combobox(
                self.up_dynamic_op_panel,
                values=settings.preprocessing_operation,
                state="readonly",
                width=20
            )
            self.preprocessing_select.pack(side="left", pady=15, padx=5)

        elif operation_type == settings.operation_select[2]:
            self.filtering_select = ttk.Combobox(
                self.up_dynamic_op_panel,
                values=settings.filter_type,
                state="readonly",
                width=20
            )
            self.filtering_select.pack(side="left", pady=15, padx=5)

        elif operation_type == settings.operation_select[3]:
            pass

        elif operation_type == settings.operation_select[4]:
            pass

        elif operation_type == settings.operation_select[5]:
            pass

        elif operation_type == settings.operation_select[6]:
            pass

    def record_audio(self):
        amp = self.amp_selector.get()
        sampling = self.sampling_select.get()
        duration = abs(float(self.duration_var.get()))
        signal = self.signal_selector.get()
        fs = abs(float(self.fs_var.get()))
        shift = float(self.t_shift_var.get())
        n0 = float(self.start_var.get())
        
        n, y = audio_utils.record_audio(duration, fs, shift, n0)
        self.handle_audio_parameters(amp, sampling, n, y, fs, n0, signal, duration)

    def load_audio(self):
        amp = self.amp_selector.get()
        sampling = self.sampling_select.get()
        duration = abs(float(self.duration_var.get()))
        signal = self.signal_selector.get()
        shift = float(self.t_shift_var.get())
        n0 = float(self.start_var.get())

        n, y, fs, type= file_manager.load_audio_file(duration, shift, n0)

        if type == settings.audio_types[0]: 
            self.handle_audio_parameters(amp, sampling, n[0], y[0], fs, n0, signal)
        else:
            self.handle_audio_parameters(amp, sampling, n[0], y[0], fs, n0, settings.GRAPH[0])
            self.handle_audio_parameters(amp, sampling, n[0], y[0], fs, n0, settings.GRAPH[1])

    def generate_synthetic(self):
        amp = self.amp_selector.get()
        signal = self.signal_selector.get()
        synthetic = self.signal_synthetic.get()
        fa = abs(float(self.fa_var.get()))
        fs = abs(float(self.fs_var.get()))
        gain = float(self.gain_var.get())
        n0 = float(self.start_var.get())
        duration = abs(float(self.duration_var.get()))
        shift = float(self.t_shift_var.get())
        sampling = self.sampling_select.get()

        try:
            n, y = generation.signal_selector(synthetic, fa, fs, gain, n0, duration, shift)
            self.handle_signal_parameters(amp, sampling, n, y, fs, n0, signal, duration)
        except:
            messagebox.showwarning("Warning", "Select signal first.")

    def handle_operation(self, event=None):
        try:
            if hasattr(self, "basic_select"):
                basic_action = self.basic_select.get()
                self.n3, self.y3, self.fs3 = math.basic_operations(basic_action, self.y1, self.fs1, self.n01, self.y2, self.fs2, self.n02)
            elif hasattr(self, "filtering_select"):
                filtering_action = self.filtering_select.get()
                self.n3, self.y3 = math.filtering_operation(filtering_action, self.y1, self.y2, 0, 0)
        except:
            messagebox.showwarning("Warning", "Select at least two functions")

    def handle_features(self):
        try:
            signal_utils.stadistics(self.y1, self.fs1, self.y2, self.fs2, self.y3, self.fs3)
        except:
            messagebox.showwarning("Warning", "Select at least two functions")
        
    def handle_signal_to_signal(self):
        pass

    def handle_fourier_t(self):
        pass

    def handle_cosine_t(self):
        pass

    def handle_wavelet_t(self):
        pass

    def handle_none(self):
        pass

    def handle_signal_parameters(self, amp, sampling, n, y, fs, n0, signal_name, duration):
        if hasattr(self, "preprocessing_select"):
            action = self.preprocessing_select.get()
        else:
            action = settings.preprocessing_operation[3]

        if sampling not in settings.sampling_method:
            sampling = settings.sampling_method[2]

        n , y = signal_utils.time_sampling(sampling ,y, n0, fs, 'synthetic', duration)
        y = signal_utils.amplitud_selector(amp, y)
        y = math.preprocessing_operations(action, y)
        if signal_name == settings.GRAPH[0]:
            self.y1, self.n1, self.fs1, self.n01 = y, n, fs, n0
        elif signal_name == settings.GRAPH[1]:
            self.y2, self.n2, self.fs2, self.n02 = y, n, fs, n0

        self.plotter.update_plot(signal_name, n, y)

    def handle_audio_parameters(self, amp, sampling, n, y, fs, n0, signal_name, duration):
        if hasattr(self, "preprocessing_select"):
            action = self.preprocessing_select.get()
        else:
            action = settings.preprocessing_operation[3]

        if sampling not in settings.sampling_method:
            sampling = settings.sampling_method[2]
            
        n, y = signal_utils.time_sampling(sampling ,y, n0, fs, 'audio', duration)
        y = signal_utils.amplitud_selector(amp, y)
        y = math.preprocessing_operations(action, y)
        if signal_name == settings.GRAPH[0]:
            self.y1, self.n1, self.fs1 = y, n, fs
        elif signal_name == settings.GRAPH[1]:
            self.y2, self.n2, self.fs2 = y, n, fs

        self.plotter.update_plot(signal_name, n, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()