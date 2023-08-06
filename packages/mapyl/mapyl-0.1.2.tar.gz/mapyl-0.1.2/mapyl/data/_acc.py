import numpy as np

def accuracy(y, y_hat):
        """
        calculates the accuracy of the prediction
        Parameters:

        `y`: ndarray of the correct values
        `y_hat`: ndarray of the predicted values
        """
        return np.sum(y==y_hat)/len(y)