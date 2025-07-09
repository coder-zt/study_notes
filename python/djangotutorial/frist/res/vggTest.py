import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from torch.utils.data import DataLoader
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import matplotlib.pyplot as plt
import newDataset
from sklearn.metrics import roc_auc_score

class VGG16FeatureExtractor(nn.Module):
    def __init__(self):
        super(VGG16FeatureExtractor, self).__init__()
        # 加载预训练的VGG16模型
        vgg16 = models.vgg16(pretrained=True)
        
        # 使用VGG16的前30层作为特征提取器
        self.features = nn.Sequential(*list(vgg16.features.children())[:30])
        
        # 冻结所有卷积层参数
        for param in self.features.parameters():
            param.requires_grad = False
        
        # 自适应池化层
        self.adaptive_pool = nn.AdaptiveAvgPool2d((7, 7))

    def forward(self, x):
        x = self.features(x)
        x = self.adaptive_pool(x)
        return x

class VGGSimilarityModel(nn.Module):
    def __init__(self):
        super(VGGSimilarityModel, self).__init__()
        
        # 彩色图像特征提取器
        self.color_extractor = VGG16FeatureExtractor()
        
        # 黑白图像特征提取器（使用相同的结构但独立实例）
        self.bw_extractor = VGG16FeatureExtractor()
        
        # 黑白图像适配器（将单通道转为3通道）
        self.bw_adapter = nn.Conv2d(1, 3, kernel_size=1)
        
        # 特征融合模块
        self.fusion = nn.Sequential(
            nn.Conv2d(512 * 2, 512, kernel_size=1),  # 1x1卷积融合特征
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        # 分类器
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, color_img, bw_img):
        # 处理黑白图像：单通道转3通道
        bw_img = self.bw_adapter(bw_img)
        
        # 提取特征
        color_features = self.color_extractor(color_img)
        bw_features = self.bw_extractor(bw_img)
        
        # 融合特征
        combined = torch.cat([color_features, bw_features], dim=1)
        fused = self.fusion(combined)
        
        # 相似度预测
        similarity = self.classifier(fused)
        return similarity

# 数据预处理函数
def get_transforms():
    # VGG16的标准预处理
    vgg_preprocess = transforms.Compose([
        transforms.Resize((224, 224)),  # VGG16的标准输入尺寸
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])
    ])
    
    # 彩色图像预处理
    color_transform = vgg_preprocess
    
    # 黑白图像预处理
    bw_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # 单通道标准化
    ])
    
    return color_transform, bw_transform

# 训练函数
def train_vgg_model(model, train_loader, val_loader, device, epochs=30, lr=0.0001):
    # 损失函数和优化器
    criterion = nn.BCELoss()
    optimizer = optim.Adam([
        {'params': model.bw_adapter.parameters()},
        {'params': model.fusion.parameters()},
        {'params': model.classifier.parameters()}
    ], lr=lr)
    
    # 学习率调度器
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=5, verbose=True
    )
    
    best_auc = 0.0
    history = {'train_loss': [], 'val_loss': [], 'val_auc': []}
    
    for epoch in range(epochs):
        print(f"==========> {epoch}")
        # 训练阶段
        model.train()
        train_loss = 0.0
        for color_imgs, bw_imgs, labels in train_loader:
            color_imgs = color_imgs.to(device)
            bw_imgs = bw_imgs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(color_imgs, bw_imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * color_imgs.size(0)
        
        train_loss = train_loss / len(train_loader.dataset)
        history['train_loss'].append(train_loss)
        
        # 验证阶段
        model.eval()
        val_loss = 0.0
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for color_imgs, bw_imgs, labels in val_loader:
                color_imgs = color_imgs.to(device)
                bw_imgs = bw_imgs.to(device)
                labels = labels.to(device)
                
                outputs = model(color_imgs, bw_imgs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * color_imgs.size(0)
                
                all_probs.extend(outputs.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        val_loss = val_loss / len(val_loader.dataset)
        auc = roc_auc_score(all_labels, all_probs)
        
        history['val_loss'].append(val_loss)
        history['val_auc'].append(auc)
        
        print(f'Epoch {epoch+1}/{epochs}: '
              f'Train Loss: {train_loss:.4f}, '
              f'Val Loss: {val_loss:.4f}, '
              f'Val AUC: {auc:.4f}')
        
        # 更新学习率
        scheduler.step(auc)
        
        # 保存最佳模型
        if auc > best_auc:
            best_auc = auc
            torch.save(model.state_dict(), 'best_vgg_model.pth')
            print(f'Saved best model with AUC: {auc:.4f}')
    
    print(f'Training complete. Best Validation AUC: {best_auc:.4f}')
    return history

# 主函数
def test():
    # 设备配置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 初始化模型
    model = VGGSimilarityModel().to(device)
    
    # 打印模型结构
    print(model)
    
    # 获取数据预处理
    color_transform, bw_transform = get_transforms()
    
    data_dir = '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/secDataset'
    
    # 创建数据集和数据加载器（假设使用之前的ImagePairDataset）
    dataset = newDataset.ImagePairDataset(
        root_dir=data_dir,
        transform=color_transform,
        bw_transform=bw_transform,
        label_file = "dataset_train.csv"
    )
    
    # 划分训练集和验证集
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    # 创建数据加载器（使用较小的批量大小）
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=4)
    
    # 训练模型
    history = train_vgg_model(
        model, 
        train_loader, 
        val_loader, 
        device, 
        epochs=30, 
        lr=0.0001
    )
    
    # 可视化训练过程
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Val Loss')
    plt.title('Loss Curve')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['val_auc'], 'r-', label='Validation AUC')
    plt.title('Validation AUC')
    plt.xlabel('Epoch')
    plt.ylabel('AUC')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('vgg_training_history.png')
    plt.show()

if __name__ == '__main__':
    test()