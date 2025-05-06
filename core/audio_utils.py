import numpy as np
import sounddevice as sd
from time import sleep
from tkinter import simpledialog, messagebox
from core.signal_utils import resample_signal, axis_time
from core import settings

def record_audio(duration: float, fs: int, shift:int, n0:int):

    top = simpledialog.Toplevel()
    top.title("Recording")
    sleep(1)
    tk_label = simpledialog.Label(top, text="Recording... Speak")
    tk_label.pack(padx=20, pady=20)
    top.update()

    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32', device=5)
        sd.wait()
    except Exception as e:
        top.destroy()
        messagebox.showerror("Error", f"INVALID Fs:\n{e}")
        return None, None

    top.destroy()

    y = shift_audio(audio_data, shift, fs, n0, duration)
    n = axis_time(len(y), fs, n0, 'audio', duration)

    return n, y

def play_audio(type, signal, y1, fs1, y2, fs2):
    gain = simpledialog.askfloat("Volume Gain", "Factor:", initialvalue=1.5)
    indx = simpledialog.askinteger("Playback method", "\n1 Direct audio\n2 Invert audio\n3 ECO", minvalue=1, maxvalue=3, initialvalue=1)
    
    if type == settings.audio_types[0]:
        if signal == settings.GRAPH[0]:
            mono = np.column_stack((y1, np.zeros_like(y1)))
        elif signal == settings.GRAPH[1]:
            mono = np.column_stack((np.zeros_like(y1), y1))
        fs = fs1
    elif type == settings.audio_types[1]:
        y1_resampled, y2_resampled, fs = resample_signal(y1, fs1, y2, fs2)
        mono = 0.5 * (y1_resampled + y2_resampled)

    if indx==1:
        y_louder = mono * gain
        sd.play(y_louder, fs)
        sd.wait()
    elif indx==2:
        mono = np.flip(mono, axis=0)
        y_louder = mono * gain
        sd.play(y_louder, fs)
        sd.wait()
    elif indx==3:
        mono_mono = mono[:, 0] if np.any(mono[:, 0]) else mono[:, 1]
        A = simpledialog.askfloat("Eco Amplitud", "value:", initialvalue=1)
        K = simpledialog.askfloat("Eco shift"   , "value:", initialvalue=1)
        A1, A2, A3 = A * 1.5, A * 0.5, A * 0.2
        k1, k2, k3 = int(K * fs), int(K * 2 * fs), int(K * 3 * fs)

        y_echo = np.zeros(len(mono_mono) + k3, dtype=np.float32)
        y_echo[:len(mono_mono)] += mono_mono
        y_echo[k1:k1+len(mono_mono)] += A1 * mono_mono
        y_echo[k2:k2+len(mono_mono)] += A2 * mono_mono
        y_echo[k3:k3+len(mono_mono)] += A3 * mono_mono

        try:
            y_louder = y_echo * gain
            sd.play(y_louder, fs)
            sd.wait()
        except:
            messagebox.showerror("Error", "Playback failed")
            return

def shift_audio(audio, shift_seconds, fs, n0_seconds, total_duration_seconds):
    audio = np.squeeze(audio).flatten()
    audio_length = len(audio)

    n_total_samples = int(total_duration_seconds * fs)
    y = np.zeros(n_total_samples)

    shift_samples = int(shift_seconds * fs)
    n0_samples = int(n0_seconds * fs)

    insert_start = shift_samples - n0_samples
    insert_end = insert_start + audio_length

    #clipping
    clip_start = max(insert_start, 0)
    clip_end = min(insert_end, n_total_samples)

    audio_clip_start = max(0, -insert_start)
    audio_clip_end = audio_clip_start + (clip_end - clip_start)

    if clip_end > clip_start:
        y[clip_start:clip_end] = audio[audio_clip_start:audio_clip_end]

    return y