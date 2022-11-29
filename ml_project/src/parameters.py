from dataclasses import dataclass
import os

import yaml
from marshmallow_dataclass import class_schema


CONFIGPATH = 'configs'


@dataclass()
class Parameters:
    model_name: str
    data_raw: str
    random_state: int
    split_share: float
    neighbours: int
    penalty: str
    c: float


def load_params_config(model_name: str) -> Parameters:
    ParametersSchema = class_schema(Parameters)
    filename = os.path.join(CONFIGPATH, model_name + '_parameters.yml')
    with open(filename, 'r') as yaml_file:
        yaml_config = yaml.safe_load(yaml_file)
        shema = ParametersSchema()
        params = shema.load(yaml_config)
        return params
