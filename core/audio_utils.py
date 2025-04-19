import numpy as np
import sounddevice as sd
from scipy.signal import resample
from tkinter import simpledialog, messagebox
from core import settings

def record_audio(duration: float, fs: int):

    top = simpledialog.Toplevel()
    top.title("Recording")
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

def resample_and_align(y1, fs1, y2, fs2, fs_target=44100):
    dur1 = len(y1) / fs1
    dur2 = len(y2) / fs2

    n1_target = int(fs_target * dur1)
    n2_target = int(fs_target * dur2)

    y1_resampled = resample(y1, n1_target)
    y2_resampled = resample(y2, n2_target)

    ly1 = len(y1_resampled)
    ly2 = len(y2_resampled)
    pad = abs(ly1 - ly2)

    if ly1 > ly2:
        y2_resampled = np.pad(y2_resampled, (0, pad), mode='constant', constant_values=0)
    elif ly1 < ly2:
        y1_resampled = np.pad(y1_resampled, (0, pad), mode='constant', constant_values=0)

    return y1_resampled, y2_resampled, fs_target

def play_mono(signal, y, fs):
    if signal == settings.GRAPH[0]:
        mono = np.column_stack((y, np.zeros_like(y)))
    elif signal == settings.GRAPH[1]:
        mono = np.column_stack((np.zeros_like(y), y))
    sd.play(mono, fs)
    sd.wait()

def play_stereo(y1, fs1, y2, fs2):
    while True:
        fs_target = abs(simpledialog.askinteger("stereo playback", "Frequency value:", initialvalue=settings.SAMPLERATE))
        if fs_target < 1:
            messagebox.showwarning("Warning", "Frequency value must exceed 40000 Hz.")
            continue
        break
    y1_aligned, y2_aligned, fs_common = resample_and_align(y1, fs1, y2, fs2, fs_target)
    stereo = np.stack([y1_aligned, y2_aligned], axis=1)
    sd.play(stereo, fs_common)
