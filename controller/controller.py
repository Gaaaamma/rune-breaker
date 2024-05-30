import serial
import time

import pyautogui
from controller.command import command
from controller.detector import Map
from setting import SETTINGS
from logger import logger
from controller.communicate import Communicator

print(SETTINGS.board_port)
comm: Communicator = Communicator(
    port=SETTINGS.board_port,
    baudrate=SETTINGS.baudrate,
)

time.sleep(3)
comm.ask_ack("move")
comm.ask_ack("-5.5")
comm.ask_ack("move")
comm.ask_ack("5.5")
comm.ask_ack("updown")
comm.ask_ack("up")
comm.ask_ack("updown")
comm.ask_ack("down")
exit(0)

# ========= Get map information =========
logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p1 = pyautogui.position()

logger.info("Move mouse to left-top corner of map and press 'Enter'")
input()
p2 = pyautogui.position()

maple_map = Map(p1.x, p1.y, p2.x, p2.y)
# maple_map.screenshot()


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