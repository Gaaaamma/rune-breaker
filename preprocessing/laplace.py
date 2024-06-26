"""Preprocess raw data and save it to trained data"""

from os import listdir
from typing import List

import cv2 as cv

from logger import logger
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
            logger.info(f"Processed: {file}")
            laplace(file)
        else:
            logger.warning(f"Not processed: {file}")

def laplace(filename: str):
    """Do laplace to the image and save result"""

    img = cv.imread(f"{SETTINGS.raw_data_dir}/{filename}")
    laplace = cv.Laplacian(img, 3, ksize=7)
    cv.imwrite(f"{SETTINGS.laplace_data_dir}lap_{filename}", laplace)

def laplace_inference(filename: str, target_dir: str = SETTINGS.inference_tmp) -> str:
    """Do laplace to the image and save result"""

    img = cv.imread(f"{SETTINGS.upload_path}{filename}")
    laplace = cv.Laplacian(img, 3, ksize=7)
    
    filepath: str = f"{target_dir}lap_{filename}"
    cv.imwrite(filepath, laplace)

    return filepath

if __name__ == "__main__":
    laplace_all()