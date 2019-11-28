import sys, os
import numpy as np
import scipy
from scipy.io import loadmat
from Data.logger import get_logger
import h5py
import tensorflow as tf


# data
class OptiDrapeData:
    def __init__(self, data_path_list):
        self._data_path_list = data_path_list
        self._data = dict()
        self._dim_info = dict()

    def dump_data(self, path=os.path.realpath(__file__)):
        pass


    @staticmethod
    def extract_data_from_matlab(path, dim_info, return_data=False):

        try:
            _data = h5py.File(path, 'r')
            



        except:
            pass









    def get_drape_data_info(self):
        pass






data_path = ""














