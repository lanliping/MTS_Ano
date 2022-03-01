import csv

import numpy as np


def read_data(file):
    data = []
    with open(file) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data.append(row)
    return data


def deal_data(file_format_data):
    data = []  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    label = None  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    inter_label = None  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    time_stamp = []  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    metrics = [i for i in file_format_data[0]][1:]
    file_format_data = file_format_data[1:]
    for d in file_format_data:
        time_stamp_ = d[0].split()
        time_stamp_ = time_stamp_[0].split("/")
        time_stamp_ = f"{time_stamp_[2]}-{time_stamp_[1]}-{time_stamp_[0]} 00:00:00"
        time_stamp.append(time_stamp_)
        data_ = [float(i) for i in d[1:]]
        data.append(data_)
    data = [np.asarray(data).transpose().tolist()]
    time_stamp = [time_stamp]
    out_data = {"data": data, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data
