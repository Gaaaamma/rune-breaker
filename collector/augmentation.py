from PIL import Image
import os
from setting import SETTINGS
from typing import List

def rotate_right_90(image_path: str, save_path: str):
    mapping: List[str] = ['w', 'd', 's', 'a']

    # Get direction and find index
    direction: str = image_path.split("-")[-1].split(".")[0]
    prefix: str = image_path.split("/")[-1].split("-")[0]
    prefix += "-"
    directoin_index: int = mapping.index(direction)

    # 讀取圖片
    image = Image.open(image_path)
    # 向右翻轉 90 度
    for _ in range(4):
        directoin_index = (directoin_index + 1) % 4
        direction = mapping[directoin_index]
        image = image.rotate(-90, expand=True)
        path: str = f"{save_path}{prefix}{direction}.png"
        print(path)
        image.save(path)

def flip_horizontal(image_path, save_path):
    # 讀取圖片
    image = Image.open(image_path)
    # 水平翻轉
    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    # 保存圖片
    flipped_image.save(save_path)

def flip_vertical(image_path, save_path):
    # 讀取圖片
    image = Image.open(image_path)
    # 垂直翻轉
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # 保存圖片
    flipped_image.save(save_path)

if __name__ == "__main__":
    # Get all standard images
    images = os.listdir(f"{SETTINGS.standard_data_dir}")
    images = sorted(images)
    for i, v in enumerate(images):
        images[i] = f"{SETTINGS.standard_data_dir}{v}"
    
    for img in images:
        rotate_right_90(img, SETTINGS.train_data_dir)