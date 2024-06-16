import time
import pyautogui
from typing import Dict
from setting import SETTINGS
from logger import logger
from controller.communicate import Communicator
from io import BytesIO
import requests
from http import HTTPStatus


class Map():
    def __init__(
        self, x1: int, y1: int,
        x2: int, y2: int,
        standby_x: int, standby_y: int,
    ) -> None:
        self.x1: int = x1
        self.y1: int = y1
        self.x2: int = x2
        self.y2: int = y2
        self.width: int = x2 - x1
        self.height: int = y2 - y1
        self.standby_x: int = standby_x - self.x1
        self.standby_y: int = standby_y - self.y1

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
    
    def find_npc(self) -> bool:
        self.screenshot()
        for row in range(self.height):
            for col in range(self.width):
                if self.is_npc(self.image.getpixel((col, row))):
                    return True
        return False

    def is_npc(self, rgba) -> bool:
        r, g, b = rgba
        return (
            r == SETTINGS.npc_r and
            g == SETTINGS.npc_g and 
            b == SETTINGS.npc_b
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
        
        for row in range(self.height):
            for col in range(self.width):
                rgba = self.image.getpixel((col, row))
                r, g, b = rgba
                logger.info(f"({col}, {row}) = ({r}, {g}, {b})")

    def solve_rune(self, comm: Communicator) -> bool:
        """
        Solve rune
        return True: rune exists and is solved by Leonardo
        return False: rune isn't exist
        """

        # Get rune and player position
        self.screenshot()
        self.find_player()
        wheel_exist: bool = self.find_wheel()
        if not wheel_exist:
            logger.warning("Wheel isn't exist now - not solved")
            return False
        
        while wheel_exist:
            # Moving x axis
            player_to_wheel_x: int = self.wheel_x - self.player_x
            while abs(player_to_wheel_x) > SETTINGS.x_miss:
                comm.go_to_x(player_to_wheel_x)
                self.screenshot()
                self.find_player()
                player_to_wheel_x = self.wheel_x - self.player_x
                logger.info(f"Player and Wheel distance X: {player_to_wheel_x}")

            # Moving y axis
            self.screenshot()
            self.find_player()
            player_to_wheel_y: int = self.wheel_y - self.player_y
            y_fail: int = 0
            while abs(player_to_wheel_y) > SETTINGS.y_miss:
                if y_fail >= SETTINGS.y_fail_threshold:
                    logger.info(f"Player go_to_y fails {y_fail} times - CANCEL")
                    break
                comm.go_to_y(player_to_wheel_y)
                self.screenshot()
                self.find_player()
                player_to_wheel_y = self.wheel_y - self.player_y
                logger.info(f"Player and Wheel distance Y: {player_to_wheel_y}")
                y_fail += 1

            # Mine
            logger.info("At wheel position: Ready to mine")
            time.sleep(1)
            comm.mine()
        
            # Ask rune-break for answer
            answer: str = self.ask_rune_breaker()

            # Break rune
            comm.break_rune(answer)

            # Move a little left/right to check if rune is solved
            direction: int = -1 if self.wheel_x >= int(self.width / 2) else 1
            comm.go_to_x(direction * SETTINGS.player_speed)
            self.screenshot()
            self.find_player()
            wheel_exist = self.find_wheel()
            logger.info(f"Rune is solved: {not wheel_exist}")

        return True

    def go_to_position(self, x: int, y: int, comm: Communicator):
        """
        Move player to position x, y of map
        x, y must be the pixel in map
        not the pixel in screen
        """

        # Moving x axis
        self.screenshot()
        self.find_player()
        player_to_x: int = x - self.player_x
        logger.debug(f"x: {x}, self.player_x: {self.player_x}")
        while abs(player_to_x) > SETTINGS.x_miss:
            comm.go_to_x(player_to_x)
            self.screenshot()
            self.find_player()
            player_to_x = x - self.player_x
            logger.info(f"Player and Wheel distance X: {player_to_x}")

        # Moving y axis
        self.screenshot()
        self.find_player()
        player_to_y: int = y - self.player_y
        while abs(player_to_y) > SETTINGS.y_miss:
            comm.go_to_y(player_to_y)
            self.screenshot()
            self.find_player()
            player_to_y = y - self.player_y
            logger.info(f"Player and Wheel distance Y: {player_to_y}")

    def ask_rune_breaker(self) -> str:
        """Use HTTP requests to ask rune-breaker"""

        # Get 800 x 600 screen image
        image = pyautogui.screenshot(region=(
            SETTINGS.screenshot_x,
            SETTINGS.screenshot_y,
            SETTINGS.screenshot_width,
            SETTINGS.screenshot_height,
        ))
        image_byte = BytesIO()
        image.save(image_byte, format='PNG')
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

def initialize_map() -> Map:
    """Procedure to initialize the map"""

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
    return maple_map