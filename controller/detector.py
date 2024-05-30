import time
import pyautogui
from PIL import ImageGrab
from typing import Dict
from serial import Serial
from setting import SETTINGS
from logger import logger
from controller.communicate import Communicator
from io import BytesIO
import requests
from http import HTTPStatus

class Map():
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1: int = x1
        self.y1: int = y1
        self.x2: int = x2
        self.y2: int = y2
        self.width: int = x2 - x1
        self.height: int = y2 - y1

        self.wheel_x: int = -1
        self.wheel_y: int = -1
        self.player_x: int = -1
        self.player_y: int = -1

    def screenshot(self):
        self.image = pyautogui.screenshot(region=(self.x1, self.y1, self.width, self.height))
    
    def find_wheel(self) -> bool:
        for row in range(self.height):
            for col in range(self.width):
                if self.is_wheel(self.image.getpixel((col, row))):
                    self.wheel_x = col
                    self.wheel_y = row
                    return True
        self.wheel_x = -1
        self.wheel_y = -1
        return False

    def is_wheel(self, rgba) -> bool:
        r, g, b = rgba
        return (
            r == SETTINGS.wheel_r and
            g == SETTINGS.wheel_g and 
            b == SETTINGS.wheel_b
        )

    def find_player(self) -> bool:
        for row in range(self.height):
            for col in range(self.width):
                if self.is_player(self.image.getpixel((col, row))):
                    self.player_x = col
                    self.player_y = row
                    return True
        self.player_x = -1
        self.player_y = -1
        return False

    def is_player(self, rgba) -> bool:
        r, g, b = rgba
        return (
            r == SETTINGS.player_r and
            g == SETTINGS.player_g and 
            b == SETTINGS.player_b
        )

    def speed_test(self):
        """Test player moving speed"""
        
        last_x: int = 0
        while True:
            self.screenshot()
            logger.info(
                f"Find player: {self.find_player()} - ({self.player_x}, {self.player_y}) = {self.player_x - last_x}"
            )
            last_x = self.player_x
            time.sleep(1)

    def color_test(self):
        """Test the color user point to"""
        while True:
            point = pyautogui.position()
            x, y = point
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel = screenshot.getpixel((0, 0))
            logger.info(f"({x}, {y}) = {pixel}")
            time.sleep(1)

    def solve_rune(self, comm: Communicator):
        """Solve rune"""

        # Get rune and player position
        self.screenshot()
        self.find_player()
        wheel_exist: bool = self.find_wheel()
        if not wheel_exist:
            logger.warning("Wheel isn't exist now")
            return

        # Moving x axis
        player_to_wheel_x: int = self.wheel_x - self.player_x
        while wheel_exist and abs(player_to_wheel_x) > SETTINGS.x_miss:
            comm.go_to_x(player_to_wheel_x)
            self.screenshot()
            self.find_player()
            player_to_wheel_x = self.wheel_x - self.player_x
            logger.info(f"Player and Wheel distance X: {player_to_wheel_x}")

        # Moving y axis
        self.screenshot()
        self.find_player()
        wheel_exist = self.find_wheel()
        player_to_wheel_y: int = self.player_y - self.wheel_y
        while wheel_exist and abs(player_to_wheel_y) > SETTINGS.y_miss:
            comm.go_to_y(player_to_wheel_y)
            self.screenshot()
            self.find_player()
            wheel_exist = self.find_wheel()
            player_to_wheel_y = self.player_y - self.wheel_y
            logger.info(f"Player and Wheel distance Y: {player_to_wheel_y}")

        # Mine
        logger.info("At wheel position: Ready to mine")
        time.sleep(1)
        comm.mine()
        
        # Ask rune-break for answer
        answer: str = self.ask_rune_breaker()

        # Break rune
        comm.break_rune(answer)

    def ask_rune_breaker(self) -> str:
        """Use HTTP requests to ask rune-breaker"""

        self.screenshot()
        image_byte = BytesIO()
        self.image.save(image_byte, format='PNG')
        image_byte.seek(0)

        rune_upload: str = f"http://{SETTINGS.rune_host}:{SETTINGS.rune_port}{SETTINGS.rune_upload}"
        files = {'file': ('screenshot.png', image_byte, 'image/png')}
        response = requests.post(rune_upload, files=files)

        if response.status_code == HTTPStatus.OK:
            ans: Dict[str, str] = response.json()
            logger.info(f"Rune-break Success: {ans['answer']}")
            return ans["answer"]
        
        logger.error(f"Rune-break Fail: {response.status_code} - {response.reason}")
        return ""
