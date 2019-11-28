import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import itertools
import openmesh
from Data.import_cad import create_drape_mesh_object

from gui.ui.ui_parameter_manager import Ui_DrapeParameterManager
from gui.viewer.viewer_utils.utils import *
from Data.drape_object import DrapeTriMesh
from gui.viewer.viewer_utils.DrapeInteract import DrapeInteractiveView, DrapeInteractScene

from evolAlgo.constrains import EvolAlgoConstraints


class ParameterManager(QWidget, Ui_DrapeParameterManager):
    def __init__(self, parent):
        super(ParameterManager, self).__init__(parent)
        self.setupUi(self)

        # global variable
        self._parent = parent
        self._echo = parent.echo_info

        self._textile_selected = dict()
        self._textile_database = {}
        self._target_geometry = None
        self.interact_constraints_viewer = None
        self._constraints = EvolAlgoConstraints()

        # ui actions
        self.pB_tex_load.clicked.connect(self._load_tex_clicked)
        self.pB_tex_set.setDisabled(True)
        self.gBox_interaction.setDisabled(True)
        self.pB_tex_set.clicked.connect(self._set_tex_clicked)
        self.pB_geo_load.clicked.connect(self._load_geo_clicked)
        self.pB_model_load.clicked.connect(self._load_model_clicked)
        self.checkBox_global.clicked.connect(self._checkBox_global_clicked)

        self.pB_clean.clicked.connect(self._clean_all_constraints_clicked)
        self.pB_set.clicked.connect(self._set_constraints_clicked)
        self.pB_save.clicked.connect(self._save_constraints_clicked)

        self.hSlider_x.setMin(-100)
        self.hSlider_x.setMax(100)
        self.hSlider_x.setRange(-100, 100)
        self.hSlider_y.setMin(-100)
        self.hSlider_y.setMax(100)
        self.hSlider_y.setRange(-100, 100)
        self.hSlider_z.setMin(-100)
        self.hSlider_z.setMax(100)
        self.hSlider_z.setRange(-100, 100)

        self.hSlider_global_x_length.setMin(-100)
        self.hSlider_global_x_length.setMax(100)
        self.hSlider_global_x_length.setRange(-100, 100)

        self.hSlider_global_y_length.setMin(-100)
        self.hSlider_global_y_length.setMax(100)
        self.hSlider_global_y_length.setRange(-100, 100)

        self.hSlider_global_z_length.setMin(-100)
        self.hSlider_global_z_length.setMax(100)
        self.hSlider_global_z_length.setRange(-100, 100)

        self._checkBox_global_clicked()

    @property
    def textile_manager(self):
        return self._parent.textile_manager

    @property
    def constraints(self):
        return self._constraints

    @property
    def target_geometry(self):

        return self._target_geometry

    @property
    def selected_textile(self):
        return self._textile_selected

    def _load_tex_clicked(self):
        self._textile_database = self.textile_manager.textile_database

        if not self._textile_database:
            QMessageBox.warning(self, "Warning", "No Database loaded! Try to load it on DataBaseManager!", QMessageBox.Ok)
            return
        self.pB_tex_set.setDisabled(False)
        model = QStandardItemModel(0, 1, self.treeView_textile)
        for textile in self._textile_database.keys():
            _textile_item = QStandardItem(textile)
            _textile_item.setEditable(False)
            _textile_item.setSelectable(True)
            _textile_item.setCheckable(True)
            model.appendRow(_textile_item)
        self.treeView_textile.setModel(model)
        self.treeView_textile.setHeaderHidden(True)

    def _set_tex_clicked(self):
        model = self.treeView_textile.model()
        self._textile_selected = [item.text() for item in [model.item(i) for i in range(model.rowCount())] if item.checkState()]
        if not self._textile_selected:
            QMessageBox.warning(self, "Warning", "There is no textile for optimization selected!", QMessageBox.Ok)
        _selected_textile_dict = dict()
        for tex in self._textile_selected:
            _selected_textile_dict.update({tex: self._textile_database[tex]['property']['cangle']})
        self._textile_selected = _selected_textile_dict
        print(self._textile_selected)

    def _checkBox_global_clicked(self):
        if self.checkBox_global.isChecked():
            self.tabWidget_dim.setEnabled(True)
            self.gBox_interaction.setDisabled(False)

        else:
            self._clean_all_constraints_clicked()
            self.tabWidget_dim.setEnabled(False)

            self.gBox_interaction.setDisabled(True)

    def _clean_all_constraints_clicked(self):
        self.hSlider_x.setStart(self.hSlider_x.min())
        self.hSlider_x.setEnd(self.hSlider_x.max())

        self.hSlider_y.setStart(self.hSlider_y.min())
        self.hSlider_y.setEnd(self.hSlider_y.max())

        self.hSlider_z.setStart(self.hSlider_z.min())
        self.hSlider_z.setEnd(self.hSlider_z.max())

        if self.interact_constraints_viewer:
            self.interact_constraints_viewer.clean_all_rects()
        pass

    def _set_constraints_clicked(self):
        _rects, scene_rect, raw_size = self.interact_constraints_viewer.get_all_rects()
        # nun we need to get the vertexes from the rects,
        # first of all we normalize the rects size into raw image size, which
        _ratio_width = raw_size.width() / scene_rect.width()
        _ratio_height = raw_size.height() / scene_rect.height()
        #_rect_normalized = []
        _node_excepted = []
        _node_expected = []
        # then we could insert the node id directly from the normalized rect
        for rect in _rects:
            _this_rect = QRect(rect.x() * _ratio_width,
                               rect.y() * _ratio_height,
                               rect.width() * _ratio_width,
                               rect.height() * _ratio_height)
            #_rect_normalized.append(_this_rect)
            for i, j in itertools.product(range(_this_rect.x(), _this_rect.x() + _this_rect.width() ),
                                          range(_this_rect.y(), _this_rect.y() + _this_rect.height() )):
                if i < 0 or j < 0 or i >= raw_size.width() or j >= raw_size.height():
                    continue
                _this_node = self.target_geometry.xy_matrix[j, i]
                if _this_node not in _node_excepted:
                    _node_excepted.append(_this_node)

        for _vh in self.target_geometry.vertices():
            if _vh.idx() not in _node_excepted:
                _node_expected.append(_vh.idx())

        self._constraints['x'] = [self.hSlider_x.start(), self.hSlider_x.end()]
        self._constraints['y'] = [self.hSlider_y.start(), self.hSlider_y.end()]
        self._constraints['z'] = [self.hSlider_z.start(), self.hSlider_z.end()]

        self._constraints['length'] = [self.hSlider_global_x_length.start(), self.hSlider_global_x_length.end()]
        self._constraints['width'] = [self.hSlider_global_y_length.start(), self.hSlider_global_y_length.end()]
        self._constraints['height'] = [self.hSlider_global_z_length.start(), self.hSlider_global_z_length.end()]

        import pickle

        pickle.dump(_node_expected, open('node_expected_useful.p', "wb"))
        self._constraints['node_excepted'] = _node_excepted
        self._constraints['node_expected'] = _node_expected

    def _save_constraints_clicked(self):
        pass

    def _load_geo_clicked(self):
        _opt = QFileDialog.Options()
        _opt |= QFileDialog.DontUseNativeDialog

        _path, is_ok = QFileDialog.getOpenFileName(self, "Load CAD File", "",
                                                         "OBJ (*.obj);;"
                                                         "STL (*.stl);;"
                                                         "OFF (*.off);;"
                                                         "PLY (*.ply);;"
                                                         "OM (*.om);;"
                                                         "All Files (*)", options=_opt)

        if is_ok:
            # first we get the format of the cad file
            _splited_cad_name = os.path.splitext(os.path.basename(_path))
            _cad_name = _splited_cad_name[0]
            _cad_format = _splited_cad_name[1]

            self.label_geo_name.setText("Name of Mesh: {}".format(_cad_name))

            if _splited_cad_name[1] in ['.obj', '.stl', '.off', '.ply', '.om']:
                # This cad file could be read from openmesh directly
                self._target_geometry = DrapeTriMesh(name=_cad_name, has_face=True)
                create_drape_mesh_object(mesh_path=_path, mesh_obj=self._target_geometry)
                self._target_geometry.mesh_option_request()
                self._target_geometry.update_viewer()
                self.update_interaction_viewer()

    def update_interaction_viewer(self):
        if not self.target_geometry:
            # todo echo
            return
        self.widget_interaction.clear()
        self.widget_interaction.addTab(self._target_geometry.viewer, "Geometry Viewer")
        # get the image viewer
        _qimage, _ = self.target_geometry.generate_xy_projection_image_from_z()
        self.interact_constraints_viewer = DrapeInteractiveView(bg_image=_qimage)
        self.widget_interaction.addTab(self.interact_constraints_viewer, "Constraints Setter")

    def _load_model_clicked(self):
        pass



