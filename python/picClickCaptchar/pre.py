from torchvision import transforms
import numpy as np

# 将图片缩放到固定大小 72x60（可能会拉伸或压缩）
transform = transforms.Compose([
    transforms.Resize((80, 80)),  # 指定高度和宽度
    transforms.ToTensor()
])

from PIL import Image

img = Image.open("/Users/edy/owner/study_notes/python/picClickCaptchar/ji_m.png").convert("L")  # 转为灰度图
print(img.width , img.height)

processed = transform(img)  # 应用上面的 transform
print(processed.shape)  # 输出: torch.Size([1, 72, 60])
