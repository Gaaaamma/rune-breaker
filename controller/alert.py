"""Use to alert if in village, have other players"""

from controller.detector import Map, Communicator
from controller.event import alert_event, stop_event
from logger import logger
import time


def alert(comm: Communicator, mmap: Map, alert_period: float):
    """Detect mmap and check every alert_period"""

    logger.info("Alert start scanning")
    alert_event.clear()
    counter: int = 0
    while not stop_event.is_set():
        if mmap.find_npc():
            logger.info(f"Find NPC - you are in the village")
            alert_event.set()
            counter += 1
            logger.info(f"Send stop command to Leonardo: {counter}")
            comm.send("stop")
        if mmap.find_others():
            logger.info(f"Find other player - notice cheating checker")
        time.sleep(alert_period)
    logger.info("Alert has been terminated")

def alert_handler(comm: Communicator):
    """If alert happened, follow this procedure to solve"""

    if alert_event.is_set():
        logger.info("Process alert... (Leonardo must be controllable)")

        logger.info("Alert_event clear")
        alert_event.clear()
    