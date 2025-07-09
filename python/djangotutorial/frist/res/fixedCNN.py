import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import pandas as pd
import os
import newCnn

# 1. 修改模型确保正确输出形状
class ImagePairCNN(nn.Module):
    def __init__(self):
        super(ImagePairCNN, self).__init__()
        
        # 分支1: 处理80x80图像
        self.branch1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
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
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
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
        feat1 = self.branch1(img1)  # [b, 128, 5, 5]
        feat2 = self.branch2(img2)  # [b, 128, 5, 5]
        
        combined = torch.cat((feat1, feat2), dim=1)  # [b, 256, 5, 5]
        similarity = self.fusion(combined)
        
        # 确保输出形状为 [batch_size, 1]
        return similarity

# 2. 修正数据集类
class ImagePairDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None, 
                 size1=(80, 80), size2=(27, 30)):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        self.size1 = size1
        self.size2 = size2
        
    def __len__(self):
        return len(self.annotations)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        row = self.annotations.iloc[idx]
        img1_path = os.path.join(self.root_dir, row[0])
        img2_path = os.path.join(self.root_dir, row[1])
        label = row[2]
        
        # 加载并调整图像尺寸
        img1 = Image.open(img1_path).convert('L').resize(self.size1, Image.LANCZOS)
        img2 = Image.open(img2_path).convert('L').resize(self.size2, Image.LANCZOS)
        
        # 应用变换
        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)
        
        # 确保标签是标量值
        return img1, img2, torch.tensor(label, dtype=torch.float32)

# 3. 修正训练循环
def train_model():
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 数据预处理
    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])
    ])
    
    # 创建数据集
    train_dataset = ImagePairDataset(
        csv_file='/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/dataset_train.csv',
        root_dir='/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/',
        transform=transform
    )
    
    val_dataset = ImagePairDataset(
        csv_file='/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/dataset_val.csv',
        root_dir='/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/',
        transform=transform
    )
    
    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=2)
    
    # 初始化模型
    model = ImagePairCNN().to(device)
    
    # 损失函数和优化器
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=3)
    
    # 训练循环
    num_epochs = 100
    best_val_loss = float('inf')
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for img1, img2, labels in train_loader:
            img1 = img1.to(device)
            img2 = img2.to(device)
            labels = labels.to(device).view(-1, 1)  # 确保标签形状为 [batch_size, 1]
            
            optimizer.zero_grad()
            
            # 前向传播
            outputs = model(img1, img2)
            
            # 计算损失
            loss = criterion(outputs, labels)
            
            # 反向传播
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * img1.size(0)
        
        # 计算平均训练损失
        epoch_loss = running_loss / len(train_loader.dataset)
        
        # 验证阶段
        model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for img1, img2, labels in val_loader:
                img1 = img1.to(device)
                img2 = img2.to(device)
                labels = labels.to(device).view(-1, 1)  # 确保标签形状为 [batch_size, 1]
                
                outputs = model(img1, img2)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * img1.size(0)
                
                # 计算准确率
                predicted = (outputs > 0.5).float()
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
        
        val_loss /= len(val_loader.dataset)
        accuracy = correct / total
        
        # 更新学习率
        scheduler.step(val_loss)
        
        # 保存最佳模型
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'best_model.pth')
        
        print(f'Epoch {epoch+1}/{num_epochs} | '
              f'Train Loss: {epoch_loss:.4f} | '
              f'Val Loss: {val_loss:.4f} | '
              f'Acc: {accuracy:.4f}')
    
    print('训练完成')
    return model

# 4. 预测函数
def predict(model, img1_path, img2_path, device='cuda'):
   # 彩色图像变换
    color_transform = transforms.Compose([
        transforms.Resize((80, 80)),  # 调整到统一尺寸
        transforms.RandomHorizontalFlip(),  # 数据增强
        transforms.RandomRotation(10),  # 数据增强
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])  # ImageNet标准化
    ])
    
    # 黑白图像变换
    bw_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # 单通道标准化
    ])
    
    # 加载图像
    img1 = Image.open(img1_path).convert('RGB').resize((80, 80), Image.LANCZOS)
    img2 = Image.open(img2_path).convert('L').resize((27, 30), Image.LANCZOS)
    # Image.open(bw_path).convert('L')
    img1 = color_transform(img1).unsqueeze(0).to(device)  # 添加批次维度
    img2 = bw_transform(img2).unsqueeze(0).to(device)
    
    # 预测
    # model.eval()
    with torch.no_grad():
        similarity = model(img1, img2)
    
    return similarity.item()

if __name__ == "__main__":
    # 训练模型
    # model = train_model()
    
    # 测试预测
    model = newCnn.MinimalConvModel()
    
    checkpoint = torch.load('/Users/edy/owner/study_notes/python/djangotutorial/frist/best_model.pth', map_location='cpu') 
    target = "segment_T_0.jpg"
    for i in range(0,4):
        source = f"segment_S_{i}.jpg"
        img1_path = f"/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/64/{target}"
        img2_path = f"/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset/64/{source}"
        similarity = predict(model, img1_path, img2_path, device='cpu')
        print(f"{target}, {source} ===> 相似度概率: {similarity:.4f}")