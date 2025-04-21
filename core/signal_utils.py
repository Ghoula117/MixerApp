import numpy as np
from scipy.signal import resample
from tkinter import simpledialog, messagebox
from core import settings

def amplitud_scaling(signal: list[float] | np.ndarray)-> np.ndarray: 
    gain = simpledialog.askfloat  ("Constant Value:", "Value:", initialvalue=1.0)
    return gain * np.array(signal)

def amplitud_log(signal: list[float] | np.ndarray)-> np.ndarray:
    return np.log(signal)

def amplitud_exponential(signal: list[float] | np.ndarray)-> np.ndarray:
    power = simpledialog.askfloat  ("Constant Value:", "Value:", initialvalue=1.0)
    return power**np.array(signal)

def amplitud_inversion(signal: list[float] | np.ndarray)-> np.ndarray:
    return 1/np.array(signal)

def amplitud_power(signal: list[float] | np.ndarray)-> np.ndarray:
    power = simpledialog.askfloat  ("Constant Value:", "Value:", initialvalue=1.0)
    return np.array(signal)**power

def amplitud_none(signal: list[float] | np.ndarray)-> np.ndarray:
    return np.array(signal)

options = {
    settings.opera_amp[0]: amplitud_scaling,
    settings.opera_amp[1]: amplitud_log,
    settings.opera_amp[2]: amplitud_exponential,
    settings.opera_amp[3]: amplitud_inversion,
    settings.opera_amp[4]: amplitud_power,
    settings.opera_amp[5]: amplitud_none
}

def resample_and_align(y1, fs1, y2, fs2):
    if fs1 >= fs2:
        fs_target = fs1
    else:
        fs_target = fs2
    fs_target = abs(simpledialog.askinteger("Warning", "Frequency value:", initialvalue=fs_target))
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
    

def amplitud_selector(name: str, signal: list[float] | np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y = options[name](signal)
    y = verification(y)
    return y