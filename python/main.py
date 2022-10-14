import numpy as np
# import math
# 模拟函数 y = x^2
#  输入层（1） 隐藏层（6） 输出层（1）
#   5       w1-w6 b1-b6 w' b' 25
# 
#   Z2 = np.dot(W2, Z1) + b2
#   A2 = sigmoid(Z2) 
#  A2 - Y = sigmoid(Z2) - Y
#  令 y = A2 - Y
#  y = sigmoid(Z2) - Y
#  dy/dZ2 = sigmoid(Z2)‘
# dZ2/dw = Z1
# dy/dw = Z1 * sigmod(Z2)
def activeValues(x):
    vals = []
    for loc in x:
        locVals = []
        for value in loc:
            if value > 0:
                locVals.append(value)
            else:
                locVals.append(0.05 * value)
        vals.append(locVals)
    return np.array(vals)

def activeValuesRes(x):
    vals = []
    for loc in x:
        locVals = []
        for value in loc:
            if value > 0:
                locVals.append(value)
            else:
                locVals.append(value /0.05)
        vals.append(locVals)
    return np.array(vals)


def activeNormalize(x):
    return 1 / (1 + np.exp(-x))
    # vals = []
    # for loc in x:
    #     locVals = []
    #     for value in loc:
    #         if value > 0:
    #             locVals.append(1)
    #         else:
    #             locVals.append(0.05)
    #     vals.append(locVals)
    # return np.array(vals)

def initilizeHideParams(dim):
    w = np.array([[1],[2],[3]])
    b = np.array([[3,2,1]])
    return w,b

def initilizeOutputParams(dim):
    w = np.array([[1],[2],[3]])
    b = 10
    return w,b

def prograte(x, Y, w, b,wo,bo, learnRatio):
    count = x.shape[0]
    # print("np.dot(w.T,x) + b ===> " + str(np.dot(x, w.T) + np.dot(np.ones(shape=(count, 1)), b)))
    hideVals = activeNormalize(np.dot(x, w.T) + np.dot(np.ones(shape=(count, 1)), b))
    print("hideVals ===>" + str(hideVals)) # 3*1
    _y = activeNormalize(np.dot(hideVals, wo) + bo)
    print("预测：" + str(1/_y))
    # print("平方差" + str(np.square(Y - _y)))
    # #误差的导数
    dy = 2 * (_y - Y) * activeNormalize(_y)
    # print("误差的导数 ===> " + str(dy))
    # # 输出层w'的导数
    dw_ = np.dot(dy.T, hideVals)/count
    dw_diff = dw_ * learnRatio
    newWo = wo - dw_diff.T
    # print("输出层w'的导数 ===> " + str(newWo))
    # # 输出层b'的导数
    db_ = dy
    db_diff = db_ * learnRatio
    newBo = np.mean(bo - db_diff.T)
    # print("输出层b'的导数 ===> " + str(newBo))
    # # 隐藏层w的导数 x * wo * dy * activeizal(hideVals)
    # # (1,2) (1,3) (1,2)
    dw = np.array([np.mean(np.dot(wo, (x * dy).T) * activeNormalize(hideVals).T,axis=1) * learnRatio])
    newW = w - dw.T
    # print("隐//藏层w的导数 ===> " + str(newW))
    #  # 隐藏层b的导数
    db = np.array([np.mean(np.dot(wo, dy.T) * activeNormalize(hideVals).T,axis=1) * learnRatio])
    newB =  b - db
    # print("隐藏层b的导数 ===> " + str(newB))

    return {"w":newW,
            "b":newB,
            "wo":newWo,
            "bo":newBo}


# x = 1
# y = [[2],[3],[2]]
# y = wx+b
def test():
    w,b = initilizeHideParams(6)
    wo,bo = initilizeOutputParams(6)
    # x = np.array([[5],[6]])
    # y = [[25],[36]]
    
    x = np.array([[2],[4],[6]])#,[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24],[25],[26],[27],[28],[29],[30]
    y = np.array([[1/4],[1/16],[1/36]])
    print(y)
    ratio = 0.01
    result = prograte(x,y,w,b,wo,bo, ratio)
    print("\n\n")
    # for i in range(0,4000):
    #     # print(result)
    #     result = prograte(x,y,result["w"],result["b"],result["wo"],result["bo"], ratio)
    #     print("\n\n")
    # wo 
    #     # result = prograte([[6]],[[36]],result["w"],result["b"],result["wo"],result["bo"], ratio)

    result = prograte(np.array([[3]]),np.array([[0.05]]),result["w"],result["b"],result["wo"],result["bo"], ratio)

test()