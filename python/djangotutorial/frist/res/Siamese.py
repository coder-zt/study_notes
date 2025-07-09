import torch
import torch.nn as nn
import torch.nn.functional as F

class ImagePairCNN(nn.Module):
    def __init__(self):
        super(ImagePairCNN, self).__init__()
        
        # 分支1: 处理80x80图像
        self.branch1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 40x40
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 20x20
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 10x10
            
            nn.AdaptiveAvgPool2d((5, 5))  # 统一到5x5
        )
        # 分支2: 处理27x30图像
        self.branch2 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 13x15
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 6x7 (向下取整)
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((5, 5))  # 统一到5x5
        )
        
        # 特征融合和分类
        self.fusion = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 2x2
            
            nn.Flatten(),
            
            nn.Linear(128 * 2 * 2, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            
            nn.Linear(256, 64),
            nn.ReLU(),
            
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, img1, img2):
        # 分别提取特征
        feat1 = self.branch1(img1)  # [b, 128, 5, 5]
        feat2 = self.branch2(img2)  # [b, 128, 5, 5]
        
        # 连接特征图 (通道维度拼接)
        combined = torch.cat((feat1, feat2), dim=1)  # [b, 256, 5, 5]
        
        # 融合特征并分类
        similarity = self.fusion(combined)
        return similarity

# 示例用法
if __name__ == "__main__":
    # 初始化模型
    model = ImagePairCNN()
    print(f"模型参数量: {sum(p.numel() for p in model.parameters())/1e6:.2f}M")
    
    # 模拟输入数据 (batch_size=8)
    img1_batch = torch.randn(8, 3, 80, 80)  # 80x80图像
    img2_batch = torch.randn(8, 3, 27, 30)  # 27x30图像
    
    # 前向传播
    output = model(img1_batch, img2_batch)
    
    print(f"输入1形状: {img1_batch.shape}")
    print(f"输入2形状: {img2_batch.shape}")
    print(f"输出形状: {output.shape}")
    print(f"预测样例: {output[:2].data}")