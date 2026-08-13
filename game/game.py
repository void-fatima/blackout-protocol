"""Core game state."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from game.player import Player
from game.room import Room
from game.puzzles import Puzzle
from game.items import Item

@dataclass
class Game:
    game_id: str
    duration_seconds: int
    rooms: dict[str, Room]
    puzzles: dict[str, Puzzle]
    items: dict[str, Item]
    players: dict[str, Player] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    finished: bool = False
    won: bool = False

    def add_player(self, player: Player) -> None:
        self.players[player.player_id] = player

    def time_left(self) -> int:
        elapsed = datetime.now() - self.started_at
        remaining = timedelta(seconds=self.duration_seconds) - elapsed
        return max(0, int(remaining.total_seconds()))

    def is_time_over(self) -> bool:
        return self.time_left() <= 0

    def move_player(self, player_id: str, target_room_id: str) -> bool:
        player = self.players.get(player_id)
        if player is None:
            return False

        current_room = self.rooms.get(player.current_room_id)
        target_room = self.rooms.get(target_room_id)
        if current_room is None or target_room is None:
            return False

        if target_room_id not in current_room.connected_rooms:
            return False

        inventory_ids = {item.item_id for item in player.inventory}
        if not target_room.can_enter(inventory_ids):
            return False

        player.current_room_id = target_room_id
        return True
