"""Responsible for communicating with Leonardo"""

from typing import Optional, List, Literal
import serial
import time

from pydantic import BaseModel

from controller.boss import InventoryControl, Boss
from logger import logger
from setting import SETTINGS, CONFIG


class LeonardoCommand(BaseModel):
    """Parse config file leonardo and player commands"""

    class PlayerCommand(BaseModel):
        """Define Leonardo player command"""

        enter: str
        confirm: str
        up: str
        down: str
        left: str
        right: str

    class DeviceCommand(BaseModel):
        """Define Leonardo device command"""

        hunt: str
        move_to_boss_map: str
        frenzy: str
        move_x: str
        move_y: str
        mine: str
        break_rune: str
        cursor_move: str
        cursor_click: str
        key: str
        enter: str
    
    player: PlayerCommand
    device: DeviceCommand


class Communicator():
    def __init__(self, port: str, baudrate: int, timeout: Optional[float] = None) -> None:
        # Connect to Leonardo
        self.serial = serial.Serial(
            port=port, 
            baudrate=baudrate, 
            timeout=timeout
        )
        logger.info(f"Connect to dev board success: {port}")

        # Get leonardo commands
        self.leonardo_command: LeonardoCommand = LeonardoCommand(**CONFIG["leonardo"])
        logger.info(f"Get leonardo command")
    
    def send(self, command: str):
        """Send message to Leonardo and return"""

        self.serial.write((command + "\n").encode())
        logger.info(f"Send command and return: {command}")

    def ask_ack(self, command: str):
        """Send message to Leonardo and wait for ack"""

        self.serial.write((command + "\n").encode())
        logger.info(f"Send command: {command}")

        received_message = self.serial.readline().decode().strip()
        logger.info(f"Leonardo ack: {received_message}")

    def key(self, message: str, open_chat: bool = False, close_chat: bool = False):
        """
        Control player to key something (commands/message).
        The function will send your message character one by one with key prefix.
        - message: The message or command you want to send
        - open_chat: True = Type ENTER first to open chat
        - close_chat: True = Type ENTER at the end to send message
        """

        # Open chat (if needed)
        if open_chat:
            self.ask_ack(
                f"{self.leonardo_command.device.key}{self.leonardo_command.device.enter}"
            )
            time.sleep(0.5)
        
        # Key message
        for char in message:
            self.ask_ack(
                f"{self.leonardo_command.device.key}{char}"
            )
            time.sleep(0.5)
        
        # Send (Close chat if needed)
        if close_chat:
            self.ask_ack(
                f"{self.leonardo_command.device.key}{self.leonardo_command.device.enter}"
            )
            time.sleep(0.5)

    def hunting(self, seconds: int):
        """Control player to hunt for seconds"""

        commands: List[str] = [f"{self.leonardo_command.device.hunt}{seconds}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def songsky(self, seconds: int):
        """Control player to hunt(standby with songsky only) for seconds"""

        commands: List[str] = [f"songsky-{seconds}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def standby(self, seconds: int):
        """Control player to hunt(standby) for seconds"""

        commands: List[str] = [f"standby-{seconds}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def fountain(self, seconds: int):
        """Control player to hunt(fountain) for seconds"""

        commands: List[str] = [f"fountain-{seconds}"]
        for cmd in commands:
            self.ask_ack(cmd)
    
    def frenzy(self, minutes: int):
        """Control player to use frenzy for minutes"""

        commands: List[str] = [f"{self.leonardo_command.device.frenzy}{minutes}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def move_cursor_to(self, x: int, y: int):
        """Control cursor to (x, y)"""

        commands: List[str] = [
            f"{self.leonardo_command.device.cursor_move}{x},{y}"
        ]
        for cmd in commands:
            self.ask_ack(cmd)

    def click_cursor(self, direction: Literal["LEFT", "RIGHT"]):
        """Make cursor click MOUSE_LEFT or MOUSE_RIGHT"""

        direction = "l" if direction == "LEFT" else "r"
        commands: str = f"{self.leonardo_command.device.cursor_click}{direction}"
        self.ask_ack(commands)

    def move_to_boss_map(self, index: int, delay_secs: float = 3.0):
        """Move to boss map at specified index and wait"""

        commands: List[str] = [
            f"{self.leonardo_command.device.move_to_boss_map}{index}"
        ]
        for cmd in commands:
            self.ask_ack(cmd)

        time.sleep(delay_secs)

    def go_to_x(self, player_to_x: int):
        """Control player to move to wheel in x axis"""

        # Calculate press duration
        duration: str = format(player_to_x / SETTINGS.player_speed, ".1f")

        # Send x moving command to Leonardo
        commands: List[str] = [f"{self.leonardo_command.device.move_x}{duration}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def go_to_x_duration(self, duration: float):
        """Control player to move in duration seconds"""

        # Send x moving command to Leonardo
        commands: List[str] = [f"{self.leonardo_command.device.move_x}{duration}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def go_to_y(self, player_to_y: int):
        """Control player to move to wheel in y axis"""

        # Decide to jump up or jump down
        direction: str = "up" if player_to_y < 0 else "down"
        commands: List[str] = [f"{self.leonardo_command.device.move_y}{direction}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def go_to_y_count(self, count: int):
        """
        Continuously use skill-rope to go up / down with count times.
        - count == 0: do nothing (needless to go up / down).
        - count > 0: up with longer delay seconds, count -= 1 at the end.
        - count < 0: down with shorter delay seconds, count += 1 at the end.
        """

        direction: str = "up" if count > 0 else "down"
        command: str = f"{self.leonardo_command.device.move_y}{direction}"

        while count != 0:
            self.ask_ack(command)
            
            # Going up takes more delay time
            if count > 0:
                count -= 1
                time.sleep(3)
            
            elif count < 0:
                count +=1
                time.sleep(1.5)

    def mine(self):
        """Ask player to mine"""
        
        self.ask_ack(self.leonardo_command.device.mine)

    def throw_item(self, throw_setting: Optional[Boss.Command.ThrowSetting], delay_secs: float = 0.5):
        """throw item out of inventory"""

        if throw_setting:
            # Open inventory
            self.key(InventoryControl.inventory.shortcut)
            time.sleep(delay_secs)

            # Get category coordination
            category_x, category_y = InventoryControl.get_category_coordination(
                throw_setting.category_index_x
            )

            # Move to specified category and click
            self.move_cursor_to(category_x, category_y)
            time.sleep(delay_secs)
            self.click_cursor("LEFT")
            time.sleep(delay_secs)

            # Move to specified item and click
            item_x, item_y = InventoryControl.get_item_coordination(
                throw_setting.item_index_x, throw_setting.item_index_y
            )
            self.move_cursor_to(item_x, item_y)
            time.sleep(delay_secs)
            self.click_cursor("LEFT")
            time.sleep(delay_secs)

            # Move to spare position and click
            self.move_cursor_to(
                InventoryControl.inventory.item.spare_x, InventoryControl.inventory.item.spare_y
            )
            time.sleep(delay_secs)
            self.click_cursor("LEFT")
            time.sleep(delay_secs)

            # Check multiple items to check if we need to type number to throw
            if throw_setting.multiple_item:
                # Just throw one item out of inventory
                self.key("1", open_chat=False, close_chat=True)
                time.sleep(delay_secs)
            
            # Close inventory
            self.key(InventoryControl.inventory.shortcut)
            time.sleep(delay_secs)

    def break_rune(self, answer: str):
        """Send answer to Leonardo and break rune"""
        
        commands: List[str] = [f"{self.leonardo_command.device.break_rune}{answer}"]
        for cmd in commands:
            self.ask_ack(cmd)
