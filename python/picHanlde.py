import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def scale(img):
    # print("scale ===> " + str(scale_factor))
    # 设置缩放比例（放大 2 倍）
    # scale_factor = 2
    new_width = int(img.shape[1] * 4)  # 计算新宽度
    new_height = int(img.shape[0] * 4)  # 计算新高度

    # 使用 INTER_CUBIC 进行放大（比 INTER_LINEAR 效果更好）
    resized_image = cv2.resize(
        img, (new_width, new_height), interpolation=cv2.INTER_CUBIC
    )
    # cv2.imshow('Resized Image', resized_image)
    # cv2.waitKey(0)
    return resized_image


def handle(path):
    # 读取图像
    img = cv2.imread(path)
    if img is None:
        print("Error: Image not found.")
        exit()

    # 将图像转换为二维数组，每行是一个像素的RGB值
    pixel_values = img.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)  # K均值需要浮点型数据

    # 定义K均值的参数
    K = 2  # 聚类的数量（颜色数量）
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        100,
        0.2,
    )  # 停止条件

    _, labels, centers = cv2.kmeans(
        pixel_values, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    # 将簇中心转换为8位整型
    centers = np.uint8(centers)

    colors = np.array([[0, 0, 0], [255, 255, 255], ], dtype=np.uint8)  # 黄色

    # 用簇中心颜色替换原始像素颜色
    segmented_image = colors[labels.flatten()]
    segmented_image = segmented_image.reshape(img.shape)  # 恢复图像形状

    cv2.imwrite(testPath + "/AA-K均值.jpg", segmented_image)

    # # segmented_image = scale(segmented_image)
    
    # # cv2.imwrite(testPath + "/AB-放大.jpg", segmented_image)
    # # 定义核（Kernel），可以调整核的大小来改变效果
    # kernel = np.ones((2, 2), np.uint8)  # 5x5方形核
    # # segmented_image = cv2.dilate(segmented_image, kernel, iterations=2)
    # # segmented_image = cv2.erode(segmented_image, kernel, iterations=1)
    # # cv2.imwrite(testPath + "/BA-腐蚀.jpg", segmented_image)
    
    
    # # 中值滤波
    # # kernel_size = 3  # 可根据色块大小调整核大小
    # # for i in range(0,10):
    # #     segmented_image = cv2.medianBlur(segmented_image, kernel_size)
    # #     cv2.imwrite(testPath + "/BB-中值滤波-" +str(i) + ".jpg", segmented_image)

    # # segmented_image = cv2.erode(segmented_image, kernel, iterations=4)

    # segmented_image = cv2.dilate(segmented_image, kernel, iterations=2)
    # cv2.imwrite(testPath + "/BA-膨胀.jpg", segmented_image)
    # # cv2.imwrite(testPath + "/Canny-Pre.jpg", segmented_image)



    # segmented_image = cv2.Canny(segmented_image, 100, 200)  # 阈值可调整
    
    # cv2.imwrite(testPath + "/Canny.jpg", segmented_image)
    # # 查找轮廓
    # contours, _ = cv2.findContours(
    #     segmented_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    # )

    # # 遍历轮廓并提取小图片
    # for i, contour in enumerate(contours):
    #     # 获取轮廓的边界框
    #     x, y, w, h = cv2.boundingRect(contour)
    #     print(str(x) + "=" + str(y) + "=" + str(w) + "=" + str(h))
    #     # 过滤太小的区域（可选）
    #     if w * h < 20:  # 忽略面积小于100的区域
    #         continue

    #     # 提取边界框区域
    #     small_img = img[y : y + h, x : x + w]
    #     # print(small_img)
    #     # if len(small_img) == 0:
    #     #     return
    #     # 保存小图片
    #     cv2.imwrite(f"/Users/edy/owner/study_notes/python/djangotutorial/frist/img/res/res-{i}-{x}:{x+h}-{y}:{y+h}.jpg",small_img)

    #     # 显示小图片（可选）
    #     # cv2.imshow(f"Small Image {i}", small_img)
    #     # cv2.waitKey(0)
    # # os.remove(path)


testPath = "/Users/edy/owner/study_notes/python/djangotutorial/frist/img/res"

for picPath in sorted(os.listdir(testPath)):
    if not picPath.endswith("png"):
        os.remove(testPath + "/" + picPath)
index = 0
for picPath in sorted(os.listdir(testPath)):
    index = index + 1
    if not picPath.endswith("png"):
        continue
    print(f"{index}：{picPath}")
    handle(testPath + "/" + picPath)
    print(f"{index}: 处理完成：{picPath}")
    print("-------------------------------------------------")
    if index == 1:
        break
