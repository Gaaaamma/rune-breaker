"""Use to alert if in village, have other players"""

from controller.detector import Map
from logger import logger
import time

alert_active: bool = True

def alert(mmap: Map, alert_period: float):
    """Detect mmap and check every alert_period"""

    logger.info("alert start scanning")
    while alert_active:
        if mmap.find_npc():
            logger.info(f"Find NPC - you are in the village")
        if mmap.find_others():
            logger.info(f"Find other player - notice cheating checker")
        time.sleep(alert_period)
    logger.info("alert termination")