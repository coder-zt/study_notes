from ultralytics import YOLO
import math
import cv2
import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

# 加载预训练模型
# 1. 初始化模型（不加载默认权重）
resnetModel = models.resnet50(pretrained=False)

# 2. 加载本地权重文件
try:
    checkpoint = torch.load(f"{os.path.dirname(__file__)}/resnet50-0676ba61.pth")
    resnetModel.load_state_dict(checkpoint)
except FileNotFoundError:
    print("Error: 权重文件未找到！")
except Exception as e:
    print(f"加载权重失败: {str(e)}")

# 3. 切换模型为评估模式（推理时必需）
resnetModel.eval()

# 图像预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485], std=[0.229, 0.224, 0.225]),
])
    
def otsu(img):
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img.shape[:2]
    threshold_t = 0
    max_g = 0
    
    for t in range(255):
        front = img[img < t]
        back = img[img >= t]
        front_p = len(front) / (h * w)
        back_p = len(back) / (h * w)
        front_mean = np.mean(front) if len(front) > 0 else 0.
        back_mean = np.mean(back) if len(back) > 0 else 0.
        
        g = front_p * back_p * ((front_mean - back_mean)**2)
        if g > max_g:
            max_g = g
            threshold_t = t
    print(f"threshold = {threshold_t}")
    img[img < threshold_t] = 0
    img[img >= threshold_t] = 255
    return img


def extract_features(image_path, index):
    img = otsu(image_path)
    if index == 1:
        img = cv2.bitwise_not(img)
    color_imgs = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    color_imgs[:,:,2] = img
    color_imgs[:,:,0] = img
    color_imgs[:,:,1] = img
    cv2.imwrite(f"{os.path.dirname(__file__)}/temp_{index}.jpg", color_imgs)
    img = Image.open(f"{os.path.dirname(__file__)}/temp_{index}.jpg")
    
    img_t = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        features = resnetModel(img_t)
    return features



modelPath = "/Users/edy/owner/study_notes/python/djangotutorial/frist/runs/detect/train12/weights/best.pt"
segmentModel = YOLO(modelPath)


# 344*384
basePath = os.path.dirname(os.path.abspath(__file__))
sourcePicPath = "/Users/edy/owner/docker/files/train_xkw/result_620.png"
results = segmentModel(sourcePicPath)
sourceImg = cv2.imread(sourcePicPath)
# results[0].show()
confRes = 0
boxRes = []
for i in results[0].boxes:
    boxRes.append([
        int(i.xyxy[0][0]),
        int(i.xyxy[0][1]),
        int(i.xyxy[0][2]),
        int(i.xyxy[0][3]),
    ])
# dist = (boxRes[0] + boxRes[2])/2
tList = []
sList = []
for index, box in enumerate(boxRes):
    segmentT = sourceImg[box[1]:box[3], box[0]:box[2]]
    segmentS = sourceImg[350:380, 27 * index:27 * (index + 1)]
    cv2.imwrite(f"{basePath}/test/segment_S_{index}.jpg", segmentS)
    cv2.imwrite(f"{basePath}/test/segment_T_{index}.jpg", segmentT)
    sList.append(f"{basePath}/test/segment_S_{index}.jpg")
    tList.append(f"{basePath}/test/segment_T_{index}.jpg")
    # cv2.imwrite("segment.png", segmentPic)
    

res = []
for t in tList:
    r = []
    for s in sList:
        # 计算余弦相似度 
        print(f"t: {t}, s: {s}")
        features1 = extract_features(t, 1)
        # print(features1)
        features2 = extract_features(s, 2)
        cos_sim = torch.cosine_similarity(torch.tensor(features1), torch.tensor(features2))
        print("深度学习特征相似度:", cos_sim.item())
        r.append(cos_sim.item())
        # img1 = cv2.imread(f"{os.path.dirname(__file__)}/{m}", cv2.IMREAD_GRAYSCALE)
        # img2 = cv2.imread(f"{os.path.dirname(__file__)}/{s}", cv2.IMREAD_GRAYSCALE)
        # value = hu_moments_similarity(img1, img2)
        # r.append(value)
    res.append(r)



def getAllSort(resList,input, list):
    # print(f"input: ${input}")
    # print(list)
    if len(input) == 0:
        resList.append(list)
        return
    for i in input:
        nList = list.copy()
        nList.append(i)
        nInput = input.copy()
        nInput.remove(i)
        # print(f"input: ${nInput}")
        # print(f"list: ${nList}")
        getAllSort(resList, nInput, nList)
     
   
        
list = []
getAllSort(list,[0,1,2,3], [])
maxValue = 4
targetItem = 0
for item in list:
    sum = 0
    for index, i in enumerate(item):
        sum = sum + res[index][i]
        if sum > maxValue:
            maxValue = sum
            targetItem = item
    print(item , sum)
# print(maxValue)
# print(targetItem)