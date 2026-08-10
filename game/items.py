"""Item models for inventory and interactions."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ItemType(str, Enum):
    KEY = "key"
    ACCESS_CARD = "access_card"
    DOCUMENT = "document"
    FLASHLIGHT = "flashlight"
    TOOL = "tool"

@dataclass
class Item:
    item_id: str
    name: str
    item_type: ItemType
    description: str
    target: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(data["id"], data["name"], ItemType(data["type"]), data.get("description", ""), data.get("target"))
