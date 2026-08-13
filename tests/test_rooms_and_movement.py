"""Tests for room data integrity and player movement."""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from game.game import Game
from game.items import Item, ItemType
from game.player import Player, PlayerRole
from game.room import Room
from server.game_manager import GameManager


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


class RoomAccessTests(unittest.TestCase):
    def test_unlocked_room_allows_entry(self) -> None:
        room = Room("laboratory", "Laboratory", "An unlocked lab.")

        self.assertTrue(room.can_enter(set()))

    def test_locked_room_rejects_entry_without_required_item(self) -> None:
        room = Room(
            "security",
            "Security",
            "A locked security room.",
            locked=True,
            required_item="security_key",
        )

        self.assertFalse(room.can_enter(set()))

    def test_locked_room_allows_entry_with_required_item(self) -> None:
        room = Room(
            "security",
            "Security",
            "A locked security room.",
            locked=True,
            required_item="security_key",
        )

        self.assertTrue(room.can_enter({"security_key"}))


class RoomDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.room_data = cls._load_json("rooms.json")
        cls.item_data = cls._load_json("items.json")
        cls.puzzle_data = cls._load_json("puzzles.json")
        cls.room_ids = {room["id"] for room in cls.room_data}
        cls.item_ids = {item["id"] for item in cls.item_data}
        cls.puzzle_ids = {puzzle["id"] for puzzle in cls.puzzle_data}

    @staticmethod
    def _load_json(filename: str) -> list[dict[str, Any]]:
        with (DATA_DIR / filename).open(encoding="utf-8") as data_file:
            return json.load(data_file)

    def test_room_json_loads_into_room_objects(self) -> None:
        manager = GameManager()

        manager.load_data()

        self.assertEqual(len(manager.rooms), len(self.room_data))
        self.assertTrue(all(isinstance(room, Room) for room in manager.rooms.values()))

    def test_every_connected_room_exists(self) -> None:
        for room in self.room_data:
            with self.subTest(room=room["id"]):
                self.assertLessEqual(set(room.get("connected_rooms", [])), self.room_ids)

    def test_every_room_puzzle_reference_exists(self) -> None:
        for room in self.room_data:
            with self.subTest(room=room["id"]):
                self.assertLessEqual(set(room.get("puzzles", [])), self.puzzle_ids)

    def test_every_room_item_reference_exists(self) -> None:
        for room in self.room_data:
            with self.subTest(room=room["id"]):
                self.assertLessEqual(set(room.get("items", [])), self.item_ids)

    def test_every_required_item_reference_exists(self) -> None:
        for room in self.room_data:
            required_item = room.get("required_item")
            with self.subTest(room=room["id"]):
                self.assertTrue(required_item is None or required_item in self.item_ids)

    def test_room_ids_are_unique(self) -> None:
        self.assertEqual(len(self.room_ids), len(self.room_data))

    def test_room_ids_and_names_are_non_empty(self) -> None:
        for room in self.room_data:
            with self.subTest(room=room.get("id")):
                self.assertTrue(str(room.get("id", "")).strip())
                self.assertTrue(str(room.get("name", "")).strip())

    def test_rooms_do_not_connect_to_themselves(self) -> None:
        for room in self.room_data:
            with self.subTest(room=room["id"]):
                self.assertNotIn(room["id"], room.get("connected_rooms", []))

    def test_room_connections_are_bidirectional(self) -> None:
        rooms_by_id = {room["id"]: room for room in self.room_data}

        for room in self.room_data:
            for connected_room_id in room.get("connected_rooms", []):
                with self.subTest(room=room["id"], connected_room=connected_room_id):
                    connected_room = rooms_by_id[connected_room_id]
                    self.assertIn(room["id"], connected_room.get("connected_rooms", []))


class MovementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.security_key = Item(
            "security_key",
            "Security Key",
            ItemType.KEY,
            "Unlocks Security.",
        )
        self.rooms = {
            "control_room": Room(
                "control_room",
                "Control Room",
                "The starting room.",
                connected_rooms=["laboratory", "security"],
            ),
            "laboratory": Room(
                "laboratory",
                "Laboratory",
                "An unlocked lab.",
                connected_rooms=["control_room"],
            ),
            "security": Room(
                "security",
                "Security",
                "A locked security room.",
                connected_rooms=["control_room"],
                locked=True,
                required_item="security_key",
            ),
            "archive": Room("archive", "Archive", "A disconnected room."),
        }
        self.game = Game(
            game_id="movement-tests",
            duration_seconds=900,
            rooms=self.rooms,
            puzzles={},
            items={self.security_key.item_id: self.security_key},
        )
        self.player = Player(
            "player-1",
            "Ada",
            PlayerRole.INVESTIGATOR,
            "control_room",
        )
        self.game.add_player(self.player)

    def test_add_player_uses_player_id_as_key(self) -> None:
        self.assertIs(self.game.players["player-1"], self.player)

    def test_player_can_move_to_connected_unlocked_room(self) -> None:
        self.assertTrue(self.game.move_player("player-1", "laboratory"))
        self.assertEqual(self.player.current_room_id, "laboratory")

    def test_player_cannot_move_to_non_connected_room(self) -> None:
        self.assertFalse(self.game.move_player("player-1", "archive"))
        self.assertEqual(self.player.current_room_id, "control_room")

    def test_player_cannot_enter_locked_room_without_item(self) -> None:
        self.assertFalse(self.game.move_player("player-1", "security"))
        self.assertEqual(self.player.current_room_id, "control_room")

    def test_player_can_enter_locked_room_after_receiving_item(self) -> None:
        self.player.add_item(self.security_key)

        self.assertTrue(self.game.move_player("player-1", "security"))
        self.assertEqual(self.player.current_room_id, "security")

    def test_failed_movement_does_not_change_current_room(self) -> None:
        original_room_id = self.player.current_room_id

        self.assertFalse(self.game.move_player("player-1", "archive"))
        self.assertEqual(self.player.current_room_id, original_room_id)

    def test_unknown_player_is_handled_safely(self) -> None:
        self.assertFalse(self.game.move_player("missing-player", "laboratory"))

    def test_unknown_target_room_is_handled_safely(self) -> None:
        self.rooms["control_room"].connected_rooms.append("missing-room")

        self.assertFalse(self.game.move_player("player-1", "missing-room"))
        self.assertEqual(self.player.current_room_id, "control_room")

    def test_unknown_current_room_is_handled_safely(self) -> None:
        self.player.current_room_id = "missing-room"

        self.assertFalse(self.game.move_player("player-1", "laboratory"))
        self.assertEqual(self.player.current_room_id, "missing-room")

    def test_actual_room_data_supports_movement(self) -> None:
        manager = GameManager()
        manager.load_data()
        game = Game(
            game_id="json-integration",
            duration_seconds=900,
            rooms=manager.rooms,
            puzzles=manager.puzzles,
            items=manager.items,
        )
        player = Player(
            "json-player",
            "Grace",
            PlayerRole.ENGINEER,
            "control_room",
        )
        game.add_player(player)

        self.assertTrue(game.move_player("json-player", "laboratory"))
        self.assertEqual(player.current_room_id, "laboratory")


if __name__ == "__main__":
    unittest.main()
