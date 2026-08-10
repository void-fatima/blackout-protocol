"""Room model for the facility map."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Room:
    room_id: str
    name: str
    description: str
    connected_rooms: list[str] = field(default_factory=list)
    puzzle_ids: list[str] = field(default_factory=list)
    item_ids: list[str] = field(default_factory=list)
    locked: bool = False
    required_item: str | None = None

    def can_enter(self, inventory_item_ids: set[str]) -> bool:
        if not self.locked:
            return True
        return self.required_item is not None and self.required_item in inventory_item_ids

    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        return cls(
            room_id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            connected_rooms=data.get("connected_rooms", []),
            puzzle_ids=data.get("puzzles", []),
            item_ids=data.get("items", []),
            locked=data.get("locked", False),
            required_item=data.get("required_item"),
        )
