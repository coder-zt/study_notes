from ultralytics import YOLO


# model = YOLO("/Users/edy/owner/study_notes/python/djangotutorial/frist/res/yolo11n.pt")


# results = model.train(data="/Users/edy/owner/study_notes/python/djangotutorial/frist/res/data.yaml", epochs=50, imgsz=128)

import predict
import os

if __name__ == "__main__":
    path = "/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test"
    count = 0
    right = 0
    for i in os.listdir(path):
        if not i.endswith("png"):
            continue
        count = count + 1
        print(f"{path}/{i}")
        answer = predict.predictLocal(f"{path}/{i}")
#         TrueAnswer = i.split("_")[-1].split(".")[0]
#         # print(answer)
#         # print(TrueAnswer == str(answer))
#         if str(answer) == TrueAnswer:
#             right = right + 1
#         else:
#             print(f"{answer}===={TrueAnswer}==== {path}/{i}")
        
#     print(f"正确率：{right/count}")


# 根据dataset目录下的标签文件复制docker/files/下的文件到dataset中
# import os

# path = "/Users/edy/owner/study_notes/python/djangotutorial/frist/res/dataset"
# docker目录下存放文件的目录
# sourcePath = "/Users/edy/owner/docker/files/train1"
# 放入val还是train
# labelsPath = f"{path}/val/labels"

# for i in os.listdir(labelsPath):
#     # print(f"{labelsPath}/{i}")
#     name = i.split(".")[0]
#     # print(f"{sourcePath}/{name}.jpg")
#     # print(f"{path}/train/images/{name}.jpg")
#     os.system(f"cp {sourcePath}/{name}.png {path}/val/images/{name}.png")


# import os

# # path = "/Users/edy/owner/study_notes/python/djangotutorial/frist/res/dataset"
# sourcePath = "/Users/edy/owner/docker/mydata"

# # labelsPath = f"{path}/val/labels"

# index = 0
# for i in os.listdir(sourcePath):
#     index = index + 1
#     os.rename(f"{sourcePath}/{i}", f"{sourcePath}/{index}.jpg")
