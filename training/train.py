import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets
import os
from PIL import Image
from setting import SETTINGS

# 確認使用 GPU，如果可用的話
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ArrowDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.image_files = os.listdir(data_dir)
        self.label_map = {'w': 0, 's': 1, 'a': 2, 'd': 3}

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.data_dir, img_name)
        image = Image.open(img_path)
        
        # 獲取標註
        label_char = img_name.split('-')[1].split('.')[0]
        label = self.label_map[label_char]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# 資料增強與轉換
transform = transforms.Compose([
    #transforms.RandomHorizontalFlip(),
    #transforms.RandomVerticalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 建立資料集與資料加載器
train_dataset = ArrowDataset(data_dir=SETTINGS.train_data_dir, transform=transform)

#train_dataset = ArrowDataset(data_dir="./data/standard")
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 4)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# 初始化模型、損失函數和優化器
model = CNNModel().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(model, device, train_loader, criterion, optimizer, epoch):
    model.train()
    running_loss = 0.0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        
        # 零梯度
        optimizer.zero_grad()
        
        # 前向傳播
        outputs = model(data)
        loss = criterion(outputs, target)
        
        # 反向傳播與優化
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        if batch_idx % 100 == 99:
            print(f'Epoch [{epoch+1}], Step [{batch_idx+1}], Loss: {loss.item():.4f}')

# 訓練模型
num_epochs = 20
for epoch in range(num_epochs):
    train(model, device, train_loader, criterion, optimizer, epoch)
torch.save(model.state_dict(), 'arrow_cnn.pth')