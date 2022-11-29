import logging
from typing import Dict, Tuple, Any
import pickle
import os

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import yaml

from .parameters import Parameters


DATAPATH = 'data'
MODELPATH = 'models'
MODELNAME = 'model.pkl'

logger = logging.getLogger("fit")


def load_config(filepath: str) -> Dict:
    """
    function to upload configuration
    """
    with open(filepath, 'r') as yml_file:
        configuration = yaml.safe_load(yml_file)
        logger.info(f'configuration loaded from {filepath}')
    return configuration


def load_raw_data(filename: str) -> (pd.DataFrame, pd.DataFrame):
    """
    function to uppload raw data
    """
    df = pd.read_csv(os.path.join(DATAPATH, filename))
    X = df.drop('condition', axis=1)
    y = df['condition']
    logger.info(f'{filename} was loaded')
    return X, y


def split_data(X: pd.DataFrame, y: pd.DataFrame, parameters: Any) -> Tuple[pd.DataFrame]:
    """
    function to split parameters
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters.split_share,
    )
    logger.info(f'raw data was splitted')
    return X_train, X_test, y_train, y_test


def save_data(X_train, X_test, y_train, y_test):
    """
    function to save splitted dataframes
    """
    X_test.to_csv(os.path.join(DATAPATH, 'X_test.csv'), index=False)
    y_test.to_csv(os.path.join(DATAPATH, 'y_test.csv'), index=False)
    X_train.to_csv(os.path.join(DATAPATH, 'X_train.csv'), index=False)
    y_train.to_csv(os.path.join(DATAPATH, 'y_train.csv'), index=False)
    logger.info(f'splitted data was saved to {DATAPATH}')


def fit_model(X_train: pd.DataFrame,
              y_train: pd.DataFrame,
              config: Parameters,
              model: str = 'knn',
              ) -> sklearn.base.BaseEstimator:
    """
    function to fit model
    """
    if model is 'knn':
        model = KNeighborsClassifier(n_neighbors=config.neighbours)
        logger.info('Default KNN model was created')
    elif model == 'lr':
        model = LogisticRegression(penalty=config.penalty, C=config.c)
        logger.info('Logistic regression model was created')
    model.fit(X_train, y_train)
    logging.info('model was fitted')
    return model


def save_model(model):
    """
    function to save model pickle
    """
    with open(os.path.join(MODELPATH, MODELNAME), 'wb') as pkl_file:
        pickle.dump(model, pkl_file)
        logger.info('model pickle was saved')
