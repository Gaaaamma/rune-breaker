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

command: str = input("Please input command: ")

if command == "hunting":
    logger.info("Hunting mode")

    # ========= Get map information =========
    logger.info("Move mouse to left-top corner of map and press 'Enter'")
    input()
    p1 = pyautogui.position()

    logger.info("Move mouse to right-bottom corner of map and press 'Enter'")
    input()
    p2 = pyautogui.position()

    logger.info("Move mouse to standby position of map and press 'Enter'")
    input()
    standby = pyautogui.position()

    maple_map = Map(p1.x, p1.y, p2.x, p2.y, standby.x, standby.y)

    # ========= working loop =========
    time.sleep(3)
    while True:
        logger.info(f"Hunting start: solve rune")
        
        rune_solved: bool = maple_map.solve_rune(comm)
        
        logger.info("Player moves to standby position")
        maple_map.screenshot()
        maple_map.find_player()
        comm.go_to_x(maple_map.standby_x - maple_map.player_x)
        comm.go_to_y(maple_map.standby_y - maple_map.player_y)

        if rune_solved:
            comm.hunting(930)
        else:
            comm.standby(60)

else:
    logger.info(f"Unknown command: {command}")