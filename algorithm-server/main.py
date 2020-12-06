# @Time : 2020/12/6 22:47
# @Author : 亓瑞
# @File : main.py
# @desc :
import numpy as np

from flask import Flask,request,jsonify,make_response
from flask_cors import CORS
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


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
                return fit
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
                    return fit
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
                return fit
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
                    return fit
                else:
                    row_index = temp.index(min(temp))
                    # 更新data
                    base_list[row_index] = column
                    row_index += 1
                    data[row_index, :] /= data[row_index, column]
                    for i in [x for x in range(1, width) if x != row_index]:
                        data[i, :] += (-data[i, column] * data[row_index, :])


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


@app.route('/simplexMin',methods=['GET','POST'])
def simplex_min():
    params = request.get_data()
    json_data = json.loads(params.decode('utf-8'))
    metaData = json_data["meta"]

    rawMetaData = metaData.replace('#', '\n')
    filename = './simplex.txt'
    with open(filename, 'w') as file_object:
        file_object.write(rawMetaData)

    data_min = np.loadtxt(filename, dtype=np.float)
    value = Simplex.min(data_min)

    result = {
        'status': 20000,
        'message': '这里你看到的是单纯形法',
        "data": value
    }
    # cur.close()
    # conn.close()
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    response.status = "200"
    return response


@app.route('/simplexMax',methods=['GET','POST'])
def simplex_max():
    params = request.get_data()
    json_data = json.loads(params.decode('utf-8'))
    metaData = json_data["meta"]

    rawMetaData = metaData.replace('#', '\n')
    filename = './simplex.txt'
    with open(filename, 'w') as file_object:
        file_object.write(rawMetaData)

    data_max = np.loadtxt(rawMetaData, dtype=np.float)
    value = Simplex.max(data_max)

    result = {
        'status': 20000,
        'message': '这里你看到的是单纯形法',
        "data": value
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
    data_min = np.loadtxt("data-3.1.2.txt", dtype=np.float)
    print(data_min)
    app.run(host="0.0.0.0")
