import time
from controller.detector import Map, initialize_map
from controller.alert import alert, stop_event
from setting import SETTINGS
from logger import logger
from controller.communicate import Communicator
from threading import Thread

print(SETTINGS.board_port)
comm: Communicator = Communicator(
    port=SETTINGS.board_port,
    baudrate=SETTINGS.baudrate,
)

# ========= Get map information =========
maple_map: Map = initialize_map()

while True:
    command: str = input("Please input command: ")

    if command == "hunting":
        # ========= monitor task =========
        stop_event.clear()
        monitor: Thread = Thread(target=alert, args=(maple_map, SETTINGS.alert_period))
        monitor.start()

        # ========= hunting task =========
        logger.info("Hunting mode")
        time.sleep(3)
        try:
            while True:
                logger.info(f"Find NPC to check if we are in the village")
                if maple_map.find_npc():
                    logger.info(f"Find NPC - stop hunting to prevent from dancing in the village")
                    break

                logger.info(f"Hunting start: solve rune")
                rune_solved: bool = maple_map.solve_rune(comm)

                logger.info("Player moves to standby position")
                maple_map.go_to_position(maple_map.standby_x, maple_map.standby_y, comm)

                if rune_solved:
                    comm.hunting(SETTINGS.hunting_time)
                else:
                    comm.songsky(SETTINGS.songsky_time)
        except Exception as e:
            logger.error(f"Exception: {e}")

        # Stop monitor test
        stop_event.set()
        monitor.join()

    elif command == "color":
        maple_map.screenshot()
        maple_map.color_test()

    elif command == "reset":
        maple_map = initialize_map()

    elif command == "test":
        alert(maple_map, SETTINGS.alert_period)

    else:
        logger.info(f"Unknown command: {command}")