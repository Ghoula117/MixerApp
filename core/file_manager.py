import json
import numpy as np
import serial
import time
from tkinter import filedialog, messagebox
import soundfile as sf
from core import settings
from core.audio_utils import shift_audio
from core.signal_utils import axis_time

def load_audio_file(duration:float, shift:int, n0:int):
    file_path = filedialog.askopenfilename(filetypes=settings.file_types)
    if not file_path:
        messagebox.showwarning("Warning", "No file selected")
        return

    audio, fs = sf.read(file_path)

    if audio.ndim == 1:
        file = settings.audio_types[0]
        channels = [audio]
    elif audio.ndim == 2 and audio.shape[1] == 2:
        file = settings.audio_types[1]
        channels = [audio[:, i] for i in range(audio.shape[1])]

    if duration is not None:
        max_samples = int(duration * fs)
        channels = [ch[:max_samples] for ch in channels]

    shifted_channels = [shift_audio(c, shift, fs, n0, duration) for c in channels]
    time_axes = [axis_time(len(c), fs, n0, 'audio', duration) for c in shifted_channels]

    messagebox.showinfo("File type", f"File: {file}")
    
    return time_axes, shifted_channels, fs, file

def load_signal(n0): 
    file_path = filedialog.askopenfilename(filetypes=settings.file_in_types)
    if not file_path:
        messagebox.showwarning("Warning", "No file selected")
        return None

    with open(file_path, 'r') as f:
        data = json.load(f)

    h = np.array(data["y1"])
    fs = int(data["fs"])

    nf = n0 + len(h) - 1
    n = np.linspace(n0, nf, len(h))

    return n, h, fs

def load_coeficients(): 
    file_path = filedialog.askopenfilename(filetypes=settings.file_in_types)
    if not file_path:
        messagebox.showwarning("Warning", "No file selected")
        return None

    with open(file_path, 'r') as f:
        data = json.load(f)

    ax = np.array(data["ax"])
    bx = np.array(data["bx"])

    return ax, bx

def recibe_signal(baudrate, fs, n0, duration):
    import serial
    import numpy as np
    import time

    puerto = '/dev/ttyACM0'
    max_time = 5
    N = 10  # número fijo de datos a leer
    serialInstance = serialInstance = serial.Serial(port=puerto, baudrate=baudrate, timeout=1)

    y = np.zeros(N)

    while True:
        if serialInstance.in_waiting==0:
            packet = serialInstance.readline().decode('utf-8').strip()
            print(packet)
            y = int(packet.split(","))
        """elif serialInstance.in_waiting == 0:
            print("No data received")
            break"""
        time.sleep(0.1)
    serialInstance.close()

    n = np.arange(n0, n0 + len(y))
    y = np.array(y, dtype=float)
    return n, y 

def save_signal(fs, y1, y2, y3):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=settings.file_in_types)
    if not file_path:
        messagebox.showwarning("Warning", "No file selected")
        return
    
    metadata = {
        "fs": fs,
        "duration_y1_seg": len(y1) / fs,
        "duration_y2_seg": len(y2) / fs,
        "duration_y3_seg": len(y3) / fs,
        "y1": y1.tolist(), 
        "y2": y2.tolist(),
        "y3": y3.tolist(),
        "Created by": "Alejandro M.",
    }

    with open(file_path, "w") as f:
        json.dump(metadata, f, indent=4)

    messagebox.showinfo("Done", "File successfully saved")