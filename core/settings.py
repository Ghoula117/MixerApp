#Global var
SAMPLERATE = 44100

#Combobox Menu
source_select = ["Microphone", "Audio File", "Synthetic", "Board"]

control_select = ["Play x1", "Play x2", "Play result", "Save"]

operation_select = ["Basic operations", "Preprocessing", "Processing (Filtering)", "Signal-to-signal processing", "Fourier Transform", "Cosine Transform", "Wavelet Transform"]

GRAPH = ["x1(n)", "x2(n)"]

opera_amp = ["A*x(n)", "log(x(n))", "A^x(n)", "1/x(n)", "x(n)^k", "None"]

sampling_method = ["Downsampling", "Upsampling", "None"]

#Combobox Option
signalSelector = ["Impulse", "Step", "Ramp", "Triangular", "Sawtooth", "Sine", "Cosine", "SinC", "Chirp"]

basic_operation = ["y1 + y2", "y1 - y2", " y1 * y2", "y1 / y2", "y1 ** y2",  "Stadistics"]

preprocessing_operation = ["Normalization 0 & 1", "Normalization -1 & 1", "Standard normalization", "None"]

filter_type = ["FIR_FILTER", "IIR_FILTER"]

#File data
file_types = [("WAV Files", "*.wav"), ("All Files", "*.*")]

file_in_types = [("JSON files", "*.json"), ("All Files", "*.*")]

audio_types = ["Mono", "Stereo"]

metadata = {"fs": SAMPLERATE, "description": "Two input signals -> One result"}