"""Player models and role behavior."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from game.items import Item

class PlayerRole(str, Enum):
    INVESTIGATOR = "investigator"
    ENGINEER = "engineer"
    HACKER = "hacker"

@dataclass
class Player:
    player_id: str
    username: str
    role: PlayerRole
    current_room_id: str
    score: int = 0
    inventory: list[Item] = field(default_factory=list)

    def add_item(self, item: Item) -> None:
        self.inventory.append(item)

    def has_item(self, item_id: str) -> bool:
        return any(item.item_id == item_id for item in self.inventory)
