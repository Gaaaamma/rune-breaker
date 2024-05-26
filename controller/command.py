from pydantic_settings import BaseSettings

class Command(BaseSettings):
    hunting: str = "h"
    walk_left: str = "l"
    walk_right: str = "r"
    jump_up: str = "u"
    jump_down: str = "d"
    mine: str = "m"

command: Command = Command()