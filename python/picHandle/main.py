import numpy as np
from PIL import Image
import imgSegment
import os
basePath = os.path.dirname(__file__)


# 加载图片
image_path = f"{basePath}/2_副本.png"
image = Image.open(image_path).convert("1")
print(image.height, image.width)
strRes = imgSegment.img2StrForPath(image_path)
print(strRes)