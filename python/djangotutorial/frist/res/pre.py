import cv2
import numpy as np
from keras.models import load_model
from keras.layers import Lambda
from keras import backend as K
import os
import random
from PIL import Image

# input1 = "/Users/edy/owner/study_notes/python/dianxuan/sample/0a0ff90c-2ec5-425c-8781-41ad87f23796_1.jpg"
# input1 = "/Users/edy/owner/study_notes/python/dianxuan/sample/0a1ee7d6-140a-4910-a5f5-c18d549ea0ab_1.jpg"
# input2 = "/Users/edy/owner/study_notes/python/dianxuan/sample/0a0ff90c-2ec5-425c-8781-41ad87f23796_2.jpg"

def predictSamll(input1, input2):
    print("===========> ", input1)
    print("===========> ", input2)
    output = Lambda(lambda x: K.abs(x[0] - x[1]))
    weight = f"{os.path.dirname(os.path.abspath(__file__))}/best.h5"
    # 加载模型
    # model = load_model(weight, custom_objects={'contrastive_loss': contrastive_loss, 'binary_accuracy': binary_accuracy})
    model = load_model(weight, custom_objects={'output': output})


    resize = 52
    img1 = cv2.imread(input1)
    img2 = cv2.imread(input2)

    img1 = cv2.resize(img1, (resize, resize)) / 255
    img2 = cv2.resize(img2, (resize, resize)) / 255

    img1 = np.expand_dims(img1, axis=0)
    img2 = np.expand_dims(img2, axis=0)

    result = model.predict([img1, img2])

    return result[0][0]

res = predictSamll("/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset//348/segment_S_3.jpg", "/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset//348/segment_T_2.jpg")
print(res)