"""Use to alert if in village, have other players"""

from controller.detector import Map
from logger import logger
from threading import Event
import time

stop_event: Event = Event()

def alert(mmap: Map, alert_period: float):
    """Detect mmap and check every alert_period"""

    logger.info("Alert start scanning")
    while not stop_event.is_set():
        if mmap.find_npc():
            logger.info(f"Find NPC - you are in the village")
        if mmap.find_others():
            logger.info(f"Find other player - notice cheating checker")
        time.sleep(alert_period)
    logger.info("Alert has been terminated")