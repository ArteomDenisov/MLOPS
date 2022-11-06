import os
import random
from typing import Dict
from dataclasses import dataclass, fields

import yaml
import pandas as pd
from marshmallow_dataclass import class_schema
import click


DATA_FILENAME = 'synthetic_data.csv'
TARGET_FILENAME = 'synthetic_target.csv'
TARGET_COLUMN = 'condition'


@dataclass()
class IntFeatureParameters:
    type: str
    min: int
    max: int
    step: int


@dataclass()
class FloatFeatureParameters:
    type: str
    min: float
    max: float
    step: float


@dataclass()
class GeneratorParameters:
    age: IntFeatureParameters
    sex: IntFeatureParameters
    cp: IntFeatureParameters
    trestbps: IntFeatureParameters
    chol: IntFeatureParameters
    fbs: IntFeatureParameters
    restecg: IntFeatureParameters
    thalach: IntFeatureParameters
    exang: IntFeatureParameters
    oldpeak: FloatFeatureParameters
    slope: IntFeatureParameters
    ca: IntFeatureParameters
    thal: IntFeatureParameters
    condition: IntFeatureParameters


def load_data_generation_config(filename: str) -> GeneratorParameters:
    GeneratorParametersSchema = class_schema(GeneratorParameters)
    with open(filename, 'r') as yaml_file:
        yaml_config = yaml.safe_load(yaml_file)
        shema = GeneratorParametersSchema()
        params = shema.load(yaml_config)
        return params


def generate_dataset(dataset_params: GeneratorParameters, rows: int = 100) -> pd.DataFrame:
    dataset = []
    for i in range(int(rows)):
        dataset_row = []
        columns = []
        for field in fields(dataset_params):
            value = getattr(dataset_params, field.name)
            field_type = type(value)
            columns.append(field.name)
            if field_type is IntFeatureParameters:
                random_value = random.randrange(value.min, value.max, value.step)
            elif field_type is FloatFeatureParameters:
                random_value = round(random.uniform(value.min, value.max), 1)
            dataset_row.append(random_value)
        dataset.append(dataset_row)
    return pd.DataFrame(dataset, columns=columns)


def save_dataset(dataset: pd.DataFrame, filepath: str) -> None:
    os.makedirs(filepath, exist_ok=True)
    data = dataset.loc[:, dataset.columns != TARGET_COLUMN]
    target = dataset[TARGET_COLUMN]
    data.to_csv(os.path.join(filepath, DATA_FILENAME), index=False)
    target.to_csv(os.path.join(filepath, TARGET_FILENAME), index=False)
