

import openmesh, sys
from PyQt5.QtWidgets import *
from gui.viewer.drape_viewer import MeshViewerWidgetT


_this_mesh = openmesh.TriMesh()

openmesh.read_mesh(_this_mesh, "/home/haoming/Desktop/mytest.obj")

print(_this_mesh.n_faces())

print(_this_mesh.n_vertices())


app = QApplication(sys.argv)

opt = openmesh.Options()


opt += openmesh.Options.FaceNormal
opt += openmesh.Options.VertexNormal
opt += openmesh.Options.VertexTexCoord
opt += openmesh.Options.FaceTexCoord

_this_mesh.request_face_colors()
_this_mesh.request_face_normals()
_this_mesh.request_vertex_colors()
_this_mesh.request_vertex_normals()


_this_viewer = MeshViewerWidgetT()

_this_viewer.set_mesh(_this_mesh, opt)

_this_viewer.show()

sys.exit(app.exec_())