from os import listdir
from setting import SETTINGS

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

# 定義與訓練時相同的 CNN 模型結構
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

# 初始化模型並載入儲存的權重
model = CNNModel()
model.load_state_dict(torch.load(SETTINGS.arrow_model))
model.eval()  # 設置模型為推論模式

# 定義資料增強與轉換
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 讀取並預處理圖像
def load_image(image_path):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # 增加一個 batch 維度
    return image

# 進行推論
def predict(image_path):
    image = load_image(image_path)
    outputs = model(image)
    _, predicted = torch.max(outputs, 1)
    return predicted.item()

# 使用示例
images = listdir(SETTINGS.testing_data_dir)
images = sorted(images)
for img in images:
    image_path = f"{SETTINGS.testing_data_dir}{img}"
    print(image_path)
    label_map = {0: 'w', 1: 's', 2: 'a', 3: 'd'}
    predicted_label = predict(image_path)
    print(f'The predicted label is: {label_map[predicted_label]}')