import mnist_loader
import math
import network

training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = network.NetWork([784,100, 30, 10], loadModel=False)
# # print(len(list(training_data)))
# # print(len(list(test_data)))

net.SGD(training_data, 30, 30, 3.0, test_data=test_data)

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


