import numpy as np
import simdjson as json
import csv
import datetime


point_num = []


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data)  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    metrics = get_metrics(data)  # 指标物理意义说明；数据形状为（指标数量）；
    label = None  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    inter_label = None  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    time_stamp = get_timestamp(data)  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_data(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


def trans_data(data):
    ret_data = [[]]
    for i, line_data in enumerate(data[5:]):
        line_data.pop(87)
        line_data.pop(86)
        line_data.pop(51)
        line_data.pop(50)
        line_data = line_data[3:]
        data_point = []
        for j in line_data:
            try:
                data_point.append(float(j))
            except ValueError:
                data_point.append(float('nan'))
        ret_data[0].append(data_point)
    ret_data[0] = np.transpose(ret_data[0]).tolist()
    return ret_data


def get_metrics(data):
    ret = []
    for i, inter in enumerate(data[4]):
        if i != 87 and i != 86 and i != 51 and i != 50:
            ret.append(inter)
    return ret[3:]


def get_timestamp(data):
    ret = [[]]
    for line_data in data[5:]:
        date = line_data[1]
        time = line_data[2]
        dt = datetime.datetime.strptime(date, '%m/%d/%Y')
        tm = datetime.datetime.strptime(time[:-3], '%H.%M.%S')
        if 'PM' in time and tm.hour != 12:
            tm = tm + datetime.timedelta(hours=12)
        if 'AM' in time and tm.hour == 12:
            tm = tm - datetime.timedelta(hours=12)
            date = datetime.datetime(dt.year, dt.month, dt.day, tm.hour, tm.minute, tm.second).strftime('%Y-%m-%d %H:%M:%S')
            ret[0].append(date)
    return ret
