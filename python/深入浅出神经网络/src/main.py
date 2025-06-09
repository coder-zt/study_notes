import mnist_loader
import math
import numpy as np


training_data, validation_data, test_data = mnist_loader.load_data_wrapper()


# import network
# net = network.NetWork([784, 30, 10], loadModel=False)
# net.SGD(training_data, 30, 30, 3.0, test_data=test_data)

import network2

net = network2.Network([784, 1, 10], cost=network2.CrossEntoryCost)
net.SGD(
    training_data,
    30,
    10,
    0.5,
    lmbda = 5.0,
    evaluation_data=test_data,
    monitor_training_accuarcy=True,
    monitor_training_cost=True,
    monitor_evaluation_accuracy=True,
    monitor_evaluation_cost=True
)

# Epoch 0:8842/10000
# Epoch 1:8997/10000
# Epoch 2:9169/10000
# Epoch 3:9175/10000
# Epoch 4:9256/10000
# Epoch 5:9265/10000
# Epoch 6:9282/10000
# Epoch 7:9295/10000
# Epoch 8:9343/10000
# Epoch 9:9342/10000
# Epoch 10:9345/10000
# Epoch 11:9372/10000
# Epoch 12:9376/10000
# Epoch 13:9386/10000
# Epoch 14:9385/10000
# Epoch 15:9396/10000
# Epoch 16:9393/10000
# Epoch 17:9406/10000
# Epoch 18:9380/10000
# Epoch 19:9426/10000
# Epoch 20:9404/10000
# Epoch 21:9419/10000
# Epoch 22:9424/10000
# Epoch 23:9428/10000
# Epoch 24:9421/10000
# Epoch 25:9420/10000
# Epoch 26:9412/10000
# Epoch 27:9429/10000
# Epoch 28:9427/10000
# Epoch 29:9430/10000
# test_data = list(validation_data)

# def printNum(x):
#     for index, i in enumerate(x):
#         if i > 0.5:
#             print("11", end="")
#         else:
#             print("00", end="")
#         if index > 0 and (index + 1) % 28 == 0:
#             print()

# for x,y in test_data[0:2]:
#     printNum(x)
#     print(net.predict(x))
# break


# print(f"{net.evaluate(test_data)}/{len(test_data)}")

# net.save()
