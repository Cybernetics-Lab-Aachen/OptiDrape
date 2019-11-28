


import os, sys

import openmesh
import random
from Data.drape_object import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from Data.import_cad import create_drape_mesh_object
import pylab

from mpl_toolkits.mplot3d import Axes3D

from mytest.gaussian_curvature import surface_curvature
import scipy
import numpy as np
import qimage2ndarray

from Data.import_cad import *

from Data.data_extraction import load_and_extract_data_from_simulation

import openmesh, pickle

from Data.drape_object import DrapeTriMesh


app = QApplication(sys.argv)

mainWin = QMainWindow(flags=Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)


ori_pos = DrapeTriMesh(name="p4035_pos", auto_face_generation="True")

create_drape_mesh_object("/home/optidrape/Desktop/OptiDrape/gui/Pyramidenstumpf_P40_35_B412C.obj", ori_pos)

ori_pos.generate_vertex_color_of_z_coordinate()

ori_z_projection = ori_pos.create_xy_normalized_projection()


node_expected = pickle.load(open('./node_expected_useful.p', "rb"))

print(node_expected)

for vh in ori_pos.vertices():
    if vh.idx() in node_expected:
        _point = ori_pos.point(vh)
        ori_pos.set_point(vh, openmesh.Vec3d(_point[0]- np.random.random_sample() * 0, _point[1]- np.random.random_sample() * 0, _point[2] - np.random.random_sample() * 2))





ori_pos.update_viewer()

mainWin.setCentralWidget(ori_pos.viewer)
mainWin.show()




#print(pyramidenstumpf_p40_35_negative_point_with_id_dict)

#print(pyramidenstumpf_p40_35_positiv_point_with_id_dict)


openmesh.write_mesh(ori_pos, "./Pyramidenstumpf_P40_35_B412C.obj")

#with open("./test6.xyz", 'a') as f:
#    for _id in sorted(pyramidenstumpf_p40_35_positiv_point_with_id_dict, key=lambda t: int(t)):#

#        s = "%s %s %s\n" % (str(pyramidenstumpf_p40_35_positiv_point_with_id_dict[_id][0]),
#                          str(pyramidenstumpf_p40_35_positiv_point_with_id_dict[_id][2]),
#                          str(pyramidenstumpf_p40_35_positiv_point_with_id_dict[_id][1]))
#        f.writelines(s)



#key_sorted = sorted(pyramidenstumpf_p40_35_negative_point_with_id_dict, key=lambda t: int(t))

app.exec_()




"""
from collections import OrderedDict




dict_sorted = OrderedDict()

vertex_list = []
for key in key_sorted:
    dict_sorted.update({key: pyramidenstumpf_p40_35_negative_point_with_id_dict[key]})
    vertex_list.append([pyramidenstumpf_p40_35_negative_point_with_id_dict[key][0],
                        pyramidenstumpf_p40_35_negative_point_with_id_dict[key][2],
                        pyramidenstumpf_p40_35_negative_point_with_id_dict[key][1]])

vertex_list = np.array(vertex_list)

x_vec = vertex_list[:, 0]
y_vec = vertex_list[:, 1]
z_vec = vertex_list[:, 2]
print(vertex_list)

print(x_vec)
print(y_vec)
print(z_vec)"""










