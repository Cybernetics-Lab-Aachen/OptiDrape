import sys, os, re
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Data import data_extraction, drape_object
from gui.ui.ui_database_manager import Ui_DataBaseManager

import openmesh
from pymongo import MongoClient, errors as mongo_error

from gui.viewer import mesh_grid_layout, textile_manger
from gui.viewer.viewer_utils.utils import *
from Data.import_cad import *

#TODO : NOW FACING PROBLEM, WHEN NEW MESH SHOW, THE OLD ONE WOULD BE RESET
#TODO : no upgrage bar shown from the second visualization on


class DrapeDatabaseManager(QWidget, Ui_DataBaseManager):
    def __init__(self, parent=None):
        # we set the initialization for parent class, so we can use the gui items directly
        super(self.__class__, self).__init__(parent)
        # we setup the Ui
        self.setupUi(self)
        self.statusBar = parent.statusBar
        
        # global variables
        self.parent = parent

        # Push Buttons
        self.pb_load_geometry.clicked.connect(self._load_geometry_db)
        self.pb_load_simulation.clicked.connect(self._load_simulation_db)
        self._geometry_data_dict = dict()
        self._simulation_data_dict = dict()

        self.tree_viewer_sim.doubleClicked.connect(self._tree_sim_doubleClicked)
        self.tree_viewer_geo.doubleClicked.connect(self._tree_geo_doubleClicked)

        self._database = None

        self._vertex_property_origin_id_handle = openmesh.VPropHandle()
        self._face_property_origin_id_handle = openmesh.FPropHandle()

        # global varibales
        self._mesh_table = None
        self._drape_geometry_objects = dict()
        self._mesh_data_roadmap =[]
        self._layout = QGridLayout()

        self.current_data_form_tree = {}
        self.current_route_form_tree =[]

        self.gBox_viewer.setEnabled(True)

    def __get_files(self, name_of_dialog="", sim=True):
        _db_path = QFileDialog.getExistingDirectory(self, name_of_dialog)
        if not _db_path:
            return None

        _check_sub_folder = []
        for _, d, _ in os.walk(_db_path):
            if d and all([s in ['geometry', 'label'] for s in d]):
                _check_sub_folder = d
                break
            else:
                _check_sub_folder = None

        if sim and not _check_sub_folder:
            # self.statusBar.
            print("Not a valid data path!")
            return None

        geo_variant = []

        if sim:
            os_walt_list = os.walk(_db_path + '/geometry')
        else:
            os_walt_list = os.walk(_db_path)

        for _, _, f in os_walt_list:
            # get the filtering for the list of all files with extension because there are [] in f
            if f:
                geo_variant = f
                break

        def sort_geo_name(elem):
            s_list = re.split('(\d+)', elem)
            i = ''
            for s in s_list:
                if s.isdigit():
                    i += s
            return int(i)

        geo_name = []
        for geo_name_with_format in geo_variant:
            # get all geometry names without extension
            geo_name.append(os.path.splitext(geo_name_with_format)[0])

        if sim:
            geo_name.sort(key=sort_geo_name)
        else:
            geo_name = geo_variant

        return os.path.basename(_db_path), _db_path, geo_name

    def _load_geometry_db(self):
        geo_name, geo_path, geo_variant = self.__get_files(name_of_dialog="Import Optimization DataBase", sim=False)

        if geo_variant and geo_name:
            self._geometry_data_dict.update({geo_name: {'path': geo_path, 'geo': geo_variant}})
            self._update_tree_view(self.tree_viewer_geo, self._geometry_data_dict)

        #self._geometry_path_dict.update(_db_dict)
        #self._update_tree_view(is_sim=False)

    def _load_simulation_db(self):
        geo_name, geo_path, geo_variant = self.__get_files(name_of_dialog="Import Simulation DataBase")
        if geo_variant and geo_name:
            self._simulation_data_dict.update({geo_name: {'path': geo_path, 'geo': geo_variant}})
            self._update_tree_view(self.tree_viewer_sim, self._simulation_data_dict)

    @staticmethod
    def _update_tree_view(tree_handle, data_dict):
        _model = QStandardItemModel(0, 1, tree_handle)
        for geo_name in data_dict.keys():
            _tree_l0 = QStandardItem(geo_name)
            _tree_l0.setEditable(False)
            for geo_variate in data_dict[geo_name]['geo']:
                _tree_l1 = QStandardItem(geo_variate)
                _tree_l1.setEditable(False)
                _tree_l0.appendRow(_tree_l1)
            _model.appendRow(_tree_l0)
        tree_handle.setModel(_model)
        tree_handle.setHeaderHidden(True)

    @staticmethod
    def __check_tree_level_index(tree_handle, index=0):
        return not tree_handle.selectedIndexes()[0].child(index, index).data()

    @staticmethod
    def __get_tree_roadmap(tree_handle):
        _road_map = []
        _last_index = tree_handle.selectedIndexes()[0]
        _road_map.append(_last_index.data())
        while _last_index.parent().data():
            _last_index = _last_index.parent()
            _road_map.append(_last_index.data())
        _road_map.reverse()
        return _road_map

    def _tree_sim_doubleClicked(self):
        _data_router = self.__get_tree_roadmap(self.tree_viewer_sim)
        if len(_data_router) < 2:
            return

        try:
            _geo_path = self._simulation_data_dict[_data_router[0]]['path']

            self._build_and_visualize_meshes(_data_router, _geo_path)

        except KeyError or IndexError:
            print("Key Error")

    def _tree_geo_doubleClicked(self):
        _data_router = self.__get_tree_roadmap(self.tree_viewer_geo)
        if len(_data_router) < 2:
            return
        try:
            _geo_path = self._geometry_data_dict[_data_router[0]]['path']

            self._build_and_visualize_meshes(_data_router, _geo_path, sim=False)

        except KeyError or IndexError:
            print("Key Error")

    def _build_and_visualize_meshes(self, mesh_name_list, mesh_path, sim=True):
        """
        :param mesh_name_list: a list quered from tree viewer contains 2 strings, mesh name and mesh variant
        :param mesh_path: path where the lib can be found
        :return:
        """
        # check if there is mesh object to use directly
        _mesh_name = mesh_name_list[0] + '.' + mesh_name_list[1]
        if _mesh_name in self._drape_geometry_objects.keys():
            if _mesh_name not in [self.widget_db_viewer.tabText(i) for i in range(self.widget_db_viewer.count())]:
                self.widget_db_viewer.addTab(self._drape_geometry_objects[_mesh_name].geometry_viewer, _mesh_name)
            else:
                print("Mesh already shown!")
        else:
            # we have the face generated, then we do not need to regenerate them
            if sim:
                _new_mesh_geometry = drape_object.OptiDrapeGeometry(mesh_path=mesh_path, mesh_name_list=mesh_name_list,
                                                                    auto_build=True, viewer_parent=self)
                self.widget_db_viewer.addTab(_new_mesh_geometry.geometry_viewer, _new_mesh_geometry.name)
                self._drape_geometry_objects.update({_mesh_name: _new_mesh_geometry})
            else:
                _opt = QFileDialog.Options()
                _opt |= QFileDialog.DontUseNativeDialog

                _geometry = drape_object.DrapeTriMesh(name=_mesh_name, has_face=True)
                create_drape_mesh_object(mesh_path=mesh_path + '/' + mesh_name_list[1], mesh_obj=_geometry)
                _geometry.mesh_option_request()
                _geometry.update_viewer()

                self.widget_db_viewer.addTab(_geometry.viewer, _geometry.name)
                self._drape_geometry_objects.update({_mesh_name: _geometry})
            # update the geometry data for further use



    def hide_mesh_tab(self, mesh_name):
        for i in range(self.widget_db_viewer.count()):
            if str(self.widget_db_viewer.tabText(i)) == mesh_name:
                self.widget_db_viewer.removeTab(i)
                break

    # TODO: check what kind of data should we extract
    def _get_meta_data_request(self):
        _request = ['E_X','E_Y']
        return _request

    def mesh_data_to_db(self,_vertex_data,_face_data, _route):
        _vertex_face_dict = {"Vertex": _vertex_data, "Faces": _face_data}
        _docu = self.mongo_client['OptiDrape'][_route[0]]
        _mesh_name = _route[1] + '.' + _route[2]
        _docu.update_one({_mesh_name: {'$exists': True}},{'$set': {_mesh_name: _vertex_face_dict}})




if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = DrapeDatabaseManager()
    test.show()
    app.exec()





