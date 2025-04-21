import numpy as np
from tkinter import filedialog, messagebox
import soundfile as sf
from core import settings

def load_audio_file():
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

    n = [np.arange(len(c)) / fs for c in channels]
    messagebox.showinfo("File type", f"File: {file}")
    
    return n, channels, fs, file