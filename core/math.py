import numpy as np
import tkinter as tk
from tkinter import messagebox
from core import settings
from core.plotter import Plotter, ProcessedSignalPlot
from core.signal_utils import resample_and_align

processed_plot = ProcessedSignalPlot()

def basic_operations(action: str, y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int):
    actions = {
        settings.basic_operation[0]: addition,
        settings.basic_operation[1]: subtraction,
        settings.basic_operation[2]: multiply,
        settings.basic_operation[3]: division,
        settings.basic_operation[4]: power
    }
    result, freq = actions[action](y1, fs1, y2, fs2)

    return result, freq

def addition(y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int)-> np.ndarray: 
    y1_align, y2_align, freq = resample_and_align(y1, fs1, y2, fs2)
    result = y1_align + y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result, freq)
    return result, freq

def subtraction(y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int)-> np.ndarray: 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1_align - y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result, freq)
    return result, freq

def multiply(y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int)-> np.ndarray: 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1_align * y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result, freq)
    return result, freq

def division(y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int)-> np.ndarray: 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1_align / y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result, freq)
    return result, freq

def power(y1: list[float] | np.ndarray, fs1:int, y2: list[float] | np.ndarray, fs2:int)-> np.ndarray: 
    y1_align, y2_align, freq =resample_and_align(y1, fs1, y2, fs2)
    result = y1_align ** y2_align
    n = np.arange(len(result)) / freq
    generate_result(n, result, freq)
    return result, freq

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

def processing_filtering():
    pass

def signal_to_signal_processing():
    pass

def fourier_t():
    pass

def cosine_t():
    pass

def wavelet_t():
    pass

def generate_result(n, y, fs):
    root = tk.Tk()
    root.withdraw()
    try:
        processed_plot.show(root, n, y, fs)
    except:
        messagebox.showwarning("Warning", "Signal first...")