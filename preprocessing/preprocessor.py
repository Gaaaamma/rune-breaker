"""
Preprocessor is responsible for get the position of arrows
and cut it into 4 small pictures for training
"""

from os import listdir
from typing import List, Tuple

import cv2 as cv
import numpy as np

from collector.label import label_raw_data
from logger import logger
from preprocessing.laplace import laplace_all
from setting import SETTINGS

width: int = SETTINGS.counter_width
counter: int = SETTINGS.counter_start

def blue_calculator_hz(file: str) -> List[int]:
    """Read from a image file and calculate blue point of each row"""

    result: List[int] = []
    img = cv.imread(file)
    
    for row in range(img.shape[0]):
        counter: int = 0
        for col in range(img.shape[1]):
            if is_blue_purple(img, row, col):
                counter += 1
        result.append(counter)
    
    return result

def blue_calculator_vt(
        file: str, 
        top: int = 0,
        down: int = SETTINGS.screenshot_height,
        left: int = 0,
        right: int = SETTINGS.screenshot_width
        ) -> List[int]:
    """
    Read from a image file and calculate blue point of each column
    top: top start with this row index (close)
    down: down end with this row index (open)
    left: left start with this column index (close)
    right: right end with this column index (open)
    """

    result: List[int] = []
    img = cv.imread(file)
    img = img[top:down, left:right]
    logger.info(f"judge images shape: {img.shape}")

    for col in range(img.shape[1]):
        counter: int = 0
        for raw in range(img.shape[0]):
            if is_blue_purple(img, raw, col):
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

def cut_arrows(file: str, show: bool):
    """Use blue calculator to determine how to cut"""

    img_top: int = 0
    img_btm: int = 0
    threshold: int = SETTINGS.laplace_blue_threshold
    toleration: int = SETTINGS.laplace_blue_tolerantion
    statistic_hz: List[int] = blue_calculator_hz(file)
    statistic_hz = statistic_hz[SETTINGS.laplace_blue_height_start:SETTINGS.laplace_blue_height_end]
    maximum_score: int = 0

    # ===============Find horizontal cut ===============
    for row, count in enumerate(statistic_hz):
        if count >= threshold:
            up: int = row - SETTINGS.captcha_height
            if up > 0 and statistic_hz[up] >= threshold - toleration:
                score: int = count + statistic_hz[up]
                if score > maximum_score:
                    maximum_score = score
                    img_top, img_btm = up , row
                    img_top += SETTINGS.laplace_blue_height_start
                    img_btm += SETTINGS.laplace_blue_height_start
                    logger.info(f"Horizontal cut img_top: {img_top}, img_btm: {img_btm}")
                    logger.info(f"blue points: (top, btm) = ({statistic_hz[up]}, {statistic_hz[row]})")

            down: int = row + SETTINGS.captcha_height
            if down < len(statistic_hz) and statistic_hz[down] >= threshold - toleration:
                score: int = count + statistic_hz[down]
                if score > maximum_score:
                    maximum_score = score
                    img_top, img_btm = row , down
                    img_top += SETTINGS.laplace_blue_height_start
                    img_btm += SETTINGS.laplace_blue_height_start
                    logger.info(f"Horizontal cut img_top: {img_top}, img_btm: {img_btm}")
                    logger.info(f"blue points: (top, btm) = ({statistic_hz[row]}, {statistic_hz[down]})")
    
    if img_top == 0 and img_btm == 0:
        logger.info("Not found img_top & img_btm")
        return
    
    # We can go further small with vertical height (Manual test)
    img_top += SETTINGS.magic_crop_vertical
    img_btm -= SETTINGS.magic_crop_vertical

    vt_cut_top = img_top + SETTINGS.magic_crop_vertical_t2
    vt_cut_btm = img_btm - SETTINGS.magic_crop_vertical_t2
    height = vt_cut_btm - vt_cut_top
    logger.info(f"Vertical cut params: (vt_cut_top, vt_cut_btm, height) = ({vt_cut_top}, {vt_cut_btm}, {height})")

    # =============== Find vertical cut ===============
    img_left: int = 0
    img_right: int = 0
    statistic_vt: List[int] = blue_calculator_vt(
        file, vt_cut_top, vt_cut_btm,
        SETTINGS.laplace_blue_width_start, SETTINGS.laplace_blue_width_end
    )
    maximum_score = 0
    for col, _ in enumerate(statistic_vt): # 0 ~ len(statisc_vt)
        outer_left: int = col
        outer_right: int = outer_left + SETTINGS.captcha_width
        inner_left: int = outer_left + 1
        inner_right: int = outer_right - 1

        if outer_right >= len(statistic_vt):
            break
        
        judge: int = (statistic_vt[outer_left] + statistic_vt[outer_right] +
                      statistic_vt[inner_left] + statistic_vt[inner_right])

        if judge >= SETTINGS.laplace_blue_vt_threshold and judge > maximum_score:
            maximum_score = judge
            img_left = outer_left + SETTINGS.laplace_blue_width_start
            img_right = img_left + SETTINGS.captcha_width
            logger.info(f"Vertical cut img_left: {img_left}, img_right: {img_right}")
            logger.info(f"blue points: (out_l, in_l, in_r, out_r) = ({statistic_vt[outer_left]}, {statistic_vt[inner_left]}, {statistic_vt[inner_right]}, {statistic_vt[outer_right]})")
    
    if img_left == 0 and img_right == 0:
        logger.info("Not found img_left & img_right")
        for col, _ in enumerate(statistic_vt): # 0 ~ len(statisc_vt)
            outer_left: int = col
            outer_right: int = outer_left + SETTINGS.captcha_width
            inner_left: int = outer_left + 1
            inner_right: int = outer_right - 1
            if outer_right >= len(statistic_vt):
                break
            
            judge: int = (statistic_vt[outer_left] + statistic_vt[outer_right] +
                          statistic_vt[inner_left] + statistic_vt[inner_right])
            logger.info(f"blue points: (out_l, in_l, in_r, out_r) = ({statistic_vt[outer_left]}, {statistic_vt[inner_left]}, {statistic_vt[inner_right]}, {statistic_vt[outer_right]}) = {judge}")

        return
    
    # We can go further small with horizontal width (Manual test)
    img_left += SETTINGS.magic_crop_horizontal
    img_right -= SETTINGS.magic_crop_horizontal

    # =============== Cut original file ===============
    file = file.split("_")[-1]
    file = f"{SETTINGS.raw_data_dir}{file}"
    raw = cv.imread(file)
    if show:
        cv.imshow(file, raw)
    img = raw[img_top:img_btm, img_left:img_right]
    need_cut = img
    
    # =============== Use opencv method to find arrows ===============    
    _, threshold = cv.threshold(img, 200, 255, cv.THRESH_BINARY)
    #cv.imshow("thrshold_binary", threshold)
    
    gray = cv.cvtColor(threshold, cv.COLOR_BGR2GRAY)
    # _, gray = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)
    #cv.imshow("gray", gray)
    logger.info(f"img.shape = {gray.shape}")

    kernel = np.ones([9, 9])
    canny = cv.Canny(gray, 100, 200)
    canny = cv.dilate(canny, kernel)
    # cv.imshow("canny", canny)

    # =============== Get contour areas maximum 4 ===============
    areas = []
    contours, _ = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area: float = cv.contourArea(c)
        areas.append((int(area), c))
    
    areas = sorted(areas, reverse=True, key=lambda x: x[0])
    areas = areas[:4]

    # Draw
    arrows: List[Tuple[int, int, int, int]] = []
    for _, contour in areas:
        x, y, w, h = cv.boundingRect(contour)
        logger.info(f"Draw the rectangle: [{x}, {y}] w: {w}, h: {h}")
        cv.rectangle(img, [x, y], [x+w, y+h], [255, 255, 255], 2)
        arrows.append((x, y, w, h))
    
    if show:
        cv.imshow("draw", img)

    # Cut
    arrows = sorted(arrows, key=lambda tp: tp[0])
    global counter
    label: str = file.split("-")[-1].split(".")[0]
    index: int = 0
    for pos in arrows:
        x, y, w, h = pos
        arrow = need_cut[y:y+h, x:x+w]
        filename: str = f"{str(counter).zfill(width)}-{label[index]}.png"
        if show:
            cv.imshow(filename, arrow)
        cv.imwrite(f"{SETTINGS.cut_data_dir}{filename}", arrow)
        index += 1
        counter += 1

    if show:
        cv.waitKey(0)
        cv.destroyAllWindows()
    

if __name__ == "__main__":
    # Label raw data with (w/s/a/d)
    label_raw_data(SETTINGS.raw_data_dir)
    
    # Transform all data into laplace
    laplace_all()

    # Get all filename
    files: List[str] = listdir(SETTINGS.laplace_data_dir)
    files = [
        f"{SETTINGS.laplace_data_dir}{file}"
        for file in files if file.split(".")[-1] == "png"
    ]
    # files = [
    #     f"{SETTINGS.laplace_data_dir}lap_1716025137-ssaw.png",
    #     f"{SETTINGS.laplace_data_dir}lap_1716027125-wada.png",
    # ]
    files = sorted(files)

    # Cut 4 arrows and store it as trained data
    for file in files:
        logger.info(f"File: {file}")
        cut_arrows(file, SETTINGS.debug)