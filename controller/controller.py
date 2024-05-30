import serial
import time

import pyautogui
from controller.detector import Map
from setting import SETTINGS
from logger import logger
from controller.communicate import Communicator

print(SETTINGS.board_port)
comm: Communicator = Communicator(
    port=SETTINGS.board_port,
    baudrate=SETTINGS.baudrate,
)

# ========= Get map information =========
logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p1 = pyautogui.position()

logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p2 = pyautogui.position()

maple_map = Map(p1.x, p1.y, p2.x, p2.y)

# ========= Try to solve rune =========
time.sleep(5)
logger.info("Ready to solve rune for testing")
maple_map.solve_rune(comm)


# ========= Find location of wheel and player =========
# logger.info(f"Find wheel: {maple_map.find_wheel()} - ({maple_map.wheel_x}, {maple_map.wheel_y})")
#logger.info(f"Find player: {maple_map.find_player()} - ({maple_map.player_x}, {maple_map.player_y})")

# ========== Testing communication between PC and Leonardo ============
# TODO

# Send hunting command to Leonardo
# while not ser.writable():
    # time.sleep(1)

# Working loop
# while True:
    # pass
# 