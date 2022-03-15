import pathlib
import numpy as np
import simdjson as json


point_num = []


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data['data'])
    label = get_label(data['label'])
    inter_label = get_inter(data['inter_label'])
    time_stamp = None
    metrics = None
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_each(file):
    with open(file, "r") as r:
        data = r.read().splitlines()
    return data


def read_data(parent):
    data = []
    label = []
    inter_label = []
    test_parent = pathlib.Path(parent['data_path'])
    label_parent = pathlib.Path(parent['label_path'])
    interpretation_parent = pathlib.Path(parent['interpretation_path'])
    for i in test_parent.iterdir():
        file_format_data = read_each(i)
        data.append(file_format_data)
    for i in label_parent.iterdir():
        file_format_data = read_each(i)
        label.append(file_format_data)
    for i in interpretation_parent.iterdir():
        file_format_data = read_each(i)
        inter_label.append(file_format_data)
    out_data = {"data": data, "label": label, "inter_label": inter_label}
    return out_data


def trans_data(data):
    ret_data = []
    for file_format_data in data:
        data_metric = []
        for line_data in file_format_data:
            line_data = line_data.split(',')
            data_point = [float(i) for i in line_data]
            data_metric.append(data_point)
        data_metric = np.transpose(data_metric).tolist()
        ret_data.append(data_metric)
    return ret_data


def get_label(data):
    label = []
    for file_format_data in data:
        label_point = []
        point_num.append(len(file_format_data))
        for line_data in file_format_data:
            label_point.append(int(line_data))
        label.append(label_point)
    return label


def get_inter(data):
    inter = []
    for i in point_num:
        tmp = []
        for j in range(i):
            tmp.append(None)
        inter.append(tmp)
    for i, file_format_data in enumerate(data):
        for line_data in file_format_data:
            line = line_data.split(':')
            point_range, metrics = line[0].split('-'), line[1].split(',')
            start = int(point_range[0])
            end = int(point_range[1])
            for j in range(start, end + 1):
                inter[i][j] = metrics
    return inter
