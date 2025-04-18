import numpy as np
from tkinter import simpledialog
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

def amplitud_selector(
        name: str, 
        signal: list[float] | np.ndarray,)-> np.ndarray:
    
    y = options[name](signal)
    if np.isinf(y).any():
        print("Advertencia", "Verificar: Algún Resultado es Infinito")
    if np.isnan(y).any():
        print("Advertencia", "Verificar: Algún Resultado es NAN")  

    return y