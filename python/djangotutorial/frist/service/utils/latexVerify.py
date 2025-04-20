# 公式图片识别服务

import requests as req
import json
import re
import cv2 as cv

SIMPLETEX_UAT = "P4FIUDl3rMGShrIkHDVMGWlKLLS7LLQXKSiU0PkixHouTnSMSK5DjXmkvLBVNN8o"

# 是否开启手动输入验证码结果
manualInput = False

def scale(imgPath, scale_factor):
    print("scale ===> " + str(scale_factor))
    img = cv.imread(imgPath)
    # 设置缩放比例（放大 2 倍）
    # scale_factor = 2  
    new_width = int(img.shape[1] * scale_factor)  # 计算新宽度
    new_height = int(img.shape[0] * scale_factor)  # 计算新高度

    # 使用 INTER_CUBIC 进行放大（比 INTER_LINEAR 效果更好）
    resized_image = cv.resize(img, (new_width, new_height), interpolation=cv.INTER_CUBIC)
    # cv2.imshow('Resized Image', resized_image)
    # cv2.waitKey(0)
    return resized_image

def getAnwer(imgPath, file=None):
    # img = scale(imgPath, 4)
    # cv.imwrite(imgPath, img)
    if manualInput:
        print(imgPath)
        res = input("请输入公式答案：")
        return res
    
    api_url = "https://server.simpletex.cn/api/latex_ocr"  # 接口地址
    data = {}  # 请求参数数据（非文件型参数），视情况填入，可以参考各个接口的参数说明
    header = {"token": SIMPLETEX_UAT}  # 鉴权信息，此处使用UAT方式sss
    if file == None:
        uploadFile = [("file", ("test.png", open(imgPath, "rb")))]
    else:
        uploadFile = file
    res = req.post(
        api_url, files=uploadFile, data=data, headers=header
    )  # 使用requests库上传文件
    print(res.text)
    # 公式识别服务错误
    if "err_info" in res.text:
        # return getAnwer(imgPath, file)
        return 1
    latexStr = json.loads(res.text)["res"]["latex"]
    numbers = re.findall("\d", latexStr)
    operator = re.findall("[-+]", latexStr)
    if len(numbers) == 0:
        return 1
    countRes = int(numbers[0])
    for n in numbers[1:]:
        if len(operator) > 0:
            if operator.pop(0) == "+":
                countRes = countRes + int(n)
            else:
                countRes = countRes - int(n)
    return countRes


if __name__ == "__main__":
    getAnwer(
        "/Users/edy/owner/study_notes/python/djangotutorial/frist/img/1_1_66bdadf-44b6-66bdadf-44b6-66b.png"
    )
