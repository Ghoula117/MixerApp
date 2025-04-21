import numpy as np
import sounddevice as sd
import time
from time import sleep
from tkinter import simpledialog, messagebox
from core.signal_utils import resample_and_align
from core import settings

def record_audio(duration: float, fs: int):

    top = simpledialog.Toplevel()
    top.title("Recording")
    time.sleep(1)
    tk_label = simpledialog.Label(top, text="Recording... Speak")
    tk_label.pack(padx=20, pady=20)
    top.update()

    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32', device=5)
        sd.wait()

    except Exception as e:
        top.destroy()
        messagebox.showerror("Error", f"Recording failed:\n{e}")
        return None, None

    top.destroy()

    n = np.arange(len(audio_data)) / fs

    return n, audio_data[:, 0]

def play_mono(signal, y, fs):
    if signal == settings.GRAPH[0]:
        mono = np.column_stack((y, np.zeros_like(y)))
    elif signal == settings.GRAPH[1]:
        mono = np.column_stack((np.zeros_like(y), y))
    sd.play(mono, fs)
    sd.wait()

def play_stereo(y1, fs1, y2, fs2):
    y1_aligned, y2_aligned, fs_common = resample_and_align(y1, fs1, y2, fs2)
    stereo = np.stack([y1_aligned, y2_aligned], axis=1)
    sd.play(stereo, fs_common)
