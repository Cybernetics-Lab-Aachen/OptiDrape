# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'optidrape_main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DataBaseManager(object):
    def setupUi(self, DataBaseManager):
        # the main window widget - dbmanager
        DataBaseManager.setObjectName("DataBaseManager")
        DataBaseManager.resize(679, 745)


        """
        self.gbox_connection = QtWidgets.QGroupBox()

        self.le_dburl_input = QtWidgets.QLineEdit()
        self.le_dburl_input.setObjectName("le_dburl_input")

        self.label_url = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_url.setFont(font)
        self.label_url.setObjectName("label_url")

        self.pB_connect_db = QtWidgets.QPushButton()
        self.pB_connect_db.setFont(font)
        self.pB_connect_db.setObjectName("pB_connect_db")
        self.pB_connect_db.setMaximumHeight(self.le_dburl_input.height())

        self.pB_disconnect_db = QtWidgets.QPushButton()
        self.pB_disconnect_db.setFont(font)
        self.pB_disconnect_db.setObjectName("pB_disconnect_db")
        self.pB_disconnect_db.setDisabled(True)
        self.pB_disconnect_db.setMaximumHeight(self.le_dburl_input.height())

        self.pB_load_db = QtWidgets.QPushButton()
        self.pB_load_db.setFont(font)
        self.pB_load_db.setObjectName("pB_load_db")
        self.pB_load_db.setDisabled(True)
        self.pB_load_db.setMaximumHeight(self.le_dburl_input.height())

        self.cBox_databases = QtWidgets.QComboBox()
        self.cBox_databases.setFont(font)
        self.cBox_databases.setObjectName("cBox_databases")
        self.cBox_databases.addItem("")
        self.cBox_databases.setMaximumHeight(self.le_dburl_input.height())

        self.label_db = QtWidgets.QLabel()
        self.label_db.setFont(font)
        self.label_db.setObjectName("label_db")

        self.pB_set_db = QtWidgets.QPushButton()
        self.pB_set_db.setFont(font)
        self.pB_set_db.setObjectName("pB_set_db")
        self.pB_set_db.setDisabled(True)
        self.pB_set_db.setMaximumHeight(self.le_dburl_input.height())

        self.pB_delete_db = QtWidgets.QPushButton()
        self.pB_delete_db.setDisabled(True)
        self.pB_delete_db.setFont(font)
        self.pB_delete_db.setObjectName("pB_delete_db")
        self.pB_delete_db.setMaximumHeight(self.le_dburl_input.height())

        self.pB_export_db = QtWidgets.QPushButton()
        self.pB_export_db.setDisabled(True)
        self.pB_export_db.setFont(font)
        self.pB_export_db.setObjectName("pB_export_db")
        self.pB_export_db.setDisabled(True)
        self.pB_export_db.setMaximumHeight(self.le_dburl_input.height())

        self.pB_refresh_db = QtWidgets.QPushButton()
        self.pB_refresh_db.setFont(font)
        self.pB_refresh_db.setObjectName("pB_refresh_db")
        self.pB_refresh_db.setDisabled(True)
        self.pB_refresh_db.setMaximumHeight(self.le_dburl_input.height())

        self.pB_import_files = QtWidgets.QPushButton()
        self.pB_import_files.setFont(font)
        self.pB_import_files.setObjectName("pB_import_files")
        self.pB_import_files.setDisabled(True)
        self.pB_import_files.setMaximumHeight(self.le_dburl_input.height())
        """

        self.gBox_db = QtWidgets.QGroupBox(DataBaseManager)
        self.gBox_db.setGeometry(QtCore.QRect(20, 20, 691, 71))
        self.gBox_db.setMinimumSize(QtCore.QSize(0, 71))
        self.gBox_db.setMaximumSize(QtCore.QSize(16777215, 71))
        self.gBox_db.setObjectName("gBox_db")
        self.gridLayout = QtWidgets.QGridLayout(self.gBox_db)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_load_simulation = QtWidgets.QPushButton(self.gBox_db)
        self.pb_load_simulation.setMinimumSize(QtCore.QSize(121, 31))
        self.pb_load_simulation.setMaximumSize(QtCore.QSize(121, 31))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.pb_load_simulation.setFont(font)
        self.pb_load_simulation.setObjectName("pb_load_simulation")
        self.gridLayout.addWidget(self.pb_load_simulation, 0, 1, 1, 1)
        self.pb_load_geometry = QtWidgets.QPushButton(self.gBox_db)
        self.pb_load_geometry.setMinimumSize(QtCore.QSize(121, 31))
        self.pb_load_geometry.setMaximumSize(QtCore.QSize(121, 31))
        self.pb_load_geometry.setObjectName("pb_load_geometry")
        self.gridLayout.addWidget(self.pb_load_geometry, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(410, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)

        self.gBox_viewer = QtWidgets.QGroupBox(DataBaseManager)
        self.gBox_viewer.setObjectName("gBox_viewer")
        self.gBox_viewer.setDisabled(True)
        self.tree_viewer_geo = QtWidgets.QTreeView()
        self.tree_viewer_geo.setObjectName("tree_db_viewer")
        self.tree_viewer_geo.setMinimumWidth(0)
        self.tree_viewer_geo.setMaximumWidth(200)

        self.label_tree_geo = QtWidgets.QLabel()
        self.label_tree_geo.setFont(font)
        self.label_tree_geo.setObjectName("label_tree_geo")

        self.label_tree_sim = QtWidgets.QLabel()
        self.label_tree_sim.setFont(font)
        self.label_tree_sim.setObjectName("label_tree_sim")

        self.tree_viewer_sim = QtWidgets.QTreeView()
        self.tree_viewer_sim.setObjectName("tree_db_viewer")
        self.tree_viewer_sim.setMinimumWidth(0)
        self.tree_viewer_sim.setMaximumWidth(200)

        self.widget_db_viewer = QtWidgets.QTabWidget()

        self.widget_db_viewer.setObjectName("widget_db_viewer")
        #self.checkBox_rotate = QtWidgets.QCheckBox(self.gBox_viewer)
        #self.checkBox_rotate.setGeometry(QtCore.QRect(530, 0, 141, 20))
        #self.checkBox_rotate.setObjectName("checkBox_rotate")

        self.action_New_Project = QtWidgets.QAction(DataBaseManager)
        self.action_New_Project.setObjectName("action_New_Project")
        self.action_Load_Project = QtWidgets.QAction(DataBaseManager)
        self.action_Load_Project.setObjectName("action_Load_Project")
        self.action_Close_current_Project = QtWidgets.QAction(DataBaseManager)
        self.action_Close_current_Project.setObjectName("action_Close_current_Project")
        self.action_Exit = QtWidgets.QAction(DataBaseManager)
        self.action_Exit.setObjectName("action_Exit")
        self.actionSettings = QtWidgets.QAction(DataBaseManager)
        self.actionSettings.setObjectName("actionSettings")
        self.actionTools = QtWidgets.QAction(DataBaseManager)
        self.actionTools.setObjectName("actionTools")

        # organize gbox_connection and gbox_viewer layout
        # self.central_widget_layout = QtWidgets.QVBoxLayout(self.centralWidget)
        # # self.central_widget_layout.setContentsMargins(10,50,10,600)
        # # self.central_widget_layout.setSizeConstraint()
        # self.central_widget_layout.addWidget(self.label,0,QtCore.Qt.AlignTop)
        # self.central_widget_layout.addWidget(self.gbox_connection)

        self.central_widget_layout = QtWidgets.QGridLayout(DataBaseManager)
        self.central_widget_layout.setSpacing(2)
        self.central_widget_layout.addWidget(self.gBox_db, 1, 0, 1, 1)
        self.central_widget_layout.addWidget(self.gBox_viewer, 0, 0, 1, 1)

        """"
        self.gbox_connection_layout = QtWidgets.QGridLayout(self.gbox_connection)
        self.gbox_connection_layout.setSpacing(10)
        self.gbox_connection_layout.addWidget(self.label_url, 0, 0, 1, 1)
        self.gbox_connection_layout.addWidget(self.le_dburl_input, 0, 1, 1, 7)
        self.gbox_connection_layout.addWidget(self.pB_connect_db, 0, 8, 1, 1)
        self.gbox_connection_layout.addWidget(self.pB_disconnect_db, 0, 9, 1, 1)
        self.gbox_connection_layout.addWidget(self.label_db, 1, 0, 1, 1)
        self.gbox_connection_layout.addWidget(self.cBox_databases, 1, 1, 1, 7)
        self.gbox_connection_layout.addWidget(self.pB_set_db, 1, 8, 1, 1)
        self.gbox_connection_layout.addWidget(self.pB_delete_db, 1, 9, 1, 1)
        self.gbox_connection_layout.addWidget(self.pB_refresh_db, 2, 0, 1, 1)
        self.gbox_connection_layout.addWidget(self.pB_import_files, 2, 1, 1, 1)
        self.gbox_connection_layout.addWidget(self.pB_load_db, 2, 2, 1, 1)
        self.gbox_connection_layout.addWidget(self.pB_export_db, 2, 3, 1, 1)
        """
        self.gbox_viewer_layout = QtWidgets.QGridLayout(self.gBox_viewer)
        self.gbox_viewer_layout.setSpacing(2)
        self.gbox_viewer_layout.addWidget(self.label_tree_geo, 2, 0, 1, 1)
        self.gbox_viewer_layout.addWidget(self.tree_viewer_geo, 3, 0, 1, 1)
        self.gbox_viewer_layout.addWidget(self.label_tree_sim, 0, 0, 1, 1)
        self.gbox_viewer_layout.addWidget(self.tree_viewer_sim, 1, 0, 1, 1)
        self.gbox_viewer_layout.addWidget(self.widget_db_viewer, 0, 1, 4, 1)


        self.retranslateUi(DataBaseManager)
        QtCore.QMetaObject.connectSlotsByName(DataBaseManager)

    def retranslateUi(self, DataBaseManager):
        _translate = QtCore.QCoreApplication.translate
        DataBaseManager.setWindowTitle(_translate("DataBaseManager", "OptiDrape_Main"))
        """
        self.gbox_connection.setTitle(_translate("DataBaseManager", "Connection"))
        self.le_dburl_input.setText(_translate("DataBaseManager", "mongodb://localhost:27017"))
        self.label_url.setText(_translate("DataBaseManager", "Database-URL:"))
        self.pB_connect_db.setText(_translate("DataBaseManager", "Connect"))
        self.pB_disconnect_db.setText(_translate("DataBaseManager", "Disconnect"))
        self.pB_load_db.setText(_translate("DataBaseManager", "Load Database"))
        self.cBox_databases.setItemText(0, _translate("DataBaseManager", "No Database"))
        self.label_db.setText(_translate("DataBaseManager", "Databases:"))
        self.pB_set_db.setText(_translate("DataBaseManager", "View Database"))
        self.pB_delete_db.setText(_translate("DataBaseManager", "Delete Database"))
        self.pB_export_db.setText(_translate("DataBaseManager", "Export Database"))
        self.pB_refresh_db.setText(_translate("DataBaseManager", "Refresh"))
        self.pB_import_files.setText(_translate("DataBaseManager", "Import Simulation Data"))
        """
        self.label_tree_geo.setText(_translate("DataBaseManager", "Optimization Database:"))
        self.label_tree_sim.setText(_translate("DataBaseManager", "Simulation Database:"))
        self.gBox_viewer.setTitle(_translate("DataBaseManager", "Viewer"))
        self.action_New_Project.setText(_translate("DataBaseManager", "&New Project"))
        self.action_Load_Project.setText(_translate("DataBaseManager", "&Load Project"))
        self.action_Close_current_Project.setText(_translate("DataBaseManager", "&Close current Project"))
        self.action_Exit.setText(_translate("DataBaseManager", "&Exit"))
        self.actionSettings.setText(_translate("DataBaseManager", "Settings"))
        self.actionTools.setText(_translate("DataBaseManager", "Tools"))
        #self.checkBox_content.setText(_translate("DataBaseManager", "User Content only"))
        #self.checkBox_rotate.setText(_translate("DataBaseManager", "Auto rotating"))
        self.gBox_db.setTitle(_translate("DataBaseManager", "DataBaseControl"))
        self.pb_load_simulation.setText(_translate("DataBaseManager", "Load Simulation"))
        self.pb_load_geometry.setText(_translate("DataBaseManager", "Load Geometry"))
