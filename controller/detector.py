import pyautogui
from setting import SETTINGS

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