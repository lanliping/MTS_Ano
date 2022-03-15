import yaml


def conf_load(path):
    with open(path, 'r') as r:
        config = yaml.load(r, Loader=yaml.FullLoader)
    return config
