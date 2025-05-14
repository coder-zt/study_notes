# mnist_loader.py
"""
一个加载 MNIST 图像数据的库。关于返回的数据结构的细节，参见 load_data 和 load_data_wrapper 的文档字符
串。在实践中，load_data_wrapper 通常是神经网络代码调用的函数。
"""

#### Libraries
# Standard library
import pickle
import gzip

# Third-party libraries
import numpy as np

import os

basePath = os.path.abspath(os.path.dirname(__file__))


def load_data():
    """
    以元组形式返回 MNIST 数据，包含训练数据、验证数据和测试数据。
    返回的 training_data 是有两项的元组，第一项包含实际的训练图像，是一个有 50 000 项的 NumPy ndarray。
    每一项是一个有着 784 个值的 NumPy ndarray，代表一幅 MNIST 图像中的 28×28=784 像素。
    元组 training_data 的第二项是一个包含 50 000 项的 NumPy ndarray，这些项对应于元组第一项中包含的
    图像数字（0～9）。
    validation_data 和 test_data 类似，但图像仅有 10 000 幅。
    这种数据格式很好，但在神经网络中，对 training_data 的格式进行微调很有用。这通过封装函数
    load_data_wrapper()完成，参见下面的代码。
    """
    f = gzip.open(f"{basePath}/../dataset/mnist.pkl.gz", "rb")
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()
    return (training_data, validation_data, test_data)


def load_data_wrapper():
    """
    回一个元组，包含(training_data, validation_data, test_data)。基于 load_data，但是这个格式更便于实现神经网络。
    training_data 是一个包含 50 000 个二元组(x, y)的列表，其中 x 是一个 784 维的 NumPy ndarray，对应输入图像；y 是一个 10 维的 NumPy ndarray，表示对应 x 正确数字的单位向量。
    validation_data 和 test_data 各包含 10 000 个二元组(x, y)，其中 x 是一个包含输入图像的 784 维的 NumPy ndarray；y 是相应的分类，对应于 x 的值（整数）。
    显然，这意味着训练数据、验证数据和测试数据采用不同的格式。这些格式对于神经网络代码来说是最方便的."""
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)


def vectorized_result(j):
    '''
    返回一个 10 维的单位向量，在第 j 个位置为 1.0，其余均为 0。这可以用于将一个数字（0～9）转换成神经网络的一个对应
    '''
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e
