# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drapeoptimizationmanager.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from enum import Enum


class VertexSelectionPolicy(Enum):
    RANDOMLY = 0
    RANDOMLY_NEIGHBORS = 1
    MAX_COORDINATE = 2
    MAX_COORDINATE_NEIGHBORS = 3
    MAX_CURVATURE = 4
    MAX_CURVATURE_NEIGHBORS = 5


class MutationPolicy(Enum):
    RANDOMLY = 0
    REDUCE_Z_COORDINATE = 1
    REDUCE_CURVATURE = 2


class NeighbourPolicy(Enum):
    RANDOMLY = 0
    CONTINUOUS = 1


class Ui_DrapeOptimizationManager(object):
    def setupUi(self, DrapeOptimizationManager):
        DrapeOptimizationManager.setObjectName("DrapeOptimizationManager")
        DrapeOptimizationManager.resize(725, 581)
        self.gridLayout_3 = QtWidgets.QGridLayout(DrapeOptimizationManager)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gBox_ea = QtWidgets.QGroupBox(DrapeOptimizationManager)
        self.gBox_ea.setObjectName("gBox_ea")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gBox_ea)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.toolBox = QtWidgets.QToolBox(self.gBox_ea)
        self.toolBox.setMinimumSize(QtCore.QSize(280, 500))
        self.toolBox.setObjectName("toolBox")

        self.page_general = QtWidgets.QTextBrowser(self.toolBox)

        self.page_general.setGeometry(QtCore.QRect(0, 0, 221, 352))
        self.page_general.setObjectName("page_general")
        self.toolBox.addItem(self.page_general, "")

        self.page_ea_parameter = QtWidgets.QWidget()
        self.page_ea_parameter.setGeometry(QtCore.QRect(0, 0, 221, 352))
        self.page_ea_parameter.setObjectName("page_2")

        _ea_page_layout = QtWidgets.QGridLayout(self.page_ea_parameter)

        _label_size_population = QtWidgets.QLabel(self.page_ea_parameter)
        _label_size_population.setObjectName("Label of pupulation size")
        _label_size_population.setText("Size of Population: ")
        _ea_page_layout.addWidget(_label_size_population, 0, 0, 1, 1)

        self.spinBox_size_pop = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_size_pop.setObjectName("Input of population size")
        self.spinBox_size_pop.setMinimum(0)
        self.spinBox_size_pop.setValue(5)
        self.spinBox_size_pop.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_size_pop, 0, 1, 1, 1)

        _label_num_iteration = QtWidgets.QLabel(self.page_ea_parameter)
        _label_num_iteration.setObjectName("label of iteration number")
        _label_num_iteration.setText("Iteration:")
        _ea_page_layout.addWidget(_label_num_iteration, 1, 0, 1, 1)

        self.spinBox_size_iteration = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_size_iteration.setObjectName("Input of population size")
        self.spinBox_size_iteration.setMinimum(1)
        self.spinBox_size_iteration.setMaximum(5000)
        self.spinBox_size_iteration.setValue(1000)
        self.spinBox_size_iteration.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_size_iteration, 1, 1, 1, 1)

        _label_min_nodes_to_eva = QtWidgets.QLabel(self.page_ea_parameter)
        _label_min_nodes_to_eva.setObjectName("label of max. number of nodes")
        _label_min_nodes_to_eva.setText("Min. Vertex:")
        _ea_page_layout.addWidget(_label_min_nodes_to_eva, 2, 0, 1, 1)

        self.spinBox_min_mutations_nodes = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_min_mutations_nodes.setObjectName("Input of max mutation nodes")
        self.spinBox_min_mutations_nodes.setMinimum(1)
        self.spinBox_min_mutations_nodes.setMaximum(1000)
        self.spinBox_min_mutations_nodes.setValue(5)
        self.spinBox_min_mutations_nodes.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_min_mutations_nodes, 2, 1, 1, 1)

        _label_max_nodes_to_eva = QtWidgets.QLabel(self.page_ea_parameter)
        _label_max_nodes_to_eva.setObjectName("label of max. number of nodes")
        _label_max_nodes_to_eva.setText("Max. Vertex:")
        _ea_page_layout.addWidget(_label_max_nodes_to_eva, 3, 0, 1, 1)

        self.spinBox_max_mutations_nodes = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_max_mutations_nodes.setObjectName("Input of max mutation nodes")
        self.spinBox_max_mutations_nodes.setMinimum(1)
        self.spinBox_max_mutations_nodes.setMaximum(1000)
        self.spinBox_max_mutations_nodes.setValue(10)
        self.spinBox_max_mutations_nodes.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_max_mutations_nodes, 3, 1, 1, 1)

        _label_adaptive_mutation = QtWidgets.QLabel(self.page_ea_parameter)
        _label_adaptive_mutation.setObjectName("label of max. number of nodes")
        _label_adaptive_mutation.setText("Adaptive Mutation:")
        _ea_page_layout.addWidget(_label_adaptive_mutation, 4, 0, 1, 1)

        self.checkBox_adaptive_mutation = QtWidgets.QCheckBox(self.page_ea_parameter)
        self.checkBox_adaptive_mutation.setChecked(True)
        _ea_page_layout.addWidget(self.checkBox_adaptive_mutation, 4, 1, 1, 1)

        _label_terminate_fitness = QtWidgets.QLabel(self.page_ea_parameter)
        _label_terminate_fitness.setObjectName("label of max. number of nodes")
        _label_terminate_fitness.setText("Terminate Score %:")
        _ea_page_layout.addWidget(_label_terminate_fitness, 5, 0, 1, 1)

        self.spinBox_terminate_fiteness = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_terminate_fiteness.setObjectName("Input of terminate fitness")
        self.spinBox_terminate_fiteness.setMinimum(0)
        self.spinBox_terminate_fiteness.setMaximum(100)
        self.spinBox_terminate_fiteness.setValue(80)
        self.spinBox_terminate_fiteness.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_terminate_fiteness, 5, 1, 1, 1)

        _label_critical_sangle_offset = QtWidgets.QLabel(self.page_ea_parameter)
        _label_critical_sangle_offset.setObjectName("label of max. number of nodes")
        _label_critical_sangle_offset.setText("Crit. sAngle Offset °:")
        _ea_page_layout.addWidget(_label_critical_sangle_offset, 6, 0, 1, 1)

        self.lineEdit_critical_sangle_offset = QtWidgets.QLineEdit(self.page_ea_parameter)
        self.lineEdit_critical_sangle_offset.setObjectName("Input of terminate fitness")
        self.lineEdit_critical_sangle_offset.setMaximumWidth(70)
        self.lineEdit_critical_sangle_offset.setText("0")
        _ea_page_layout.addWidget(self.lineEdit_critical_sangle_offset, 6, 1, 1, 1)

        _label_node_selection_policy = QtWidgets.QLabel(self.page_ea_parameter)
        _label_node_selection_policy.setObjectName("label of max. number of nodes")
        _label_node_selection_policy.setText("Vertex Selection Policy:")
        _ea_page_layout.addWidget(_label_node_selection_policy, 7, 0, 1, 1)

        self.comboBox_node_select_policy = QtWidgets.QComboBox(self.page_ea_parameter)

        for policy in VertexSelectionPolicy.__members__:
            self.comboBox_node_select_policy.addItem(policy)

        _ea_page_layout.addWidget(self.comboBox_node_select_policy, 8, 0, 1, 2)

        _label_mutation_policy = QtWidgets.QLabel(self.page_ea_parameter)
        _label_mutation_policy.setObjectName("label of max. number of nodes")
        _label_mutation_policy.setText("Mutation Policy:")
        _ea_page_layout.addWidget(_label_mutation_policy, 9, 0, 1, 1)

        self.comboBox_mutation_policy = QtWidgets.QComboBox(self.page_ea_parameter)
        self.comboBox_node_select_policy.setMaximumWidth(260)
        self.comboBox_mutation_policy.setMaximumWidth(260)
        for policy in MutationPolicy.__members__:
            self.comboBox_mutation_policy.addItem(policy)
        _ea_page_layout.addWidget(self.comboBox_mutation_policy, 10, 0, 1, 2)

        _label_size_mutation_base = QtWidgets.QLabel(self.page_ea_parameter)
        _label_size_mutation_base.setObjectName("label of Size mu. base:")
        _label_size_mutation_base.setText("Size mu. base:")
        _ea_page_layout.addWidget(_label_size_mutation_base, 11, 0, 1, 1)

        self.spinBox_size_mu_base = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_size_mu_base.setObjectName("Input of Size mu. base:")
        self.spinBox_size_mu_base.setMinimum(0)
        self.spinBox_size_mu_base.setMaximum(100)
        self.spinBox_size_mu_base.setValue(3)
        self.spinBox_size_mu_base.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_size_mu_base, 11, 1, 1, 1)

        _label_size_inv_to_select = QtWidgets.QLabel(self.page_ea_parameter)
        _label_size_inv_to_select.setObjectName("label of size of inv-selection:")
        _label_size_inv_to_select.setText("Size inv-selection:")
        _ea_page_layout.addWidget(_label_size_inv_to_select, 12, 0, 1, 1)

        self.spinBox_size_inv_to_select = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_size_inv_to_select.setObjectName("Input of Size inv-selection")
        self.spinBox_size_inv_to_select.setMinimum(0)
        self.spinBox_size_inv_to_select.setMaximum(100)
        self.spinBox_size_inv_to_select.setValue(3)
        self.spinBox_size_inv_to_select.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_size_inv_to_select, 12, 1, 1, 1)



        _label_min_neighbour_each_grp = QtWidgets.QLabel(self.page_ea_parameter)
        _label_min_neighbour_each_grp.setObjectName("label of max. number of nodes")
        _label_min_neighbour_each_grp.setText("Min. Neighbour:")
        _ea_page_layout.addWidget(_label_min_neighbour_each_grp, 13, 0, 1, 1)

        self.spinBox_min_neighbour_each_grp = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_min_neighbour_each_grp.setObjectName("Input of terminate fitness")
        self.spinBox_min_neighbour_each_grp.setMinimum(0)
        self.spinBox_min_neighbour_each_grp.setMaximum(100)
        self.spinBox_min_neighbour_each_grp.setValue(3)
        self.spinBox_min_neighbour_each_grp.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_min_neighbour_each_grp, 13, 1, 1, 1)

        _label_max_neighbour_each_grp = QtWidgets.QLabel(self.page_ea_parameter)
        _label_max_neighbour_each_grp.setObjectName("label of max. number of nodes")
        _label_max_neighbour_each_grp.setText("Max. Neighbour:")
        _ea_page_layout.addWidget(_label_max_neighbour_each_grp, 14, 0, 1, 1)

        self.spinBox_max_neighbour_each_grp = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_max_neighbour_each_grp.setObjectName("Input of terminate fitness")
        self.spinBox_max_neighbour_each_grp.setMinimum(0)
        self.spinBox_max_neighbour_each_grp.setMaximum(100)
        self.spinBox_max_neighbour_each_grp.setValue(80)
        self.spinBox_max_neighbour_each_grp.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_max_neighbour_each_grp, 14, 1, 1, 1)

        _label_min_neighbour_grp = QtWidgets.QLabel(self.page_ea_parameter)
        _label_min_neighbour_grp.setObjectName("label of max. number of nodes")
        _label_min_neighbour_grp.setText("Min. Neigh. Grps:")
        _ea_page_layout.addWidget(_label_min_neighbour_grp, 15, 0, 1, 1)

        self.spinBox_min_neighbour_grp = QtWidgets.QSpinBox(self.page_ea_parameter)
        self.spinBox_min_neighbour_grp.setObjectName("Input of terminate fitness")
        self.spinBox_min_neighbour_grp.setMinimum(1)
        self.spinBox_min_neighbour_grp.setMaximum(100)
        self.spinBox_min_neighbour_grp.setValue(2)
        self.spinBox_min_neighbour_grp.setMaximumWidth(70)
        _ea_page_layout.addWidget(self.spinBox_min_neighbour_grp, 15, 1, 1, 1)

        _label_neighbour_policy = QtWidgets.QLabel(self.page_ea_parameter)
        _label_neighbour_policy.setObjectName("label of max. number of nodes")
        _label_neighbour_policy.setText("Neighbourvertex Policy:")
        _ea_page_layout.addWidget(_label_neighbour_policy, 16, 0, 1, 1)

        self.comboBox_neighbour_policy = QtWidgets.QComboBox(self.page_ea_parameter)
        self.comboBox_neighbour_policy.setMaximumWidth(260)
        self.comboBox_neighbour_policy.setMaximumWidth(260)
        for policy in NeighbourPolicy.__members__:
            self.comboBox_neighbour_policy.addItem(policy)
        _ea_page_layout.addWidget(self.comboBox_neighbour_policy, 17, 0, 1, 2)

        ea_parameter_spacer = QtWidgets.QSpacerItem(10, 1, QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Minimum)
        _ea_page_layout.addItem(ea_parameter_spacer, 18, 1, 1, 1)
        self.page_ea_parameter.setLayout(_ea_page_layout)
        self.toolBox.addItem(self.page_ea_parameter, "")
        self.gridLayout_2.addWidget(self.toolBox, 0, 0, 1, 2)

        self.pB_update_info = QtWidgets.QPushButton(self.gBox_ea)
        self.pB_update_info.setMinimumSize(QtCore.QSize(211, 31))
        #self.pB_update_info.setMaximumSize(QtCore.QSize(211, 31))
        self.pB_update_info.setObjectName("pB_start")
        self.gridLayout_2.addWidget(self.pB_update_info, 1, 0, 1, 2)

        self.pB_init = QtWidgets.QPushButton(self.gBox_ea)
        self.pB_init.setMinimumSize(QtCore.QSize(101, 31))
        # self.pB_start.setMaximumSize(QtCore.QSize(211, 31))
        self.pB_init.setObjectName("pB_init")
        self.gridLayout_2.addWidget(self.pB_init, 2, 0, 1, 1)


        self.pB_start = QtWidgets.QPushButton(self.gBox_ea)
        self.pB_start.setMinimumSize(QtCore.QSize(101, 31))
        #self.pB_start.setMaximumSize(QtCore.QSize(211, 31))
        self.pB_start.setObjectName("pB_start")
        self.gridLayout_2.addWidget(self.pB_start, 2, 1, 1, 1)

        self.pB_pause = QtWidgets.QPushButton(self.gBox_ea)
        self.pB_pause.setMinimumSize(QtCore.QSize(101, 31))
        #self.pB_pause.setMaximumSize(QtCore.QSize(101, 31))
        self.pB_pause.setObjectName("pB_pause")
        self.gridLayout_2.addWidget(self.pB_pause, 3, 0, 1, 1)

        self.pB_stop = QtWidgets.QPushButton(self.gBox_ea)
        self.pB_stop.setMinimumSize(QtCore.QSize(101, 31))
        #self.pB_stop.setMaximumSize(QtCore.QSize(101, 31))
        self.pB_stop.setObjectName("pB_stop")
        self.gridLayout_2.addWidget(self.pB_stop, 3, 1, 1, 1)

        self.gridLayout_3.addWidget(self.gBox_ea, 0, 0, 1, 1)
        self.gBox_visu = QtWidgets.QGroupBox(DrapeOptimizationManager)
        self.gBox_visu.setObjectName("gBox_visu")
        self.gridLayout = QtWidgets.QGridLayout(self.gBox_visu)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(201, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.checkBox_activated = QtWidgets.QCheckBox(self.gBox_visu)
        self.checkBox_activated.setObjectName("checkBox_activated")
        self.gridLayout.addWidget(self.checkBox_activated, 0, 1, 1, 1)

        self.tabWidget = QtWidgets.QTabWidget(self.gBox_visu)
        self.tabWidget.setObjectName("QTabWidget")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 3)
        self.gridLayout_3.addWidget(self.gBox_visu, 0, 1, 1, 1)

        self.prograssbar = QtWidgets.QProgressBar(self.gBox_visu)
        self.prograssbar.setObjectName("QPrograssBar")
        self.gridLayout.addWidget(self.prograssbar, 2, 0, 1, 3)

        self.prograssbar.setMaximum(100)
        self.prograssbar.setMinimum(0)
        self.prograssbar.setValue(0)
        self.retranslateUi(DrapeOptimizationManager)
        self.toolBox.setCurrentIndex(1)

        self.checkBox_activated.setChecked(True)
        QtCore.QMetaObject.connectSlotsByName(DrapeOptimizationManager)
        DrapeOptimizationManager.setTabOrder(self.pB_stop, self.pB_start)
        DrapeOptimizationManager.setTabOrder(self.pB_start, self.checkBox_activated)
        DrapeOptimizationManager.setTabOrder(self.checkBox_activated, self.tabWidget)
        DrapeOptimizationManager.setTabOrder(self.tabWidget, self.pB_pause)

    def retranslateUi(self, DrapeOptimizationManager):
        _translate = QtCore.QCoreApplication.translate
        DrapeOptimizationManager.setWindowTitle(_translate("DrapeOptimizationManager", "DrapeOptimizationManager"))
        self.gBox_ea.setTitle(_translate("DrapeOptimizationManager", "Evolutionary Algorithm"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_general), _translate("DrapeOptimizationManager", "Overview"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_ea_parameter), _translate("DrapeOptimizationManager", "Parameter EvolAlgo"))
        self.pB_update_info.setText(_translate("DrapeOptimizationManager", "Update Info"))
        self.pB_start.setText(_translate("DrapeOptimizationManager", "Start"))
        self.pB_init.setText(_translate("DrapeOptimizationManager", "Initialize"))
        self.pB_pause.setText(_translate("DrapeOptimizationManager", "Pause"))
        self.pB_stop.setText(_translate("DrapeOptimizationManager", "Stop"))
        self.gBox_visu.setTitle(_translate("DrapeOptimizationManager", "Visualization:"))
        self.checkBox_activated.setText(_translate("DrapeOptimizationManager", "Activated"))

