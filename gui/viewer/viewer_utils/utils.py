import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from enum import Enum


class InfoType(Enum):
    NORMAL   = 0,
    WARNING  = 1,
    ERROR    = 2

def build_geometry_data_tree(tree_handle, collections, database_instance):
    _model = QStandardItemModel(0, 1, tree_handle)
    for collection in collections:
        _tree_l0 = QStandardItem(collection)
        _tree_l0.setEditable(False)
        for docu in database_instance[collection].find({}, {'_id': 0}):
            for sub_docu in docu.keys():
                # should be iterated only once, but we need to get the keys hier, because we donnot wanna iterate the whole document
                ## perhaps there is a better way ...
                _tree_l1 = QStandardItem(sub_docu)
                _tree_l1.setEditable(False)
                # _tree_l1.setCheckable(True)
                for sub_sub_docu in docu[sub_docu].keys():
                    _tree_l2 = QStandardItem(sub_sub_docu)
                    _tree_l2.setEditable(False)
                    # _tree_l2.setCheckable(True)
                    for sub_sub_sub_docu in docu[sub_docu][sub_sub_docu].keys():
                        _tree_l3 = QStandardItem(sub_sub_sub_docu)
                        _tree_l3.setEditable(False)
                        _tree_l3.setDragEnabled(True)
                        _tree_l2.appendRow(_tree_l3)
                    _tree_l1.appendRow(_tree_l2)
                _tree_l0.appendRow(_tree_l1)
        _model.appendRow(_tree_l0)
    tree_handle.setModel(_model)
    tree_handle.setHeaderHidden(True)


def build_textile_data_tree(tree_handle, collections, database_instance):
    _model = QStandardItemModel(0, 1, tree_handle)
    for textile in collections:
        _textile_item = QStandardItem(textile)
        _textile_item.setEditable(False)
        _textile_item.setSelectable(True)
        for _data_dict in database_instance[textile].find({}, {'_id': 0}):
            for data_type in _data_dict.keys():
                _textile_data_item = QStandardItem(data_type)
                _textile_data_item.setEditable(False)
                _textile_item.appendRow(_textile_data_item)
        _model.appendRow(_textile_item)
    tree_handle.setModel(_model)
    tree_handle.setHeaderHidden(True)


def build_textile_data_tree_from_dict(tree_handle, data_dict):
    _model = QStandardItemModel(0, 1, tree_handle)
    for textile in data_dict.keys():
        _textile_item = QStandardItem(textile)
        _textile_item.setEditable(False)
        _textile_item.setSelectable(True)
        for _textile_data in data_dict[textile].keys():
            _textile_data_item = QStandardItem(_textile_data)
            _textile_data_item.setEditable(False)
            _textile_item.appendRow(_textile_data_item)
        _model.appendRow(_textile_item)
    tree_handle.setModel(_model)
    tree_handle.setHeaderHidden(True)


def build_data_view_tree(tree_handle, data_bases, database_instance):
    _model = QStandardItemModel(0, 1, tree_handle)
    for data_base in data_bases:
        _collections = [collec for collec in database_instance[data_base].collection_names() if 'system' not in collec]
        _tree_l0 = QStandardItem(data_base)
        _tree_l0.setEditable(False)
        if "Textile" not in data_base:
            for collection in _collections:
                _tree_l1 = QStandardItem(collection)
                _tree_l1.setEditable(False)
                for docu in database_instance[data_base][collection].find({}, {'_id': 0}):
                    for sub_docu in docu.keys():
                        # should be iterated only once, but we need to get the keys hier, because we donnot wanna iterate the whole document
                        ## perhaps there is a better way ...
                        _tree_l2 = QStandardItem(sub_docu)
                        _tree_l2.setEditable(False)
                        # _tree_l1.setCheckable(True)
                        for sub_sub_docu in docu[sub_docu].keys():
                            _tree_l3 = QStandardItem(sub_sub_docu)
                            _tree_l3.setEditable(False)
                            # _tree_l2.setCheckable(True)
                            for sub_sub_sub_docu in docu[sub_docu][sub_sub_docu].keys():
                                _tree_l4 = QStandardItem(sub_sub_sub_docu)
                                _tree_l4.setEditable(False)
                                _tree_l4.setDragEnabled(True)
                                _tree_l3.appendRow(_tree_l4)
                            _tree_l2.appendRow(_tree_l3)
                    _tree_l1.appendRow(_tree_l2)
                _tree_l0.appendRow(_tree_l1)
        else:
            for textile in _collections:
                _textile_item = QStandardItem(textile)
                _textile_item.setEditable(False)
                for _data_dict in database_instance[data_base][textile].find({}, {'_id': 0}):
                    for data_type in _data_dict.keys():
                        _textile_data_item = QStandardItem(data_type)
                        _textile_data_item.setEditable(False)
                        _textile_item.appendRow(_textile_data_item)
                _tree_l0.appendRow(_textile_item)
        _model.appendRow(_tree_l0)
    tree_handle.setModel(_model)
    tree_handle.setHeaderHidden(True)






