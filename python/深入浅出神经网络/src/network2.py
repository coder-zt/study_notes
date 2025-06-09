"""
network.py 的一个改进版本，实现了针对前馈神经网络的随机梯度下降算法。改进之处包括增加了交叉熵代价函
数、正则化和更好的权重初始化方法。注意，这里着重于让代码简单易读且易修改，并没有进行优化，略去了不
少可取的特性。
"""

import numpy as np
import json
import sys
import random


class CrossEntoryCost(object):
    """
    交叉熵损失函数
    """

    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y * np.log(a) - (1 - y)) * np.log(1 - a))

    @staticmethod
    def delta(z, a, y):
        return a - y


class QuadraticCost(object):
    """
    二次损失函数
    """

    @staticmethod
    def fn(a, y):
        return 0.5 * np.sum((a - y) ** 2)

    @staticmethod
    def delta(z, a, y):
        return (a - y) * sigmoid_prime(z)


class Network(object):

    def __init__(self, sizes, cost=CrossEntoryCost):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.default_weight_initializer()
        self.cost = cost

    # 权重初始化方法，均值为0，标准差为1/sqrt(n),n为对应的输入连接数
    def default_weight_initializer(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [
            np.random.randn(y, x) / np.sqrt(x)
            for x, y in zip(self.sizes[:-1], self.sizes[1:])
        ]

    # 旧的初始化方法
    def large_weight_initializer(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [
            np.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])
        ]

    # 前向传播
    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(
        self,
        training_data,
        epochs,
        mini_batch_size,
        eta,
        lmbda=0.0,
        evaluation_data=None,
        monitor_evaluation_cost=False,
        monitor_evaluation_accuracy=False,
        monitor_training_cost=False,
        monitor_training_accuarcy=False,
    ):
        training_data = list(training_data)
        evaluation_data = list(evaluation_data)
        if evaluation_data:
            n_data = len(evaluation_data)
        n = len(training_data)
        evaluation_cost, evaluation_accuracy = [], []
        training_cost, training_accuray = [], []
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k : k + mini_batch_size]
                for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta, lmbda, len(training_data))
            print(f"Epoch {j} complete")
            if monitor_training_cost:
                cost = self.total_cost(training_data, lmbda)
                training_cost.append(cost)
                print(f"Cost on training data: {cost}")
            if monitor_training_accuarcy:
                accuracy = self.accuracy(training_data, convert=True)
                training_accuray.append(accuracy)
                print(f"Accuracy on training data: {accuracy} / {n}")
            if monitor_evaluation_cost:
                cost = self.total_cost(evaluation_data, lmbda, convert=True)
                evaluation_cost.append(cost)
                print(f"Cost on evaluation data: {cost}")
            if monitor_evaluation_accuracy:
                accuracy = self.accuracy(evaluation_data)
                evaluation_accuracy.append(accuracy)
                print(f"Accuracy on evaluation data: {accuracy} / {n_data}")
            print("\n\n")
        return evaluation_cost, evaluation_accuracy, training_cost, training_accuray

    # 梯度下降
    def update_mini_batch(self, mini_batch, eta, lmbda, n):
        """
        mini_batch: 小批量数据集
        eta: 学习率
        lmbda: 正则化参数
        n: 训练数据集的大小
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delat_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delat_nabla_w)]
        self.weights = [
            (1 - eta * (lmbda / n)) * w - (eta / len(mini_batch)) * nw
            for w, nw in zip(self.weights, nabla_w)
        ]
        self.biases = [
            b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)
        ]

    # 后向传播
    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = (self.cost).delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_b, nabla_w)

    def accuracy(self, data, convert=False):
        """
        计算神经网络在数据集上的准确率
        data: 数据集
        convert: 是否将数据转换为向量形式
        """
        if convert:
            results = [
                (np.argmax(self.feedforward(x)), np.argmax(y)) for (x, y) in data
            ]
        else:
            results = [(np.argmax(self.feedforward(x)), y) for (x, y) in data]
        return sum(int(x == y) for (x, y) in results)

    def total_cost(self, data, lmbda, convert=False):
        """
        计算代价函数的总和
        data: 数据集
        lmbda: 正则化参数
        convert: 是否将数据转换为向量形式
        """
        cost = 0.0
        for x, y in data:
            a = self.feedforward(x)
            if convert:
                y = vectorized_result(y)
            cost += self.cost.fn(a, y) / len(data)
        cost += (
            0.5
            * (lmbda / len(data))
            * sum(np.linalg.norm(w) ** 2 for w in self.weights)
        )
        return cost

    # 保存神经网络参数
    def save(self, filename):
        data = {
            "sizes": self.sizes,
            "cost": self.cost.__class__.__name__,
            "weights": [w.tolist() for w in self.weights],
            "biases": [b.tolist() for b in self.biases],
        }
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


#### 加载神经网络
def load(filename):
    """从 filename 文件加载神经网络，并返回神经网络实例。"""
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["sizes"], cost=cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net


def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


# 激活函数：sigmoid
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


# 激活函数(sigmoid)的导函数
def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))
