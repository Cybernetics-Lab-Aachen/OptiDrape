
import os, sys
import openmesh
from Data.drape_object import DrapeTriMesh
#from Data.drape_object import DEFAULT_MESH_OPTION

def create_drape_mesh_object(mesh_path, mesh_obj):
    DEFAULT_MESH_OPTION = openmesh.Options()
    DEFAULT_MESH_OPTION += openmesh.Options.FaceNormal
    DEFAULT_MESH_OPTION += openmesh.Options.VertexNormal
    DEFAULT_MESH_OPTION += openmesh.Options.FaceColor
    DEFAULT_MESH_OPTION += openmesh.Options.VertexColor
    DEFAULT_MESH_OPTION += openmesh.Options.VertexTexCoord
    DEFAULT_MESH_OPTION += openmesh.Options.FaceTexCoord

    mesh_obj.mesh_option_request()
    openmesh.read_mesh(mesh_obj, mesh_path, DEFAULT_MESH_OPTION)
    mesh_obj.update_normals()


