import numpy as np

# 向量内积
x = np.array([1, 2])
y = np.array([1, 2])
result = np.dot(x, y)
print(result)

# 矩阵的乘法运算
# 2 * 3     3*2
# [[1,2,3] [[1,2]  [[14, 20]
# [4,5,6]] [2,3]   [32, 47]]
#          [3,4]]
x = np.array([[1, 2, 3], [4, 5, 6]])
y = np.array([[1, 2], [2, 3], [3, 4]])
result = np.dot(x, y)
print(result)

# 矩阵的乘法运算
# 2 * 3        3         2
# [[1,2,3] [1, 2, 4]  [17 38]
# [4,5,6]]             
# 矩阵和向量的乘法,向量会自动转为n*1的矩阵，计算结果也会自动转为向量
x = np.array([[1, 2, 3], [4, 5, 6]])
y = np.array([1, 2, 4])
result = np.dot(x, y)
print(result)