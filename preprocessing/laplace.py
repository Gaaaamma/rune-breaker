"""Preprocess raw data and save it to trained data"""

from os import listdir
from typing import List

import cv2 as cv

from setting import SETTINGS

def laplace_all():
    """Do laplace to all image in raw/data and save results"""

    # Get all image name from raw_data_dir
    files: List[str] = listdir(SETTINGS.raw_data_dir)
    files = sorted(files)

    # Process each image if it is a png file
    for file in files:
        file_type: str = file.split(".")[-1]
        if file_type == "png":
            print(f"laplace processed: {file}")
            laplace(file)

def laplace(filename: str):
    """Do laplace to the image and save result"""

    img = cv.imread(f"{SETTINGS.raw_data_dir}/{filename}")
    laplace = cv.Laplacian(img, 3, ksize=7)
    cv.imwrite(f"{SETTINGS.laplace_data_dir}lap_{filename}", laplace)

if __name__ == "__main__":
    laplace_all()