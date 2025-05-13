# 以 PyTorch 为例的孪生网络结构
import torch
import torch.nn as nn

class SiameseNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # 共享权重的 CNN 分支
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=10),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=7),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 128, kernel_size=4),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(128 * 6 * 6, 4096),
            nn.Sigmoid()
        )

    def forward_one(self, x):
        return self.cnn(x)

    def forward(self, x1, x2):
        out1 = self.forward_one(x1)
        out2 = self.forward_one(x2)
        return out1, out2


class ContrastiveLoss(nn.Module):
    def __init__(self, margin=2.0):
        super().__init__()
        self.margin = margin

    def forward(self, distance, label):
        loss = (1 - label) * torch.pow(distance, 2) + \
               label * torch.pow(torch.clamp(self.margin - distance, min=0), 2)
        return torch.mean(loss)

# 计算欧氏距离
def euclidean_distance(f1, f2):
    return torch.sqrt(torch.sum((f1 - f2)**2, dim=1))

model = SiameseNetwork()
criterion = ContrastiveLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
num_epochs = 20
dataloader = [
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_0.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_0.jpg') ,1),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_0.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_1.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_0.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_2.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_0.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_3.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_1.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_0.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_1.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_1.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_1.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_2.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_1.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_3.jpg') ,1),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_2.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_0.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_2.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_1.jpg') ,1),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_2.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_2.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_2.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_3.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_3.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_0.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_3.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_1.jpg') ,0),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_3.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_2.jpg') ,1),
    (('/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_S_3.jpg', '/Users/edy/owner/study_notes/python/djangotutorial/frist/res/test/segment_T_3.jpg') ,0),
              ]
for epoch in range(num_epochs):
    print(f"Epoch {epoch+1}/{num_epochs}")
    for (img1, img2), label in dataloader:
        print(f"img1: {img1}, img2: {img2}, label: {label}")
        optimizer.zero_grad()
        f1, f2 = model(img1, img2)
        distance = euclidean_distance(f1, f2)
        loss = criterion(distance, label)
        loss.backward()
        optimizer.step()