from regression import LinearRegressor
import numpy as np
from itertools import combinations, combinations_with_replacement
from preprocessing import PolyExp

class PolyRegressor:
    """Polynomial Regressor instance, uses the degree of the data"""
    def __init__(self, degree=2):
        self.degree = degree
    
    lin = LinearRegressor()

    def fit(self, X, y):
        """
        Fits the `PolyRegressor` instance

        Parameters:
        ===========
        `X`: ndarray of shape (num_samples, num_features) for input
        `y`: numpy array of shape (num_samples,) for output

        returns none
        """
        X = PolyExp(self.degree).evalnum(X)
        #X = self.evalnum(X)
        self.lin.fit(X, y)

    def predict(self, X):
        """
        Predicts `y` value for `x` instance

        Parameter: `X`: ndarray of shape (num_samples, num_features)

        Returns: `y`: ndarray containning `y` value
        """
        X = PolyExp(self.degree).evalnum(X)
        return self.lin.predict(X)

