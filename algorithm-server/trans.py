# @Time : 2020/12/9 9:13
# @Author : 亓瑞
# @File : trans.py
# @desc : using pymprog !

from pymprog import *
import numpy as np


def trans(a, b, c):
    # print(a)
    # print(b)
    # print(c)
    (width, length) = np.array(c).shape
    # print(length)
    price = dict()
    for i in a:
        for j in b:
            price[i, j] = c[a.index(i)][b.index(j)]
    # 产地:产量
    d = c[:, length-1]
    produce = dict()
    for i in a:
        produce[i] = d[a.index(i)]
    # 销地:销量
    e = c[width-1, :]
    sale = dict()
    for i in b:
        sale[i] = e[b.index(i)]
    # 模型及求解
    begin('transport')
    x = var('x', price.keys())                                             # 调运方案
    minimize(sum(price[i, j]*x[i, j] for (i, j) in price.keys()), 'Cost')  # 总运费最少
    for i in produce.keys():                                               # 产地产量约束
        sum(x[i, j] for j in sale.keys()) == produce[i]
    for j in sale.keys():                                                  # 销地销量约束
        sum(x[i ,j] for i in produce.keys()) == sale[j]
    solve()
    s = ''
    s += "Result Cost(Total):%6.2f\n" % vobj()
    # print("\nResult Cost(Total):%6.2f" % vobj())
    echo = [['运量'] + [j for (i, j) in price.keys() if i == 'A1']]
    count = 0
    for (i, j) in price.keys():
        if count % length == 0:
            echo.append([i] + [int(x[e, k].primal) for (e, k) in price.keys() if e == i])
            count = 0
        count += 1
    # print(echo)
    for c in echo[0]:
        s += '%-4s\t' % c
    s += '\n'
    for r in echo[1:]:
        for c in r:
            s += '%-10s\t' % c
        s += '\n'
    # print(s)
    end()
    return s

if __name__ == '__main__':
    trans()

