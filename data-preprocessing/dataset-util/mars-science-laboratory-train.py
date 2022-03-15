import pathlib
import numpy as np
import simdjson as json


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data)  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    label = None  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    inter_label = None  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    time_stamp = None  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    metrics = None  # 指标物理意义说明；数据形状为（指标数量）；
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_each(file):
    data = np.load(file)
    return data


def read_data(parent):
    data = []
    data_path = pathlib.Path(parent)
    for i in data_path.iterdir():
        data.append(read_each(i))
    return data


def trans_data(data):
    ret = []
    for i in data:
        ret.append(i.T.tolist())
    return ret
