"""Pydantic BaseSettings"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    screenshot_x: int = 0
    screenshot_y: int = 0
    screenshot_width: int = 800
    screenshot_height: int = 600
    raw_data_dir: str = "./data/raw/"
    laplace_data_dir: str = "./data/laplace/"
    standard_data_dir: str = "./data/standard/"
    answer_data_dir: str = "./data/ans/"
    train_data_dir: str = "./data/train/"
    testing_data_dir: str = "./data/test/"
    
    arrow_model: str = "./arrow_cnn.pth"
    upload_path: str = "./data/upload/"
    inference_tmp: str = "./data/inference/"
    
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

    start_img: str = ""
    counter_start: int = 1
    counter_width: int = 5

    filter_start_img: str = ""
    train_img_size: int = 32

    board_port: str = "COM1"
    baudrate: int = 9600

    wheel_r: int = 221
    wheel_g: int = 102
    wheel_b: int = 255
    player_r: int = 255
    player_g: int = 221
    player_b: int = 68
    npc_r: int = 0
    npc_g: int = 221
    npc_b: int = 0
    transport_r: int = 51
    transport_g: int = 204
    transport_b: int = 255
    player_speed: int = 15 # pixels/second
    x_miss: int = 6
    y_miss: int = 5
    y_fail_threshold: int = 8
    hunting_time: int = 910
    songsky_time: int = 10
    standby_time: int = 60
    rune_host: str = "localhost"
    rune_port: str = "32980"
    rune_upload: str = "/v1/rune-break/image"
    

    debug: bool = False
    log_level: int = 20
    formatter: str = "%(asctime)s - [%(funcName)s] - %(levelname)s - %(message)s"

    class Config:
        env_file: str = ".env"
    
SETTINGS: Settings = Settings()

# inner: 455 - 62 = 393
# outer: 456 - 61 = 395