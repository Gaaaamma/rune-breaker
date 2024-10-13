"""Define maple story boss functions"""

from typing import Dict, List, Optional, Tuple
import time

from pydantic import BaseModel, model_validator

from logger import logger
from setting import CONFIG


class Inventory(BaseModel):
    """Parse inventory config"""

    class Category(BaseModel):
        max_index_x: int
        diff_x: int
        equipment_x: int
        equipment_y: int

    class Item(BaseModel):
        max_index_x: int
        max_index_y: int
        diff_x: int
        diff_y: int
        first_x: int
        first_y: int
        spare_x: int
        spare_y: int

    shortcut: str
    category: Category
    item: Item


class InventoryControl():
    """Collect all inventory control useful functions"""
    
    inventory = Inventory(**CONFIG["inventory"])
    
    @classmethod
    def get_category_coordination(cls, index_x: int) -> Tuple[int, int]:
        """use index_x to calculate category coordination"""
        
        # index validation
        if index_x < 0 or index_x > cls.inventory.category.max_index_x:
            raise(
                f"category index_x must within 0 and {cls.inventory.category.max_index_x}: get {index_x}"
            )
        
        # calculate x y coordination
        x: int = cls.inventory.category.equipment_x + index_x * cls.inventory.category.diff_x
        y: int = cls.inventory.category.equipment_y
        logger.info(f"Get index({index_x}, 0) => coordination({x}, {y})")

        return (x, y)

    @classmethod
    def get_item_coordination(cls, index_x: int, index_y: int) -> Tuple[int, int]:
        """use index_x and index_y to calculate item coordination"""
        
        # index_x, index_y validation
        if index_x < 0 or index_x > cls.inventory.item.max_index_x:
            raise(
                f"item index_x must within 0 and {cls.inventory.item.max_index_x}: get {index_x}"
            )
        if index_y < 0 or index_y > cls.inventory.item.max_index_y:
            raise(
                f"item index_y must within 0 and {cls.inventory.item.max_index_y}: get {index_y}"
            )
        
        # calculate x y coordination
        x: int = cls.inventory.item.first_x + index_x * cls.inventory.item.diff_x
        y: int = cls.inventory.item.first_y + index_y * cls.inventory.item.diff_y
        logger.info(f"Get index({index_x}, {index_y}) => position({x}, {y})")

        return (x, y)


class Boss(BaseModel):
    """Parse boss config"""

    class Command(BaseModel):

        class ThrowSetting(BaseModel):
            category_index_x: int
            item_index_x: int
            item_index_y: int
            multiple_item: bool

        x_move: int
        y_move: int
        cursor_move: Optional[List[int]]
        throw_item: Optional[ThrowSetting]
        keyboard: Optional[List[str]]
        delay: Optional[List[int]]

        @model_validator(mode="after")
        def keyboard_delay_len_check(cls, values):
            keyboard = values.keyboard
            delay = values.delay

            l_keyboard: int = len(keyboard) if keyboard is not None else -1
            l_delay: int = len(delay) if delay is not None else -1
            if l_keyboard != l_delay:
                raise ValueError(f"len(keyboard)={l_keyboard} != len(delay)={l_delay}.")

            return values
    
    name: str
    index: int
    commands: Optional[List[Command]]


if __name__ == "__main__":
    print("========== Get category ==========")
    for i in range(InventoryControl.inventory.category.max_index_x + 1):
        InventoryControl.get_category_coordination(i)

    print("\n========== Get item ==========")
    for i_y in range(InventoryControl.inventory.item.max_index_y + 1):
        for i_x in range(InventoryControl.inventory.item.max_index_x + 1):
            InventoryControl.get_item_coordination(i_x, i_y)
        print()