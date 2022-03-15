import numpy as np
import simdjson as json
import xlrd
import datetime


point_num = []


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data)  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    label = get_label(data)  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    inter_label = None  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    time_stamp = get_timestamp(data)  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    metrics = get_metrics(data)  # 指标物理意义说明；数据形状为（指标数量）；
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_data(file):
    data = []
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name('Normal.csv')
    row_len = sh.nrows
    for i in range(row_len):
        data.append(sh.row_values(rowx=i))
    return data


def trans_data(data):
    ret = []
    data = data[2:]
    for i in data:
        ret.append(i[1:-1])
    ret = np.transpose(ret).tolist()
    ret = [ret]
    return ret


def get_label(data):
    ret = [[]]
    for i in data[2:]:
        if i[-1] == 'Normal':
            ret[0].append(0)
        else:
            ret[0].append(1)
    return ret


def get_timestamp(data):
    ret = [[]]
    for d in data[2:]:
        time_str = d[0][:-3].strip()
        tm = datetime.datetime.strptime(time_str, '%d/%m/%Y %H:%M:%S')
        if 'PM' in d[0]:
            tm = tm + datetime.timedelta(hours=12)
        tm_str = tm.strftime('%Y-%m-%d %H:%M:%S')
        ret[0].append(tm_str)
    return ret


def get_metrics(data):
    ret = []
    for i in data[1][1:-1]:
        ret.append(i)
    return ret
