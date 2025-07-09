import torch
import torch.nn as nn
from torchvision.models import vgg16
import os
import cv2
import numpy as np


class SiameseVGG(nn.Module):
    def __init__(self, input_size=56):
        super(SiameseVGG, self).__init__()
        
        # 加载预训练VGG16的卷积部分（不含全连接层）
        vgg = vgg16(pretrained=True)
        self.feature_extractor = vgg.features
        
        # 修改VGG以支持56x56输入 - 移除前两个池化层
        features = list(self.feature_extractor.children())
        features[4] = nn.Identity()  # 移除第一个池化层
        features[9] = nn.Identity()  # 移除第二个池化层
        self.feature_extractor = nn.Sequential(*features)
 # 计算特征向量长度
        with torch.no_grad():
            test_out = self.feature_extractor(torch.randn(1, 3, input_size, input_size))
            self.feature_dim = test_out.view(1, -1).shape[1]  # 25088 for 56x56 input
        
        # 相似度计算网络（修正维度）
        self.similarity_net = nn.Sequential(
            nn.Linear(self.feature_dim, 512),  # 输入是特征差异向量 |f1-f2|
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )
        
        # 打印特征维度信息
        print(f"特征向量维度: {self.feature_dim}")  # 应输出25088
    
    def forward_once(self, x):
        """处理单张图像"""
        features = self.feature_extractor(x)
        features = features.view(features.size(0), -1)  # 展平特征图
        return features
    
    def forward(self, input1, input2):
        """处理两张图像并计算相似度"""
        # 提取特征
        features1 = self.forward_once(input1)
        features2 = self.forward_once(input2)
        
        # 计算特征差异（使用绝对值差）
        features_diff = torch.abs(features1 - features2)
        
        # 计算相似度分数
        similarity = self.similarity_net(features_diff)
        return similarity

# 2. 图像预处理函数（更新版）
def preprocess_image(image_path, size=(56, 56), device=None):
    """加载并预处理单张图像"""
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"无法加载图像: {image_path}")
    
    # 调整大小并归一化
    img = cv2.resize(img, size).astype(np.float32) / 255.0
    
    # 转换通道顺序 (HWC to CHW)
    img = img.transpose(2, 0, 1)
    
    # 转换为张量并添加批次维度
    img_tensor = torch.from_numpy(img).unsqueeze(0)
    
    # 如果指定了设备，直接转移到该设备
    if device:
        img_tensor = img_tensor.to(device)
    
    return img_tensor

# 3. 加载训练好的模型（更新版）
def load_trained_model(model_path, device='auto'):
    # 自动选择设备
    if device == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(device)
    
    # 初始化模型结构
    model = SiameseVGG(input_size=56)
    
    # 加载模型权重并映射到目标设备
    checkpoint = torch.load(model_path, map_location=device)
    
    # 处理不同的保存格式
    if 'model_state_dict' in checkpoint:
        # 如果是包含多个组件的检查点
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        # 如果是直接保存的模型权重
        model.load_state_dict(checkpoint)
    
    # 将整个模型转移到目标设备
    model = model.to(device)
    model.eval()  # 设置为评估模式
    
    print(f"模型已加载到 {device}")
    return model, device

# 4. 预测相似度函数（更新版）
def predict_similarity(model, device, img1_path, img2_path):
    """预测两张图像的相似度"""
    # 预处理图像并直接转移到目标设备
    img1 = preprocess_image(img1_path, device=device)
    img2 = preprocess_image(img2_path, device=device)
    
    # 确保模型在正确设备上
    model = model.to(device)
    
    # 推理
    with torch.no_grad():
        similarity_score = model(img1, img2)
    
    # 返回相似度分数
    return similarity_score.item()

# 加载模型
model, device = load_trained_model('/Users/edy/owner/study_notes/python/djangotutorial/JYWFetchService/service/utils/xkw/best_model_o.pth')

def predict(img1_path, img2_path):
    similarity = predict_similarity(model, device, img1_path, img2_path)
    return similarity
    
# 5. 使用示例（添加设备检查）
if __name__ == "__main__":
    similarity = predict("/Users/edy/owner/study_notes/python/dianxuan/data/secDataset/640/segment_S_0.jpg","/Users/edy/owner/study_notes/python/dianxuan/data/secDataset/640/segment_T_1.jpg")
    print(f"相似度分数: {similarity:.4f}")
