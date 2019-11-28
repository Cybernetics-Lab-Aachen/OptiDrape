from PyQt5.QtWidgets import *
from gui.ui.ui_result import *


class Result(QWidget, Ui_Result):
    def __init__(self, parent=None):
        super(Result, self).__init__(parent=parent)

        # self.tB_text
        # self.tabWidget
        # self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.setupUi(self)
