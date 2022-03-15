import pathlib
import numpy as np
import simdjson as json
import csv


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data['data'])  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    label = trans_label(data)  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    inter_label = None  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    time_stamp = None  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    metrics = None  # 指标物理意义说明；数据形状为（指标数量）；
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_each(file):
    data = np.load(file)
    return data


def read_label(file):
    data = []
    csv_reader = csv.reader(open(file))
    for row in csv_reader:
        data.append(row)
    return data[1:]


def read_data(parent):
    data = []
    label = read_label(parent['label_path'])
    data_path = pathlib.Path(parent['data_path'])
    for i in data_path.iterdir():
        name = i.name.split('/')[-1].split('.')[0]
        file_format_data = read_each(i)
        data.append({'name': name, 'data': file_format_data})
    out_data = {"data": data, "label": label}
    return out_data


def trans_data(data):
    ret = []
    for i in data:
        ret.append(i['data'].T.tolist())
    return ret


def trans_label(data):
    ret = []
    data_ = data['data']
    label = data['label']
    for i in data_:
        for j in label:
            if j[1] != 'MSL':
                continue
            if j[0] == i['name']:
                metric = [0] * int(j[4])
                for range_ in eval(j[2]):
                    for k in range(range_[0], range_[1] + 1):
                        metric[k] = 1
                ret.append(metric)
    return ret
