"""SQLite database manager for game history and scores."""
from __future__ import annotations
import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str | Path = "blackout.db") -> None:
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def initialize(self) -> None:
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    total_score INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id TEXT PRIMARY KEY,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    result TEXT,
                    duration INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id TEXT NOT NULL,
                    player_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    role TEXT NOT NULL
                )
            """)
            connection.commit()

if __name__ == "__main__":
    DatabaseManager().initialize()
    print("Database initialized.")
