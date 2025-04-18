import numpy as np
from tkinter import simpledialog, messagebox
from core import settings

def signal_impulse(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(n0, n0 + int(fs * duration))
    y = np.zeros_like(n)
    y[n == shift] = gain
    return n, y

def signal_step(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(n0, n0 + int(fs * duration))
    y = np.zeros_like(n) 
    y[n >= shift] = gain 
    return n, y

def signal_ramp(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(n0, n0 + int(fs * duration))
    y = np.zeros_like(n) 
    y[n >= shift] = gain*(n[n >= shift]-shift) 
    return n, y

def signal_triangular(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(n0, n0 + int(fs * duration))
    period = int(fs / fa)
    y = gain * 2 * np.abs(2 * (n / period - np.floor(n / period + 0.5)))
    return n, y

def signal_sawtooth(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(n0, n0 + int(fs * duration))
    period = int(fs / fa)
    y = gain * 2 * ((n / period) - np.floor(0.5 + n / period))
    return n, y

def signal_sine(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    An = simpledialog.askfloat  ("Fase (Rad)",      "valor:", initialvalue=0  )
    n = np.arange(n0, n0 + int(fs * duration))
    g = 2 * np.pi * fa * (n + shift) / fs
    y = gain * np.sin(g + An)
    return n, y

def signal_cosine(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    An = simpledialog.askfloat  ("Fase (Rad)",      "valor:", initialvalue=0  )
    n = np.arange(n0, n0 + int(fs * duration))
    g = 2 * np.pi * fa * (n + shift) / fs
    y = gain * np.cos(g + An)
    return n, y

def signal_sinc(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    An = simpledialog.askfloat  ("Fase (Rad)",      "valor:", initialvalue=0  )
    n = np.arange(n0, n0 + int(fs * duration))
    g = 2 * np.pi * fa * (n + shift) / fs
    y = gain * np.sinc(g + An)
    return n, y

def signal_chirp(fa, fs, gain, n0, duration, shift) -> tuple[np.ndarray, np.ndarray]:
    n = np.arange(n0, n0 + int(fs * duration))
    K  = simpledialog.askfloat  ("Factor de escala","valor:", initialvalue=0.01)
    An = simpledialog.askfloat  ("Fase (Rad)",      "valor:", initialvalue=0  )
    indx = simpledialog.askinteger("Selección de Operación", "\n1Chirp Lineal\n2Chirp Expo",initialvalue=1, minvalue=1, maxvalue=2)
    if indx == 1:
        phase = K*(n**2 + shift)/fs +  2 * np.pi * fa
        y = gain * np.sin(phase + An)
    else:
        while True:
            B  = simpledialog.askfloat("Base Real",      "valor:", initialvalue=0.9)
            if B <= 0:
                messagebox.showwarning("Error", "Debe ingresar un valor real mayor a 0.")
                continue
            break
        phase =  K* B**(n + shift) / fs + 2 * np.pi * fa
        y = gain * np.sin(phase + An)

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
    fa: float,
    fs: int,
    gain: float,
    n0: int,
    duration: float,
    shift: float) -> tuple[np.ndarray, np.ndarray]:



    n, y = options[name](fa, fs, gain, n0, duration, shift)

    if np.isinf(y).any():
        print("Advertencia: Hay valores infinitos en la señal.")
    if np.isnan(y).any():
        print("Advertencia: Hay valores NaN en la señal.")

    return n, y
