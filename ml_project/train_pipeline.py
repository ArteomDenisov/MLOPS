import logging

import click

from src.train_model import load_raw_data, split_data, save_data, fit_model, save_model
from src.parameters import load_params_config
from src.transformer import CustomTransformer


@click.command()
@click.option('--model_name', default='knn', help='model to make predictions')
def main(model_name):
    config = load_params_config(model_name)
    X, y = load_raw_data(config.data_raw)
    X_train, X_test, y_train, y_test = split_data(X, y, config)
    save_data(X_train, X_test, y_train, y_test)
    transformer = CustomTransformer()
    transformer.fit(X_train)
    X_transformed = transformer.transform(X_train)
    trained_model = fit_model(X_transformed, y_train, config, model_name)
    save_model(trained_model)


if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
