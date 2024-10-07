"""Define maple story boss functions"""

from typing import Dict, List, Optional

from pydantic import BaseModel
import yaml

from setting import SETTINGS


class Inventory(BaseModel):
    
    class Category(BaseModel):
        diff_x: int
        diff_y: int
        equipment_x: int
        equipment_y: int

    class Item(BaseModel):
        diff_x: int
        diff_y: int
        first_x: int
        first_y: int

    category: Category
    item: Item

    @classmethod
    def get_inventory_setting(cls) -> "Inventory":
        """Load boss config file and parse inventory setting"""

        with open(SETTINGS.config_file) as file:
            config: Dict = yaml.safe_load(file)
            inventory: Inventory = Inventory(**config["inventory"])
        
        return inventory


class BossControl(BaseModel):

    class Command(BaseModel):

        class ThrowSetting(BaseModel):
            category_index: int
            x_index: int
            y_index: int

        x_move: int
        y_move: int
        throw_item: Optional[ThrowSetting]
        keyboard: List[str]
    
    name: str
    index: int
    commands: Optional[List[Command]]

    @classmethod
    def get_boss_control_list(cls) -> List["BossControl"]:
        """
        Load boss config file and parse it to list of BossControl object
        """

        control_list: List[BossControl] = []
        with open(SETTINGS.config_file) as file:
            config: Dict = yaml.safe_load(file)
            for boss_control in config["boss"]:
                b = BossControl(**boss_control)
                control_list.append(b)
        
        return control_list


if __name__ == "__main__":
    inventory: Inventory = Inventory.get_inventory_setting()
    boss_control_list: List[BossControl] = BossControl.get_boss_control_list()

    print(inventory)
    print(boss_control_list)