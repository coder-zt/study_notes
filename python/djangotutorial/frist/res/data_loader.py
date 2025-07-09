from PIL import Image
import os

basePath = os.path.dirname(os.path.abspath(__file__))
secDatasetPath = f"{basePath}/secDataset/"
labelIndex = 40


def load():
    trianData = []
    for i in range(labelIndex):
        # print(f"{secDatasetPath}{i + 1}")
        singleSourceImgPath = f"{secDatasetPath}{i + 1}"
        listSmallImgSegment = []
        listBigImgSegment = []
        for j in range(5):
            smallImgPath = f"{singleSourceImgPath}/segment_S_{j}.jpg"
            bigImgPath = f"{singleSourceImgPath}/segment_T_{j}.jpg"
            if os.path.exists(smallImgPath):
                listSmallImgSegment.append(smallImgPath)
                listBigImgSegment.append(bigImgPath)
        # print(len(listSmallImgSegment))
        for k in range(len(listSmallImgSegment)):
            for l in range(k, len(listSmallImgSegment)):
                # print(listSmallImgSegment[k])
                # print(listBigImgSegment[l])
                # print(k == l)
                trianData.append((listSmallImgSegment[k], listBigImgSegment[l], k == l))
    # print(len(trianData))
    # print(trianData[0])
    return trianData


def data_loader():
    data = []
    for img1, img2, label in load():
        if label:
            label = 1
        else:
            label = 0
        img1 = img1.replace("/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/", "")
        img2 = img2.replace("/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/", "")
        print(f"{img2},{img1},{label}")
    # return data
    print(len(load()))


if __name__ == "__main__":
    data_loader()
