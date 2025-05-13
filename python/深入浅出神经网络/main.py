import mnist_loader
import math

def getNumber(r):
    num = -1
    for i in r:
        num += 1
        if i == 1:
            return num
res = mnist_loader.load_data_wrapper()
j = 0
for r in res[0]:
    for index, i in enumerate(r[0]):
        if index % 28 == 0:
            print()
        print(math.ceil(i[0]), end="")
        print(math.ceil(i[0]), end="")
    print()
    # print(r[0].sum())
    # print(r[1])
    print(getNumber(r[1]))
    j = j + 1
    if j > 10:
        break

#     return (training_data, validation_data, test_data)