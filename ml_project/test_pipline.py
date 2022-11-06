import logging
import click

from src.predict_model import load_model, load_test_data, predict, estimate, save_predictions
from src.train_model import DATAPATH, MODELPATH
from src.transformer import CustomTransformer



@click.command()
@click.option('--metric', default='accuracy', help='metric to estimate')
def main(metric):
    X_test, y_test = load_test_data(DATAPATH)
    model = load_model(MODELPATH)
    transformer = CustomTransformer()
    transformer.load_scaler()
    transformer.load_encoder()
    X_transformed = transformer.transform(X_test)
    predictions = predict(model, X_transformed)
    estimate(predictions, y_test, metric)
    save_predictions(predictions, DATAPATH)


if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
