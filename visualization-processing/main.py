import argparse
import json
import pathlib
from visual_utils import *


def main():
    ret = {}
    data_path = paths['data']
    with open(data_path, 'r', encoding='utf8') as fp:
        test_data = json.load(fp)
        all_label = test_data['label']
        all_data = test_data['data']
    for i in range(len(all_data)):
        label = all_label[i]
        data = all_data[i]
        entity = {'data': data, 'label': label}
        algorithms = paths['algorithms']
        for algorithm in algorithms:
            parent = algorithms[algorithm] + '/' + str(i)
            score = np.load(parent + '/test_score.npy', allow_pickle=True)
            score = [float(x) for x in score]
            multi_score = None
            with open(parent + '/threshold.txt', 'r', encoding='utf8') as fp:
                threshold = float(fp.read())
            entity_algorithm = {'score': score, 'multi_score': multi_score, 'threshold': threshold}
            entity[algorithm] = entity_algorithm
        ret[str(i + 1)] = entity
    with open(paths['save_path'], "w") as w:
        json.dump(ret, w)


if __name__ == "__main__":
    config = conf_load('conf.yml')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default=config['dataset'],
        type=str,
        required=False,
        help="配置文件关键词",
    )
    args = parser.parse_args()
    paths = config[args.dataset]
    main()
