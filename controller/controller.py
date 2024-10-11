import time
from controller.detector import Map, initialize_map
from controller.alert import alert, alert_handler
from controller.event import alert_event, stop_event
from setting import SETTINGS
from logger import logger
from controller.communicate import Communicator
from threading import Thread
import signal
import sys

def signal_handler(sig, frame):
    stop_event.set()
    print('Controller exit')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    print(SETTINGS.board_port)
    comm: Communicator = Communicator(
        port=SETTINGS.board_port,
        baudrate=SETTINGS.baudrate,
    )

    # ========= Get map information =========
    maple_map: Map = initialize_map()

    while True:
        command: str = input("Please input command: ")

        if command == "hunt":
            # ========= monitor task =========
            stop_event.clear()
            monitor: Thread = Thread(target=alert, args=(comm, maple_map, SETTINGS.alert_period))
            monitor.start()

            # ========= hunting task =========
            logger.info("Hunting mode")
            time.sleep(3)
            try:
                while True:
                    logger.info("Check if alert_event is set")
                    if alert_event.is_set():
                        logger.info("Alert event is set, stop hunting")
                        break

                    logger.info(f"Hunting start: solve rune")
                    rune_solved: bool = maple_map.solve_rune(comm)

                    logger.info("Player moves to standby position")
                    maple_map.go_to_position(maple_map.standby_x, maple_map.standby_y, comm)

                    if alert_event.is_set():
                        logger.info("Alert event is set, stop hunting")
                        break

                    if rune_solved:
                        # Doube check if rune is solved
                        maple_map.screenshot()
                        if not maple_map.find_wheel():
                            comm.hunting(SETTINGS.hunting_time)
                    else:
                        # Rune hasn't appeared
                        comm.songsky(SETTINGS.songsky_time)
            except Exception as e:
                logger.error(f"Exception: {e}")

            finally:
                # Stop monitor task
                stop_event.set()
                monitor.join()
                alert_handler(comm)

        elif command.startswith("frenzy-") and len(command) > 7:
            try:
                minutes: int = int(command[7:])
                logger.info("Play frenzy after 5 seconds")
                time.sleep(5)
                logger.info(f"Play frenzy for {minutes} minutes")
                comm.frenzy(minutes)

            except Exception as e:
                logger.error(f"Command: {command} - {e}")
        
        elif command == "wait":
            comm.hunting(SETTINGS.hunting_time)

        elif command == "color":
            maple_map.screenshot()
            maple_map.color_test()

        elif command == "reset":
            maple_map = initialize_map()

        elif command == "reconnect":
            comm = Communicator(
                port=SETTINGS.board_port,
                baudrate=SETTINGS.baudrate,
            )

        elif command == "coordination":
            logger.info(f"Testing map coordination difference")
            while True:
                maple_map.map_coordination_test()

        elif command == "test_cursor":
            logger.info(f"Input x,y to move your cursor to that position")
            logger.info(f"Input 'exit' to exit test_cursor")

            while True:
                # Get coordination from user
                coordination: str = input("Please input x,y coordination: ")
                if coordination == "exit":
                    break
                
                # Parse cursor position
                try:
                    find_comma: str = coordination.find(",")
                    if find_comma == -1:
                        logger.error(f"Invalid coordination format: {coordination}")
                        continue
                    x: int = int(coordination[:find_comma])
                    y: int = int(coordination[find_comma+1:])
                except Exception as e:
                    logger.error(e)
                    continue
                
                # Move cursor
                logger.info(f"Get move_cursor_to coordination: ({x}, {y})")
                comm.move_cursor_to(x, y)

        elif command == "test":
            logger.info("Nothing to test now")

        else:
            logger.info(f"Unknown command: {command}")

if __name__ == "__main__":
    main()