

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np


def null_func(data):
    return 0.


def fit_data(x, y, deg=5):
    if len(x) != len(y):
        raise ValueError
    if (x and y) or (len(x) > 1 and len(y) > 1):
        return np.polyfit(x, y, deg)
    else:
        return None


def fitted_data_func(coeff):
    if coeff is not None:
        return np.poly1d(coeff)
    else:
        return null_func
