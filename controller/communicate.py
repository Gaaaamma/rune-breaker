"""Responsible for communicating with Leonardo"""

from typing import Optional

import serial
from logger import logger
import time

class Communicator():
    def __init__(self, port: str, baudrate: int, timeout: Optional[float] = None) -> None:
        self.serial = serial.Serial(
            port=port, 
            baudrate=baudrate, 
            timeout=timeout
        )
        logger.info(f"Connect to dev board success: {port}")
    
    def ask_ack(self, command: str):
        """Send message to Leonardo and wait for ack"""

        self.serial.write((command + "\n").encode())
        logger.info(f"Send command: {command}")

        received_message = self.serial.readline().decode().strip()
        logger.info(f"Leonardo ack: {received_message}")
