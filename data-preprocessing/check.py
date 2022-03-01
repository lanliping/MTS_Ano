import simdjson as json
import argparse
import numpy as np


def check(path):
    with open(path, "r") as w:
        data = json.load(w)
    print(f"{np.asarray(data['data']).shape=}")
    print(f"{np.asarray(data['label']).shape=}")
    print(f"{np.asarray(data['inter_label']).shape=}")
    print(f"{np.asarray(data['time_stamp']).shape=}")


def main():
    check(args.data_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="/home/lidongwen/MTS_Ano/Dataset/satellite-dataset/json-version/satellite-dataset.json",
        type=str,
        required=False,
        help="处理后数据存储地址",
    )
    args = parser.parse_args()
    main()
