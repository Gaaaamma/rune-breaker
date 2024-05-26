import serial
import time

import pyautogui
from controller.command import command
from controller.detector import Map
from setting import SETTINGS
from logger import logger

# ser = serial.Serial(
    # port=SETTINGS.board_port,
    # sbaudrate=SETTINGS.baudrate,
    # timeout=3
# )
logger.info(f"Connect to dev board success: {SETTINGS.board_port}")

# Get map location
logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p1 = pyautogui.position()

logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p2 = pyautogui.position()

maple_map = Map(p1.x, p1.y, p2.x, p2.y)
maple_map.screenshot()
maple_map.find_wheel()
# Find location of wheel and player


# Send hunting command to Leonardo
# while not ser.writable():
    # time.sleep(1)

# Working loop
# while True:
    # pass
# 