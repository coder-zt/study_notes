from ultralytics import YOLO
import math

modelPath = "/Users/edy/owner/study_notes/python/djangotutorial/frist/runs/detect/train11/weights/best.pt"
model = YOLO(modelPath)
names = [
    "+",
    "-",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "一",
    "七",
    "三",
    "九",
    "二",
    "五",
    "八",
    "六",
    "减",
    "加",
    "四",
]


def boxDiff(box1, box2):
    count = 0
    for i in range(len(box1)):
        count = count + math.pow((box1[i] - box2[i]), 2)
    return math.sqrt(count)


def deleteOpears(opears):
    print(f"deleteOpears ===> {opears}")
    minDiff = boxDiff(opears[0]["box"], opears[1]["box"])
    nearNum1 = 0
    nearNum2 = 1
    indexI = 0
    indexJ = 0
    for i in opears[:-1]:
        indexI = indexI + 1
        indexJ = 0
        for j in opears[indexI:]:
            indexJ = indexJ + 1
            diff = boxDiff(opears[indexI]["box"], opears[indexJ]["box"])
            if diff < minDiff:
                nearNum1 = indexI
                nearNum2 = indexJ
                minDiff = diff
    if opears[nearNum1]["conf"] < opears[nearNum2]["conf"]:
        opears.pop(nearNum1)
    else:
        opears.pop(nearNum2)
    if len(opears) > 2:
        return deleteOpears(opears)
    else:
        return opears


def addOpears(opears):
    if len(opears) == 0:
        opears.append({"cls": "减", "conf": 0.0, "box": [35, 35, 44, 37]})
        opears.append({"cls": "减", "conf": 0.0, "box": [78, 23, 87, 25]})
    else:
        opears.append({"cls": "减", "conf": 0.0, "box": [78, 23, 87, 25]})
    return opears


def preHandleOpears(opears):

    if len(opears) == 2:
        return opears
    elif len(opears) > 2:
        return deleteOpears(opears)
    else:
        return addOpears(opears)


def deleteNum(nums):
    # print(f"deleteNum ===> {nums}")
    minDiff = boxDiff(nums[0]["box"], nums[1]["box"])
    nearNum1 = 0
    nearNum2 = 1
    indexI = 0
    indexJ = 0
    for i in nums[:-1]:
        indexI = indexI + 1
        indexJ = 0
        for j in nums[indexI:]:
            indexJ = indexJ + 1
            diff = boxDiff(nums[indexI]["box"], nums[indexJ]["box"])
            if diff < minDiff:
                nearNum1 = indexI
                nearNum2 = indexJ
                minDiff = diff
    if nums[nearNum1]["conf"] < nums[nearNum2]["conf"]:
        nums.pop(nearNum1)
    else:
        nums.pop(nearNum2)
    if len(nums) > 3:
        return deleteNum(nums)
    else:
        return nums


def addNum(nums, opears):
    opearX1 = opears[0]["box"][0]
    opearX2 = opears[1]["box"][0]
    if opearX2 < opearX1:
        temp = opearX1
        opearX1 = opearX2
        opearX2 = temp
    if len(nums) == 0:
        nums.append({"cls": "3", "conf": 0.0, "box": []})
        nums.append({"cls": "3", "conf": 0.0, "box": []})
        nums.append({"cls": "3", "conf": 0.0, "box": []})
    elif len(nums) == 1:
        if nums[0]["box"][0] <= opearX1:
            nums.append({"cls": "3", "conf": 0.0, "box": []})
            nums.append({"cls": "3", "conf": 0.0, "box": []})
        elif nums[0]["box"][0] > opearX1 and nums[0]["box"][0] > opearX2:
            nums.append({"cls": "3", "conf": 0.0, "box": []})
            nums.insert(0, {"cls": "3", "conf": 0.0, "box": []})
        else:
            nums.insert(0, {"cls": "3", "conf": 0.0, "box": []})
            nums.insert(0, {"cls": "3", "conf": 0.0, "box": []})
    else:
        if nums[0]["box"][0] <= opearX1 and nums[1]["box"][0] <= opearX2:
            nums.append({"cls": "3", "conf": 0.0, "box": []})
        elif nums[0]["box"][0] <= opearX1 and nums[1]["box"][0] >= opearX2:
            nums.insert(1, {"cls": "3", "conf": 0.0, "box": []})
        else:
            nums.insert(0, {"cls": "3", "conf": 0.0, "box": []})
    return nums


def preHandleNumbers(nums, opears):
    if len(nums) == 3:
        return nums
    elif len(nums) > 3:
        return deleteNum(nums)
    else:
        return addNum(nums, opears)


def cn2NumStrs(cnStr):
    if cnStr == "一":
        return "1"
    elif cnStr == "二":
        return "2"
    elif cnStr == "三":
        return "3"
    elif cnStr == "四":
        return "4"
    elif cnStr == "五":
        return "5"
    elif cnStr == "六":
        return "6"
    elif cnStr == "七":
        return "7"
    elif cnStr == "八":
        return "8"
    else:
        return "9"

def predictLocal(imgPath):
    results = model(imgPath)
    results[0].show()
    confRes = 0
    boxRes = []
    for i in results[0].boxes:
        clsRes = names[int(i.cls[0])]
        if confRes < float(i.conf[0]):
            confRes = float(i.conf[0])
            boxRes = [
                int(i.xyxy[0][0]),
                int(i.xyxy[0][1]),
                int(i.xyxy[0][2]),
                int(i.xyxy[0][3]),
            ]
    dist = (boxRes[0] + boxRes[2])/2
    print(dist)
    
def predictAnswer(imgPath):
    results = model(imgPath)
    # results[0].show()
    numbers = []
    opears = []

    for i in results[0].boxes:
        clsRes = names[int(i.cls[0])]
        confRes = float(i.conf[0])
        boxRes = [
            int(i.xyxy[0][0]),
            int(i.xyxy[0][1]),
            int(i.xyxy[0][2]),
            int(i.xyxy[0][3]),
        ]
        # res = clsRes in "-+加减"
        # print(f"clsRes ===> {clsRes} ::::: {res}")
        if clsRes in "-+加减":
            if clsRes == "-":
                clsRes = "减"
            elif clsRes == "+":
                clsRes = "加"
            opears.append({"cls": clsRes, "conf": confRes, "box": boxRes})
        else:
            if clsRes in "一二三四五六七八九":
                clsRes = cn2NumStrs(clsRes)
            numbers.append({"cls": clsRes, "conf": confRes, "box": boxRes})
    # print(f"opears ====> {opears}")
    opears = sorted(opears, key=lambda s: s["box"][0])
    # print(f"opears ====> {opears}")
    opears = preHandleOpears(opears)
    numbers = sorted(numbers, key=lambda s: s["box"][0])
    numbers = preHandleNumbers(numbers, opears)
    # print(f"opears ====> {opears}")
    answer = int(numbers[0]["cls"])
    index = 1
    for o in opears:
        if o["cls"] == "减":
            answer = answer - int(numbers[index]["cls"])
        else:
            answer = answer + int(numbers[index]["cls"])
        index = index + 1
    return answer