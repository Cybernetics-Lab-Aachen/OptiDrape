# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DrapeGeometryWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DrapeGeometryWidget(object):
    def setupUi(self, DrapeGeometryWidget):
        DrapeGeometryWidget.setObjectName("DrapeGeometryWidget")
        DrapeGeometryWidget.resize(626, 546)
        self.gridLayout = QtWidgets.QGridLayout(DrapeGeometryWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.mesh_name = QtWidgets.QLabel(DrapeGeometryWidget)
        self.mesh_name.setObjectName("mesh_name")
        self.gridLayout.addWidget(self.mesh_name, 0, 0, 1, 1)
        self.btn_split = QtWidgets.QPushButton(DrapeGeometryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_split.sizePolicy().hasHeightForWidth())
        self.btn_split.setSizePolicy(sizePolicy)
        self.btn_split.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btn_split.setObjectName("btn_split")
        self.gridLayout.addWidget(self.btn_split, 0, 1, 1, 1)
        self.btn_close = QtWidgets.QPushButton(DrapeGeometryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btn_close.setObjectName("btn_close")
        self.gridLayout.addWidget(self.btn_close, 0, 2, 1, 1)

        self.btn_update = QtWidgets.QPushButton(DrapeGeometryWidget)
        self.btn_update.setSizePolicy(sizePolicy)
        self.btn_update.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btn_update.setObjectName("btn_update")
        self.gridLayout.addWidget(self.btn_update, 0, 3, 1, 1)

        self.tabWidget = QtWidgets.QTabWidget(DrapeGeometryWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.process_tab = QtWidgets.QWidget()
        self.process_tab.setObjectName("process_tab")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.process_tab)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.process_name = QtWidgets.QLabel(self.process_tab)
        self.process_name.setObjectName("process_name")
        self.verticalLayout.addWidget(self.process_name)
        self.process_content = QtWidgets.QLabel(self.process_tab)
        self.process_content.setObjectName("process_content")
        self.verticalLayout.addWidget(self.process_content)
        self.progressBar = QtWidgets.QProgressBar(self.process_tab)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        #self.tabWidget.addTab(self.process_tab, "Process")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 4)
        #self.infoBrowser = QtWidgets.QTextBrowser(DrapeGeometryWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(1)
        #sizePolicy.setHeightForWidth(self.infoBrowser.sizePolicy().hasHeightForWidth())
        #self.infoBrowser.setSizePolicy(sizePolicy)
        #self.infoBrowser.setMaximumSize(QtCore.QSize(16777215, 50))
        #self.infoBrowser.setObjectName("infoBrowser")
        #self.gridLayout.addWidget(self.infoBrowser, 2, 0, 1, 3)

        self.retranslateUi(DrapeGeometryWidget)
        self.tabWidget.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(DrapeGeometryWidget)

    def retranslateUi(self, DrapeGeometryWidget):
        _translate = QtCore.QCoreApplication.translate
        DrapeGeometryWidget.setWindowTitle(_translate("DrapeGeometryWidget", "DrapeGeometryWidget"))
        self.mesh_name.setText(_translate("DrapeGeometryWidget", "TextLabel"))
        self.btn_split.setText(_translate("DrapeGeometryWidget", "Split"))
        self.btn_update.setText(_translate("DrapeGeometryWidget", "Update"))
        self.btn_close.setText(_translate("DrapeGeometryWidget", "Close"))
        self.process_name.setText(_translate("DrapeMeshWidget", "Noting processed"))
        self.process_content.setText(_translate("DrapeMeshWidget", "No Progress"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.process_tab), _translate("DrapeMeshWidget", "ProcessInfo"))

