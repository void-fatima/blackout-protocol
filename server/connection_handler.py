"""Client connection handling."""
from __future__ import annotations
import socket
from shared.protocol import decode_message, encode_message, make_message, ERROR, STATE_UPDATE

class ConnectionHandler:
    def __init__(self, client_socket: socket.socket, address: tuple[str, int]) -> None:
        self.client_socket = client_socket
        self.address = address

    def handle(self) -> None:
        with self.client_socket:
            file = self.client_socket.makefile("r", encoding="utf-8")
            for raw_line in file:
                try:
                    message = decode_message(raw_line)
                    print(f"[{self.address}] {message}")
                    response = make_message(STATE_UPDATE, {"message": "Event received."})
                except Exception as exc:
                    response = make_message(ERROR, {"message": str(exc)})
                self.client_socket.sendall(encode_message(response))
