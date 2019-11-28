
import os, sys

import openmesh

from Data.drape_object import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

import pylab

from mpl_toolkits.mplot3d import Axes3D

from mytest.gaussian_curvature import surface_curvature
import scipy

import qimage2ndarray

from Data.import_cad import *


app = QApplication(sys.argv)

mainWin = QMainWindow(flags=Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)


test = DrapeTriMesh(name="mytest", has_face=True)

create_drape_mesh_object(mesh_path="/home/optidrape/Desktop/cloud_reformed_2.ply", mesh_obj=test)

test.mesh_option_request()

test.create_xy_projection_muster()

test.generate_vertex_color_of_z_coordinate()


x = []
y = []
z = []

for _vh in test.vertices():
    _point = test.point(_vh)
    x.append(_point[0])
    y.append(_point[0])
    z.append(_point[0])

x = np.array(x)
y = np.array(y)
z = np.array(z)

P = np.stack((x, y), axis=-1)


grid_x, grid_y = np.mgrid[-700:700:1000j, -700:700:1000j]


from scipy.interpolate import griddata

test.viewer.meshViewer.update_viewer()

#grid_z0 = griddata(P, z, (grid_x, grid_y), method='nearest')

#tmp = surface_curvature(grid_x, grid_y, grid_z0)
#print ("maximum curvatures: ", tmp[0])
#print ("minimum curvatures", tmp[1])
#fig = pylab.figure()
#ax = Axes3D(fig)

#ax.plot_surface(grid_x, grid_y, grid_z0)
#pylab.show()
mainWin.setCentralWidget(test.viewer)
mainWin.show()


app.exec_()
