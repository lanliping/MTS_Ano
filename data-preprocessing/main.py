import argparse
import pathlib
from importlib import import_module
from utils import *


def main():
    data = module.read_data(config["data_path"])
    data = module.deal_data(data)
    module.write_data(config["save_path"], data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_path",
        default="config/conf.yml",
        type=str,
        required=False,
        help="配置文件",
    )
    parser.add_argument(
        "--config_key",
        default="server-machine-dataset-test",
        type=str,
        required=False,
        help="配置文件关键词",
    )
    args = parser.parse_args()
    config = conf_load(args.config_path)[args.config_key]
    save_path = pathlib.Path(config["save_path"])
    save_path.parent.mkdir(parents=True, exist_ok=True)
    module = import_module("dataset-util." + config["dataset"])
    main()
