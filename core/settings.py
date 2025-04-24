#Global
SAMPLERATE = 44100
INPUT_FOLDER = "data/input/"
OUTPUT_FOLDER = "data/output/"

GRAPH = ["x1(n)", "x2(n)"]

opera_amp = ["A*x(n)", "log(x(n))", "A^x(n)", "1/x(n)", "x(n)^k", "None"]

signalSelector = ["Impulse", "Step", "Ramp", "Triangular", "Sawtooth", "Sine", "Cosine", "SinC", "Chirp"]

source_select = ["Microphone", "Audio File", "Synthetic", "Board"]

control_select = ["Play x1", "Play x2", "Play result", "Save"]

operation_select = ["Basic operations", "Preprocessing", "Processing (Filtering)", "Signal-to-signal processing", "Fourier Transform", "Cosine Transform", "Wavelet Transform"]

file_types = [("WAV Files", "*.wav"), ("All Files", "*.*")]

audio_types = ["Mono", "Stereo"]

preprocessing_operation = ["Normalization 0 & 1", "Normalization -1 & 1", "Standard normalization", "None"]

basic_operation = ["y1 + y2", "y1 - y2", " y1 * y2", "y1 / y2", "y1 ** y2", ]

sampling_method = ["Downsampling", "Upsampling", "None"]

metadata = {"fs": SAMPLERATE, "description": "Two input signals -> One result"}