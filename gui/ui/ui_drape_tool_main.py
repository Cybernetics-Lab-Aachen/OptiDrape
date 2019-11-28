# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DrapeMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DrapeToolMainWindow(object):
    def setupUi(self, DrapeTool):
        DrapeTool.setObjectName("DrapeMainWindow")
        DrapeTool.resize(801, 772)

        self.centralWidget = QtWidgets.QWidget(DrapeTool)
        self.centralWidget.setObjectName("centralWidget")

        self.gridLayout_main_window = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_main_window.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_main_window.setSpacing(6)
        self.gridLayout_main_window.setObjectName("gridLayout_main_window")

        self.gb_info = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.gb_info.sizePolicy().hasHeightForWidth())
        self.gb_info.setSizePolicy(sizePolicy)
        self.gb_info.setObjectName("gb_info")
        self.gb_info.hide()
        self.info_browser = QtWidgets.QTextBrowser(self.centralWidget)
        self.gb_gridLayout = QtWidgets.QGridLayout(self.gb_info)
        self.gb_gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gb_gridLayout.addWidget(self.info_browser)
        #self.gridLayout_main_window.addWidget(self.gb_info, 1, 0, 1, 1)

        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")

        self.gridLayout_main_window.addWidget(self.tabWidget, 0, 0, 1, 1)
        DrapeTool.setCentralWidget(self.centralWidget)

        self.statusBar = QtWidgets.QStatusBar(DrapeTool)
        self.statusBar.setObjectName("statusBar")
        #DrapeTool.setStatusBar(self.statusBar)

        self.action_New_Project = QtWidgets.QAction(DrapeTool)
        self.action_New_Project.setObjectName("action_New_Project")
        self.action_Load_Project = QtWidgets.QAction(DrapeTool)
        self.action_Load_Project.setObjectName("action_Load_Project")
        self.action_Close_current_Project = QtWidgets.QAction(DrapeTool)
        self.action_Close_current_Project.setObjectName("action_Close_current_Project")
        self.action_Exit = QtWidgets.QAction(DrapeTool)
        self.action_Exit.setObjectName("action_Exit")
        self.actionSettings = QtWidgets.QAction(DrapeTool)
        self.actionSettings.setObjectName("actionSettings")
        self.actionTools = QtWidgets.QAction(DrapeTool)
        self.actionTools.setObjectName("actionTools")

        self.retranslateUi(DrapeTool)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DrapeTool)

    def retranslateUi(self, DrapeMainWindow):
        _translate = QtCore.QCoreApplication.translate
        DrapeMainWindow.setWindowTitle(_translate("DrapeTool", "OptiDrapeTool"))
        self.gb_info.setTitle(_translate("DrapeMainWindow", "Information"))





"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrapeMainWindow = QtWidgets.QMainWindow()
    ui = Ui_DrapeToolMainWindow()
    ui.setupUi(DrapeMainWindow)
    DrapeMainWindow.show()
    sys.exit(app.exec_())

"""