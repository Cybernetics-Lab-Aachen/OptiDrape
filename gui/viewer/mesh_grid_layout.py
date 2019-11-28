from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import math, numpy

from collections import OrderedDict

import itertools


class MeshGridLayout(object):
    def __init__(self, layout_widget):
        super(MeshGridLayout, self).__init__()
        self._layout_widget = layout_widget
        self._layout_object_dict = OrderedDict()
        self._layout = QGridLayout()

    # arrange widget in _drape_objects_roadmap into the grid layout
    def arrange_layout(self):
        if not len(self._layout_object_dict):
            print('no_data_to be shown')
            return

        # decide the grid number and arrange grid*grid space in the layout
        if len(self._layout_object_dict) == 1:
            _grid_number = 1
        else:
            _grid_number = numpy.square(math.ceil(math.sqrt(len(self._layout_object_dict))))

        _loop_time = 0

        # put the widget into a single block in the layout one by one
        for _grid_col, _grid_row in itertools.product(range(int(math.sqrt(_grid_number))), range(int(math.sqrt(_grid_number)))):
                if len(self._layout_object_dict) <= _loop_time:
                    continue
                else:
                    self._layout.addWidget(self._layout_object_dict[_loop_time]['_viewer_widget'], _grid_col,
                                          _grid_row)
                    _loop_time += 1

    # there are not only viewer widget but also other info in the object, and what we need is only viewer widget here
    def extract_viewer_widget_from_object(self):
        for k in self._mesh_objects_roadmap.keys():
            _viewer_widget = self._mesh_objects_roadmap[k].geometry_viewer
            self._widget_object_roadmap.append({'mesh_name': self._mesh_objects_roadmap[k], '_viewer_widget': _viewer_widget})

    # initialize the mama layout for put another child layout into it
    def boxdelete(self, layout_mama):
        for i in range(layout_mama.count()):
            _poor_layout = layout_mama.itemAt(i)

            # there might be widget in the poor layout, before removing the poor layout, you have to remove the poor widget first
            for j in reversed(range(_poor_layout.count())):
                _poor_layout.itemAt(j).widget().setParent(None)
            layout_mama.removeItem(_poor_layout)
        return layout_mama

    def layout(self, mesh_object):


        pass
