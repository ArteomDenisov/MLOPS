import os
import pickle
import logging

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler


SCALER_NAME = 'scaler.pkl'
ENCODER_NAME = 'encoder.pkl'
MODELS_PATH = 'models'


logger = logging.getLogger("transformer")


class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.category = ['sex', 'cp', 'restecg', 'exang', 'slope', 'ca', 'thal']
        self.numerical = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
        self.scaler = None

    def fit(self, X):
        self.scaler = StandardScaler()
        self.scaler.fit(X[self.numerical])
        logger.info('scaler was fitted')
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
        self.encoder.fit(X[self.category])
        logger.info('One hot encoder was fitted')
        self.save_scaler()
        self.save_encoder()

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        scaler_raw = self.scaler.transform(X[self.numerical])
        X_scaled = pd.DataFrame(scaler_raw, columns=self.numerical)

        X_encoded = self.encoder.transform(X[self.category])
        X_encoded = pd.DataFrame(X_encoded)

        X_transformed = pd.concat([X_encoded, X_scaled], axis=1)
        logger.debug(X_scaled.shape, X_encoded.shape, X_transformed.shape)
        logger.info('data was transformed')
        return X_transformed

    def load_scaler(self):
        with open(os.path.join(MODELS_PATH, SCALER_NAME), 'rb') as pkl:
            self.scaler = pickle.load(pkl)
            logger.info('scaler loaded')

    def load_encoder(self):
        with open(os.path.join(MODELS_PATH, ENCODER_NAME), 'rb') as pkl:
            self.encoder = pickle.load(pkl)
            logger.info('encoder loaded')

    def save_scaler(self):
        with open(os.path.join(MODELS_PATH, SCALER_NAME), 'wb') as pkl:
            pickle.dump(self.scaler, pkl)

    def save_encoder(self):
        with open(os.path.join(MODELS_PATH, ENCODER_NAME), 'wb') as pkl:
            pickle.dump(self.encoder, pkl)