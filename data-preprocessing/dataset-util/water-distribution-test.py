import numpy as np
import simdjson as json
import csv
import datetime
import xlrd


point_num = []


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data['data'])  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    metrics = get_metrics(data['data'])  # 指标物理意义说明；数据形状为（指标数量）；
    inter_label = None  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    time_stamp = get_timestamp(data['data'])  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    label = get_label(time_stamp, data['label'])  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_data(parent):
    data_ = []
    with open(parent['data_path'], 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data_.append(row)

    label = []
    wb = xlrd.open_workbook(parent['label_path'])
    sh = wb.sheet_by_name('Table 1')
    row_len = sh.nrows
    for i in range(row_len):
        label.append(sh.row_values(rowx=i))

    out_data = {"data": data_, "label": label}
    return out_data


def trans_data(data):
    ret_data = [[]]
    for i, line_data in enumerate(data[1:]):
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
    for i, inter in enumerate(data[0]):
        if i != 87 and i != 86 and i != 51 and i != 50:
            ret.append(inter)
    return ret[3:]


def get_timestamp(data):
    ret = [[]]
    for line_data in data[1:]:
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


def read_label(file, sheet):
    data = []
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name(sheet)
    row_len = sh.nrows
    for i in range(row_len):
        data.append(sh.row_values(rowx=i))
    return data


def get_label(timestamp, data):
    ret = [[]]
    for tm in timestamp[0]:
        tm = datetime.datetime.strptime(tm, '%Y-%m-%d %H:%M:%S')
        for i in data[1:]:
            start = datetime.datetime.strptime(str_insert(i[1], '20', -11), '%d/%m/%Y %H:%M:%S')
            end = datetime.datetime.strptime(str_insert(i[2], '20', -11), '%d/%m/%Y %H:%M:%S')
            if start.__le__(tm) and tm.__le__(end):
                ret[0].append(1)
                break
        ret[0].append(0)
    return ret


def str_insert(s, ins, pos):
    str_list = list(s)
    str_list.insert(pos, ins)
    return ''.join(str_list)
