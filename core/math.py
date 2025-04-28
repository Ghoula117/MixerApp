import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog
from core import settings
from core.plotter import ProcessedSignalPlot
from core.signal_utils import resample_and_align

processed_plot = ProcessedSignalPlot()

def addition(y1, fs1, y2, fs2): 
    #y1_align, y2_align, freq = resample_and_align(y1, fs1, y2, fs2)
    result = y1 + y2
    n = np.arange(len(result))
    generate_result(n, result)
    return result

def subtraction(y1, fs1, y2, fs2): 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1- y2
    n = np.arange(len(result)) / freq
    generate_result(n, result)
    return result

def multiply(y1, fs1, y2, fs2): 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1* y2
    n = np.arange(len(result))
    generate_result(n, result)
    return result

def division(y1, fs1, y2, fs2): 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1_align / y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result)
    return result

def power(y1, fs1, y2, fs2): 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1_align ** y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result)
    return result

def basic_operations(action: str, y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int)-> np.ndarray: 
    actions = {
        settings.basic_operation[0]: addition,
        settings.basic_operation[1]: subtraction,
        settings.basic_operation[2]: multiply,
        settings.basic_operation[3]: division,
        settings.basic_operation[4]: power
    }
    result = actions[action](y1, fs1, y2, fs2)

    return result

def preprocessing_operations(action: str, y: list[float] | np.ndarray):
    actions = {
        settings.preprocessing_operation[0]: min_max_normalization,
        settings.preprocessing_operation[1]: signed,
        settings.preprocessing_operation[2]: standard_normalization,
        settings.preprocessing_operation[3]: operation_none
    }
    y = actions[action](y)
    return y

def min_max_normalization(y: list[float] | np.ndarray)-> np.ndarray: 
    return (y - np.min(y)) / (np.max(y) - np.min(y))

def signed(y: list[float] | np.ndarray)-> np.ndarray: 
    return y / np.max(np.abs(y))

def standard_normalization(y: list[float] | np.ndarray)-> np.ndarray: 
    return (y - np.mean(y)) / np.std(y)

def operation_none(y: list[float] | np.ndarray)-> np.ndarray:
    return np.array(y)

def processing_filtering(action:str, x:list[float] | np.ndarray, h: list[float] | np.ndarray, ax, bx):
    actions = {
        settings.filter_type[0]: FIR_FILTER,
        settings.filter_type[1]: IIR_FILTER
    }
    y = actions[action](x, h, ax, bx)
    return y

def FIR_FILTER(x, h)-> np.ndarray:
    Lx = len(x)
    Lh = len(h)

    xi = simpledialog.askinteger("Initial value of x", "value:", initialvalue=0)
    xf = simpledialog.askinteger("Final value of x", "value:",   initialvalue=0)
    hi = simpledialog.askinteger("Initial value of h", "value:", initialvalue=0)
    hf = simpledialog.askinteger("Final value of h", "value:",   initialvalue=0)

    Ly = Lx + Lh - 1
    yi = xi + hi
    yf = xf + hf

    y = np.zeros(Ly)

    for n in range(Ly): 
        for k in range(Lh): 
            if 0 <= n - k < Lx:
                y[n] += x[k] * h[n - k]

    n = np.linspace(yi, yf, Ly)
    generate_result(n, y)

    return y

def IIR_FILTER():
    pass

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