"""Data-driven puzzle engine."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class PuzzleType(str, Enum):
    PASSWORD = "password"
    SEQUENCE = "sequence"
    LOGIC = "logic"
    RIDDLE = "riddle"
    COMBINATION = "combination"

@dataclass
class Puzzle:
    puzzle_id: str
    puzzle_type: PuzzleType
    question: str
    answer: str
    reward: str | None = None
    solved: bool = False

    def check_answer(self, answer: str) -> bool:
        if self.solved:
            return True
        is_correct = answer.strip().lower() == self.answer.strip().lower()
        if is_correct:
            self.solved = True
        return is_correct

    @classmethod
    def from_dict(cls, data: dict) -> "Puzzle":
        return cls(data["id"], PuzzleType(data["type"]), data["question"], str(data["answer"]), data.get("reward"))
