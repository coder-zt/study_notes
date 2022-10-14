import numpy as np
# 利用numpy从零搭建一个神经网络

# 激活函数
def sigmoid(x):
    
    return 1 / (1 + np.exp(-x))

# 初始化模型参数，权值和偏置
def initilize_with_zeros(dim):
    w = np.zeros((dim, 1))
    b = 0.0
    #assert(w.shape == (dim, 1))
    #assert(isinstance(b, float) or isinstance(b, int))
    return w, b

def propagate(w, b, X, Y):
    m = X.shape[1]
    print("w ===> " + str(w))
    print("m ===> " + str(m))
    
    print("np.dot(w.T, X) + b ===> " + str(np.dot(w.T, X) + b))
    A = sigmoid(np.dot(w.T, X) + b)
    print("A ===> " + str(A))
    
    cost = -1/m * np.sum(Y*np.log(A) + (1-Y)*np.log(1-A))
    
    print("cost ===> " + str(cost))
# 求导数推导
# y = sigmoid(u) u = wx+b
# dy/du = d(sigmoid(u)) du/dx = w

x = np.array([[1],[2],[3],[4]])
y = np.array([[1],[1/4],[1/9],[1/16]])
w,b = initilize_with_zeros(x.shape[0])
propagate(w,b,x,y)
print(np.exp(0))