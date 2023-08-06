import numpy as np

class BinLogitRegressor:
    """
    Binary Logistic Regressor instance

    Parameters:
        lr: float of the learning rate
        iters: int of the number of iterations
    """
    def __init__( self, lr=0.01, iters=500):  
        if type(lr) != (float or int):
            raise TypeError("learning rate must be of type float or int") 
        if type(iters) != int:
            raise TypeError("iterations must be of type int")

        self.learning_rate = lr        
        self.iterations = iters
          
    def fit(self, X, y, precision=False):
        """
        Fits the instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input
            y (ndarray): ndarray of shape (num_samples,) of the output

        Returns none
        """
        self.m, self.n = X.shape           
        self.W = np.zeros(self.n)        
        self.b = 0        
        self.X = X        
        self.Y = y
                  
        for i in range(self.iterations) :            
            self._update_weights() 

        if precision:
            _pres = self.calc_precision(X, y)
            print("precision : {}".format(_pres))
      
    def _update_weights(self) :           
        A = 1 / (1 + np.exp( - (self.X.dot(self.W)+self.b))) 
        tmp = (A - self.Y.T)        
        tmp = np.reshape(tmp, self.m)        
        dW = np.dot(self.X.T, tmp) / self.m         
        db = np.sum(tmp) / self.m    
        self.W = self.W - self.learning_rate * dW    
        self.b = self.b - self.learning_rate * db
      
    def predict(self, X):
        """
        Predicts the class of the supplied `X`

        Parameter: 
            X (ndarray): ndarray of shape (num_samples, num_features) to be classified

        Returns: int classifying as 1 or 0
        """
        Z = 1 / (1 + np.exp( - (X.dot(self.W) + self.b)))        
        Y = np.where( Z > 0.5, 1, 0 )        
        return Y
    
    def predict_prob(self, X):
        """
        Predicts the probability of the classification

        Parameter: 
            X (ndarray): ndarray to be classified

        Returns: float of the probability of being 1
        """
        Z = 1 / (1 + np.exp( - (X.dot(self.W) + self.b)))
        return Z
    

