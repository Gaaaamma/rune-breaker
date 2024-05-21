"""Pydantic BaseSettings"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    screenshot_width: int = 800
    screenshot_height: int = 600
    raw_data_dir: str = "./data/raw/"
    laplace_data_dir: str = "./data/laplace/"
    cut_data_dir: str = "./data/cut/"

    left_bound: int = 50
    right_bonud: int = 400

    laplace_blue_threshold: int = 240
    laplace_blue_tolerantion: int = 50
    laplace_blue_height_start: int = 150
    laplace_blue_height_end: int = screenshot_height / 2
    laplace_blue_vt_threshold: int = 40
    laplace_blue_width_start: int = 140
    laplace_blue_width_end: int = 660

    captcha_height: int = 80
    captcha_width: int = 395
    magic_crop_vertical: int = 15
    magic_crop_vertical_t2: int = 11
    magic_crop_horizontal: int = 20

    start_img: str = "lap_1716290708-wwsd.png"
    counter_start: int = 385
    counter_width: int = 5

    debug: bool = True
    log_level: int = 20
    formatter: str = "%(asctime)s - [%(funcName)s] - %(levelname)s - %(message)s"

    class Config:
        env_file: str = ".env"
    
SETTINGS: Settings = Settings()

# inner: 455 - 62 = 393
# outer: 456 - 61 = 395