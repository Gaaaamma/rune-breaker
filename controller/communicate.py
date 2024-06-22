"""Responsible for communicating with Leonardo"""

from typing import Optional, List

import serial
from logger import logger
from setting import SETTINGS
import time

class Communicator():
    def __init__(self, port: str, baudrate: int, timeout: Optional[float] = None) -> None:
        self.serial = serial.Serial(
            port=port, 
            baudrate=baudrate, 
            timeout=timeout
        )
        logger.info(f"Connect to dev board success: {port}")
    
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

        commands: List[str] = [f"hunt-{seconds}"]
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

        commands: List[str] = [f"frenzy-{minutes}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def go_to_x(self, player_to_x: int):
        """Control player to move to wheel in x axis"""

        # Calculate press duration
        duration: str = format(player_to_x / SETTINGS.player_speed, ".1f")

        # Send x moving command to Leonardo
        commands: List[str] = [f"move-{duration}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def go_to_y(self, player_to_y: int):
        """Control player to move to wheel in y axis"""

        # Decide to jump up or jump down
        direction: str = "up" if player_to_y < 0 else "down"
        commands: List[str] = [f"updown-{direction}"]
        for cmd in commands:
            self.ask_ack(cmd)

    def mine(self):
        """Ask player to mine"""
        
        self.ask_ack("mine")
    
    def break_rune(self, answer: str):
        """Send answer to Leonardo and break rune"""
        
        commands: List[str] = [f"rune-{answer}"]
        for cmd in commands:
            self.ask_ack(cmd)
