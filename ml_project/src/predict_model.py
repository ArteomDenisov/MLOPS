import logging
import pickle
from typing import Tuple
import os

import pandas as pd
import sklearn
from sklearn.metrics import accuracy_score, f1_score

PREDICTIONS = 'predictions'

logger = logging.getLogger("predict")


def load_model(path_to_model: str):
    with open(os.path.join(path_to_model, 'model.pkl'), 'rb') as pkl:
        model = pickle.load(pkl)
    logging.info('model was loaded')
    logging.info('test sample was loaded')
    return model


def load_test_data(path_to_data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    X_test = pd.read_csv(os.path.join(path_to_data, 'X_test.csv'))
    y_test = pd.read_csv(os.path.join(path_to_data, 'y_test.csv'))
    return X_test, y_test


def predict(model: sklearn.base.BaseEstimator, X_test: pd.DataFrame) -> pd.DataFrame:
    prediction = model.predict(X_test)
    logging.info('prediction was made')
    return prediction


def save_predictions(prediction, datapath):
    df_prediction = pd.DataFrame(prediction)
    df_prediction.to_csv(os.path.join(datapath, PREDICTIONS), index=False)