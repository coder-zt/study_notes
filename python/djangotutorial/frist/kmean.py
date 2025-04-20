import cv2 
import numpy as np 
import matplotlib.pyplot  as plt 
 
path = "/Users/edy/owner/study_notes/python/djangotutorial/frist/img/"
# 读取图像 
image = cv2.imread(f"{path}1348.png")  
# 转换颜色空间，从BGR转换为RGB（matplotlib使用RGB格式） 
image = cv2.cvtColor(image,  cv2.COLOR_BGR2RGB) 
 
# 数据预处理 
# 将图像数据转换为二维数组，每行代表一个像素，每列代表一个颜色通道 
pixel_values = image.reshape((-1,  3)) 
# 转换为浮点型数据，K均值算法要求输入为浮点型 
pixel_values = np.float32(pixel_values)  
 
# 定义停止条件 
# 停止条件由三个部分组成：类型、最大迭代次数和误差阈值 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2) 
 
# 定义聚类的类别数K 
k = 12
# 运行K均值算法 
_, labels, centers = cv2.kmeans(pixel_values,  k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS) 
 
# 将中心值转换为整数类型 
centers = np.uint8(centers)  
# 根据标签将每个像素替换为对应的聚类中心值 
segmented_data = centers[labels.flatten()] 
# 将一维数组重新转换为图像的形状 
segmented_image = segmented_data.reshape(image.shape)  
 
# 显示原始图像和分类后的图像 
plt.figure(figsize=(10,  5)) 
plt.subplot(121)  
plt.imshow(image)  
plt.title('Original  Image') 
plt.axis('off')  
 
plt.subplot(122)  
plt.imshow(segmented_image)  
plt.title(f'K-Means  Clustered Image (K={k})') 
plt.axis('off')  
 
plt.show()  