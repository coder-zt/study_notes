from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
import os

path = f"{os.path.dirname(__file__)}/dataset/"

print(path)

train = MNIST(path, train=True, download=True, transform=ToTensor())
test = MNIST(path, train=False, download=True, transform=ToTensor())


# from PIL import Image
# import torch
# import torchvision.transforms as transforms

# imagePath = ""
# image = Image.open(imagePath)
# transform = transforms.ToTensor()
# tensor = transform(image)
# print(image)
# print(tensor)
# print(tensor.shape)
# print(tensor.dtype)


from torch.utils.data import DataLoader
import matplotlib.pyplot as pyplot

trainDL = DataLoader(train, batch_size=64, shuffle=True)
testDL = DataLoader(test, batch_size=32, shuffle=True)

# i, (inputs, targets) = next(enumerate(trainDL))
# for i in range(25):
#     pyplot.subplot(5, 5, i + 1)
#     pyplot.imshow(inputs[i][0], cmap="gray")
# pyplot.show()


from torch.nn import Module, Conv2d, ReLU, MaxPool2d, init, Linear, Softmax


class CNN(Module):

    def __init__(self, n_channels):
        super().__init__()
        # 卷积层
        self.hidden1 = Conv2d(n_channels, 32, (3, 3))
        # 初始化权重
        init.kaiming_uniform_(self.hidden1.weight, nonlinearity="relu")
        # 设置激活函数
        self.act1 = ReLU()
        # 池化层(池化大小，池化步长)
        self.pool1 = MaxPool2d((2, 2), stride=(2, 2))

        # 卷积层2
        self.hidden2 = Conv2d(32, 32, (3, 3))
        # 初始化权重
        init.kaiming_uniform_(self.hidden2.weight, nonlinearity="relu")
        self.act2 = ReLU()

        # 池化层2(池化大小，池化步长)
        self.pool2 = MaxPool2d((2, 2), stride=(2, 2))

        # 全连接层
        self.hidden3 = Linear(5 * 5 * 32, 1024)
        init.kaiming_uniform_(self.hidden3.weight, nonlinearity="relu")
        self.act3 = ReLU()


        self.hidden5 = Linear(1024, 1024)
        init.kaiming_uniform_(self.hidden5.weight, nonlinearity="relu")
        self.act5 = ReLU()
        
        # 输出层
        self.hidden4 = Linear(1024, 10)
        init.xavier_uniform_(self.hidden4.weight)
        self.act4 = Softmax(dim=1)

    # def test():

    def forward(self, X):
        # 第一次卷积池化
        X = self.hidden1(X)
        X = self.act1(X)
        X = self.pool1(X)
        # 第二次卷积池化
        X = self.hidden2(X)
        X = self.act2(X)
        X = self.pool2(X)
        # 扁平化
        X = X.view(-1, 5 * 5 * 32)
        # 全连接层的隐藏层
        X = self.hidden3(X)
        X = self.act3(X)
        
        
        X = self.hidden5(X)
        X = self.act5(X)
        
        # 输出层
        X = self.hidden4(X)
        X = self.act4(X)
        return X


from torch.nn import CrossEntropyLoss
from torch.optim import SGD


def train_model(trainDL, model):
    # 定义优化器
    criterion = CrossEntropyLoss()  # 交叉熵损失函数
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9)  # 动量
    for epoch in range(20):
        # 每句mini batch
        for i, (inputs, tragets) in enumerate(trainDL):
            optimizer.zero_grad()  # 清除梯度
            yhat = model(inputs)
            loss = criterion(yhat, tragets)  # 计算损失
            loss.backward()  # 反向传播
            optimizer.step()  # 更新参数
            if i % 1000 == 0:  
                acc = evaluate_model(testDL, model)
                print(f"epoch<{epoch}>: Accuracy: {acc * 100:.3f}%")  

import numpy as np
from sklearn.metrics import accuracy_score

def evaluate_model(testDL, model):
    predictions,actuals = list(),list()
    for i,(inputs, tragets) in enumerate(testDL):
        yhat = model(inputs)
        yhat = yhat.detach().numpy()
        yhat = yhat.argmax(axis=1)
        actual = tragets.numpy()
        yhat = yhat.reshape((len(yhat), 1))
        
        # print(f"yhat ===> {yhat}")
        actual = actual.reshape((len(actual), 1))
        # print(f"actual ===> {actual}")
        predictions.append(yhat)
        actuals.append(actual)
    actuals, predictions = np.vstack(actuals), np.vstack(predictions)
    acc = accuracy_score(actuals, predictions)
    return acc

train_model(trainDL, CNN(1))