from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.ui.ui_result_manager import *
from gui.viewer.result import *


class ResultManager(QWidget, Ui_ResultManager):
    def __init__(self, parent=None):
        super(ResultManager, self).__init__(parent=parent)
        self.setupUi(self)

    




