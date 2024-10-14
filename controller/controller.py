import signal
import sys
import time
from threading import Thread
from typing import List

from controller.alert import alert, alert_handler
from controller.boss import Boss
from controller.communicate import Communicator
from controller.detector import Map, initialize_map
from controller.event import alert_event, stop_event
from setting import SETTINGS, CONFIG
from logger import logger


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
        
        elif command == "test_duration":
            logger.info(f"Input duration to move your character for duration seconds")
            logger.info(f"Input 'exit' to exit test_duration")

            while True:
                # Get duration from user
                duration: str = input("Please input duration: ")
                if duration == "exit":
                    break
                
                # Parse duration to seconds
                try:
                    seconds: float = float(duration)
                except Exception as e:
                    logger.error(e)
                    continue
                
                # Move character
                logger.info(f"Move character for duration={seconds}")
                time.sleep(1)
                comm.go_to_x_duration(seconds)

        elif command == "boss":
            logger.info("daily boss hunting")
            time.sleep(3)

            # Iterate all boss
            for boss in CONFIG["boss"]:
                boss: Boss = Boss(**boss)
                if boss.enabled and boss.commands:
                    logger.info(f"Hunting: {boss.name}")
                    comm.move_to_boss_map(boss.index)
                    for boss_command in boss.commands:
                        logger.info(f"Move x (with duration seconds): {boss_command.move_x_duration}")
                        comm.go_to_x_duration(boss_command.move_x_duration)
                        time.sleep(1)

                        # Move y (with count times up / down)
                        logger.info(f"Move y (with count times up / down): {boss_command.move_y_count}")
                        comm.go_to_y_count(boss_command.move_y_count)
                        time.sleep(1)

                        # Move cursor
                        if boss_command.cursor:
                            logger.info(f"Move cursor to ({boss_command.cursor.cursor_x},{boss_command.cursor.cursor_y})")
                            comm.move_cursor_to(
                                boss_command.cursor.cursor_x,
                                boss_command.cursor.cursor_y
                            )
                            time.sleep(0.5)

                            if boss_command.cursor.click:
                                comm.click_cursor("LEFT")
                                time.sleep(0.5)

                        # Throw item
                        logger.info("Throw item")
                        comm.throw_item(boss_command.throw_item)
                        time.sleep(0.5)

                        # Arrow exectuion
                        logger.info("Arrow excution")
                        for direction, delay in zip(boss_command.arrow, boss_command.arrow_delay):
                            comm.arrow(direction)
                            time.sleep(delay)

                        # Keyboard execution
                        logger.info("Keyboard excution")
                        for command, delay in zip(boss_command.keyboard, boss_command.keyboard_delay):
                            comm.key(command)
                            time.sleep(delay)

                        logger.info(f"Get next command")
                        time.sleep(2)

        elif command == "test":
            logger.info("Nothing to test now")

        else:
            logger.info(f"Unknown command: {command}")

if __name__ == "__main__":
    main()