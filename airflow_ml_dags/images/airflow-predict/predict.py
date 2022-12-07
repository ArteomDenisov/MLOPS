import os.path
import pickle

import click
import pandas as pd
import sklearn


SCALER_FILE = 'scaler.pkl'
MODEL_FILE = 'classification_model.pkl'

X_VAL_FILE = 'X_test.csv'

PREDICTION_FILE = 'predictions.csv'


def load_scaler(filepath: str) -> sklearn.base.BaseEstimator:
    """
    function to load StandartScaler

    :param
    filepath: str
        path to scaler pickle file
    :return:
    """
    with open(os.path.join(filepath, SCALER_FILE), 'rb') as pkl:
        scaler = pickle.load(pkl)
    return scaler


def load_data(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(os.path.join(filepath, X_VAL_FILE))
    return data


def transform_data(data: pd.DataFrame, scaler: sklearn.base.BaseEstimator) -> pd.DataFrame:
    scaled_data = scaler.transform(data)
    return scaled_data


def load_classification_model(filepath):
    with open(os.path.join(filepath, MODEL_FILE), 'rb') as pkl:
        model = pickle.load(pkl)
    return model


def predict(features: pd.DataFrame, model: sklearn.base.BaseEstimator) -> pd.DataFrame:
    prediction = model.predict(features)
    return prediction


def save_prediction(prediction, prediction_path):
    df_prediction = pd.DataFrame(prediction, columns=['prediction'])
    os.makedirs(prediction_path, exist_ok=True)
    df_prediction.to_csv(os.path.join(prediction_path, PREDICTION_FILE), index=False)


@click.command('predict')
@click.option('--data-path', help='processed data filepath')
@click.option('--model-path', help='scaler model data path')
@click.option('--prediction-path', help='predictions data path')
def main(data_path: str, model_path: str, prediction_path: str) -> None:
    scaler = load_scaler(model_path)
    data = load_data(data_path)
    scaled_data = transform_data(data, scaler)
    model = load_classification_model(model_path)
    prediction = predict(scaled_data, model)
    save_prediction(prediction, prediction_path)


if __name__ == "__main__":
    main()

