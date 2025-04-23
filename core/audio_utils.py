import numpy as np
import sounddevice as sd
import time
from time import sleep
from tkinter import simpledialog, messagebox
from core.signal_utils import resample_and_align
from core import settings

def record_audio(duration: float, fs: int, shift:int, n0:int):

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

    y = shift_audio(audio_data, shift, fs, n0)
    n = axis_time(len(y), fs, n0)

    return n, y

def shift_audio(audio, shift_seconds, fs, n0_seconds):
    audio = np.squeeze(audio).flatten()
    n_samples = len(audio)
    
    shift_samples = int(shift_seconds * fs)
    n0_samples = int(n0_seconds * fs)

    y = np.zeros(n_samples)

    insert_start = max(0, shift_samples - n0_samples)
    insert_end = min(n_samples, insert_start + n_samples)

    audio_start = max(0, n0_samples - shift_samples)
    audio_end = min(n_samples, audio_start + (insert_end - insert_start))

    if insert_end > insert_start and audio_end > audio_start:
        y[insert_start:insert_end] = audio[audio_start:audio_end]

    return y

def axis_time(n_samples, fs, n0_seconds):
    return np.arange(n0_seconds * fs, n0_seconds * fs + n_samples) / fs

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
