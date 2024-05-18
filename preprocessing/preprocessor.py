"""
Preprocessor is responsible for get the position of arrows
and cut it into 4 small pictures for training
"""

from os import listdir
from typing import List

import cv2 as cv

from setting import SETTINGS

def blue_calculator(file: str) -> List[int]:
    """Read from a image file and calculate blue point of each row"""
    result: List[int] = []
    img = cv.imread(file)
    print(img.shape)
    
    for row in range(img.shape[0]):
        counter: int = 0
        for col in range(img.shape[1]):
            if is_blue_purple(img, row, col):
                counter += 1
        result.append(counter)
    
    return result

def is_blue_purple(img, row: int, col: int) -> bool:
    """Check if a certain point in img is blue"""

    if (
        img[row][col][0] == 255 and img[row][col][1] == 0 and img[row][col][2] == 0 or
        img[row][col][0] == 255 and img[row][col][1] == 0 and img[row][col][2] == 255
    ):
        return True

    return False

def cut(file: str) -> bool:
    """Use blue calculator to determine the cut height"""

    img_top: int = 0
    img_btm: int = 0
    threshold: int = SETTINGS.laplace_blue_threshold
    toleration: int = SETTINGS.laplace_blue_tolerantion
    statistic: List[int] = blue_calculator(file)
    statistic = statistic[SETTINGS.laplace_blue_height_start:SETTINGS.laplace_blue_height_end]
    
    for row, count in enumerate(statistic):
        if count >= threshold:
            up: int = row - SETTINGS.captcha_height
            if up > 0 and statistic[up] >= threshold - toleration:
                img_top, img_btm = up , row
                img_top += SETTINGS.laplace_blue_height_start
                img_btm += SETTINGS.laplace_blue_height_start
                print(f"[Cut][Up] find img_top: {img_top}, img_btm: {img_btm}")
                print(f"[Cut][Up] blue points: ({statistic[up]}, {statistic[row]})")
                break
            
            down: int = row + SETTINGS.captcha_height
            if down < len(statistic) and statistic[down] >= threshold - toleration:
                img_top, img_btm = row , down
                img_top += SETTINGS.laplace_blue_height_start
                img_btm += SETTINGS.laplace_blue_height_start
                print(f"[Cut][Down] find img_top: {img_top}, img_btm: {img_btm}")
                print(f"[Cut][Down] blue points: ({statistic[row]}, {statistic[down]})")
                break
    
    if img_top == 0 and img_btm == 0:
        print(f"[Cut] Not found")
        return False
    
    # Cut original file
    file = file.split("_")[-1]
    file = f"{SETTINGS.raw_data_dir}{file}"
    img = cv.imread(file)
    img = img[img_top:img_btm + 1]

    cv.imshow(file, img)

    cv.waitKey(0)
    cv.destroyAllWindows()
    return True
    

if __name__ == "__main__":
    files: List[str] = listdir(SETTINGS.laplace_data_dir)
    files = [
        f"{SETTINGS.laplace_data_dir}{file}"
        for file in files if file.split(".")[-1] == "png"
    ]
    files = sorted(files)
    for file in files:
        print(f"\nFile: {file}")
        result: bool = cut(file)