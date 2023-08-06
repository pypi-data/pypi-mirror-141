import numpy as np
from classification import SVM
from data import accuracy
from data import generate_data
from preprocessing import Normalizer
from regression import PolyRegressor
from clustering import KMeans
import matplotlib.pyplot as plt
from sklearn import datasets
#from keras.datasets import mnist
#(train_X, train_y), (test_X, test_y) = mnist.load_data()
# Keep these commented when not used, they take too much time to load


X, y = generate_data(deg3=2, deg2=0.1, ang=3)

'''
This is a test file

Here all the tests are done for the library

it is a mess, but dont worry about it
'''


p = PolyRegressor(3)
p.fit(X, y)
print(p.predict(np.array([[1]])))

