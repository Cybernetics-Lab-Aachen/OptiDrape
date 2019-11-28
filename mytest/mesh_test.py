
import openmesh, os
from scipy.io import loadmat
import tensorflow as tf
import numpy as np
import pickle


#  for the simulation data it is enough only to import the xy-plane-matrix ZG or ZT
#


test = openmesh.read_mesh("/home/optidrape/Desktop/Data/mytest.obj")

tri = openmesh.TriMesh()

print(tri.n_faces())

