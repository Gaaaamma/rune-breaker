import pyautogui

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
    
    def find_wheel(self):
        for row in range(self.height):
            for col in range(self.width):
                print(self.image.getpixel((col, row)))

    def find_player(self):
        pass