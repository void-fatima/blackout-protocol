"""Blackout Protocol entry point.

For development, run the server and client separately:
    python server/server.py
    python client/client.py
"""

from server.game_manager import GameManager


def main() -> None:
    manager = GameManager()
    manager.load_data()
    print("Blackout Protocol project scaffold is ready.")
    print(f"Loaded {len(manager.rooms)} rooms, {len(manager.puzzles)} puzzles, and {len(manager.items)} items.")


if __name__ == "__main__":
    main()
