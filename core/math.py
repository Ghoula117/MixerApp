import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog
from core import settings
from core.plotter import ProcessedSignalPlot
from core.signal_utils import resample_signal, signals_padding

processed_plot = ProcessedSignalPlot()

def basic_operations(action: str, y1: list[float] | np.ndarray, fs1:int, n01:float, y2: list[float] | np.ndarray, fs2:int, n02:float)-> np.ndarray: 
    actions = {
        settings.basic_operation[0]: addition,
        settings.basic_operation[1]: subtraction,
        settings.basic_operation[2]: multiply,
        settings.basic_operation[3]: division,
        settings.basic_operation[4]: power,
    }
    n, result, freq = actions[action](y1, fs1, n01, y2, fs2, n02)

    return n, result, freq

def addition(y1, fs1, n01, y2, fs2, n02):
    y1_resampled, y2_resampled, freq = resample_signal(y1, fs1, y2, fs2)
    n, y1_pad, y2_pad = signals_padding(y1_resampled, n01, y2_resampled, n02, freq)
    result = y1_pad + y2_pad

    generate_result(n, result)
    return n, result, freq

def subtraction(y1, fs1, n01, y2, fs2, n02):
    y1_resampled, y2_resampled, freq = resample_signal(y1, fs1, y2, fs2)
    n, y1_pad, y2_pad = signals_padding(y1_resampled, n01, y2_resampled, n02, freq)
    result = y1_pad - y2_pad

    generate_result(n, result)
    return n, result, freq

def multiply(y1, fs1, n01, y2, fs2, n02):
    y1_resampled, y2_resampled, freq = resample_signal(y1, fs1, y2, fs2)
    n, y1_pad, y2_pad = signals_padding(y1_resampled, n01, y2_resampled, n02, freq)
    result = y1_pad * y2_pad

    generate_result(n, result)
    return n, result, freq

def division(y1, fs1, n01, y2, fs2, n02):
    y1_resampled, y2_resampled, freq = resample_signal(y1, fs1, y2, fs2)
    n, y1_pad, y2_pad = signals_padding(y1_resampled, n01, y2_resampled, n02, freq)
    result = y1_pad / y2_pad

    generate_result(n, result)
    return n, result, freq

def power(y1, fs1, n01, y2, fs2, n02):
    y1_resampled, y2_resampled, freq = resample_signal(y1, fs1, y2, fs2)
    n, y1_pad, y2_pad = signals_padding(y1_resampled, n01, y2_resampled, n02, freq)
    result = y1_pad ** y2_pad

    generate_result(n, result)
    return n, result, freq

def preprocessing_operations(action: str, y: list[float] | np.ndarray):
    actions = {
        settings.preprocessing_operation[0]: min_max_normalization,
        settings.preprocessing_operation[1]: signed,
        settings.preprocessing_operation[2]: standard_normalization,
        settings.preprocessing_operation[3]: operation_none
    }
    y = actions[action](y)
    return y

def min_max_normalization(y):
    return (y - np.min(y)) / (np.max(y) - np.min(y))

def signed(y):
    return y / np.max(np.abs(y))

def standard_normalization(y):
    return (y - np.mean(y)) / np.std(y)

def operation_none(y):
    return np.array(y)

def filtering_operation(action:str, x:list[float] | np.ndarray, h: list[float] | np.ndarray, ax, bx)-> np.ndarray:
    actions = {
        settings.filter_type[0]: FIR_FILTER,
        settings.filter_type[1]: IIR_FILTER
    }
    n, result = actions[action](x, h, ax, bx)

    return n, result

def FIR_FILTER(x, h, ax, bx):
    Lx = len(x)
    Lh = len(h)

    indx = simpledialog.askinteger("Convolution method", "\n1 y1(n)*y2(n) \n2. Block", minvalue=1, maxvalue=2, initialvalue=1)
    xi = simpledialog.askinteger("Initial value of x", "value:", initialvalue=0)
    xf = simpledialog.askinteger("Final value of x", "value:",   initialvalue=1)
    hi = simpledialog.askinteger("Initial value of h", "value:", initialvalue=0)
    hf = simpledialog.askinteger("Final value of h", "value:",   initialvalue=1)

    Ly = Lx + Lh - 1
    yi = xi + hi
    yf = xf + hf

    """for n in range(Ly): 
        for k in range(Lh): 
            if 0 <= n - k < Lx:
                y[n] += x[k] * h[n - k]"""

    y = np.convolve(x, h)
    n = np.linspace(yi, yf, Ly)
    generate_result(n, y)

    return n, y

def IIR_FILTER(x, h, ax, bx):
    n = 0
    y = 0
    return n, y

def signal_to_signal_processing():
    pass

def fourier_t():
    pass

def cosine_t():
    pass

def wavelet_t():
    pass

def generate_result(n, y):
    root = tk.Tk()
    root.withdraw()
    try:
        processed_plot.show(root, n, y)
    except:
        messagebox.showwarning("Warning", "Signal first...")