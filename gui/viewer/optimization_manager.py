from PyQt5.QtWidgets import *
from gui.ui.ui_optimization_manager import Ui_DrapeOptimizationManager
import openmesh, copy, random
from Data.drape_object import *
import copyreg

from gui.viewer.viewer_utils.utils import *

from evolAlgo.evolIndividual import EvolConfig
from evolAlgo.evolAlgImpl import EvolAlgImpl
from evolAlgo.optimizationThread import EAThread

class OptimizationManager(QWidget, Ui_DrapeOptimizationManager):
    def __init__(self, parent):
        super(OptimizationManager, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("OptimizationManager")

        # Global variables
        self._parent = parent
        self._echo = parent.echo_info
        self._target_geometry = None
        self._constraints = None
        self._selected_textile = {}
        # while initializing, all of ea algorithm objects will be created and put here
        self._evol_algorithm_dict = dict()
        self.result_manager = None

        # GUI
        self.toolBox.setCurrentIndex(0)
        # Push Buttons
        #self.pB_start.clicked.connect(self._start_clicked)
        self.pB_start.setEnabled(False)

        self.pB_pause.clicked.connect(self._pause_clicked)
        self.pB_pause.setEnabled(False)
        self.pB_stop.clicked.connect(self._stop_clicked)
        self.pB_stop.setEnabled(False)
        self.pB_update_info.clicked.connect(self._update_info_clicked)
        self.pB_init.clicked.connect(self._initialize_clicked)
        self.pB_init.setEnabled(False)
        self.page_general.append("Information not updated!")
        self.page_general.append("Please click Update Info!")

        self.checkBox_activated.clicked.connect(self._cbox_activated_clicked)
        self.optThread = None

    def setThread(self, optThread):
        self.optThread = optThread

    def put_info(self, it, list1, list2, list3):
        self.page_general.append("- Iteration %s" % str(it))
        self.page_general.append("-- Gaussian Curvature:")
        self.page_general.append("-- %s" % str(list1))
        self.page_general.append("-- Norm. Gaussian Curvature:")
        self.page_general.append("-- %s" % str(list2))
        self.page_general.append("-- Selected Individuals:")
        self.page_general.append("-- %s" % str(list3))
        self.page_general.append("")

    def updatePbar(self, value):
        self.prograssbar.setValue(value)

    def ind2visu(self, list):
        self.tabWidget.clear()

        for i in range(5):
            self.tabWidget.addTab(list[i].viewer, "Individual %s" % str(i))


    def set_result_manager(self, result_manager):
        self.result_manager = result_manager

    def _update_info_clicked(self):
        # this function grasp the parameters from parameter manager
        self.pB_init.setEnabled(True)
        _update_original_geometry = False
        #self._target_geometry = self._parent.parameter_manager.target_geometry

        if self._constraints != self._parent.parameter_manager.target_geometry:
            self._constraints = self._parent.parameter_manager.constraints
            _update_original_geometry = True

        self._selected_textile = self._parent.parameter_manager.selected_textile

        self.page_general.clear()

        if self._target_geometry != self._parent.parameter_manager.target_geometry:
            self._target_geometry = self._parent.parameter_manager.target_geometry
            _update_original_geometry = True

        if self._target_geometry:

            self.page_general.append("Target Geometry:")
            self.page_general.append("- Name: {}".format(self._target_geometry.name))
            self.page_general.append("- Number of Vertex: {}".format(str(self._target_geometry.n_vertices())))
            self.page_general.append("- Number of Faces: {}".format(str(self._target_geometry.n_faces())))
            self.page_general.append("")
        else:
            self.page_general.append("!!! Target Geometry not loaded !!!")
            self.page_general.append("")

        if self._selected_textile:
            self.page_general.append("Selected Textile: ")
            for tex in self._selected_textile.keys():
                self.page_general.append("- {}: crit. sAngle: {}".format(tex, self._selected_textile[tex]))
            self.page_general.append("")
        else:
            self.page_general.append("!!! Textile not selected !!!")

            self.page_general.append("")

        if self._constraints:
            self.page_general.append("Constraints for EA: ")

            self.page_general.append("- x [mm]: {}".format(str(self._constraints['x'])))
            self.page_general.append("- y [mm]: {}".format(str(self._constraints['y'])))
            self.page_general.append("- z [mm]: {}".format(str(self._constraints['z'])))

            self.page_general.append("- length: {}".format(str(self._constraints['length'])))
            self.page_general.append("- width : {}".format(str(self._constraints['width'])))
            self.page_general.append("- height: {}".format(str(self._constraints['height'])))

            self.page_general.append("- Vertex excepted: {}".format(len(self._constraints['node_excepted'])))



        else:
            self.page_general.append("--- No Constraints set ---")
            self.page_general.append("")

        if self.checkBox_activated.isChecked():
            # we update the visual here
            if _update_original_geometry:
                for i in range(self.tabWidget.count()):
                    if self.tabWidget.tabText(i) == "Original":
                        self._target_geometry.viewer.hide()
                        self.tabWidget.removeTab(i)
                        break

                self._target_geometry.set_vertex_color_mono(vertex_list=self._constraints['node_excepted'],
                                                            color_in_list=openmesh.Vec4f(0., 0., 1., 1.),
                                                            color_out_list=openmesh.Vec4f(0., 1., 0., 1.))

                self.tabWidget.addTab(self._target_geometry.viewer, "Original")

    def _initialize_clicked(self):
        _evol_config = EvolConfig()
        #try:
        sangle_offset = float(self.lineEdit_critical_sangle_offset.text())
        _evol_config.update_config(size_of_population=self.spinBox_size_pop.value(),
                                   iteration=self.spinBox_size_iteration.value(),
                                   min_vertex=self.spinBox_min_mutations_nodes.value(),
                                   max_vertex=self.spinBox_max_mutations_nodes.value(),
                                   adaptive_mutation=self.checkBox_adaptive_mutation.isChecked(),
                                   convergence_threshold=self.spinBox_terminate_fiteness.value(),
                                   sangle_offset=sangle_offset
                                  )
        self.page_general.clear()
        self._update_info_clicked()
        _evol_config.show_evol_config(browser=self.page_general)

        self.page_general.append("")
        #except:
            #self._echo(msg="Error while setting parameter, please check!", instance=self, type=InfoType.ERROR)
            #print("sth wrong")
            #return
        # we setup the algorithm here

        for textile_key in self._selected_textile.keys():

            _this_evol_algorithm = EvolAlgImpl(input_geometry=self._target_geometry,
                                               textile=textile_key,
                                               crit_sAngle=self._selected_textile[textile_key],
                                               fitness_function=None, # ToDo
                                               constraints=self._constraints,
                                               config=_evol_config)

            self._evol_algorithm_dict.update({textile_key: _this_evol_algorithm})

        self.pB_start.setEnabled(True)
        self.pB_pause.setEnabled(True)
        self.pB_stop.setEnabled(True)

    def _cbox_activated_clicked(self):
        pass

    def _start_clicked(self):
        # todo: after start, the objects should be created and the information should be grasped from parameter manager!

        pass



    def _pause_clicked(self):

        if self.pB_pause.text() == "Pause":
            self.pB_pause.setText("Continue")
        else:
            self.pB_pause.setText("Pause")
        pass

    def _stop_clicked(self):
        pass

    def export_result(self):




        pass























