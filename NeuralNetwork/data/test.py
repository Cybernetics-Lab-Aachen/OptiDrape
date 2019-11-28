

from Data.pickle_data import load_halbkugel_hdf
import numpy as np


if __name__ == '__main__':
    path = "/home/optidrape/Desktop/DrapeSimulation/Hablkugel.mat"

    load_halbkugel_hdf(path)


    test = np.array().tolist()