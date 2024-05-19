"""Rename raw data to do label"""

from typing import List
from os import listdir, rename

import cv2 as cv

from logger import logger
from setting import SETTINGS

def label_raw_data(raw_data_dir: str):
    """Label all raw img at raw_data_dir"""

    files: List[str] = [
        file for file in listdir(raw_data_dir) if file.endswith(".png")
    ]
    files = sorted(files)

    # Get last labeled index
    for file in files:
        file = file[:-4]
        if "-" not in file:
            old_path: str = f"{raw_data_dir}{file}.png"
            img = cv.imread(old_path)
            cv.imshow(file, img)
            logger.info("Press (w/s/a/d) to label")
            cv.waitKey(1)
            label: str = input("Label(w/s/a/d):").strip("\n")
            
            new_path: str = f"{raw_data_dir}{file}-{label}.png"
            rename(old_path, new_path)
            logger.info(f"Renamed {old_path} to {new_path}")
            cv.destroyWindow(file)
    logger.info("Label and rename all raw data done")

if __name__ == "__main__":
    label_raw_data(SETTINGS.raw_data_dir)