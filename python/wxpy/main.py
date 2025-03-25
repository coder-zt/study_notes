import cv2
import numpy as np
import matplotlib.pyplot as plt


# 读取图像
img = cv2.imread("D:/Note/study_notes/python/wxpy/test.jpg")

# 应用双边滤波
blurred_image = cv2.bilateralFilter(img, 9, 55, 12)

# 显示结果
cv2.imshow('Bilateral Filtered Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


















# 分离通道
b, g, r = cv2.split(img)

# 对每个通道进行直方图均衡化
b_eq = cv2.equalizeHist(b)
g_eq = cv2.equalizeHist(g)
r_eq = cv2.equalizeHist(r)

# 合并通道
equalized_image = cv2.merge([b_eq, g_eq, r_eq])

# 显示结果
cv2.imshow("Equalized Color Image", equalized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
img = cv2.imwrite("D:/Note/study_notes/python/wxpy/test_equalized_image.jpg", equalized_image)

# 直方图均衡化
equalized_image = cv2.equalizeHist(img)
# 计算直方图
hist = cv2.calcHist([equalized_image], [0], None, [50], [0, 50])


print(hist)
w, h = img.shape
x = 0
y = 0
for i in range(w):
    for j in range(h):
        print(f"{i},{j}:{img[i][j]}")
        if equalized_image[i][j] <= 50 and equalized_image[i][j] >= 40:
            img[i][j] = 0
            x = x + 1
        else:
            img[i][j] = 255
            y = y + 1
print(f"--------------------------------------------> {x},{y}")
cv2.imshow("img-res", img)
# 显示结果
cv2.imshow("Equalized Image", equalized_image)
# cv2.waitKey(0)
# 绘制直方图
plt.plot(hist)
plt.title('Grayscale Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.show()
