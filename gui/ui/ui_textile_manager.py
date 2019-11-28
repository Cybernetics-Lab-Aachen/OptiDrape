# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_TextileManager.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Ui_TextileManager(object):
    def setupUi(self, TextileManager):
        TextileManager.setObjectName("TextileManager")
        TextileManager.resize(611, 792)

        self.gridLayout_7 = QtWidgets.QGridLayout(TextileManager)
        self.gridLayout_7.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gb_model_control = QtWidgets.QGroupBox(TextileManager)
        self.gb_model_control.setObjectName("gb_model_control")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_model_control)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeView_textile = QtWidgets.QTreeView(self.gb_model_control)
        self.treeView_textile.setMinimumSize(QtCore.QSize(201, 301))
        self.treeView_textile.setObjectName("treeView_textile")
        self.gridLayout_2.addWidget(self.treeView_textile, 0, 0, 8, 1)

        self.pb_new_dataset = QtWidgets.QPushButton(self.gb_model_control)
        self.pb_new_dataset.setMinimumSize(QtCore.QSize(101, 31))
        self.pb_new_dataset.setMaximumSize(QtCore.QSize(101, 31))
        self.pb_new_dataset.setObjectName("pb_new_dataset")
        self.gridLayout_2.addWidget(self.pb_new_dataset, 0, 1, 1, 1)

        self.pb_load_textile = QtWidgets.QPushButton(self.gb_model_control)
        self.pb_load_textile.setMinimumSize(QtCore.QSize(101, 31))
        self.pb_load_textile.setMaximumSize(QtCore.QSize(101, 31))
        self.pb_load_textile.setObjectName("pb_load_textile")
        self.gridLayout_2.addWidget(self.pb_load_textile, 1, 1, 1, 1)

        self.pb_add_textile = QtWidgets.QPushButton(self.gb_model_control)
        self.pb_add_textile.setMinimumSize(QtCore.QSize(101, 31))
        self.pb_add_textile.setMaximumSize(QtCore.QSize(101, 31))
        self.pb_add_textile.setObjectName("pb_add_textile")
        self.gridLayout_2.addWidget(self.pb_add_textile, 2, 1, 1, 1)

        self.pb_delete_textile = QtWidgets.QPushButton(self.gb_model_control)
        self.pb_delete_textile.setMinimumSize(QtCore.QSize(101, 31))
        self.pb_delete_textile.setMaximumSize(QtCore.QSize(101, 31))
        self.pb_delete_textile.setObjectName("pb_delete_textile")
        self.gridLayout_2.addWidget(self.pb_delete_textile, 4, 1, 1, 1)

        self.pb_save_textile = QtWidgets.QPushButton(self.gb_model_control)
        self.pb_save_textile.setMinimumSize(QtCore.QSize(102, 31))
        self.pb_save_textile.setMaximumSize(QtCore.QSize(102, 31))
        self.pb_save_textile.setObjectName("pb_save_textile")
        self.gridLayout_2.addWidget(self.pb_save_textile, 3, 1, 1, 1)


        self.gridLayout_7.addWidget(self.gb_model_control, 0, 0, 1, 1)
        self.gb_add_model = QtWidgets.QGroupBox(TextileManager)
        self.gb_add_model.setObjectName("gb_add_model")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gb_add_model)
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lb_textile_name = QtWidgets.QLabel(self.gb_add_model)
        self.lb_textile_name.setObjectName("lb_textile_name")
        self.gridLayout_4.addWidget(self.lb_textile_name, 0, 0, 1, 1)
        self.edit_textile_name = QtWidgets.QLineEdit(self.gb_add_model)
        self.edit_textile_name.setObjectName("edit_textile_name")
        self.gridLayout_4.addWidget(self.edit_textile_name, 0, 1, 1, 2)
        self.lb_variant = QtWidgets.QLabel(self.gb_add_model)
        self.lb_variant.setObjectName("lb_variant")
        self.gridLayout_4.addWidget(self.lb_variant, 1, 0, 1, 1)
        self.edit_variant_name = QtWidgets.QLineEdit(self.gb_add_model)
        self.edit_variant_name.setObjectName("edit_variant_name")
        self.gridLayout_4.addWidget(self.edit_variant_name, 1, 1, 1, 2)
        self.gb_e = QtWidgets.QGroupBox(self.gb_add_model)
        self.gb_e.setMaximumSize(QtCore.QSize(16777215, 100))
        self.gb_e.setObjectName("gb_e")
        self.gridLayout = QtWidgets.QGridLayout(self.gb_e)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.lb_Ex = QtWidgets.QLabel(self.gb_e)
        self.lb_Ex.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lb_Ex.setObjectName("lb_Ex")
        self.gridLayout.addWidget(self.lb_Ex, 0, 0, 1, 1)
        self.edit_Ex = QtWidgets.QLineEdit(self.gb_e)
        self.edit_Ex.setMinimumSize(QtCore.QSize(160, 25))
        self.edit_Ex.setObjectName("edit_Ex")
        self.gridLayout.addWidget(self.edit_Ex, 0, 1, 1, 1)
        self.lb_Ey = QtWidgets.QLabel(self.gb_e)
        self.lb_Ey.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lb_Ey.setObjectName("lb_Ey")
        self.gridLayout.addWidget(self.lb_Ey, 1, 0, 1, 1)
        self.edit_Ey = QtWidgets.QLineEdit(self.gb_e)
        self.edit_Ey.setMinimumSize(QtCore.QSize(71, 25))
        self.edit_Ey.setObjectName("edit_Ey")
        self.gridLayout.addWidget(self.edit_Ey, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.gb_e, 2, 0, 1, 3)
        self.gb_c = QtWidgets.QGroupBox(self.gb_add_model)
        self.gb_c.setMinimumSize(QtCore.QSize(211, 100))
        self.gb_c.setMaximumSize(QtCore.QSize(16777215, 100))
        self.gb_c.setObjectName("gb_c")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gb_c)
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lb_Cx = QtWidgets.QLabel(self.gb_c)
        self.lb_Cx.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lb_Cx.setObjectName("lb_Cx")
        self.gridLayout_3.addWidget(self.lb_Cx, 0, 0, 1, 1)
        self.edit_Cx = QtWidgets.QLineEdit(self.gb_c)
        self.edit_Cx.setObjectName("edit_Cx")
        self.gridLayout_3.addWidget(self.edit_Cx, 0, 1, 1, 1)
        self.lb_Cy = QtWidgets.QLabel(self.gb_c)
        self.lb_Cy.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lb_Cy.setObjectName("lb_Cy")
        self.gridLayout_3.addWidget(self.lb_Cy, 1, 0, 1, 1)
        self.edit_Cy = QtWidgets.QLineEdit(self.gb_c)
        self.edit_Cy.setObjectName("edit_Cy")
        self.gridLayout_3.addWidget(self.edit_Cy, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.gb_c, 3, 0, 1, 3)
        self.pb_save_variant = QtWidgets.QPushButton(self.gb_add_model)
        self.pb_save_variant.setMinimumSize(QtCore.QSize(101, 31))
        self.pb_save_variant.setMaximumSize(QtCore.QSize(101, 31))
        self.pb_save_variant.setObjectName("pb_save_variant")
        self.gridLayout_4.addWidget(self.pb_save_variant, 4, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(3, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 4, 1, 1, 1)
        self.pb_delete_variant = QtWidgets.QPushButton(self.gb_add_model)
        self.pb_delete_variant.setMinimumSize(QtCore.QSize(111, 31))
        self.pb_delete_variant.setMaximumSize(QtCore.QSize(111, 31))
        self.pb_delete_variant.setObjectName("pb_delete_variant")
        self.gridLayout_4.addWidget(self.pb_delete_variant, 4, 2, 1, 1)
        self.gridLayout_7.addWidget(self.gb_add_model, 0, 1, 1, 1)
        self.gb_model_raw = QtWidgets.QGroupBox(TextileManager)
        self.gb_model_raw.setObjectName("gb_model_raw")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.gb_model_raw)
        self.gridLayout_9.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gb_cell = QtWidgets.QGroupBox(self.gb_model_raw)
        self.gb_cell.setMaximumSize(QtCore.QSize(16777215, 69))
        self.gb_cell.setObjectName("gb_cell")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.gb_cell)
        self.gridLayout_8.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lb_x = QtWidgets.QLabel(self.gb_cell)
        self.lb_x.setObjectName("lb_x")
        self.gridLayout_8.addWidget(self.lb_x, 0, 0, 1, 1)
        self.lineEdit_x = QtWidgets.QLineEdit(self.gb_cell)
        self.lineEdit_x.setObjectName("lineEdit_x")
        self.gridLayout_8.addWidget(self.lineEdit_x, 0, 1, 1, 1)
        self.lb_y = QtWidgets.QLabel(self.gb_cell)
        self.lb_y.setObjectName("lb_y")
        self.gridLayout_8.addWidget(self.lb_y, 0, 2, 1, 1)
        self.lineEdit_y = QtWidgets.QLineEdit(self.gb_cell)
        self.lineEdit_y.setObjectName("lineEdit_y")
        self.gridLayout_8.addWidget(self.lineEdit_y, 0, 3, 1, 1)
        self.pb_save_cell = QtWidgets.QPushButton(self.gb_cell)
        self.pb_save_cell.setMinimumSize(QtCore.QSize(80, 25))
        self.pb_save_cell.setMaximumSize(QtCore.QSize(80, 25))
        self.pb_save_cell.setObjectName("pb_save_cell")
        self.gridLayout_8.addWidget(self.pb_save_cell, 0, 4, 1, 1)
        self.pb_del_cell = QtWidgets.QPushButton(self.gb_cell)
        self.pb_del_cell.setMinimumSize(QtCore.QSize(80, 25))
        self.pb_del_cell.setMaximumSize(QtCore.QSize(80, 25))
        self.pb_del_cell.setObjectName("pb_del_cell")
        self.gridLayout_8.addWidget(self.pb_del_cell, 0, 5, 1, 1)
        self.gridLayout_9.addWidget(self.gb_cell, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.gb_model_raw)
        self.tabWidget.setObjectName("tabWidget")

        # tab property
        self.property = QtWidgets.QWidget()
        self.property.setObjectName("property")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.property)
        self.gridLayout_14.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_14.setSpacing(6)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gb_material = QtWidgets.QGroupBox(self.property)
        self.gb_material.setMaximumSize(QtCore.QSize(16777215, 71))
        self.gb_material.setObjectName("gb_material")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.gb_material)
        self.gridLayout_10.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.cBox_material = QtWidgets.QComboBox(self.gb_material)
        self.cBox_material.setObjectName("cBox_material")
        self.cBox_material.addItem("")
        self.cBox_material.addItem("")
        self.cBox_material.addItem("")
        self.gridLayout_10.addWidget(self.cBox_material, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.gb_material, 0, 0, 1, 1)
        self.gb_art = QtWidgets.QGroupBox(self.property)
        self.gb_art.setMaximumSize(QtCore.QSize(16777215, 71))
        self.gb_art.setObjectName("gb_art")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.gb_art)
        self.gridLayout_11.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_11.setSpacing(6)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.cBox_art = QtWidgets.QComboBox(self.gb_art)
        self.cBox_art.setObjectName("cBox_art")
        self.cBox_art.addItem("")
        self.cBox_art.addItem("")
        self.cBox_art.addItem("")
        self.gridLayout_11.addWidget(self.cBox_art, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.gb_art, 0, 1, 1, 1)
        self.gb_binding = QtWidgets.QGroupBox(self.property)
        self.gb_binding.setMaximumSize(QtCore.QSize(16777215, 71))
        self.gb_binding.setObjectName("gb_binding")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.gb_binding)
        self.gridLayout_12.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.cBox_binding = QtWidgets.QComboBox(self.gb_binding)
        self.cBox_binding.setObjectName("cBox_binding")
        self.cBox_binding.addItem("")
        self.cBox_binding.addItem("")
        self.cBox_binding.addItem("")
        self.cBox_binding.addItem("")
        self.cBox_binding.addItem("")
        self.cBox_binding.addItem("")

        self.cBox_binding.addItem("")
        self.gridLayout_12.addWidget(self.cBox_binding, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.gb_binding, 0, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.property)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_13.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_13.setSpacing(6)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_13.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_angle = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_angle.setMinimumSize(QtCore.QSize(348, 25))
        self.lineEdit_angle.setObjectName("lineEdit_angle")
        self.gridLayout_13.addWidget(self.lineEdit_angle, 0, 1, 2, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_13.addWidget(self.label_2, 1, 0, 2, 1)
        self.lineEdit_tension = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_tension.setMinimumSize(QtCore.QSize(348, 25))
        self.lineEdit_tension.setObjectName("lineEdit_tension")
        self.gridLayout_13.addWidget(self.lineEdit_tension, 2, 1, 1, 1)
        self.gridLayout_14.addWidget(self.groupBox, 1, 0, 1, 3)
        self.tabWidget.addTab(self.property, "")

        # tab roving

        self.Shear = QtWidgets.QWidget()
        self.Shear.setObjectName("Shear")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.Shear)
        self.gridLayout_18.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_18.setSpacing(6)
        self.gridLayout_18.setObjectName("gridLayout_18")

        self.gBox_Roving = QtWidgets.QGroupBox(self.Shear)
        self.gBox_Roving.setMinimumSize(QtCore.QSize(181, 181))
        self.gBox_Roving.setMaximumSize(QtCore.QSize(181, 181))
        self.gBox_Roving.setObjectName("gBox_Roving")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.gBox_Roving)
        self.gridLayout_15.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_15.setSpacing(6)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.lb_rx = QtWidgets.QLabel(self.gBox_Roving)
        self.lb_rx.setObjectName("lb_rx")
        self.gridLayout_15.addWidget(self.lb_rx, 0, 0, 1, 1)
        self.lineEdit_rx = QtWidgets.QLineEdit(self.gBox_Roving)
        self.lineEdit_rx.setObjectName("lineEdit_rx")
        self.gridLayout_15.addWidget(self.lineEdit_rx, 0, 1, 1, 1)
        self.lb_ry = QtWidgets.QLabel(self.gBox_Roving)
        self.lb_ry.setObjectName("lb_ry")
        self.gridLayout_15.addWidget(self.lb_ry, 1, 0, 1, 1)
        self.lineEdit_ry = QtWidgets.QLineEdit(self.gBox_Roving)
        self.lineEdit_ry.setObjectName("lineEdit_ry")
        self.gridLayout_15.addWidget(self.lineEdit_ry, 1, 1, 1, 1)
        self.lb_rz = QtWidgets.QLabel(self.gBox_Roving)
        self.lb_rz.setObjectName("lb_rz")
        self.gridLayout_15.addWidget(self.lb_rz, 2, 0, 1, 1)
        self.lineEdit_rz = QtWidgets.QLineEdit(self.gBox_Roving)
        self.lineEdit_rz.setObjectName("lineEdit_rz")
        self.gridLayout_15.addWidget(self.lineEdit_rz, 2, 1, 1, 1)
        self.lb_cross = QtWidgets.QLabel(self.gBox_Roving)
        self.lb_cross.setObjectName("lb_cross")
        self.gridLayout_15.addWidget(self.lb_cross, 3, 0, 1, 2)
        self.lineEdit_cross = QtWidgets.QLineEdit(self.gBox_Roving)
        self.lineEdit_cross.setObjectName("lineEdit_cross")
        self.gridLayout_15.addWidget(self.lineEdit_cross, 4, 0, 1, 2)
        self.gridLayout_18.addWidget(self.gBox_Roving, 0, 0, 2, 1)
        self.gBox_Cell = QtWidgets.QGroupBox(self.Shear)
        self.gBox_Cell.setMinimumSize(QtCore.QSize(181, 131))
        self.gBox_Cell.setMaximumSize(QtCore.QSize(181, 131))
        self.gBox_Cell.setObjectName("gBox_Cell")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.gBox_Cell)
        self.gridLayout_16.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_16.setSpacing(6)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.lb_x_celldata = QtWidgets.QLabel(self.gBox_Cell)
        self.lb_x_celldata.setObjectName("lb_x_celldata")
        self.gridLayout_16.addWidget(self.lb_x_celldata, 0, 0, 1, 1)
        self.lineEdit_cellx = QtWidgets.QLineEdit(self.gBox_Cell)
        self.lineEdit_cellx.setObjectName("lineEdit_cellx")
        self.gridLayout_16.addWidget(self.lineEdit_cellx, 0, 1, 1, 1)
        self.lb_y_celldata = QtWidgets.QLabel(self.gBox_Cell)
        self.lb_y_celldata.setObjectName("lb_y_celldata")
        self.gridLayout_16.addWidget(self.lb_y_celldata, 1, 0, 1, 1)
        self.lineEdit_celly = QtWidgets.QLineEdit(self.gBox_Cell)
        self.lineEdit_celly.setObjectName("lineEdit_celly")
        self.gridLayout_16.addWidget(self.lineEdit_celly, 1, 1, 1, 1)
        self.lb_z_celldata = QtWidgets.QLabel(self.gBox_Cell)
        self.lb_z_celldata.setObjectName("lb_z_celldata")
        self.gridLayout_16.addWidget(self.lb_z_celldata, 2, 0, 1, 1)
        self.lineEdit_cellz = QtWidgets.QLineEdit(self.gBox_Cell)
        self.lineEdit_cellz.setObjectName("lineEdit_cellz")
        self.gridLayout_16.addWidget(self.lineEdit_cellz, 2, 1, 1, 1)
        self.gridLayout_18.addWidget(self.gBox_Cell, 0, 1, 1, 1)
        self.gBox_quer = QtWidgets.QGroupBox(self.Shear)
        self.gBox_quer.setObjectName("gBox_quer")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.gBox_quer)
        self.gridLayout_17.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_17.setSpacing(6)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.lb_qx = QtWidgets.QLabel(self.gBox_quer)
        self.lb_qx.setObjectName("lb_qx")
        self.gridLayout_17.addWidget(self.lb_qx, 0, 0, 1, 1)
        self.lineEdit_qx = QtWidgets.QLineEdit(self.gBox_quer)
        self.lineEdit_qx.setReadOnly(True)
        self.lineEdit_qx.setObjectName("lineEdit_qx")
        self.gridLayout_17.addWidget(self.lineEdit_qx, 0, 1, 1, 1)
        self.lb_qy = QtWidgets.QLabel(self.gBox_quer)
        self.lb_qy.setObjectName("lb_qy")
        self.gridLayout_17.addWidget(self.lb_qy, 1, 0, 1, 1)
        self.lineEdit_qy = QtWidgets.QLineEdit(self.gBox_quer)
        self.lineEdit_qy.setReadOnly(True)
        self.lineEdit_qy.setObjectName("lineEdit_qy")
        self.gridLayout_17.addWidget(self.lineEdit_qy, 1, 1, 1, 1)
        self.gridLayout_18.addWidget(self.gBox_quer, 0, 2, 1, 1)
        self.pB_calc_querstress = QtWidgets.QPushButton(self.Shear)
        self.pB_calc_querstress.setObjectName("pushButton")
        self.pB_calc_querstress.setMinimumSize(QtCore.QSize(151, 25))
        self.pB_calc_querstress.setMaximumSize(QtCore.QSize(151, 25))
        self.gridLayout_18.addWidget(self.pB_calc_querstress, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_18.addItem(spacerItem5, 1, 2, 1, 2)
        self.pB_save_querstress = QtWidgets.QPushButton(self.Shear)
        self.pB_save_querstress.setMinimumSize(QtCore.QSize(151, 25))
        self.pB_save_querstress.setMaximumSize(QtCore.QSize(151, 25))
        self.pB_save_querstress.setObjectName("pushButton_2")
        self.gridLayout_18.addWidget(self.pB_save_querstress, 1, 2, 1, 1)
        self.tabWidget.addTab(self.Shear, "")

        # tab x
        self.x = QtWidgets.QWidget()
        self.x.setObjectName("x")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.x)
        self.gridLayout_6.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.table_x = QtWidgets.QTableWidget(self.x)
        self.table_x.setObjectName("tableView_x")
        self.gridLayout_6.addWidget(self.table_x, 0, 0, 1, 1)
        self.tabWidget.addTab(self.x, "")

        # tab y
        self.y = QtWidgets.QWidget()
        self.y.setObjectName("y")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.y)
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.table_y = QtWidgets.QTableWidget(self.y)
        self.table_y.setObjectName("tableView_y")
        self.gridLayout_5.addWidget(self.table_y, 0, 0, 1, 1)
        self.tabWidget.addTab(self.y, "")

        # tab data fitting

        self.tab_fitting = QtWidgets.QWidget()
        self.tab_fitting.setObjectName("tab")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.tab_fitting)
        self.gridLayout_20.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_20.setSpacing(6)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.gBox_data2fit = QtWidgets.QGroupBox(self.tab_fitting)
        self.gBox_data2fit.setMinimumSize(QtCore.QSize(251, 131))
        self.gBox_data2fit.setMaximumSize(QtCore.QSize(251, 131))
        self.gBox_data2fit.setObjectName("gBox_data2fit")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.gBox_data2fit)
        self.gridLayout_19.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_19.setSpacing(6)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.label_3 = QtWidgets.QLabel(self.gBox_data2fit)
        self.label_3.setObjectName("label_3")
        self.gridLayout_19.addWidget(self.label_3, 0, 0, 1, 1)
        self.comboBox_data_x = QtWidgets.QComboBox(self.gBox_data2fit)
        self.comboBox_data_x.setMinimumSize(QtCore.QSize(92, 25))
        self.comboBox_data_x.setMaximumSize(QtCore.QSize(92, 25))
        self.comboBox_data_x.setObjectName("comboBox_data_x")
        self.comboBox_data_x.addItem("")
        self.comboBox_data_x.addItem("")
        self.comboBox_data_x.addItem("")
        self.gridLayout_19.addWidget(self.comboBox_data_x, 0, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.gBox_data2fit)
        self.label_4.setObjectName("label_4")
        self.gridLayout_19.addWidget(self.label_4, 0, 3, 1, 1)
        self.comboBox_data_y = QtWidgets.QComboBox(self.gBox_data2fit)
        self.comboBox_data_y.setMinimumSize(QtCore.QSize(93, 25))
        self.comboBox_data_y.setMaximumSize(QtCore.QSize(93, 25))
        self.comboBox_data_y.setObjectName("comboBox_data_y")
        self.comboBox_data_y.addItem("")
        self.comboBox_data_y.addItem("")
        self.comboBox_data_y.addItem("")
        self.comboBox_data_y.addItem("")
        self.comboBox_data_y.addItem("")
        self.gridLayout_19.addWidget(self.comboBox_data_y, 0, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gBox_data2fit)
        self.label_5.setObjectName("label_5")
        self.gridLayout_19.addWidget(self.label_5, 1, 0, 1, 2)
        self.spinBox_deg = QtWidgets.QSpinBox(self.gBox_data2fit)
        self.spinBox_deg.setProperty("value", 5)
        self.spinBox_deg.setObjectName("spinBox_deg")
        self.gridLayout_19.addWidget(self.spinBox_deg, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gBox_data2fit)
        self.label_6.setObjectName("label_6")
        self.gridLayout_19.addWidget(self.label_6, 2, 0, 1, 2)
        self.hSlider_plot = QtWidgets.QSlider(self.gBox_data2fit)
        self.hSlider_plot.setMaximum(10)
        self.hSlider_plot.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider_plot.setObjectName("horizontalSlider")
        self.gridLayout_19.addWidget(self.hSlider_plot, 2, 2, 1, 3)
        self.gridLayout_20.addWidget(self.gBox_data2fit, 0, 0, 1, 1)
        self.Widget_data_plot = QtWidgets.QWidget(self.tab_fitting)
        self.Widget_data_plot.setObjectName("Widget_data_plot")

        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)

        _layout = QtWidgets.QVBoxLayout()
        _layout.addWidget(self.plot_canvas, alignment=QtCore.Qt.AlignCenter)
        self.Widget_data_plot.setLayout(_layout)

        self.gridLayout_20.addWidget(self.Widget_data_plot, 0, 1, 2, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_fitting)
        self.groupBox_2.setMinimumSize(QtCore.QSize(251, 69))
        self.groupBox_2.setMaximumSize(QtCore.QSize(251, 69))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_14.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_14.setSpacing(6)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_14.addWidget(self.label_7, 0, 0, 1, 1)
        self.lineEdit_new_data = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_new_data.setObjectName("lineEdit_new_data")
        self.gridLayout_14.addWidget(self.lineEdit_new_data, 0, 1, 1, 1)
        self.pB_insert_data = QtWidgets.QPushButton(self.groupBox_2)
        self.pB_insert_data.setObjectName("pB_insert_data")
        self.gridLayout_14.addWidget(self.pB_insert_data, 0, 2, 1, 1)
        self.gridLayout_20.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_fitting, "")

        self.gridLayout_9.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.gridLayout_7.addWidget(self.gb_model_raw, 1, 0, 1, 2)

        self.retranslateUi(TextileManager)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TextileManager)

    def retranslateUi(self, TextileManager):
        _translate = QtCore.QCoreApplication.translate
        TextileManager.setWindowTitle(_translate("TextileManager", "TextileManager"))
        self.gb_model_control.setTitle(_translate("TextileManager", "Textile Manager"))
        self.pb_new_dataset.setText(_translate("TextileManager", "New Dataset"))
        #self.pb_drop_database.setText(_translate("TextileManager", "Save Dataset"))
        self.pb_load_textile.setText(_translate("TextileManager", "Load Textile"))
        self.pb_add_textile.setText(_translate("TextileManager", "Add Textile"))
        self.pb_delete_textile.setText(_translate("TextileManager", "Delete Textile"))
        self.pb_save_textile.setText(_translate("TextileManager", "Save Textile"))
        self.gb_add_model.setTitle(_translate("TextileManager", "Textile Model"))
        self.lb_textile_name.setText(_translate("TextileManager", "Textile Name:"))
        self.lb_variant.setText(_translate("TextileManager", "Variant Name:"))
        self.gb_e.setTitle(_translate("TextileManager", "Global Tensile Stiffness [GPa]:"))
        self.lb_Ex.setText(_translate("TextileManager", "Ex:"))
        self.lb_Ey.setText(_translate("TextileManager", "Ey:"))
        self.gb_c.setTitle(_translate("TextileManager", "Global Bending Stiffness [Nm²]:"))
        self.lb_Cx.setText(_translate("TextileManager", "Cx:"))
        self.lb_Cy.setText(_translate("TextileManager", "Cy:"))
        self.pb_save_variant.setText(_translate("TextileManager", "Save Variant"))
        self.pb_delete_variant.setText(_translate("TextileManager", "Delete Variant"))
        self.gb_model_raw.setTitle(_translate("TextileManager", "Model Raw Data"))
        self.gb_cell.setTitle(_translate("TextileManager", "Elementary Cell [mm]:"))
        self.lb_x.setText(_translate("TextileManager", "x:"))
        self.lb_y.setText(_translate("TextileManager", "y:"))
        self.pb_save_cell.setText(_translate("TextileManager", "Save"))
        self.pb_del_cell.setText(_translate("TextileManager", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.property), _translate("TextileManager", "Property"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.x), _translate("TextileManager", "X"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.y), _translate("TextileManager", "Y"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Shear), _translate("TextileManager", "Roving"))
        self.gb_material.setTitle(_translate("TextileManager", "Material:"))
        self.cBox_material.setItemText(0, _translate("TextileManager", "Not specified"))
        self.cBox_material.setItemText(1, _translate("TextileManager", "Glas"))
        self.cBox_material.setItemText(2, _translate("TextileManager", "Carbon"))
        self.gb_art.setTitle(_translate("TextileManager", "Textile Type:"))
        self.cBox_art.setItemText(0, _translate("TextileManager", "Not specified"))
        self.cBox_art.setItemText(1, _translate("TextileManager", "Gelege"))
        self.cBox_art.setItemText(2, _translate("TextileManager", "Gewebe"))
        self.gb_binding.setTitle(_translate("TextileManager", "Binding:"))
        self.cBox_binding.setItemText(0, _translate("TextileManager", "Not specified"))
        self.cBox_binding.setItemText(1, _translate("TextileManager", "0/90"))
        self.cBox_binding.setItemText(2, _translate("TextileManager", "+/-45"))
        self.cBox_binding.setItemText(3, _translate("TextileManager", "Leinwand"))
        self.cBox_binding.setItemText(4, _translate("TextileManager", "Köper"))
        self.cBox_binding.setItemText(5, _translate("TextileManager", "Kreuzköper"))
        self.cBox_binding.setItemText(6, _translate("TextileManager", "2/2-Köper"))
        self.groupBox.setTitle(_translate("TextileManager", "Critical Properties:"))
        self.label.setText(_translate("TextileManager", "Critical Shear Angle [ ° ]:"))
        self.label_2.setText(_translate("TextileManager", "Critical Tension [N/mm²]:"))
        self.gBox_Roving.setTitle(_translate("TextileManager", "RovingData:"))
        self.lb_rx.setText(_translate("TextileManager", "rx:[mm]"))
        self.lb_ry.setText(_translate("TextileManager", "ry:[mm]"))
        self.lb_rz.setText(_translate("TextileManager", "rz:[mm]"))
        self.lb_cross.setText(_translate("TextileManager", "cross-section: [mm²]"))
        self.gBox_Cell.setTitle(_translate("TextileManager", "CellData:"))
        self.lb_x_celldata.setText(_translate("TextileManager", "x:[mm]"))
        self.lb_y_celldata.setText(_translate("TextileManager", "y:[mm]"))
        self.lb_z_celldata.setText(_translate("TextileManager", "z:[mm]"))
        self.gBox_quer.setTitle(_translate("TextileManager", "QuerStress"))
        self.lb_qx.setText(_translate("TextileManager", "q(kx):"))
        self.lb_qy.setText(_translate("TextileManager", "q(ky):"))
        self.pB_calc_querstress.setText(_translate("TextileManager", "Calculate QuerStress"))
        self.pB_save_querstress.setText(_translate("TextileManager", "Save QuerStress"))
        
        self.gBox_data2fit.setTitle(_translate("TextileManager", "Data2Fit:"))
        self.label_3.setText(_translate("TextileManager", "x:"))
        self.comboBox_data_x.setItemText(0, _translate("TextileManager", "Unknown"))
        self.comboBox_data_x.setItemText(1, _translate("TextileManager", "X"))
        self.comboBox_data_x.setItemText(2, _translate("TextileManager", "Y"))
        self.label_4.setText(_translate("TextileManager", "y:"))
        self.comboBox_data_y.setItemText(0, _translate("TextileManager", "Unknown"))
        self.comboBox_data_y.setItemText(1, _translate("TextileManager", "Ex"))
        self.comboBox_data_y.setItemText(2, _translate("TextileManager", "Ey"))
        self.comboBox_data_y.setItemText(3, _translate("TextileManager", "Cx"))
        self.comboBox_data_y.setItemText(4, _translate("TextileManager", "Cy"))
        self.label_5.setText(_translate("TextileManager", "deg:"))
        self.label_6.setText(_translate("TextileManager", "plot_x:"))
        self.groupBox_2.setTitle(_translate("TextileManager", "InsertData"))
        self.label_7.setText(_translate("TextileManager", "new_x:"))
        self.pB_insert_data.setText(_translate("TextileManager", "Insert Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fitting), _translate("TextileManager", "Fitting"))


