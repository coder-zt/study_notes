import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
import newCnn
# 1. 数据集类
class ImagePairDataset(Dataset):
    
    def __init__(self, root_dir, color_dir='', bw_dir='', label_file='labels.csv', transform=None, bw_transform=None):
        """
        参数:
        root_dir: 数据集根目录
        color_dir: 彩色图片子目录
        bw_dir: 黑白图片子目录
        label_file: 包含图片对和标签的CSV文件
        transform: 彩色图片的变换
        bw_transform: 黑白图片的变换
        """
        self.root_dir = root_dir
        self.color_dir = os.path.join(root_dir, color_dir)
        self.bw_dir = os.path.join(root_dir, bw_dir)
        self.transform = transform
        self.bw_transform = bw_transform
        
        # 读取标签文件 (格式: color_img_name,bw_img_name,label)
        self.labels = []
        with open(os.path.join(root_dir, label_file), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    self.labels.append((parts[0], parts[1], int(parts[2])))
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        color_name, bw_name, label = self.labels[idx]
        
        # 加载彩色图像
        color_path = os.path.join(self.color_dir, color_name)
        color_img = Image.open(color_path).convert('RGB')
        
        # 加载黑白图像
        bw_path = os.path.join(self.bw_dir, bw_name)
        bw_img = Image.open(bw_path).convert('L')  # 转换为灰度
        
        # 应用变换
        if self.transform:
            color_img = self.transform(color_img)
        if self.bw_transform:
            bw_img = self.bw_transform(bw_img)
        
        return color_img, bw_img, torch.tensor([label], dtype=torch.float32)

# 2. 数据变换定义
def get_transforms():
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
    
    return color_transform, bw_transform

# 3. 训练函数
def train_model(model, dataloaders, criterion, optimizer, num_epochs=25, device='cuda'):
    best_val_auc = 0.0
    history = {'train_loss': [], 'val_loss': [], 'val_auc': []}
    
    for epoch in range(num_epochs):
        print(f'Epoch {epoch+1}/{num_epochs}')
        print('-' * 10)
        
        # 每个epoch都有训练和验证阶段
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # 训练模式
            else:
                model.eval()   # 评估模式
            
            running_loss = 0.0
            all_labels = []
            all_probs = []
            
            # 迭代数据
            for color_imgs, bw_imgs, labels in dataloaders[phase]:
                color_imgs = color_imgs.to(device)
                bw_imgs = bw_imgs.to(device)
                labels = labels.to(device)
                
                # 梯度清零
                optimizer.zero_grad()
                
                # 前向传播
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(color_imgs, bw_imgs)
                    loss = criterion(outputs, labels)
                    
                    # 反向传播 + 优化（仅在训练阶段）
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                
                # 统计
                running_loss += loss.item() * color_imgs.size(0)
                probs = outputs.detach().cpu().numpy()
                all_probs.extend(probs)
                all_labels.extend(labels.cpu().numpy())
            
            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            
            # 计算验证集的AUC
            if phase == 'val':
                auc = roc_auc_score(all_labels, all_probs)
                history['val_auc'].append(auc)
                history['val_loss'].append(epoch_loss)
                print(f'{phase} Loss: {epoch_loss:.4f} AUC: {auc:.4f}')
                
                # 保存最佳模型
                if auc > best_val_auc:
                    best_val_auc = auc
                    torch.save(model.state_dict(), 'best_model.pth')
                    print(f'New best model saved with AUC: {auc:.4f}')
            else:
                history['train_loss'].append(epoch_loss)
                print(f'{phase} Loss: {epoch_loss:.4f}')
    
    print(f'Training complete. Best Validation AUC: {best_val_auc:.4f}')
    return history

# 4. 主函数
def main():
    # 设置随机种子
    torch.manual_seed(42)
    np.random.seed(42)
    
    # 设备配置
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 数据路径
    data_dir = '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset'
    
    # 获取数据变换
    color_transform, bw_transform = get_transforms()
    
    # 创建数据集
    full_dataset = ImagePairDataset(
        root_dir=data_dir,
        transform=color_transform,
        bw_transform=bw_transform,
        label_file = "dataset_train.csv"
    )
    
    # 划分训练集和验证集 (80%训练, 20%验证)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    # 创建数据加载器
    batch_size = 32
    dataloaders = {
        'train': DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4),
        'val': DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    }
    
    
    # 初始化模型
    model = newCnn.ImagePatchSimilarity()
    model = model.to(device)
    
    # 损失函数和优化器
    criterion = nn.BCELoss()  # 二元交叉熵
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    
    # 学习率调度器
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=5, verbose=True
    )
    
    # 训练模型
    history = train_model(
        model, 
        dataloaders, 
        criterion, 
        optimizer, 
        num_epochs=50, 
        device=device
    )
    
    # 绘制训练曲线
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['val_auc'], 'r-', label='Validation AUC')
    plt.title('Validation AUC')
    plt.xlabel('Epochs')
    plt.ylabel('AUC')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()

if __name__ == '__main__':
    main()