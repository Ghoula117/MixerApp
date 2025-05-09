#Values
SAMPLERATE = 44100

default_h_parameters = "0.5  1  0.5  0  -0.5  -1  -0.5  0  0.5"

feature_keys = [
    'Energy',
    'Power',
    'Mode',
    'Median',
    'Mean',
    'Variance',
    'Standard Deviation',
    'Minimum',
    'Maximum',
    'Skewness',
    'Kurtosis',
    'Entropy',
    'Dominant Frequency',
    'Sampling Frequency'
]

ax = [1.0, -2.474416174978162796804781464743427932262,  2.811006311911582233875606107176281511784, -1.703772240915468749733463482698425650597,  0.544432694888534296495663511450402438641, -0.072315669102958557434845943134860135615]

bx = [0.003279216306360205161751775193579305778 , 0.016396081531801026676120613956300076097 , 0.032792163063602053352241227912600152194 , 0.032792163063602053352241227912600152194 , 0.016396081531801026676120613956300076097 , 0.003279216306360205161751775193579305778 ]

#Combobox Menu
source_select = ["Microphone", "Load File", "Synthetic", "Board"]

control_select = ["Play x1", "Play x2", "Play both", "Play result", "Save"]

operation_select = ["Basic operations", "Preprocessing", "Filtering", "Fourier Transform", "Cosine Transform", "Wavelet"]

GRAPH = ["y1(n)", "y2(n)"]

opera_amp = ["A*x(n)", "log(x(n))", "A^x(n)", "1/x(n)", "x(n)^k", "None"]

sampling_method = ["Downsampling", "Upsampling", "None"]

baudrate = ["9600", "19200", "38400", "57600", "115200"]

#Option
signalSelector = ["Impulse", "Step", "Ramp", "Triangular", "Sawtooth", "Sine", "Cosine", "SinC", "Chirp"]

basic_operation = ["y1 + y2", "y1 - y2", " y1 * y2", "y1 / y2", "y1 ** y2"]

preprocessing_operation = ["Normalization 0 & 1", "Normalization -1 & 1", "Standard normalization"]

filter_type = ["FIR Filter", "IIR Filter"]

fourier_operation = ["DFT Magnitude/Phase", "DFT Filtering"]

cosine_operation = ["Cosine Magnitude", "Cosine Filtering"]

coeficients = ["ax", "bx"]

#File data
file_types = [("WAV Files", "*.wav"), ("All Files", "*.*")]

file_in_types = [("JSON files", "*.json"), ("All Files", "*.*")]

audio_types = ["Mono", "Stereo"]

signal_types = ["audio", "signal"]

metadata = {"fs": SAMPLERATE, "description": "Two input signals -> One result"}