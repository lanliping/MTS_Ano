import pathlib

import numpy as np
import yaml


def conf_load(path):
    with open(path, 'r') as r:
        config = yaml.load(r, Loader=yaml.FullLoader)
    return config


def read_npy(file):
    data = np.load(file)
    return data


def read_algorithm(parent):
    algorithm = {}
    data_path = pathlib.Path(parent)
    for i in data_path.iterdir():
        score = read_npy(i)
    return algorithm
