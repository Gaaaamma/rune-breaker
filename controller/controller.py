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

# ========= Get map information =========
logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p1 = pyautogui.position()

logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p2 = pyautogui.position()

maple_map = Map(p1.x, p1.y, p2.x, p2.y)
maple_map.screenshot()

# ========= Find location of wheel and player =========
logger.info(f"Find wheel: {maple_map.find_wheel()} - ({maple_map.wheel_x}, {maple_map.wheel_y})")
logger.info(f"Find player: {maple_map.find_player()} - ({maple_map.player_x}, {maple_map.player_y})")

while True:
    logger.info(f"Find player: {maple_map.find_player()} - ({maple_map.player_x}, {maple_map.player_y})")
    time.sleep(1)
# Send hunting command to Leonardo
# while not ser.writable():
    # time.sleep(1)

# Working loop
# while True:
    # pass
# 