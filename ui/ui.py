import tkinter as tk
from tkinter import ttk, messagebox
from core.plotter import Plotter, ProcessedSignalPlot
from core.signal_utils import stadistics
from core import generation, signal_utils, audio_utils , file_manager, math, settings

class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mixer Signal")
        self.root.geometry("1000x600")

        self.y1  = None
        self.n01 = None
        self.fs1 = None
        self.y2  = None
        self.n02 = None
        self.fs2 = None
        self.y3  = None
        self.n03 = None
        self.fs3 = None

        #Frame superior
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
        ttk.Button(self.top_frame, text="Statistics", command=self.handle_features).pack(side="right", pady=10)

        #Frame principal 
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        #Contenedor lateral izquierdo 
        self.left_panel_container = ttk.Frame(self.main_frame)
        self.left_panel_container.pack(side="left", fill="y", padx=10, pady=10)

        #Panel fijo (parte superior del panel izquierdo)
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
        self.duration_var = self.create_labeled_entry(self.left_fixed_panel, "Duration: (s)", 2)
        self.start_var = self.create_labeled_entry(self.left_fixed_panel, "start: (s)", 0)
        self.t_shift_var = self.create_labeled_entry(self.left_fixed_panel, "Time Shift: (s)", 0)

        ttk.Label(self.left_fixed_panel, text="Sampling").pack(pady=(0, 5))
        self.sampling_select = ttk.Combobox(
            self.left_fixed_panel,
            values=settings.sampling_method,
            state="readonly",
            width=10
        )
        self.sampling_select.pack(padx=5, pady=(0, 10))
        self.sampling_select.set(settings.sampling_method[2])

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
            ttk.Button(self.left_dynamic_signal_panel, text="Load audio", command=self.load_audio).pack(padx=5, pady=(0, 10))
            ttk.Button(self.left_dynamic_signal_panel, text="Load signal",command=self.load_signal).pack(padx=5, pady=(0, 10))

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
            self.baudrate_selector = ttk.Combobox(
                self.left_dynamic_signal_panel,
                values=settings.baudrate,
                state="readonly",
                width=10
            )
            self.baudrate_selector.pack(padx=10, pady=(0, 10))

            ttk.Button(self.left_dynamic_signal_panel, text="Connect", command=self.external_signal).pack(pady=10)

    def configure_control(self, event=None):
        action = self.control_selection.get()
        actions = {
            settings.control_select[0]: lambda: audio_utils.play_audio(settings.audio_types[0] ,settings.GRAPH[0], self.y1, self.fs1, y2=None, fs2=None),
            settings.control_select[1]: lambda: audio_utils.play_audio(settings.audio_types[0] ,settings.GRAPH[1], self.y2, self.fs2, y2=None, fs2=None),
            settings.control_select[2]: lambda: audio_utils.play_audio(settings.audio_types[1] ,None, self.y1, self.fs1, self.y2, self.fs2),
            settings.control_select[3]: lambda: audio_utils.play_audio(settings.audio_types[0] ,settings.GRAPH[1], self.y3, self.fs3, y2=None, fs2=None),
            settings.control_select[4]: lambda: file_manager.save_signal(self.fs1, self.y1, self.n1, self.y2, self.n2, self.y3, self.n3)
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
            self.fourier_select = ttk.Combobox(
                self.up_dynamic_op_panel,
                values=settings.fourier_operation,
                state="readonly",
                width=20
            )
            self.fourier_select.pack(side="left", pady=15, padx=5)

        elif operation_type == settings.operation_select[4]:
            pass

        elif operation_type == settings.operation_select[5]:
            pass

    def record_audio(self):
        amp = self.amp_selector.get()
        sampling = self.sampling_select.get()
        duration = abs(float(self.duration_var.get()))
        signal = self.signal_selector.get()
        fs = abs(float(self.fs_var.get()))
        shift = float(self.t_shift_var.get())
        n0 = float(self.start_var.get())
        try:
            n, y = audio_utils.record_audio(duration, fs, shift, n0)
            self.handle_signal_parameters(amp, sampling, n, y, fs, n0, signal, duration, settings.signal_types[0])
        except:
            messagebox.showwarning("Warning", "Recording failure.")

    def external_signal(self):
        amp = self.amp_selector.get()
        baudrate = self.baudrate_selector.get()
        sampling = self.sampling_select.get()
        duration = abs(float(self.duration_var.get()))
        signal = self.signal_selector.get()
        fs = abs(float(self.fs_var.get()))
        shift = float(self.t_shift_var.get())
        n0 = float(self.start_var.get())

        n, y = file_manager.recibe_signal(baudrate, fs, n0, duration)
        self.handle_signal_parameters(amp, n, y, fs, n0, signal, duration, settings.signal_types[1])
        """try:
            n, y = file_manager.recibe_signal(baudrate, fs, n0, shift, duration)
            self.handle_signal_parameters(amp, sampling, n, y, fs, n0, signal, duration, signal)
        except:
            messagebox.showwarning("Warning", "Reading failure.")"""

    def load_audio(self):
        amp = self.amp_selector.get()
        sampling = self.sampling_select.get()
        duration = abs(float(self.duration_var.get()))
        signal = self.signal_selector.get()
        shift = float(self.t_shift_var.get())
        n0 = float(self.start_var.get())

        try:
            n, y, fs, type= file_manager.load_audio_file(duration, shift, n0)
            if type == settings.audio_types[0]: 
                self.handle_signal_parameters(amp, sampling, n[0], y[0], fs, n0, signal, duration, settings.signal_types[0])
            else:
                self.handle_signal_parameters(amp, sampling, n[0], y[0], fs, n0, settings.GRAPH[0], duration, settings.signal_types[0])
                self.handle_signal_parameters(amp, sampling, n[0], y[0], fs, n0, settings.GRAPH[1], duration, settings.signal_types[0])
        except:
            messagebox.showwarning("Warning", "Fail loading audio.")

    def load_signal(self):
        amp = self.amp_selector.get()
        sampling = self.sampling_select.get()
        duration = abs(float(self.duration_var.get()))
        n0 = float(self.start_var.get())

        n, y, fs = file_manager.load_signal(n0)
        self.handle_signal_parameters(amp, n, y, fs, n0, settings.GRAPH[1], duration, settings.signal_types[1])

        """try:
            n, y, fs = file_manager.load_signal(n0)
            self.handle_signal_parameters(amp, n, y, fs, n0, settings.GRAPH[1], duration, settings.signal_types[1])
        except:
            messagebox.showwarning("Warning", "Fail loading signal.")"""

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

        try:
            n, y = generation.signal_selector(synthetic, fa, fs, gain, n0, duration, shift)
            self.handle_signal_parameters(amp, n, y, fs, n0, signal, duration, settings.signal_types[1])
        except:
            messagebox.showwarning("Warning", "Select signal first.")

    def handle_operation(self, event=None):
        """try:"""
        if hasattr(self, "basic_select") and self.basic_select.winfo_exists():
            try:
                basic_action = self.basic_select.get()
                self.n03, self.y3, self.fs3 = math.basic_operations(basic_action, self.y1, self.fs1, self.n01, self.y2, self.fs2, self.n02)
            except tk.TclError:
                basic_action = None
        if hasattr(self, "filtering_select") and self.filtering_select.winfo_exists():
            try:
                filtering_action = self.filtering_select.get()
                self.n03, self.y3, self.fs3 = math.filtering_operation(filtering_action, x=self.y1, nx0=self.n01, fs1=self.fs1, h=self.y2, nh0=self.n02, fs2=self.fs2)
            except tk.TclError:
                filtering_action = None
        if hasattr(self, "fourier_select") and self.fourier_select.winfo_exists():
            try:
                fourier_action = self.fourier_select.get()
                self.n03, self.y3, self.fs3 = math.fourier_operation(fourier_action, x=self.y1, fs1=self.fs1, h=self.y2, fs2=self.fs2)
            except tk.TclError:
                fourier_action = None
        """except:
            messagebox.showwarning("Warning", "Invalid operation")"""

    def handle_features(self):
        try:
            stadistics(y1  = self.y1  if self.y1  is not None else [],
            fs1 = self.fs1 if self.fs1 is not None else  0,
            y2  = self.y2  if self.y2  is not None else [],
            fs2 = self.fs2 if self.fs2 is not None else  0,
            y3  = self.y3  if self.y3  is not None else [],
            fs3 = self.fs3 if self.fs3 is not None else  0)
        except:
            messagebox.showwarning("Warning", "Select at least two functions")

    def handle_cosine_t(self):
        pass

    def handle_wavelet_t(self):
        pass

    def handle_none(self):
        pass

    def handle_signal_parameters(self, amp, n, y, fs, n0, signal_name, duration, type):
        y = signal_utils.amplitud_selector(amp, y)
        if hasattr(self, "sampling_select"):
            sampling = self.sampling_select.get()
            n , y = signal_utils.time_sampling(sampling ,y, n0, fs, type, duration)
        if hasattr(self, "preprocessing_select"):
            action = self.preprocessing_select.get()
            y = math.preprocessing_operations(action, y)

        if signal_name == settings.GRAPH[0]:
            self.y1, self.n1, self.fs1, self.n01 = y, n, fs, n0
        elif signal_name == settings.GRAPH[1]:
            self.y2, self.n2, self.fs2, self.n02 = y, n, fs, n0

        self.plotter.update_plot(signal_name, n, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()