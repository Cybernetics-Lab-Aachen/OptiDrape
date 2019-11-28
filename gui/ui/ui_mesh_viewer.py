# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drapemeshwidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DrapeMeshWidget(object):
    def setupUi(self, DrapeMeshWidget):
        DrapeMeshWidget.setObjectName("DrapeMeshWidget")
        DrapeMeshWidget.resize(542, 402)
        self.gridLayout = QtWidgets.QGridLayout(DrapeMeshWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.mesh_info = QtWidgets.QLabel(DrapeMeshWidget)
        self.mesh_info.setObjectName("mesh_info")
        self.gridLayout.addWidget(self.mesh_info, 1, 0, 1, 0)

        self.retranslateUi(DrapeMeshWidget)
        QtCore.QMetaObject.connectSlotsByName(DrapeMeshWidget)

    def retranslateUi(self, DrapeMeshWidget):
        _translate = QtCore.QCoreApplication.translate
        DrapeMeshWidget.setWindowTitle(_translate("DrapeMeshWidget", "DrapeMeshWidget"))
        self.mesh_info.setText(_translate("DrapeMeshWidget", "TextLabel"))


