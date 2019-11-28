

from scipy import interpolate, misc

import numpy as np
#import cv2
import itertools
import qimage2ndarray
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


app = QApplication(sys.argv)
import pickle
from pprint import pprint
tmp = pickle.load(open('./tmp_tmp.p', 'rb'))

width = tmp['width']

z_matrix = tmp['z_matrix']

node_matrix = tmp['node_matrix']

length = tmp['length']

z_matrix[40, 50] = 5000

_z_qimage = qimage2ndarray.gray2qimage(gray=z_matrix)


main_win = QMainWindow()


image_label = QLabel()
image_label.setPixmap(QPixmap.fromImage(_z_qimage).scaled(QSize(int(length), int(width + 0.5)), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
image_label.setAlignment(Qt.AlignCenter)
#main_win.setCentralWidget(image_label)
image_label.show()
#main_win.show()

_z_qimage2 = _z_qimage.scaled(QSize(int(length), int(width + 0.5)), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
image_label_scaled = QLabel()

print( length / z_matrix.shape[1])
print( width / z_matrix.shape[0])

test_pixmap = QImage()


_z_normalized = np.zeros((1400, 1400))

np.set_printoptions(precision=2, linewidth=150)
pprint(z_matrix, width=8000)

#_arr_normalized = qimage2ndarray.g(_z_qimage)

print(_z_qimage2.height(), _z_qimage2.width())
z_matrix_normalized = np.zeros((_z_qimage2.height(), _z_qimage2.width()))

for i, j in itertools.product(range(_z_qimage2.height()), range(_z_qimage2.width())):
    z_matrix_normalized[i, j] = qGray(_z_qimage2.pixel(j, i))

pprint(z_matrix_normalized.shape, width=8000)

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
    return vector



_z_matrix_padded = np.pad(z_matrix_normalized, ((701 - 116, 701 - 118), (699 - 118, 699 - 116)), 'edge')

print(_z_matrix_padded.shape)

image_label_padded = QLabel()
image_label_padded.setPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(_z_matrix_padded)))
image_label_padded.setAlignment(Qt.AlignCenter)
#main_win.setCentralWidget(image_label)
image_label_padded.show()




image_label_scaled.setPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(z_matrix_normalized)))
image_label_scaled.setAlignment(Qt.AlignCenter)

image_label_scaled.show()


app.exec()






