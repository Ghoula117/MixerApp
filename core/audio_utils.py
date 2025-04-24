import numpy as np
import sounddevice as sd
import time
from time import sleep
from tkinter import simpledialog, messagebox
from core.signal_utils import resample_and_align, axis_time
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

    y = shift_audio(audio_data, shift, fs, n0, duration)
    n = axis_time(len(y), fs, n0)

    return n, y

def shift_audio(audio, shift_seconds, fs, n0_seconds, total_duration_seconds):
    audio = np.squeeze(audio).flatten()
    audio_length = len(audio)
    
    # Total samples in the output buffer
    n_total_samples = int(total_duration_seconds * fs)
    y = np.zeros(n_total_samples)

    # Calcula el desplazamiento en muestras
    shift_samples = int(shift_seconds * fs)
    n0_samples = int(n0_seconds * fs)

    # Índice donde comienza el audio en el vector de salida
    insert_start = shift_samples - n0_samples
    insert_end = insert_start + audio_length

    # Rango válido de inserción (clipping para evitar errores)
    clip_start = max(insert_start, 0)
    clip_end = min(insert_end, n_total_samples)

    # Ajuste en el índice de entrada del audio si insert_start < 0
    audio_clip_start = max(0, -insert_start)
    audio_clip_end = audio_clip_start + (clip_end - clip_start)

    # Inserta solo la parte válida del audio
    if clip_end > clip_start:
        y[clip_start:clip_end] = audio[audio_clip_start:audio_clip_end]

    return y

def play_mono(signal, y, fs):
    if signal == settings.GRAPH[0]:
        mono = np.column_stack((y, np.zeros_like(y)))
    elif signal == settings.GRAPH[1]:
        mono = np.column_stack((np.zeros_like(y), y))
    indx = simpledialog.askinteger("Playback method", "\n1 Direct audio\n2. Invert audio", minvalue=1, maxvalue=2, initialvalue=1)
    if indx==2:
        mono = np.flip(mono)
    sd.play(mono, fs)
    sd.wait()

def play_stereo(y1, fs1, y2, fs2):
    y1_aligned, y2_aligned, fs_common = resample_and_align(y1, fs1, y2, fs2)
    stereo = np.stack([y1_aligned, y2_aligned], axis=1)
    indx = simpledialog.askinteger("Playback method", "\n1 Direct audio\n2. Invert audio", minvalue=1, maxvalue=2, initialvalue=1)
    if indx==2:
        stereo = np.flip(stereo)
    sd.play(stereo, fs_common)
