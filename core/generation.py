import numpy as np
from core import settings

def signal_impulse(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    y = np.zeros_like(n, dtype=float)
    y[0] = gain
    return n, y

def signal_step(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    y = np.ones_like(n, dtype=float) * gain
    return n, y

def signal_ramp(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    y = gain * n
    return n, y

def signal_triangular(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    period = int(fs / freq)
    y = gain * 2 * np.abs(2 * (n / period - np.floor(n / period + 0.5)))
    return n, y

def signal_sawtooth(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    period = int(fs / freq)
    y = gain * 2 * ((n / period) - np.floor(0.5 + n / period))
    return n, y

def signal_sine(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    t = n / fs
    y = gain * np.sin(2 * np.pi * freq * t)
    return n, y

def signal_cosine(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    t = n / fs
    y = gain * np.cos(2 * np.pi * freq * t)
    return n, y

def signal_sinc(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(-fs * duration / 2), int(fs * duration / 2))
    t = n / fs
    y = gain * np.sinc(2 * freq * t)
    return n, y

def signal_chirp(freq: float, fs: int, gain: float, duration: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(int(fs * duration))
    t = n / fs
    y = gain * np.sin(2 * np.pi * freq * t ** 2)
    return n, y

options = {
    settings.signalSelector[0]: signal_impulse,
    settings.signalSelector[1]: signal_step,
    settings.signalSelector[2]: signal_ramp,
    settings.signalSelector[3]: signal_triangular,
    settings.signalSelector[4]: signal_sawtooth,
    settings.signalSelector[5]: signal_sine,
    settings.signalSelector[6]: signal_cosine,
    settings.signalSelector[7]: signal_sinc,
    settings.signalSelector[8]: signal_chirp
}


def signal_selector(
    name: str,
    freq: float = 1000,
    fs: int = 44100,
    gain: float = 1.0,
    duration: float = 1.0) -> tuple[np.ndarray, np.ndarray]:

    n, y = options[name](freq, fs, gain, duration)

    if np.isinf(y).any():
        print("Advertencia: Hay valores infinitos en la señal.")
    if np.isnan(y).any():
        print("Advertencia: Hay valores NaN en la señal.")

    return n, y
