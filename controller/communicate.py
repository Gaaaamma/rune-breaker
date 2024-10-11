"""Responsible for communicating with Leonardo"""

from typing import Optional, List
import serial

from pydantic import BaseModel
import yaml

from logger import logger
from setting import SETTINGS


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
        move_cursor: str
    
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

        # Read config to get leonardo commands
        with open(SETTINGS.config_file) as file:
            config = yaml.safe_load(file)
            self.leonardo_command: LeonardoCommand = LeonardoCommand(**config["leonardo"])
        logger.info(f"Parse leonardo command success")
    
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
            f"{self.leonardo_command.device.move_cursor}{x},{y}"
        ]
        for cmd in commands:
            self.ask_ack(cmd)

    def go_to_x(self, player_to_x: int):
        """Control player to move to wheel in x axis"""

        # Calculate press duration
        duration: str = format(player_to_x / SETTINGS.player_speed, ".1f")

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

    def mine(self):
        """Ask player to mine"""
        
        self.ask_ack(self.leonardo_command.device.mine)
    
    def break_rune(self, answer: str):
        """Send answer to Leonardo and break rune"""
        
        commands: List[str] = [f"{self.leonardo_command.device.break_rune}{answer}"]
        for cmd in commands:
            self.ask_ack(cmd)
