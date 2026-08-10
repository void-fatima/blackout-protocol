"""Network message helpers for Blackout Protocol.

Messages are newline-delimited JSON objects:
{"type": "MOVE", "data": {"target_room": "archive"}}
"""

from __future__ import annotations

import json
from typing import Any, Dict

JOIN_GAME = "JOIN_GAME"
MOVE = "MOVE"
PICK_ITEM = "PICK_ITEM"
PUZZLE_ANSWER = "PUZZLE_ANSWER"
CHAT = "CHAT"
STATE_UPDATE = "STATE_UPDATE"
GAME_OVER = "GAME_OVER"
ERROR = "ERROR"

Message = Dict[str, Any]


def make_message(message_type: str, data: dict | None = None) -> Message:
    return {"type": message_type, "data": data or {}}


def encode_message(message: Message) -> bytes:
    return (json.dumps(message) + "\n").encode("utf-8")


def decode_message(raw_message: str) -> Message:
    message = json.loads(raw_message)
    if not isinstance(message, dict):
        raise ValueError("Message must be a JSON object.")
    if "type" not in message:
        raise ValueError("Message must contain a 'type' field.")
    if "data" not in message:
        message["data"] = {}
    return message
