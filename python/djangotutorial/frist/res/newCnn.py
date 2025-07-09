import torch
import torch.nn as nn
import torch.nn.functional as F

import torch
import torch.nn as nn
import torch.nn.functional as F

class MinimalConvModel(nn.Module):
    def __init__(self):
        super(MinimalConvModel, self).__init__()
        
        # 彩色图像处理分支 - 仅2层卷积
        self.color_conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 保持尺寸
            nn.BatchNorm2d(32),
            nn.ReLU(),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 保持尺寸
            nn.BatchNorm2d(64),
            nn.ReLU(),
            
            # 无池化层，保留原始尺寸信息
            nn.AdaptiveAvgPool2d((15, 15))  # 温和的降采样
        )
        
        # 黑白图像处理分支 - 仅1层卷积
        self.bw_conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),  # 保持尺寸
            nn.BatchNorm2d(32),
            nn.ReLU(),
            
            # 无池化层，保留原始尺寸信息
            nn.AdaptiveAvgPool2d((15, 15))  # 调整到与彩色分支相同尺寸
        )
        
        # 特征融合与相似度计算
        self.similarity = nn.Sequential(
            nn.Conv2d(64+32, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),  # 全局平均池化
            nn.Flatten(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, color_img, bw_img):
        # 提取特征
        color_feat = self.color_conv(color_img)  # [B, 64, 15, 15]
        bw_feat = self.bw_conv(bw_img)          # [B, 32, 15, 15]
        
        # 拼接特征
        combined = torch.cat([color_feat, bw_feat], dim=1)  # [B, 96, 15, 15]
        
        # 计算相似度
        return self.similarity(combined)

# 替代方案：无卷积的纯Transformer方法
class ImagePatchSimilarity(nn.Module):
    def __init__(self, color_patch_size=10, bw_patch_size=5):
        super().__init__()
        self.color_patch_size = color_patch_size
        self.bw_patch_size = bw_patch_size
        
        # 彩色图像嵌入
        self.color_embed = nn.Sequential(
            nn.Linear(3 * color_patch_size * color_patch_size, 64),
            nn.ReLU()
        )
        
        # 黑白图像嵌入
        self.bw_embed = nn.Sequential(
            nn.Linear(bw_patch_size * bw_patch_size, 32),
            nn.ReLU()
        )
        
        # 相似度计算
        self.similarity = nn.Sequential(
            nn.Linear(64 + 32, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
    
    def forward(self, color_img, bw_img):
        # 将彩色图像分割成块
        B, C, H, W = color_img.shape
        color_patches = color_img.unfold(2, self.color_patch_size, self.color_patch_size) \
                              .unfold(3, self.color_patch_size, self.color_patch_size) \
                              .contiguous() \
                              .view(B, -1, 3 * self.color_patch_size * self.color_patch_size)
        
        # 将黑白图像分割成块
        bw_patches = bw_img.unfold(2, self.bw_patch_size, self.bw_patch_size) \
                          .unfold(3, self.bw_patch_size, self.bw_patch_size) \
                          .contiguous() \
                          .view(B, -1, self.bw_patch_size * self.bw_patch_size)
        
        # 提取特征
        color_feat = self.color_embed(color_patches).mean(dim=1)  # 平均所有块的特征
        bw_feat = self.bw_embed(bw_patches).mean(dim=1)
        
        # 融合特征
        combined = torch.cat([color_feat, bw_feat], dim=1)
        
        return self.similarity(combined)
    
# 示例使用
if __name__ == "__main__":
    # 初始化模型
    model = SiameseNetwork()
    
    # 模拟输入数据
    color_input = torch.randn(2, 3, 70, 60)  # 批量大小2, 70x60彩色图
    bw_input = torch.randn(2, 1, 27, 30)     # 27x30黑白图
    
    # 前向传播
    output = model(color_input, bw_input)
    print("相似度预测:", output.squeeze().tolist())
