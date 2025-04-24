import numpy as np
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
    time_axes = [axis_time(len(c), fs, n0) for c in shifted_channels]

    messagebox.showinfo("File type", f"File: {file}")
    
    return time_axes, shifted_channels, fs, file

def save_signal(fs, y1, y2, y3):
    file_path = filedialog.askopenfilename(filetypes=settings.file_types)
    if not file_path:
        messagebox.showwarning("Warning", "No file selected")
        return
    
    metadata = {
        "fs": fs,
        "duration_y1_seg": len(y1) / fs,
        "duration_y2_seg": len(y2) / fs,
        "duration_y3_seg": len(y3) / fs,
        "descripcion": "Señales procesadas y almacenadas"
    }

    np.savez(file_path, y1=y1, y2=y2, y3=y3, metadata=metadata)
    messagebox.showwarning("Done", "File succesfuly save somewhere")
