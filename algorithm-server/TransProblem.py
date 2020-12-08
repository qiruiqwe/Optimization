# @Time : 2020/12/7 20:46
# @Author : 亓瑞
# @File : TransProblem.py
# @desc : 运输问题
import numpy as np
class TranProblem(object):
    def __init__(self, data):
        self.data = data

    def initSolution(self, data):
        # 使用西北角法获得初始值
        (width, length) = data.shape
        table = np.zeros((width, length))
        for i in range(width-1):
            # 1.行最大数据
            row = data[i][length-1]
            for j in range(length-1):
                # 2.列最大数据
                col = data[width-1][j]
                if row <= col:
                    # 2.1 赋值为行，更新列的值
                    table[i][j] = row
                    data[i][length-1] = 0
                    data[width-1][j] -= row
                    break
                else:
                    # 2.2 赋值为列，更新行的值
                    table[i][j] = col
                    data[i][length - 1] -= col
                    data[width - 1][j] = 0
                    # 2.3 更新行最大
                    row = data[i][length-1]
        fit = np.multiply(table, data)
        value = np.sum(fit)
        print(table)
        print(data)
        print(fit)
        print(value)
        return table, value



if __name__ == '__main__':
    import transportation_problem as tp
    fileName = "transProblem-3.txt"
    trans_data = np.loadtxt(fileName, dtype=np.float)
    # transProblem = TranProblem(trans_data)
    # transProblem.initSolution(trans_data)
    (width, length) = trans_data.shape
    # 产地数组
    product = ['A'+str(i) for i in range(1, width)]
    # print(product)
    # 销地名称数组
    sale = ['B'+str(i) for i in range(1, length)]

    # print(sale)
    s = [(product[i], trans_data[i, length-1]) for i in range(width-1)]
    d = [(sale[i], trans_data[width-1, i]) for i in range(length-1)]
    print(s)
    print(d)
    str =''
    for i in s:
        str += '%4s %3d\t' % (i[0], i[1])
    str += '\n'
    for i in d:
        str += '%4s %3d\t' % (i[0], i[1])
    str += '\n'
    print(str)
    c = trans_data[:width-1, :length-1]
    print(c)

    # s = [('A1', 14), ('A2', 27), ('A3', 19)]
    # d = [('B1', 22), ('B2', 13), ('B3', 12), ('B4', 13)]
    # c = [[6, 7, 5, 3], [8, 4, 2, 7], [5, 9, 10, 6]]
    p = tp.TransportationProblem(s, d, c)
    r = p.solve()
    print(r)
    s = r.__str__()
    value = s.replace('\n', '#')
    print(value)