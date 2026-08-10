# Blackout Protocol

A multiplayer mystery and escape-room game built with Python.

Players connect to a shared game server, explore locked rooms, exchange clues, solve data-driven puzzles, collect items, and escape before the emergency power runs out.

## Features

- Multiplayer client/server architecture
- Room creation and joining
- Role-based gameplay
- Data-driven puzzles loaded from JSON
- Inventory and item collection
- Player movement across a locked facility map
- Simple chat/message events between players
- Timer, win condition, and lose condition
- SQLite-backed game history and scores
- Pygame-ready client UI structure

## Tech Stack

- Python
- Pygame
- socket
- threading
- sqlite3
- JSON

## Project Structure

```text
blackout-protocol/
├── README.md
├── requirements.txt
├── .gitignore
├── client/
│   ├── client.py
│   ├── ui.py
│   └── assets/
├── server/
│   ├── server.py
│   ├── connection_handler.py
│   └── game_manager.py
├── game/
│   ├── game.py
│   ├── player.py
│   ├── room.py
│   ├── items.py
│   └── puzzles.py
├── database/
│   └── database.py
├── shared/
│   └── protocol.py
├── data/
│   ├── rooms.json
│   ├── puzzles.json
│   ├── items.json
│   └── config.json
└── main.py
```

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Start the server:

```bash
python server/server.py
```

Start a client in another terminal:

```bash
python client/client.py
```

You can run two clients in separate terminals to test the multiplayer flow.

## MVP Roadmap

- [ ] Load rooms, puzzles, and items from JSON
- [ ] Implement player movement between rooms
- [ ] Implement puzzle validation on the server
- [ ] Add inventory and item pickup logic
- [ ] Add two-player state synchronization
- [ ] Add Pygame UI screens
- [ ] Add timer and win/lose conditions
- [ ] Save score/history in SQLite
- [ ] Add screenshots or GIF to README

## Suggested Git Workflow

```bash
git checkout -b feat/puzzle-engine
git checkout -b feat/server-networking
git checkout -b feat/pygame-ui
git checkout -b feat/sqlite-leaderboard
```

Example commit messages:

```text
feat: add room movement
feat: implement password puzzles
fix: prevent duplicate item pickup
fix: handle client disconnect
docs: add gameplay screenshots
```

## License

This project is currently developed for learning and portfolio purposes.
