"""
该模块用于实现前馈神经网络的随机梯度下降算法。通过反像传播算法计算梯度。
注意，这里着重于让代码简单易读且易于修改，并没有进行优化，略去了不少可取的特性
"""

import random
import numpy as np
import json
import os

basePath = f"{os.path.dirname(__file__)}"


class NetWork(object):

    # 列表sizes包含对应层的神经元的数目。
    # 如果列表是[2,3,1],那么就是指一个三层神经网络，第一层有2个神经元，第二层有3个神经元，
    # 第三层有1个神经元。
    # 使用一个均值为0，标准差为1的高斯随机分布初始化神经网络的权重和偏置。注意，假设第一层
    # 是一个输入层，一般不会对这些神经元设置任何偏置，这是因为偏置仅用于计算后面的输出
    def __init__(self, sizes, loadModel=False):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.initBiasesAndWeights(sizes, loadModel)

    def initBiasesAndWeights(self, sizes, loadModel):
        if loadModel and self.read():
            return
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def save(self):
        biasesList = []
        for layerBiases in self.biases:
            layerBiasesList = []
            for biases in layerBiases:
                layerBiasesList.append(biases.tolist().copy())
            biasesList.append(layerBiasesList.copy())

        weightsList = []
        for layerWeights in self.weights:
            layerWeightsList = []
            for weights in layerWeights:
                layerWeightsList.append(weights.tolist().copy())
            weightsList.append(layerWeightsList.copy())

        res = {"biases": biasesList, "weights": weightsList}
        with open(f"{basePath}/model.json", "w") as f:
            json.dump(res, f, ensure_ascii=False, indent=4)

    def read(self, path=None):
        if path == None:
            path = f"{basePath}/model.json"
        modeJson = None
        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            modeJson = json.load(f)
        if modeJson == None:
            return False

        weightsList = modeJson["weights"]
        weights = []
        for layerWeights in weightsList:
            weights.append(np.array(layerWeights))

        biasesList = modeJson["biases"]
        biases = []
        for layerBiases in biasesList:
            biases.append(np.array(layerBiases))
        self.weights = weights
        self.biases = biases
        return True

    # 前向传播
    def feedfoward(self, a):
        for b, w in zip(self.biases, self.weights):
            # np.dot：查看代码示例/sample/np_dot.py
            a = sigmoid(np.dot(w, a) + b)
        return a

    # 使用小批量随机梯度下降算法训练神经网络
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """
        training_data: 训练数据集
        epochs: 迭代次数
        mini_batch_size: 小批量的大小
        eta: 学习率
        test_data: 测试数据集
        使用小批量随机梯度下降算法训练神经网络。training_data 是由训练输入和目标输出的元组(x, y)
        组成的列表。其他非可选参数容易理解。如果提供了 test_data，那么神经网络会在每轮训练结束后用
        测试数据进行评估，并输出部分进度信息。这对于追
        """
        training_data = list(training_data)
        test_data = list(test_data)
        if test_data != None:
            n_test = len(test_data)
        n = len(training_data)
        print(f"tarin_data:{n}  test_data:{n_test}")
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k : k + mini_batch_size]
                for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data != None:
                print(f"Epoch {j}:{self.evaluate(test_data)}/{n_test}")
            else:
                print(f"Epoch {j} complete")

    # 对于一个小批量应用梯度下降算法和反向传播算法来更新神经网络的权重和偏置
    def update_mini_batch(self, mini_batch, eta):
        """
        mini_batch: 小批量数据集
        eta: 学习率
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [
            w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)
        ]
        self.biases = [
            b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)
        ]

    # 反向传播计算权重
    def backprop(self, x, y):
        """
        返回一个表示代价函数 C_x 梯度的元组(nabla_b, nabla_w)。nabla_b 和 nabla_w 是一层接一层的
        numpy 数组的列表，类似于 self.biases 和 self.weights。
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # 前馈
        activation = x
        activations = [x]  # 一层接一层的存放所有激活值
        zs = []  # 一层接一层的存放所用z向量
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # 反向传播
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedfoward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def predict(self, inputRes):
        res = self.feedfoward(inputRes)
        max = 0.0
        value = -1
        for index, i in enumerate(res):
            if i > max:
                max = i
                value = index

        return value

    #  返回关于输出激活值的偏导数的向量
    def cost_derivative(self, output_activations, y):
        return output_activations - y


# 激活函数：sigmoid
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


# 激活函数(sigmoid)的导函数
def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))


if __name__ == "__main__":
    net = NetWork([784, 30, 10])
    # # print(len(list(training_data)))
    # # print(len(list(test_data)))

    # net.SGD(training_data, 30, 30, 3.0, test_data=test_data)
    net.read()
