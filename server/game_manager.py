"""Game data loading and high-level game management."""
from __future__ import annotations
import json
from pathlib import Path
from game.items import Item
from game.puzzles import Puzzle
from game.room import Room

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

class GameManager:
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}
        self.puzzles: dict[str, Puzzle] = {}
        self.items: dict[str, Item] = {}

    def load_data(self) -> None:
        self.rooms = {r.room_id: r for r in self._load_rooms(DATA_DIR / "rooms.json")}
        self.puzzles = {p.puzzle_id: p for p in self._load_puzzles(DATA_DIR / "puzzles.json")}
        self.items = {i.item_id: i for i in self._load_items(DATA_DIR / "items.json")}

    def _load_rooms(self, path: Path) -> list[Room]:
        with path.open("r", encoding="utf-8") as file:
            return [Room.from_dict(item) for item in json.load(file)]

    def _load_puzzles(self, path: Path) -> list[Puzzle]:
        with path.open("r", encoding="utf-8") as file:
            return [Puzzle.from_dict(item) for item in json.load(file)]

    def _load_items(self, path: Path) -> list[Item]:
        with path.open("r", encoding="utf-8") as file:
            return [Item.from_dict(item) for item in json.load(file)]
