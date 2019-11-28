import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

os.environ['PATH'] += "/home/optidrape/Desktop/OptiDrape/Data"
os.path.join("/home/optidrape/Desktop/OptiDrape/Data")
from Data import data_extraction, drape_object
from gui.ui.ui_drape_tool_main import Ui_DrapeToolMainWindow

import openmesh
from pymongo import MongoClient, errors as mongo_error

from gui.viewer.textile_manger import TextileManagerManager
from gui.viewer.database_manager import DrapeDatabaseManager
from gui.viewer.parameter_manager import ParameterManager
from gui.viewer.optimization_manager import OptimizationManager
from gui.viewer.result_manager import ResultManager
from evolAlgo.optimizationThread import EAThread

from gui.viewer.viewer_utils.utils import InfoType

# TODO : NOW FACING PROBLEM, WHEN NEW MESH SHOW, THE OLD ONE WOULD BE RESET
# TODO : no upgrage bar shown from the second visualization on


class DrapeTool(Ui_DrapeToolMainWindow, QMainWindow):
    def __init__(self, parent=None):
        # we set the initialization for parent class, so we can use the gui items directly
        super(self.__class__, self).__init__(parent)
        # we setup the Ui
        self.setupUi(self)

        # global variables
        self._message_index = 0

        self.tab_database = DrapeDatabaseManager(parent=self)
        self.tabWidget.addTab(self.tab_database, "Geometry Manager")
        self.tab_textile_manager = TextileManagerManager(parent=self)
        self.tabWidget.addTab(self.tab_textile_manager, "Textile Manager")
        self.tab_parameter = ParameterManager(self)
        self.tabWidget.addTab(self.tab_parameter, "Parameter Manager")
        self.tab_optimization = OptimizationManager(parent=self)
        self.tabWidget.addTab(self.tab_optimization, "Optimization Manager")
        self.tab_result = ResultManager(self)
        self.tabWidget.addTab(self.tab_result, "Result Manager")
        self.tab_optimization.set_result_manager(result_manager=self.tab_result)

    def echo_info(self, msg, instance=None, type=InfoType.NORMAL):
        self._message_index += 1
        if instance:
            msg2show = str(self._message_index) + '@{}: '.format(instance.__class__.__name__) + msg
        else:
            msg2show = str(self._message_index) + ': ' + msg
        if type == InfoType.NORMAL:
            self.info_browser.append(str(self._message_index) + ': ' + msg)
        elif type == InfoType.ERROR:
            pass
        elif type == InfoType.WARNING:
            pass
        else:
            return


    @property
    def textile_manager(self):
        return self.tab_textile_manager

    @property
    def parameter_manager(self):
        return self.tab_parameter

    @property
    def optimization_manager(self):
        return self.tab_optimization


    def doOPT(self):
        self.optimization_manager.page_general.append("-- Start Optimization --")

        thr = EAThread(None, parent=self, view=None)
        self.optimization_manager.setThread(thr)

        self.optimization_manager.optThread.pbar2progressSig.connect(self.optimization_manager.updatePbar)
        self.optimization_manager.optThread.ind2visu.connect(self.optimization_manager.ind2visu)
        self.optimization_manager.optThread.dodeepcopy.connect(self.dodeepcopy)
        self.optimization_manager.optThread.updateviewer.connect(self.updateviewer)
        self.optimization_manager.optThread.puttext.connect(self.optimization_manager.put_info)
        self.optimization_manager.optThread.start()

    def dodeepcopy(self, mesh, name):
        self.optimization_manager.optThread.mesh_deep_copy = mesh.deepcopy(name=name)
        self.optimization_manager.optThread.finish_deepcopy = True

    def updateviewer(self, bool):
        for pop in self.optimization_manager.optThread.population:
            pop.update_viewer()
        self.optimization_manager.optThread.finish_deepcopy = True



if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = DrapeTool()
    test.optimization_manager.pB_start.clicked.connect(test.doOPT)

    test.show()
    app.exec()





