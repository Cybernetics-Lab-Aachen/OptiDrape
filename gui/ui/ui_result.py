# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Result.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Result(object):
    def setupUi(self, Ui_Result):
        Ui_Result.setObjectName("Ui_Result")
        Ui_Result.resize(943, 628)
        self.gridLayout = QtWidgets.QGridLayout(Ui_Result)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.gBox_info = QtWidgets.QGroupBox(Ui_Result)
        self.gBox_info.setMinimumSize(QtCore.QSize(261, 311))
        self.gBox_info.setMaximumSize(QtCore.QSize(261, 16777215))
        self.gBox_info.setObjectName("gBox_info")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gBox_info)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tB_text = QtWidgets.QTextBrowser(self.gBox_info)
        self.tB_text.setObjectName("tB_text")
        self.gridLayout_4.addWidget(self.tB_text, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_info, 0, 0, 1, 1)
        self.gBox_visu = QtWidgets.QGroupBox(Ui_Result)
        self.gBox_visu.setMinimumSize(QtCore.QSize(431, 601))
        self.gBox_visu.setObjectName("gBox_visu")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gBox_visu)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.gBox_visu)
        self.tabWidget.setObjectName("tabWidget")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.plot_widget = QtWidgets.QWidget()
        self.plot_widget.setMaximumHeight(300)
        self.plot_layout = QtWidgets.QVBoxLayout(self.plot_widget)
        self.gridLayout_3.addWidget(self.plot_widget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_visu, 0, 1, 2, 1)
        self.gBox_crtl = QtWidgets.QGroupBox(Ui_Result)
        self.gBox_crtl.setObjectName("gBox_crtl")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gBox_crtl)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.gBox_crtl)
        self.label.setMinimumSize(QtCore.QSize(91, 17))
        self.label.setMaximumSize(QtCore.QSize(91, 17))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.sB_iteration = QtWidgets.QSpinBox(self.gBox_crtl)
        self.sB_iteration.setMinimumSize(QtCore.QSize(91, 26))
        self.sB_iteration.setMaximumSize(QtCore.QSize(91, 26))
        self.sB_iteration.setObjectName("sB_iteration")
        self.gridLayout_2.addWidget(self.sB_iteration, 0, 1, 1, 1)
        self.pB_plot = QtWidgets.QPushButton(self.gBox_crtl)
        self.pB_plot.setObjectName("pB_plot")
        self.gridLayout_2.addWidget(self.pB_plot, 2, 0, 1, 1)
        self.bB_gen_mesh = QtWidgets.QPushButton(self.gBox_crtl)
        self.bB_gen_mesh.setObjectName("bB_gen_mesh")
        self.gridLayout_2.addWidget(self.bB_gen_mesh, 1, 1, 1, 1)
        self.pB_feature = QtWidgets.QPushButton(self.gBox_crtl)
        self.pB_feature.setObjectName("pB_feature")
        self.gridLayout_2.addWidget(self.pB_feature, 1, 0, 1, 1)
        self.pB_delete_tab = QtWidgets.QPushButton(self.gBox_crtl)
        self.pB_delete_tab.setObjectName("pB_delete_tab")
        self.gridLayout_2.addWidget(self.pB_delete_tab, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.gBox_crtl, 1, 0, 1, 1)

        self.retranslateUi(Ui_Result)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ui_Result)

    def retranslateUi(self, Ui_Result):
        _translate = QtCore.QCoreApplication.translate
        Ui_Result.setWindowTitle(_translate("Ui_Result", "Ui_Result"))
        self.gBox_info.setTitle(_translate("Ui_Result", "Information"))
        self.gBox_visu.setTitle(_translate("Ui_Result", "Result"))

        self.gBox_crtl.setTitle(_translate("Ui_Result", "Control"))
        self.label.setText(_translate("Ui_Result", "Iteration:"))
        self.pB_plot.setText(_translate("Ui_Result", "Plot Score"))
        self.bB_gen_mesh.setText(_translate("Ui_Result", "Show Mesh"))
        self.pB_feature.setText(_translate("Ui_Result", "Score Feature"))
        self.pB_delete_tab.setText(_translate("Ui_Result", "Delete Tab"))


