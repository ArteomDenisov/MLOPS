import requests
import logging
import pandas as pd


PREDICT_API_URL = "http://0.0.0.0:8000/predict"
DATA_PATH = 'x_test.csv'

logger = logging.getLogger("request")


def main():
    df = pd.read_csv(DATA_PATH)
    response = requests.get(PREDICT_API_URL, json={'data': df.head().to_json()})

    logging.info(response.status_code)
    logging.info(response.json())


if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()

