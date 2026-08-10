"""TCP game server scaffold."""
from __future__ import annotations
import socket, threading
from server.connection_handler import ConnectionHandler
from server.game_manager import GameManager

HOST = "127.0.0.1"
PORT = 5050

class GameServer:
    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.manager = GameManager()
        self.manager.load_data()

    def start(self) -> None:
        print(f"Starting Blackout Protocol server on {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            while True:
                client_socket, address = server_socket.accept()
                handler = ConnectionHandler(client_socket, address)
                threading.Thread(target=handler.handle, daemon=True).start()

if __name__ == "__main__":
    GameServer().start()
