from collections import OrderedDict
import copy, os
import numpy as np
import openmesh
from scipy import spatial
import itertools

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QImage, qRgb, qRgba, qRgba64

import qimage2ndarray

from gui.viewer.drape_viewer import MeshViewer, GeometryViewer, MeshViewerWidgetLite
from Data.gaussian_curvature import surface_curvature
from Data.drape_utils import *
import tqdm

import threading, pickle

from matplotlib import cm
from matplotlib.colors import Normalize as color_norm
from pprint import pprint

DEFAULT_MESH_OPTION = openmesh.Options()
DEFAULT_MESH_OPTION += openmesh.Options.FaceNormal
DEFAULT_MESH_OPTION += openmesh.Options.VertexNormal
DEFAULT_MESH_OPTION += openmesh.Options.FaceColor
DEFAULT_MESH_OPTION += openmesh.Options.VertexColor
DEFAULT_MESH_OPTION += openmesh.Options.VertexTexCoord
DEFAULT_MESH_OPTION += openmesh.Options.FaceTexCoord


class DrapeObjectT(object):
    def __init__(self, name):
        super().__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name


class DrapeTextile(DrapeObjectT):
    def __init__(self, name):
        super(DrapeTextile, self).__init__(name)


class OptiDrapeGeometry(DrapeObjectT):
    def __init__(self, mesh_path, mesh_name_list,
                 mesh_required=('simulation_end', 'original'),
                 viewer_parent=None, auto_build=False):
        super(OptiDrapeGeometry, self).__init__(name=mesh_name_list[0] + '.' + mesh_name_list[1])
        self._drape_geometry_is_full = False
        self._meshes = dict()
        self._mesh_required = mesh_required
        self._face_data = {}
        self._mesh_path = mesh_path
        self._mesh_name_list = mesh_name_list
        self._mutex = threading.RLock()
        self.geometry_viewer = GeometryViewer(name=self.name, parent=viewer_parent)
        self.geo = {}
        if auto_build:
            self.build_meshes()

    def hide_viewer(self):
        self.geometry_viewer.hide()

    def show_viewer(self):
        self.geometry_viewer.show()

    def set_mesh(self, mesh_name, trimesh):
        if mesh_name in self._meshes.keys():
            print("DrapeGeometry: mesh name %s already in meshes, it will be updated!" % mesh_name)
        self._meshes.update({mesh_name: trimesh})
        trimesh.update_viewer()
        # todo: update geometry viewer with new tab, mytest it!!!
        self.geometry_viewer.update_drape_viewer_tab(mesh_name=mesh_name, mesh_viewer=trimesh.viewer)

    def check_mesh_completion(self):
        """
        :return: 2 returns: bool, list. Bool if true then this geometry is complete, list of mesh name which is short of
        """
        _lacked_mesh = []
        _mesh_complete = True
        for key in self._mesh_required:
            if not key in self._meshes.keys():
                _lacked_mesh.append(key)
                _mesh_complete = False
        return _mesh_complete, _lacked_mesh

    @staticmethod
    def _build_mesh_thread(name, target, args):

        _thread = threading.Thread(name=name,
                                   target=target,
                                   args=args)
        _thread.setDaemon(True)
        _thread.start()

    def _get_binary_data_path(self):
        _geo_path = _sim_path = None
        if self._mesh_path:
            _geo_path = self._mesh_path + '/geometry/' + self._mesh_name_list[1] + '.pickle'
            _sim_path = self._mesh_path + '/label/' + self._mesh_name_list[1] + '.pickle'

            if not os.path.isfile(_geo_path):
                print("DrapeGeometry: File %s does not exist!" % _geo_path)
                _geo_path = None

            if not os.path.isfile(_sim_path):
                print("DrapeGeometry: File %s does not exist!" % _sim_path)
                _sim_path = None
        else:
            print("DrapeGeometry: No mesh path defined!")
        return _geo_path, _sim_path

    def build_meshes(self):
        # This function builds two meshes here:
        # 1. original mesh of the active press form
        # 2. textile form after simulation
        """
        :return: updatet mesh_dict, we want to update the vertex id in the database
        """

        # this function is used for build mesh from binary
        _geo_path, _sim_path = self._get_binary_data_path()

        if not (_geo_path and _sim_path):
            print("Build Meshes: Invalid paths given!")
            return

        # if it is the mesh from simulation, then we can generate two meshes.
        # The generation process should be split in sub threads
        _mesh_origin = DrapeTriMesh(name=self.name+'_origin', viewer_parent=self.geometry_viewer,
                                    has_face=False, has_shear_angle=True, auto_face_generation=False,
                                    is_original_mesh=True
                                    )


        self.set_mesh('origin', _mesh_origin)

        _mesh_sim = DrapeTriMesh(name=self.name+'_sim', viewer_parent=self.geometry_viewer,
                                 has_face=False, has_shear_angle=True, auto_face_generation=True)
        self.set_mesh('simulation', _mesh_sim)

        def mesh_processing():
            _mesh_origin.add_vertex_from_binary(data_path=_geo_path, processbar_cb=self.geometry_viewer.update_progress,
                                                is_origin=True)


            openmesh.write_mesh(_mesh_origin, "./origin_mesh.obj")
           # print("wrote origin")
            _mesh_sim.add_vertex_from_binary(data_path=_sim_path, processbar_cb=self.geometry_viewer.update_progress)
            openmesh.write_mesh(_mesh_sim, "./sim_mesh.obj")

           # print("wrote sim")
            _mesh_origin.generate_vertex_color_of_z_coordinate()
            #_mesh_origin.viewer.show()
            #_mesh_sim.viewer.show()

        self._build_mesh_thread(name=self.name, target=mesh_processing, args=())

    @property
    def meshes(self):
        return self._meshes

    @property
    def mutex(self):
        return self._mutex


class DrapeTriMesh(openmesh.TriMesh, DrapeObjectT):
    # This class just expands the Trimesh object for customize functions

    class ViewerUpdateSignal(QObject):
        signal = pyqtSignal()

    def __init__(self, name, parent_geometry=None,
                 has_face=False,
                 has_shear_angle=False,
                 has_thinning=False,
                 shear_angle_colored=True,
                 color_map_name='jet',
                 related_mesh=None,
                 auto_face_generation=False,
                 face_generator="structure",
                 option=None,
                 viewer_parent=None,
                 is_original_mesh=False):
        openmesh.TriMesh.__init__(self)
        DrapeObjectT.__init__(self, name=name)
        self._parent_geometry = parent_geometry
        self._has_face = has_face
        self._vertex_dict = OrderedDict()
        self._face_vertex_dict = OrderedDict()
        self._has_shear_angle=has_shear_angle
        self._has_thinning = has_thinning
        self._related_mesh=related_mesh
        self._auto_face_generation = auto_face_generation
        self._face_generator = face_generator
        self._is_shear_angle_colored = shear_angle_colored
        self._is_original_mesh = is_original_mesh
        self._is_vertex_color_z_generated  = False
        if not has_shear_angle:
            self._is_shear_angle_colored = False

        self._shear_angle_colormap = cm.get_cmap(name=color_map_name)

        self._vertex_property_origin_id_handle = openmesh.VPropHandle()
        self._vertex_property_shear_angle_handle = openmesh.VPropHandle()
        self._vertex_property_thinning_handle = openmesh.VPropHandle()
        self._projection_muster = []
        self._z_coordinate_colormap = []  # with the order of vertex index

        if option:
            self._option = option
        else:
            self._option = DEFAULT_MESH_OPTION

        self.viewer = MeshViewerWidgetLite(mesh=self, parent=viewer_parent)

        self._update_viewer_signal = self.ViewerUpdateSignal()
        self._update_viewer_signal.signal.connect(self.update_viewer)
        self._is_viewer_updated = False

        self.mesh_option_request()

        # mesh processing information


    def mesh_option_request(self):
        if self._option.check(openmesh.Options.FaceNormal):
            self.request_face_normals()

        if self._option.check(openmesh.Options.VertexNormal):
            self.request_vertex_normals()

        if self._option.check(openmesh.Options.VertexColor):
            self.request_vertex_colors()

        if self._option.check(openmesh.Options.FaceColor):
            self.request_face_colors()

        if self._option.check(openmesh.Options.VertexTexCoord):
            self.request_vertex_texcoords2D()

        if self._option.check(openmesh.Options.FaceTexCoord):
            self.request_face_texture_index()

    def get_mesh_info(self):
        return {'nv': self.n_vertices(),
                'ne': self.n_edges(),
                'nf': self.n_faces()}

    def option(self):
        return self._option

    def update_viewer(self):
        self.viewer.update_viewer()
        self._is_viewer_updated = True
        if self._is_original_mesh and not self._is_vertex_color_z_generated and self.n_vertices():
           # print("request color")
            self.generate_vertex_color_of_z_coordinate()
            self._is_vertex_color_z_generated = True

    @property
    def xy_matrix(self):
        return self._projection_muster

    def create_xy_projection_muster(self, is_square=True, scale=False, cheat=False):
        # this function creates the xy projection muster and hash the pixels to vertex
        # This must be done for the EA, because the fitness function uses the xy projection to calculate the score
        # to do so,
        # 1. the vertexes of the geometry must be homogeneous -> have same distance of x, y coordinates
        # 2. the whole geometry must be normalized to 1400 x 1400 mm
        #    if the width and length are smaller than 1400 mm, then padding
        #    if one of the width and length are bigger than 1400 mm, then to 1400mm scale, note that this is only used
        #    for fitness function, for the constraints we should not scale

        # Because we already extract the vertexes in np object by updating the viewer, then we just get them from it


        ## Requirements to run this function:
        ## 1. the geometry must be padded as a square

        if not self._is_viewer_updated:
            self.update_viewer()
        _vertexes = self.viewer.vertex_in_np.tolist()
        if not is_square:
            # here to pad the geometry as a square
            # TODO: to be done
            pass
        _faces = self.viewer.face_vertex_idx_in_np.tolist()

        rel_dist = [p[0] + p[1] for p in _vertexes]

        _first_vertex_id = np.argmin(rel_dist, axis=0)
        _last_vertex_id = np.argmax(rel_dist, axis=0)

        #print(_first_vertex_id, _last_vertex_id)
        _first_vertex_coordinate = _vertexes[_first_vertex_id]
        _last_vertex_coordinate = _vertexes[_last_vertex_id]

        _face_vertex_map_even = []
        _face_vertex_map_odd = []
        for i, m in enumerate(_faces):
            if i % 2:
                _face_vertex_map_even.append(m)
            else:
                _face_vertex_map_odd.append(m)
        # and now we could generate the projection matrix according to the face vertex map

        #print(len(_face_vertex_map_even), len(_face_vertex_map_odd))

        _num_vertex_per_row = _face_vertex_map_even[0][2] - _face_vertex_map_even[0][0]
        poly_face = []
        for i in range(len(_face_vertex_map_even)):
            _tmp = _face_vertex_map_even[i]
            _tmp.pop(0)
            _tmp.reverse()
            poly_face.append(_face_vertex_map_odd[i][0:2] + _tmp)
        _row = []
        _tmp_matrix = []
        for i in range(len(_face_vertex_map_even)):
            if i > 0 and i % (_num_vertex_per_row - 1) == 0:
                _tmp_matrix.append(_row)
                _row = []
            _row.append(poly_face[i])
        #_tmp_matrix.append(_row)
        _matrix = []
        _row_2 = []

        #print(_tmp_matrix)

        for k, vertex in enumerate(_tmp_matrix):
            _row_1 = []
            _row_2 = []
            for i in range(vertex.__len__()):
                if i < vertex.__len__() - 1:
                    _row_1.append(vertex[i][0])
                    _row_2.append(vertex[i][2])
                else:
                    _row_1.append(vertex[i][0])
                    _row_1.append(vertex[i][1])
                    _row_2.append(vertex[i][2])
                    _row_2.append(vertex[i][3])
            if k % 2 == 0:
                _matrix.append(_row_1)
                _matrix.append(_row_2)
       # if _row_2:
           # _matrix.append(_row_2)

        self._projection_muster = np.array(_matrix)

        if cheat:
            self._projection_muster = self._projection_muster[:, 0:self._projection_muster.shape[1]-1]

        def get_length_width(vec):
            # print(vec)
            # print(vec[0], vec[vec.size - 1])
            _first_point = self.point(self.vertex_handle(int(vec[0])))
            _last_point = self.point(self.vertex_handle(int(vec[vec.size - 1])))

            return spatial.distance.euclidean(list(_first_point),
                                              list(_last_point))

        self._projection_muster_length_in_mm = max(
            np.apply_along_axis(get_length_width, axis=1, arr=self._projection_muster))

        self._projection_muster_width_in_mm = max(np.apply_along_axis(get_length_width, axis=0, arr=self._projection_muster))

        #self._projection_muster_pro_vertext_length_in_mm = self._projection_muster_length_in_mm / (self._projection_muster.shape[1] - 1)
        #self._projection_muster_pro_vertex_width_in_mm = self._projection_muster_width_in_mm / (self._projection_muster.shape[0] - 1)

        #print(self._projection_muster.shape)
        #pprint(_matrix, width=800)
        #pprint(len(_matrix))

    def calc_gaussian_curvature(self):

        if self._projection_muster == []:
            self.create_xy_projection_muster(cheat=True)

        xy_matrix_x_coordinates = np.zeros(shape=self._projection_muster.shape, dtype=np.float32)
        xy_matrix_y_coordinates = np.zeros(shape=self._projection_muster.shape, dtype=np.float32)
        xy_matrix_z_coordinates = np.zeros(shape=self._projection_muster.shape, dtype=np.float32)

        for i, j in itertools.product(range(self._projection_muster.shape[0]), range(self._projection_muster.shape[1])):
            xy_matrix_x_coordinates[i, j] = self.point(self.vertex_handle(int(self._projection_muster[i, j])))[0]
            xy_matrix_y_coordinates[i, j] = self.point(self.vertex_handle(int(self._projection_muster[i, j])))[1]
            xy_matrix_z_coordinates[i, j] = self.point(self.vertex_handle(int(self._projection_muster[i, j])))[2]

        g_max, g_min = surface_curvature(xy_matrix_x_coordinates,
                                         xy_matrix_y_coordinates,
                                         xy_matrix_z_coordinates)

        k = np.multiply(g_max, g_min)

        k_sum = np.sum(k)
        k_abs_sum = np.sum(np.abs(k))

        return k_sum, k_abs_sum, k

    def calc_vertex_normal_angle(self, node_expected=None, plane_normal=np.array([0, 0, -1]), normalize=False):
        _vertex_angle = []
        if not node_expected:
            for vh in self.vertices():
                _vertex_angle.append(angle_between(v1=plane_normal,
                                                   v2=np.array([self.normal(vh)[i] for i in range(3)])))
        else:
            for v_id in node_expected:
                _vertex_angle.append(angle_between(v1=plane_normal,
                                                   v2=np.array([self.normal(self.vertex_handle(int(v_id)))[i] for i in range(3)])))
        _vertex_angle = np.asarray(_vertex_angle)
        if normalize:
            _vertex_angle_norm = _vertex_angle / _vertex_angle.max()
            _vertex_angle_norm /= _vertex_angle_norm.sum()

            return _vertex_angle_norm
        else:
            return _vertex_angle

    def generate_vertex_color_of_z_coordinate(self):
        # to set the constraints of the geometry, we need
        if not self._is_viewer_updated:
            self.update_viewer()

        #print(self.viewer.meshViewer.vertex_in_np.size)
        if not self.viewer.vertex_in_np.size:
            print("no vertex loaded")
           # return

        if len(self._z_coordinate_colormap):
            print("already done")
            return

        if self._is_original_mesh:
            #print("got here")
            _vertex_list = list(self._vertex_dict.values())
            _vertex_z = np.array(_vertex_list)
            _vertex_z = _vertex_z[:, 2]
        else:
            _vertex_z = self.viewer.vertex_in_np[:, 2]

        _color_norm = color_norm(vmin=_vertex_z.min(),
                                 vmax=_vertex_z.max())

        if not self.has_vertex_colors():
            self.request_vertex_colors()

        for _vh in self.vertices():
            _color = self._shear_angle_colormap(_color_norm(_vertex_z[_vh.idx()]))

            """
            if _vh.idx() > 4900:                                                                                                        
                self._z_coordinate_colormap.append([1,1,1,1])
                                                                                                                                                                                                                                                                                                                                                                                                self.set_color(_vh, openmesh.Vec4f(1,
                                                   1,
                                                   1,
                                                   1))
            
            else: """
            self._z_coordinate_colormap.append(_color)
            self.set_color(_vh, openmesh.Vec4f(_color[0],
                                               _color[1],
                                               _color[2],
                                               _color[3]))
        self.update_viewer()
        #self.viewer.update_mesh_info()

    def set_vertex_color_mono(self, vertex_list, color_in_list=openmesh.Vec4f(1, 1, 1, 1), color_out_list=None):
        for _vh in self.vertices():
            if _vh.idx() in vertex_list:
                self.set_color(_vh, color_in_list)
            elif color_out_list:
                try:
                    self.set_color(_vh, color_out_list)
                except:
                    pass
        self.update_viewer()

    def generate_xy_projection_image_from_z(self):
        _image_matrix = []
        if self._projection_muster == []:
            self.create_xy_projection_muster()

        if self._z_coordinate_colormap == []:
            self.generate_vertex_color_of_z_coordinate()

        for row_id in range(self._projection_muster.shape[0]):
            _this_row = []
            for col_id in range(self._projection_muster.shape[1]):
                _this_row.append(self._z_coordinate_colormap[self._projection_muster[row_id, col_id]])
            _image_matrix.append(_this_row)

        _image_matrix = np.array(_image_matrix)
        _qimage = qimage2ndarray.array2qimage(_image_matrix, normalize=True)

        return _qimage, _image_matrix

    def create_xy_normalized_projection(self, length=1400, width=1400):
        if not self._projection_muster:
            self.create_xy_projection_muster(cheat=True)

        # self._projection_muster_length_in_mm,   self._projection_muster_width_in_mm

        # self._projection_muster_pro_vertext_length_in_mm,  self._projection_muster_pro_vertex_width_in_mm

        _z_projection = np.zeros(self._projection_muster.shape)
        for i, j in itertools.product(range(self._projection_muster.shape[0]), range(self._projection_muster.shape[1])):
            _point = self.point(self.vertex_handle(int(self._projection_muster[i, j])))
            _z_projection[i, j] = _point[2]
        _z_qimage_scaled = qimage2ndarray.gray2qimage(gray=_z_projection).scaled(QSize(int(self._projection_muster_length_in_mm + 0.5),
                                                                                       int(self._projection_muster_width_in_mm + 0.5)),
                                                                                 Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        _z_scaled_matrix = np.zeros((_z_qimage_scaled.height(), _z_qimage_scaled.width()))
        for i, j in itertools.product(range(_z_qimage_scaled.height()), range(_z_qimage_scaled.width())):
            _z_scaled_matrix[i, j] = qGray(_z_qimage_scaled.pixel(j, i))

        _z_scaled_padded_matrix = np.pad(_z_scaled_matrix, ((int(width / 2) + 1 - int(_z_qimage_scaled.height() / 2), int(length / 2) + 1 - int(_z_qimage_scaled.width() / 2)),
                                                            (int(length / 2) - 1 - int(_z_qimage_scaled.width() / 2), int(width / 2) - 1 - int(_z_qimage_scaled.height() / 2))),
                                         'edge')
        return _z_scaled_padded_matrix

    def generate_faces_of_structure(self, processbar_cb=None):
        """
            Generate Faces with a fixed structure
            This may not work with other complex meshes
            The _vertex_dict must be ordered with the right geometry (x, y, z) Order!!!
        """
        if not self._has_face:
            _faces = []
            _vh_not_iterated = list(self._vertex_dict.keys())

            tt = 0
            _structure = []

            for vh in self._vertex_dict.keys():
                _vh_not_iterated.pop(_vh_not_iterated.index(vh))
                _neighbor_vhs_list = list()
                _neighbors_found = False
                _vh_not_iterated_calculate = copy.copy(_vh_not_iterated)
                while not _neighbors_found:
                    _min_distance = np.finfo(dtype=np.float64).max
                    _min_distance_vh = None

                    for _vh in _vh_not_iterated_calculate:
                        _tmp_point = self._vertex_dict[_vh]

                        _this_distance = spatial.distance.euclidean(self._vertex_dict[vh],
                                                                    _tmp_point)
                        if _this_distance < _min_distance:
                            _min_distance = _this_distance
                            _min_distance_vh = _vh

                    if _min_distance_vh:
                        # found a nearest point, then we need to validate that the vertex collected with
                        # current vertex are not already in a face
                        _vh_not_iterated_calculate.pop(_vh_not_iterated_calculate.index(_min_distance_vh))

                        if len(_faces) == 0:
                            _neighbor_vhs_list.append({_min_distance: _min_distance_vh})
                        else:
                            _point_unrelated = False
                            for face in _faces:
                                if _min_distance_vh in face:

                                    _point_unrelated = True

                                    break
                            if not _point_unrelated:

                                _neighbor_vhs_list.append({_min_distance: _min_distance_vh})

                    if len(_neighbor_vhs_list) == 3:
                        break

                _neighbors_idx_list = [list(f.values())[0].idx() for f in _neighbor_vhs_list]
                _structure = sorted(_neighbors_idx_list)
                break

            _vh = list(self._vertex_dict.keys())
            _n = self.n_vertices()
            _row_beginn_idx = 0

            with tqdm.tqdm(total= _n, desc="Generating Faces from Structure") as pbar:
                for i, vh in enumerate(_vh):
                    pbar.update()
                    try:
                        if vh.idx() != _row_beginn_idx + _structure[1] - 1:
                            _vh_list = [vh, _vh[_vh.index(vh) + _structure[1]], _vh[_vh.index(vh) + 1]]
                            self._face_vertex_dict.update({self.add_face(_vh_list): _vh_list})
                            _vh_list = [_vh[_vh.index(vh) + 1], _vh[_vh.index(vh) + _structure[1]], _vh[_vh.index(vh) + _structure[1] + 1]]
                            self._face_vertex_dict.update({self.add_face(_vh_list): _vh_list})
                        else:
                            _row_beginn_idx += _structure[1]
                    except:
                        pass

            if self.has_face_normals():
                self.update_normals()

            if self.viewer:
                self.viewer.update_mesh_info()
                self._update_viewer_signal.signal.emit()

    def generate_faces_of_related_mesh(self, related_mesh=None, processbar_cb=None):
        """
        Generate the face of current mesh with reference of a related mesh
        :param related_mesh: related mesh
        """
        _related_mesh = None
        if not related_mesh:
            if not self._related_mesh:
                raise("DrapeMesh: No related Mesh defined!")
            else:
                _related_mesh = self._related_mesh
        else:
            _related_mesh = related_mesh
        _n = self.n_vertices()

        with tqdm.tqdm(total=_n, desc="Generating Faces from related Mesh") as pbar:
            for i, fh in enumerate(_related_mesh.faces()):
                _fv = []
                for vh in _related_mesh.fv(fh):
                    _fv.append(vh)
                self._face_vertex_dict.update({fh: _fv})
                self.add_face(_fv)
                if processbar_cb:
                    processbar_cb(self.name, 'Generating Fraces of Reletiv', i/_n *100)
                pbar.update()

        if self.has_face_normals():
            self.update_normals()

        if self.viewer:
            self.viewer.update_mesh_info()

    def generate_faces(self, processbar_cb=None):
        """
            Gernerate Faces with iteration of each vertex w.r.t. its neighbor points
            via calculation of euclidean distance.
            For simple mesh stucket, because it is slow !
        """
        # this function generates the faces from vertexes of the minimal euclidean distances
        ## the idea is, we find out three nearst points of the focuing point, then build two faces

        _vh_face_dict = OrderedDict()

        # tmp save the vertex removed from the
        if not self._has_face:
            _vh_iterated = []
            _faces = []
            _last_iterated_vertex = None
            _vh_not_iterated = list(self._vertex_dict.keys())

            _n = self.n_vertices()
            with tqdm.tqdm(total=_n, desc="Generating Faces") as pbar:

                for i, vh in enumerate(self._vertex_dict.keys()):
                    pbar.update(n=1)
                    _neighbor_vhs_list = list()

                    if processbar_cb:
                        processbar_cb(self.name, 'Generating Fraces', i/_n*100)

                    # to remind that a 0 distance will be calculated, we kick off the current point

                    _vh_not_iterated.pop(_vh_not_iterated.index(vh))
                    _neighbors_found = False
                    _vh_not_iterated_calculate = copy.copy(_vh_not_iterated)

                    # then we will find the nearest three neighbors of this vertex

                    while not _neighbors_found:
                        _min_distance = np.finfo(dtype=np.float64).max
                        _min_distance_vh = None
                        # gonna iterate all of the vertexes and try to find out the neigbors
                        for _vh in _vh_not_iterated_calculate:

                            _tmp_point = self._vertex_dict[_vh]
                            _this_distance = spatial.distance.euclidean(self._vertex_dict[vh],
                                                                        _tmp_point,
                                                                        )
                            if _this_distance < _min_distance:
                                _min_distance = _this_distance
                                _min_distance_vh = _vh

                        if _min_distance_vh:
                            # found a nearest point, then we need to validate that the vertex collected with
                            # current vertex are not already in a face

                            # first of all we kick off this point so that it will not be considered once again
                            _vh_not_iterated_calculate.pop(_vh_not_iterated_calculate.index(_min_distance_vh))

                            # if we found a neighbor, then we should make sure, that this neighbor is not on the face beside it,
                            # to check this, we just need to find out, whether this point is on the face of last iterated vertex
                            if len(_faces) == 0:
                                _neighbor_vhs_list.append({_min_distance: _min_distance_vh})
                            else:
                                _point_unrelated = False
                                for face in _faces:
                                    if _min_distance_vh in face and _last_iterated_vertex in face:
                                        _point_unrelated = True
                                        break
                                if not _point_unrelated:
                                    _neighbor_vhs_list.append({_min_distance: _min_distance_vh})

                        if len(_neighbor_vhs_list) == 3:
                            break

                    # generate the face list and validate the faces
                    # get all the neighbors, the faces will be looked as a square with vh and its 3 neighbors
                    _neighbor_vhs = sorted(_neighbor_vhs_list, key=lambda f: list(f.values())[0].idx())

                    print([list(a.values())[0].idx() for a in _neighbor_vhs])
                    _first_mesh_neighbors = [list(a.values())[0] for a in _neighbor_vhs[0:2]]
                    _first_mesh_neighbors.reverse()

                    # for
                    self._face_vertex_dict.update({self.add_face([vh] + _first_mesh_neighbors): [vh] + _first_mesh_neighbors})
                    self._face_vertex_dict.update(
                        {self.add_face([list(a.values())[0] for a in _neighbor_vhs]): [list(a.values())[0] for a in _neighbor_vhs]})

                    _vh_iterated.append(vh)
                    _last_iterated_vertex = vh

                    #for face in _faces:
                        #print("face")
                        #print([x.idx() for x in face])

                    #if len(_faces) > 3:
                        #break
        if self.has_face_normals():
            self.update_normals()

    def add_vertex_with_id(self, vertex_dict, name=None, processbar_cb=None):
        # add vertex only of the mesh and id properties of each vertex

        _new_vertex_dict = OrderedDict()
        self.add_property(self._vertex_property_origin_id_handle, 'origin_id')
        self.add_property(self._vertex_property_shear_angle_handle, 'shear_angle')
        self.add_property(self._vertex_property_thinning_handle, 'thinning')
        _n = len(vertex_dict)

        if self._is_shear_angle_colored:
            _shear_angles = np.array([con['shear_angle'] for con in vertex_dict.values()], dtype=np.float64)
            _color_norm = color_norm(vmin=_shear_angles.min(),
                                     vmax=_shear_angles.max())

        with tqdm.tqdm(total=_n, desc="Adding Vertices of %s" % self.name) as pbar:
            for i, _id in enumerate(sorted(vertex_dict, key=lambda t: int(t))):

                if processbar_cb:
                    processbar_cb(self.name, 'Generating Vertices', i/_n*100)
                if name:
                    _vertex = vertex_dict[_id][name]
                else:
                    _vertex = vertex_dict[_id]
                _vh = self.add_vertex(openmesh.TriMesh.Point(_vertex[0],
                                                             _vertex[1],
                                                             _vertex[2]))
                self.set_property(self._vertex_property_origin_id_handle, _vh, _id)

                if self._has_shear_angle:
                    _shear_angle = vertex_dict[_id]['shear_angle']
                    self.set_property(self._vertex_property_shear_angle_handle, _vh, _shear_angles)

                if self._has_thinning:
                    try:
                        _thinning = vertex_dict[_id]['thinning']
                        self.set_property(self._vertex_property_thinning_handle, _vh, _thinning)
                    except KeyError:
                        pass

                if self.has_vertex_colors() and self._is_shear_angle_colored:
                    _color = self._shear_angle_colormap(_color_norm(_shear_angle))
                    self.set_color(_vh, openmesh.Vec4f(_color[0],
                                                       _color[1],
                                                       _color[2],
                                                       _color[3]))
                _new_vertex_dict.update({str(_vh.idx()): vertex_dict[_id]})
                if not self._has_face:
                    self._vertex_dict.update({_vh: np.array(_vertex, dtype=np.float64)})
                pbar.update()

        if self._auto_face_generation:
            if self._face_generator == "structure":
                self.generate_faces_of_structure()
            elif self._face_generator == "euclidean":
                self.generate_faces()
            elif self._face_generator == "related":
                self.generate_faces_of_related_mesh()
            else:
                raise("DrapeMesh: Unknown Face Generator!")

        if self.has_vertex_normals():
            self.update_vertex_normals()

        if self.viewer:
            self.viewer.update_mesh_info()

        return _new_vertex_dict

    def add_faces_with_id(self, face_list, vertex_list, processbar_cb=None):
        _n = len(face_list)
        if self._has_face:
            self._face_vertex_dict.clear()
            print("DrapeTriMesh: Mesh %s already has faces, older faces will be updated!" % self.name())
        with tqdm.tqdm(total=_n, desc="Adding Faces of %s" % (self.name)) as pbar:
            for k, face in enumerate(face_list):
                _vh_list = []
                for point in face_list[face]:
                    _vertex = vertex_list[point]['point_start']
                    _vh = self.add_vertex(openmesh.TriMesh.Point(float(_vertex[0]),float(_vertex[1]),float(_vertex[2])))
                    _vh_list.append(_vh)
                    self._face_vertex_dict.update({self.add_face(_vh_list): _vh_list})
                if processbar_cb:
                    processbar_cb(self.name, 'Adding Fraces', k/_n*100)
                pbar.update()

    def get_face_vertex_dict(self):
        return self._vertex_dict, self._face_vertex_dict

    def add_vertex_from_binary(self, data_path, is_origin=False, processbar_cb=None):
        #try:
        if not is_origin:
            self.add_property(self._vertex_property_shear_angle_handle, 'shear_angle')
            _data = pickle.load(open(data_path, 'rb'))

            if self._is_shear_angle_colored:
                _shear_angles = _data[3, :]
                _color_norm = color_norm(vmin=_shear_angles.min(),
                                         vmax=_shear_angles.max())
            # the data of simulation is an array of point list in form [x, y, z, shear angle]
            _n = len(_data)
            with tqdm.tqdm(total=_n, desc="Extracting Vertices in %s" % self.name) as pbar:
                for i, point in enumerate(_data):

                    if any(np.isnan(point)):
                        np.nan_to_num(point, copy=False)

                    point = point.tolist()

                    _vh = self.add_vertex(openmesh.TriMesh.Point(point[0],
                                                                 point[1],
                                                                 point[2]))

                    self.set_property(self._vertex_property_shear_angle_handle, _vh, point[3])

                    if self.has_vertex_colors() and self._is_shear_angle_colored:
                        _color = self._shear_angle_colormap(_color_norm(point[3]))
                        self.set_color(_vh, openmesh.Vec4f(_color[0],
                                                           _color[1],
                                                           _color[2],
                                                           _color[3]))

                    if not self._has_face:
                        self._vertex_dict.update({_vh: point[0:3]})
                    pbar.update()

        else:
            _data = pickle.load(open(data_path, 'rb'))
            _n = _data.size
            with tqdm.tqdm(total=_n, desc="Extracting Vertices in %s" % self.name) as pbar:
                for x, y in itertools.product(range(_data.shape[0]), range(_data.shape[1])):
                    _vh = self.add_vertex(openmesh.TriMesh.Point(x, y, float(_data[x, y])))

                    if not self._has_face:
                        self._vertex_dict.update({_vh: [x, y, _data[x, y]]})
                    pbar.update()

        if self._auto_face_generation:
            if self._face_generator == "structure":
                self.generate_faces_of_structure()
            elif self._face_generator == "euclidean":
                self.generate_faces()
            elif self._face_generator == "related":
                self.generate_faces_of_related_mesh()
            else:
                print("DrapeTriMesh: Unknown Face Generator!")
        else:
            if self.viewer:
                self.viewer.update_mesh_info()

                self._update_viewer_signal.signal.emit()

    def deepcopy(self, name=None):
        if self.n_faces():
            _has_facee = True
        else:
            _has_facee = False

        if name:
            _name = name
        else:
            _name = self.name + '_deepcopy'

        new_mesh = DrapeTriMesh(name=_name,
                                has_face=_has_facee,
                                viewer_parent=self.viewer.parent())

        for _vh in self.vertices():
            new_mesh.add_vertex(self.point(_vh))

        for _fh in self.faces():
            _fv = []
            for vh in self.fv(_fh):
                _fv.append(vh)
            new_mesh.add_face(_fv)
        new_mesh.update_normals()
        new_mesh.mesh_option_request()
        new_mesh.request_vertex_colors()
        new_mesh.request_face_colors()
        new_mesh.update_viewer()
        if new_mesh.viewer:
            #new_mesh.viewer.update_mesh_info()
            new_mesh._update_viewer_signal.signal.emit()

        return new_mesh






















