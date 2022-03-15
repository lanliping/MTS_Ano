import numpy as np
import simdjson as json
import xlrd
import datetime


point_num = []


def write_data(path, data):
    with open(path, "w") as w:
        json.dump(data, w)


def deal_data(data):
    data_ = trans_data(data['data'])  # 原始数据；数据形状为（实体数量*指标数量*观测时间点数量）
    label = get_label(data['data'])  # 异常标注；数据形状为（实体数量*观测时间点量）；0表示正常 1表示异常
    time_stamp = get_timestamp(data['data'])  # 原始数据收集的时间戳；数据形状为（实体数量*观测时间点量）；整理成 yyyy(年)-mm(月)-dd(日) hh(时，24小时制):mm(分):ss(秒)
    metrics = get_metrics(data['data'])  # 指标物理意义说明；数据形状为（指标数量）；
    inter_label = get_inter(time_stamp, data['inter_label'], metrics)  # 解释性标注；数据形状为（实体数量*观测时间点量）；对哪个维度发生异常进行解释，指标从0开始计数（例：某条数据共有5个指标，第一个指标和第五个指标发生异常则用[0,4]表示）
    out_data = {"data": data_, "label": label, "inter_label": inter_label, "time_stamp": time_stamp, "metrics": metrics}
    return out_data


def read_each(file, sheet):
    data = []
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name(sheet)
    row_len = sh.nrows
    for i in range(row_len):
        data.append(sh.row_values(rowx=i))
    return data


def read_attacks(file, sheet):
    data = []
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name(sheet)
    for i in range(1, 42):
        data.append(sh.row_values(rowx=i))
    for i, timestamp in enumerate(data):
        if timestamp[2] == '':
            continue
        start = xlrd.xldate_as_datetime(timestamp[1], 0)
        end = xlrd.xldate_as_datetime(timestamp[2], 0)
        end = datetime.datetime(start.year, start.month, start.day, end.hour, end.minute, end.second)
        data[i][1] = start
        data[i][2] = end
    return data


def read_data(parent):
    data = read_each(parent['data_path'], 'Combined Data')
    inter_label = read_attacks(parent['inter_path'], 'Sheet1')
    out_data = {"data": data, "inter_label": inter_label}
    return out_data


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
        if 'PM' in d[0] and tm.hour != 12:
            tm = tm + datetime.timedelta(hours=12)
        tm_str = tm.strftime('%Y-%m-%d %H:%M:%S')
        ret[0].append(tm_str)
    return ret


def get_metrics(data):
    ret = []
    for i in data[1][1:-1]:
        ret.append(i.strip())
    return ret


def get_inter(timestamp, data, metrics):
    ret = [[]]
    timestamp = timestamp[0]
    for i in timestamp:
        ret[0].append(get_attack_point(i, data, metrics))
    return ret


def get_attack_point(time, data, metrics):
    ret = []
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    for i in data:
        if i[2] == '':
            continue
        if i[1].__le__(time) and time.__le__(i[2]):
            points = i[3]
            if ', ' in points:
                points = points.split(', ')
                for point in points:
                    point = point.replace('-', '')
                    if point in metrics:
                        ret.append(metrics.index(point))
                    else:
                        return None
                return ret
            elif '; ' in points:
                points = points.split('; ')
                for point in points:
                    point = point.replace('-', '')
                    if point in metrics:
                        ret.append(metrics.index(point))
                    else:
                        return None
                return ret
            points = points.replace('-', '')
            if points in metrics:
                ret.append(metrics.index(points))
                return ret
    return None
