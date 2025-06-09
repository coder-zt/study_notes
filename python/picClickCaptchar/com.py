import torch
import torch.nn as nn
import torch.nn.functional as F

# 用于处理第一张图片（72x60）
class CNNEncoder1(nn.Module):
    def __init__(self):
        super(CNNEncoder1, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),  # 72x60 → 72x60
            nn.ReLU(),
            nn.MaxPool2d(2),                # → 36x30
            nn.Conv2d(16, 32, 3, padding=1),# 36x30
            nn.ReLU(),
            nn.MaxPool2d(2),                # → 18x15
        )
        self.fc = nn.Linear(32 * 18 * 15, 128)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# 用于处理第二张图片（30x40）
class CNNEncoder2(nn.Module):
    def __init__(self):
        super(CNNEncoder2, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),  # 30x40
            nn.ReLU(),
            nn.MaxPool2d(2),                # → 15x20
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                # → 7x10
        )
        self.fc = nn.Linear(32 * 7 * 10, 128)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# Siamese Network
class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.encoder1 = CNNEncoder1()
        self.encoder2 = CNNEncoder2()
        self.classifier = nn.Sequential(
            nn.Linear(128 * 2, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, img1, img2):
        feat1 = self.encoder1(img1)
        feat2 = self.encoder2(img2)
        combined = torch.cat([feat1, feat2], dim=1)
        output = self.classifier(combined)
        return output
    
if __name__ == "__main__":
    model = SiameseNetwork()
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    num_epochs = 30
    for epoch in range(num_epochs):
        for img1, img2, label in data_loader:
            output = model(img1, img2)
            loss = criterion(output, label.float())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()