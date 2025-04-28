import numpy as np
from scipy.signal import resample
from tkinter import simpledialog, messagebox
from core import settings

def amplitud_scaling(signal): 
    gain = simpledialog.askfloat  ("Constant Value:", "Value:", initialvalue=1.0)
    return gain * np.array(signal)

def amplitud_log(signal):
    return np.log(signal)

def amplitud_exponential(signal):
    power = simpledialog.askfloat  ("Constant Value:", "Value:", initialvalue=1.0)
    return power**np.array(signal)

def amplitud_inversion(signal):
    return 1/np.array(signal)

def amplitud_power(signal):
    power = simpledialog.askfloat  ("Constant Value:", "Value:", initialvalue=1.0)
    return np.array(signal)**power

def amplitud_none(signal):
    return np.array(signal)

def amplitud_selector(name: str, signal: list[float] | np.ndarray)-> np.ndarray:
    options = {
        settings.opera_amp[0]: amplitud_scaling,
        settings.opera_amp[1]: amplitud_log,
        settings.opera_amp[2]: amplitud_exponential,
        settings.opera_amp[3]: amplitud_inversion,
        settings.opera_amp[4]: amplitud_power,
        settings.opera_amp[5]: amplitud_none
    }

    y = options[name](signal)
    y = verification(y)
    return y

def downsampling(signal, n0, fs, type, duration):
    k = abs(simpledialog.askinteger("Downsampling for integer k", "Value:",minvalue = 0, initialvalue=2))
    y = signal[::k]
    n = axis_time(len(signal), fs, n0, type, duration)
    return n, y

def upsampling(signal, n0, fs, type, duration):
    k = simpledialog.askinteger("Upsampling for integer k", "Value:",minvalue = 1 , initialvalue=3)
    y = np.zeros(len(signal) * k - (k-1))
    n = axis_time(len(signal), fs, n0, type, duration)

    y[::k] = signal
    for i in range(0, len(y)):
        if i % k != 0 and i:
            idx_prev = i // k
            idx_next = idx_prev + 1
            
            if idx_next >= len(signal):
                idx_next = idx_prev
            
            alpha = (i % k) / k
            y[i] = signal[idx_prev] * (1 - alpha) + signal[idx_next] * alpha
            
    return n, y

def sampling_none(signal, n0, fs, type, duration):
    n = axis_time(len(signal), fs, n0, type, duration)
    return n, np.asarray(signal)

def time_sampling(name: str, signal: list[float] | np.ndarray, n0:int, fs:int, type:str, duration:float)-> tuple[np.ndarray, np.ndarray]:
    options = {
        settings.sampling_method[0]: downsampling,
        settings.sampling_method[1]: upsampling,
        settings.sampling_method[2]: sampling_none
    }
    n, y = options[name](signal, n0, fs, type, duration)

    return n, y

def axis_time(n_samples: int, fs: int, n0: float, type: str, duration: float) -> np.ndarray:
    if type == 'synthetic':
        n = np.arange(n0, n0 + duration, 1/fs)
    elif type == 'audio':
        n0_samples = int(n0 * fs)
        n = np.arange(n0_samples, n0_samples + n_samples)
        n = n / fs 
    return n

def resample_and_align(y1, fs1, y2, fs2):
    if fs1 >= fs2:
        fs_target = fs2
    else:
        fs_target = fs1
    fs_target = abs(simpledialog.askinteger("Warning", "Frequency value:", initialvalue=int(fs_target)))
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
    
    y1_resampled = verification(y1_resampled)
    y2_resampled = verification(y2_resampled)

    return y1_resampled, y2_resampled, fs_target

def verification(y: list[float] | np.ndarray)-> np.ndarray:
    y = np.asarray(y, dtype=np.float32)
    mask = np.isfinite(y)
    if not np.all(mask):
        messagebox.showwarning("Warning", "Value nan or inf deleted...")
        y = y[mask]
    return y