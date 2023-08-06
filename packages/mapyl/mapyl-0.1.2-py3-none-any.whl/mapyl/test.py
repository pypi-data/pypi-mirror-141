import numpy as np
from classification import SVM
from data._2d_data import generate_data
from data import accuracy
from preprocessing import Normalizer
from clustering import KMeans
import matplotlib.pyplot as plt
from sklearn import datasets
#from keras.datasets import mnist
#(train_X, train_y), (test_X, test_y) = mnist.load_data()
# Keep these commented when not used, they take too much time to load


X, y = datasets.make_blobs(n_samples=70, n_features=2, centers=3, cluster_std=1.05, random_state=70)
y = np.where(y == 0, 3, y)
y = np.where(y == 1, 0, y)
y = np.where(y == 2, 1, y)
y = np.where(y == 3, 2, y)
'''
This is a test file

Here all the tests are done for the library

it is a mess, but dont worry about it
'''




