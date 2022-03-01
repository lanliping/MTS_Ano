import simdjson as json
import argparse
import pathlib
from importlib import import_module
import yaml

CONF_PATH = 'conf/config.yaml'


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def conf_load():
    with open(CONF_PATH, mode='r', encoding='utf-8') as fd:
        data = yaml.load(fd, Loader=yaml.FullLoader)
    return data


def main():
    data = module.read_data(args.data_path)
    data = module.deal_data(data)
    write_data(args.save_path, data)


if __name__ == "__main__":
    conf = conf_load()
    name = conf['target']
    path = conf[name]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default=name,
        type=str,
        required=False,
        help="数据集名称（用于引入对应文件）",
    )
    parser.add_argument(
        "--data_path",
        default=path['data_path'],
        type=str,
        required=False,
        help="原始数据地址",
    )
    parser.add_argument(
        "--save_path",
        default=path['save_path'],
        type=str,
        required=False,
        help="处理后数据存储地址",
    )
    args = parser.parse_args()
    save_path = pathlib.Path(args.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    module = import_module(args.dataset)
    main()
    print('Done writing.')
