"""Collect training raw data"""

import time

import pyautogui

from setting import SETTINGS

def grab_raw_data(x: int, y: int, filename: str):
    """
    Grab screenshot start from x and y and store it as filename
    Width: set in settings
    Height: set in settings
    """

    screenshot = pyautogui.screenshot(region=(
        x, y, SETTINGS.screenshot_widht, SETTINGS.screenshot_height
        ))
    
    store_path: str = f"{SETTINGS.raw_data_dir}{filename}.png"
    screenshot.save(store_path)

if __name__ == "__main__":
    grab_raw_data(0, 0, int(time.time()))