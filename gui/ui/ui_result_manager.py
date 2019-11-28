# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_result_manager.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultManager(object):
    def setupUi(self, Ui_ResultManager):
        Ui_ResultManager.setObjectName("ui_result_manager")
        Ui_ResultManager.resize(761, 495)
        self.gridLayout = QtWidgets.QGridLayout(Ui_ResultManager)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tB_manager = QtWidgets.QToolBox(Ui_ResultManager)
        self.tB_manager.setObjectName("tB_manager")

        self.gridLayout.addWidget(self.tB_manager, 0, 0, 1, 1)

        self.retranslateUi(Ui_ResultManager)
        self.tB_manager.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ui_ResultManager)

    def retranslateUi(self, Ui_ResultManager):
        _translate = QtCore.QCoreApplication.translate
        Ui_ResultManager.setWindowTitle(_translate("Ui_ResultManager", "Ui_ResultManager"))


