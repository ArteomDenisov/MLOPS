import logging

import click

from src.generate import load_data_generation_config, generate_dataset, save_dataset


@click.command()
@click.option('--n-rows', default=100, help='number of rows in random dataset')
@click.option('--filepath', default='data', help='filepath for generated data')
def main(n_rows, filepath):
    params = load_data_generation_config('configs/data_generation.yml')
    df = generate_dataset(params, n_rows)
    save_dataset(df, filepath)


if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
