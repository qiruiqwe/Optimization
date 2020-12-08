# @Time : 2020/12/6 22:47
# @Author : 亓瑞
# @File : main.py
# @desc :
import numpy as np

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import transportation_problem as tp

app = Flask(__name__)


class Simplex(object):
    @staticmethod
    def min(data):
        (width, length) = data.shape
        base_list = list(range(length - width, length - 1))
        while True:
            no_base_list = [i for i in range(length - 1) if i not in base_list]
            c_b = data[0][base_list]
            distinguish_number = [np.dot(data[1:, i], c_b) - data[0][i] for i in no_base_list]
            # 1.计算适应度值
            b = data[1:, length - 1]
            fit = np.dot(b, c_b)
            # 2.判决数都 < 0，结束循环
            if max(distinguish_number) < 0:
                # base_list是x的序号的值，b是对应的x的值
                return fit, base_list, b
            else:
                # 3.换入列号
                column = no_base_list[distinguish_number.index(max(distinguish_number))]
                # 4.换出列号
                temp = []
                for a, c in zip(data[1:, length - 1], data[1:, column]):
                    if c <= 0:
                        temp.append(float('inf'))
                    else:
                        temp.append(a / c)
                if min(temp) == float('inf'):
                    # 4.1.没有可换出列
                    return fit, base_list, b
                else:
                    row_index = temp.index(min(temp))
                    # 更新data
                    base_list[row_index] = column
                    row_index += 1
                    data[row_index, :] /= data[row_index, column]
                    for i in [x for x in range(1, width) if x != row_index]:
                        data[i, :] += (-data[i, column] * data[row_index, :])

    @staticmethod
    def max(data):
        (width, length) = data.shape
        base_list = list(range(length - width, length - 1))
        while True:
            no_base_list = [i for i in range(length - 1) if i not in base_list]
            c_b = data[0][base_list]
            distinguish_number = [np.dot(data[1:, i], c_b) - data[0][i] for i in no_base_list]
            # 1.计算适应度值
            b = data[1:, length - 1]
            fit = np.dot(b, c_b)
            # 2.判决数都 < 0，结束循环
            if min(distinguish_number) > 0:
                return fit, base_list, b
            else:
                # 3.换入列号
                column = no_base_list[distinguish_number.index(min(distinguish_number))]
                # 4.换出列号
                temp = []
                for a, c in zip(data[1:, length - 1], data[1:, column]):
                    if c <= 0:
                        temp.append(float('inf'))
                    else:
                        temp.append(a / c)
                if min(temp) == float('inf'):
                    # 4.1.没有可换出列
                    return fit, base_list, b
                else:
                    row_index = temp.index(min(temp))
                    # 更新data
                    base_list[row_index] = column
                    row_index += 1
                    data[row_index, :] /= data[row_index, column]
                    for i in [x for x in range(1, width) if x != row_index]:
                        data[i, :] += (-data[i, column] * data[row_index, :])

    @staticmethod
    def formatString(data, flag, value, base_list, base_value):
        # flag = 0 最小值  1 最大值
        v_name = []
        (width, length) = data.shape
        for i in range(length):
            v_name.append('x'+str(i+1))
        # print(v_name)
        if flag == 0:
            message = 'min '
            param = "最小值为:"
        else:
            message = 'max '
            param = "最大值为:"
        for j in range(length - 1):
            if data[0][j] == 0:
                message = message + "   "
            else:
                message = message + '%2s' % str(int(data[0][j])) + '*' + '%4s' % v_name[j]
            if data[0][j+1] > 0:
                message = message + ' + '
            elif data[0][j+1] == 0:
                pass
        all_message = message + '#'
        for i in range(1, width):
            message = ''
            for j in range(length-1):
                if data[i][j] == 0:
                    message = message + "     "
                else:
                    message = message + '%2s' % str(int(data[i][j])) + '*' + '%4s' % v_name[j]
                if data[i][j + 1] > 0 and (j+1) != (length-1):
                    message = message + '+'
                elif data[i][j + 1] == 0:
                    pass
            message = message + ' = ' + '%2s' % str(int(data[i][length-1]))
            all_message = all_message + message + "#"
        all_message += '#'
        all_message = all_message + '%-8s' %param + '%2s' % str(value) + '#'
        result = ''
        print(base_list)
        print(base_value)
        for i in zip(base_list, base_value):
            result += '%-4s' % v_name[i[0]] + ' = ' + '%5s' % str(i[1]) + '#'
        all_message = all_message + result
        print(all_message)
        return all_message

def getString(s,d):
    str = '产量:'
    for i in s:
        str += '%4s %3d\t' % (i[0], i[1])
    str += '\n'+'销量:'
    for i in d:
        str += '%4s %3d\t' % (i[0], i[1])
    str += '\n'
    return str

@app.route('/simplexMin', methods=['GET', 'POST'])
def simplex_min():
    params = request.get_data()
    json_data = json.loads(params.decode('utf-8'))
    metaData = json_data["meta"]

    rawMetaData = metaData.replace('#', '\n')
    filename = './simplex.txt'
    with open(filename, 'w') as file_object:
        file_object.write(rawMetaData)
    dataMin = np.loadtxt(filename, dtype=np.float)
    # print(data_min)
    value, base_list, base_value = Simplex.min(dataMin)
    dataMin = np.loadtxt(filename, dtype=np.float)
    info = Simplex.formatString(dataMin, 0, value, base_list, base_value)
    print(info)
    result = {
        'status': 20000,
        'message': '这里你看到的是单纯形法',
        "data": value,
        "info": info
    }
    # cur.close()
    # conn.close()
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    response.status = "200"
    return response


@app.route('/simplexMax', methods=['GET', 'POST'])
def simplex_max():
    params = request.get_data()
    json_data = json.loads(params.decode('utf-8'))
    metaData = json_data["meta"]
    print(metaData)
    rawMetaData = metaData.replace('#', '\n')
    filename = './simplex.txt'
    with open(filename, 'w') as file_object:
        file_object.write(rawMetaData)

    dataMax = np.loadtxt(filename, dtype=np.float)
    print(dataMax)
    value, base_list, base_value = Simplex.max(dataMax)
    dataMax = np.loadtxt(filename, dtype=np.float)
    info = Simplex.formatString(dataMax, 1, value, base_list, base_value)
    print(info)
    result = {
        'status': 20000,
        'message': '这里你看到的是单纯形法',
        "data": value,
        "info": info
    }
    # cur.close()
    # conn.close()
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    response.status = "200"
    return response


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    params = request.get_data()
    json_data = json.loads(params.decode('utf-8'))
    metaData = json_data["meta"]
    print(metaData)
    rawMetaData = metaData.replace('#', '\n')
    filename = './transportation.txt'
    with open(filename, 'w') as file_object:
        file_object.write(rawMetaData)

    dataMax = np.loadtxt(filename, dtype=np.float)
    print(dataMax)

    (width, length) = dataMax.shape
    # 产地数组
    product = ['A' + str(i) for i in range(1, width)]
    print(product)
    # 销地名称数组
    sale = ['B' + str(i) for i in range(1, length)]
    print(sale)
    s = [(product[i], dataMax[i, length - 1]) for i in range(width - 1)]
    d = [(sale[i], dataMax[width - 1, i]) for i in range(length - 1)]
    c = dataMax[:width - 1, :length - 1]
    info = getString(s, d)
    print(s)
    print(d)
    print(c)
    # s = [('A1', 14), ('A2', 27), ('A3', 19)]
    # d = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    # c = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    p = tp.TransportationProblem(s, d, c)
    r = p.solve()
    s = r.__str__()
    info += s
    result = {
        'status': 20000,
        'message': '这里你看到的是单纯形法',
        "info": info,
    }
    # cur.close()
    # conn.close()
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    response.status = "200"
    return response


if __name__ == '__main__':
    '''
        第一行为数据
        其余行为约束
    '''
    # data_min = np.loadtxt("data-3.1.2.txt", dtype=np.float)
    # value = Simplex.min(data_min)
    # print(value)
    # data_max = np.loadtxt("data-3.1.3.txt", dtype=np.float)
    # value = Simplex.max(data_max)
    # print(value)

    # data_min = np.loadtxt("data-3.1.2.txt", dtype=np.float)
    data_max = np.loadtxt("data-3.1.3.txt", dtype=np.float)
    # value = Simplex.max(data_max)
    # print(data_min)
    value, base_list, base_value = Simplex.max(data_max)
    info = Simplex.formatString(data_max, 1, value, base_list, base_value)
    print(info)
    app.run(host="0.0.0.0")
