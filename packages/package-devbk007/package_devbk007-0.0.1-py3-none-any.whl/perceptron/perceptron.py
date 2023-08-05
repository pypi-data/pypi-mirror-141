import os
import numpy as np
import joblib
import logging

class Perceptron:
    """Perceptron model
    """
    
    def __init__(self, eta: float = None, epochs: int=None):
        """Initialisation

        Args:
            eta (float, optional): Learining rate. Defaults to None.
            epochs (int, optional): Number of epochs. Defaults to None.
        """
        self.weights = np.random.randn(3) * 1e-4 # small random weights
        training = (eta is not None) and (epochs is not None)
        if training:
            logging.info(f"initial weights before training: \n{self.weights}")
        self.eta = eta
        self.epochs = epochs
    
    def _z_outcome(self, inputs, weights):
        """Z Outcome

        Args:
            inputs (tuple): Input data
            weights (tuple): Weights

        Returns:
            intger: X Outcome
        """
        return np.dot(inputs, weights)
    
    def activation_function(self, z):
        """Activation Function

        Args:
            z (integer): Z Outcome

        Returns:
            Binary: Output of step function (0,1)
        """
        return np.where(z > 0, 1, 0)# Step Function. If z > 0, returns 1 else returns 0
    
    def fit(self, X, y):
        """Fitting to the model

        Args:
            X (tuple): Independent variables
            y (tuple): Label
        """
        self.X = X
        self.y = y
        
        X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))]
        logging.info(f"X with bias: \n{X_with_bias}")
        
        for epoch in range(self.epochs):
            logging.info("--"*10)
            logging.info(f"for epoch >> {epoch}")
            logging.info("--"*10)
            
            z = self._z_outcome(X_with_bias, self.weights)
            y_hat = self.activation_function(z)
            logging.info(f"predicted value after forward pass: \n{y_hat}")
            
            self.error = self.y - y_hat
            logging.info(f"error: \n{self.error}")
            
            self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error)
            logging.info(f"updated weights after epoch: {epoch + 1}/{self.epochs}: \n{self.weights}")
            logging.info("##"*10)
    
    def predict(self, X):
        """Predict output from model

        Args:
            X (tuple): Independent variables

        Returns:
            Binary: Output from the activation function
        """
        X_with_bias = np.c_[X, -np.ones((len(X), 1))] # Concatenating X with bias
        z = self._z_outcome(X_with_bias, self.weights)
        return self.activation_function(z)
    
    def total_loss(self):
        """Total Loss

        Returns:
            integer: Total loss
        """
        total_loss = np.sum(self.error)
        logging.info(f"\nTotal loss: {total_loss}\n")
        return total_loss
    
    def _create_dir_return_path(self, model_dir, filename):
        """To save the model to a directory

        Args:
            model_dir (string): Directory name
            filename (string): Filename

        Returns:
            path: Path of created directory
        """
        os.makedirs(model_dir, exist_ok=True)
        return os.path.join(model_dir, filename)
        
    def save(self, filename, model_dir=None):
        """Saving the model in directory

        Args:
            filename (string): Filename
            model_dir (string, optional): Directory name. Defaults to None.
        """
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir, filename)
            joblib.dump(self, model_file_path)
        else:
            model_file_path = self._create_dir_return_path("model", filename)
            joblib.dump(self, model_file_path)
        logging.info(f"model is saved at {model_file_path}")
    
    def load(self, filepath):
        """Loading the model

        Args:
            filepath (path): Path of model

        Returns:
            model: Loaded model
        """
        return joblib.load(filepath)