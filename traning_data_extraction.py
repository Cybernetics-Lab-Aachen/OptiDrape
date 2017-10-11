
import os, sys
from collections import OrderedDict
import pymesh
import openmesh
from openmesh import *
import vispy
import mayavi


class training_data_extractor():
    def __init__(self, path):
        self._path = path
        self._mesh_format = '.pc'
        self._shear_format = '.asc'

        self._file_dict = {'mesh':{}, 'shear':{}}

        self._mesh_dict = {}

        self._meshes = {}

    def set_file_format(self, mesh=None, shear=None):
        if mesh:
            self._mesh_format = mesh

        if shear:
            self._shear_format = shear

    def load_file_from_esi(self):
        try:
            _all_file = os.listdir(self._path)
            _file_counter = [0, 0]
            for _file in _all_file:
                _split = os.path.splitext(_file)
                if _split[1] == self._mesh_format:
                    self._file_dict['mesh'].update({_split[0]: _file})
                    _file_counter[0] += 1
                elif _split[1] == self._shear_format:
                    self._file_dict['shear'].update({_split[0]: _file})
                    _file_counter[1] += 1

            if _file_counter[0] is 0:
                print("Warning: There was no mesh file found.")

            if _file_counter[1] is 0:
                print("Warning: There was no shear file found.")
        except FileNotFoundError:
            print("Error: Invalid path!")

    def extract_mesh_from_esi(self):
        for mesh_file in self._file_dict['mesh'].keys():
            _lines = []

            _node_dict = OrderedDict()
            _shell_dict = OrderedDict()

            with open(self._path + self._file_dict['mesh'][mesh_file]) as mesh:
                _lines = mesh.readlines()

            for _line in _lines:
                _split_list = [s for s in _line.split(' ') if s is not '']

                # extract nodes
                if _split_list[0] == 'NODE':
                    _node_dict.update({_split_list[2]: _split_list[3:6]})

                elif _split_list[0] == 'SHELL':
                    _shell_dict.update({_split_list[2]: _split_list[4:8]})

            self._mesh_dict.update({mesh_file: {'node': _node_dict,
                                                'shell': _shell_dict}})

    def rebuild_mesh_from_esi(self):

        for mesh_key in self._mesh_dict.keys():
            _this_mesh = PolyMesh()
            _node_dict = {}
            for node_key in self._mesh_dict[mesh_key]['node'].keys():
                _node = [float(s) for s in self._mesh_dict[mesh_key]['node'][node_key]]

                _node_dict.update({node_key: _this_mesh.add_vertex(PolyMesh.Point(_node[0], _node[1], _node[2]))})
            _shell_dict = {}
            for shell_key in self._mesh_dict[mesh_key]['shell'].keys():
                _shell_consist = self._mesh_dict[mesh_key]['shell'][shell_key]
                _shell_dict.update({shell_key: _this_mesh.add_face([_node_dict[node] for node in _shell_consist])})

            self._meshes.update({mesh_key: {'mesh': _this_mesh,
                                            'node': _node_dict,
                                            'shell': _shell_dict}})

    def get_mesh(self):
        return self._meshes

    def get_mesh_dict(self):
        return self._mesh_dict


if __name__ == '__main__':
    test = training_data_extractor(path='/home/haoming/Desktop/USB/Data/')

    test.load_file_from_esi()

    test.extract_mesh_from_esi()

    test.rebuild_mesh_from_esi()

    print(test.get_mesh())









