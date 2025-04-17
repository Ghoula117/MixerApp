#Global
SAMPLERATE = 44100
AUDIO_FORMAT = "wav"
INPUT_FOLDER = "data/input/"
OUTPUT_FOLDER = "data/output/"
GRAPH = ["x1(n)", "x2(n)"]
opera_amp = ["A*x(n)", "log(x(n))", "A^x(n)", "1/x(n)", "x(n)^k", "None"]
signalSelector = ["Impulse", "Step", "Ramp", "Triangular", "Sawtooth", "Sine", "Cosine", "SinC", "Chirp"]
source_select = ["Microphone", "Audio File", "Synthetic", "Board"]
control_select= ["Record", "Play", "Save", "Result"]
operation_select= ["Preprocessing", "Processing (Filtering)", "Signal-to-signal processing", "Fourier Transform", "Cosine Transform", "Wavelet Transform"]