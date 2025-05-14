import os
import json
import numpy as np
import time
from PIL import Image

"""水平投影"""


def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    # 图像高与宽
    (h, w) = image.shape
    # 长度与图像高度一致的数组
    h_ = [0] * h
    # 循环统计每一行白色像素的个数
    for y in range(h):
        for x in range(w):
            # print(image[y, x])
            if image[y, x] == 255:
                h_[y] += 1
    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8)
    # 图像高与宽
    (h, w) = image.shape
    # 长度与图像宽度一致的数组
    w_ = [0] * w
    # 循环统计每一列白色像素的个数
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1
    # 绘制垂直平投影图像
    for x in range(w):
        for y in range(h - w_[x], h):
            vProjection[y, x] = 255
    return w_
    
def segmentPic(img):    
    # 图像高与宽
    (h, w) = img.shape
    Position = []
    # 水平投影
    H = getHProjection(img)
    start = 0
    H_Start = []
    H_End = []
    # 根据水平投影获取垂直分割位置
    for i in range(len(H)):
        if H[i] > 0 and start == 0:
            H_Start.append(i)
            # if not isFrist:
            # print(f"H_Start.append({i})")
            start = 1
        if H[i] <= 0 and start == 1:
            H_End.append(i)
            # if not isFrist:
            # print(f"H_End.append({i})")
            start = 0

    if len(H_Start) > len(H_End):
        H_End.append(len(H) - 1)

    # 分割行，分割之后再进行列分割并保存分割位置
    for i in range(len(H_Start)):
        # 获取行图像
        cropImg = img[H_Start[i] : H_End[i], 0:w]
        # 对行图像进行垂直投影
        W = getVProjection(cropImg)
        Wstart = 0
        Wend = 0
        W_Start = 0
        W_End = 0
        diffSize = 2
        diff = diffSize
        for j in range(len(W)):
            if W[j] > 0 and Wstart == 0:
                diff = diffSize
                W_Start = j
                Wstart = 1
                Wend = 0
            if W[j] <= 0 and Wstart == 1:
                diff = diff - 1
                W_End = j
                if diff <= 0 or W_End - W_Start > 12:
                    # print(f"{diff} <=======> {W_End - W_Start}")
                    Wstart = 0
                    Wend = 1
            if Wend == 1:
                # if isFrist:
                Position.append([W_Start, H_Start[i], W_End, H_End[i]])
                # else:
                #     Position.append([int(W_Start/4),int(H_Start[i]/4),int(W_End/4),int(H_End[i]/4)])
                Wend = 0
    return Position


def encodeSegment(blockImg):  # 5*13
    imgCode = ''
    for line in blockImg:
        lineChar = 0
        for pixel in line[::-1]:
            # print(f"encodeSegment ===> {pixel}")
            if pixel == 255:
                lineChar = lineChar * 2 + 1
            else:
                lineChar = lineChar * 2
        lineCode = '{:04x}'.format(lineChar)
        imgCode = imgCode + lineCode
    for i in range(int(len(imgCode)/4), 16):
        imgCode = '0000' + imgCode
    return imgCode

def queryCharByCode(code):
    with open(f"{basePath}/code.json", "r") as f:
        codeJson = json.load(f)
        if code in codeJson:
            return codeJson[code]
    return "~"        
   
def fun1(v):
    if v < 125:
        return False
    else:
        return True

def fun(v):
    if v:
        return 0
    else:
        return 255
    
def img2StrForPath(path):
    image = Image.open(path).convert("1")
    image_array = np.array(image)
    # 使用 numpy.vectorize() 将函数应用于数组
    vfunc = np.vectorize(fun)
    result = vfunc(image_array)
    return img2Str(result)

 
def img2Str(origineImage):
    strContent = ""
    Position = segmentPic(origineImage)
    # print(Position)
    # 根据确定的位置分割字符
    for m in range(len(Position)):
        left = int(Position[m][0])
        top = int(Position[m][1])
        right = int(Position[m][2])
        bottom = int(Position[m][3])
        segWidth = right - left
        if segWidth > 100:
            Position[m] = [left + int(segWidth / 2), top, right, bottom]
            Position.insert(m, [left, top, right - int(segWidth / 2), bottom])

    for index, m in enumerate(range(len(Position))):
        left = int(Position[m][0])
        top = int(Position[m][1])
        right = int(Position[m][2])
        bottom = int(Position[m][3])
        # print(f"({left}, {top}, {right}, {bottom})")
        segmentBlock = origineImage[top:bottom, left:right]
        segmentCode = encodeSegment(segmentBlock)
        # print(segmentCode)
        char = queryCharByCode(segmentCode)
        # print(segmentBlock.shape)
        if char == "~":
            vfunc1 = np.vectorize(fun1)
            newResult = vfunc1(segmentBlock)
            # print(newResult.shape)
            img = Image.fromarray(newResult)
            img.save(f"{basePath}/assest/{segmentCode}.png")
        strContent = strContent + char
    if "~" in strContent:
            vfunc1 = np.vectorize(fun1)
            newResult = vfunc1(origineImage)
            # print(newResult.shape)
            img = Image.fromarray(newResult)
            img.save(f"{basePath}/assest/{int(time.time()*1000)}.png")
    return strContent
    


def genCharWithCode():
    for i in os.listdir(f"{basePath}/assest/"):
        if "_" in i :
            code = i.split("_")[0]
            char = i.split("_")[1].split(".")[0]
            print(f'"{code}":"{char}",')
        if "——" in i:
            # print(i)
            code = i.split("——")[0]
            char = i.split("——")[1].split(".")[0]
            print(f'"{code}":"{char}",')


basePath = os.path.dirname(__file__)
if __name__ == "__main__":
    genCharWithCode()
        