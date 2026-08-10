"""Simple client scaffold for local testing."""
from __future__ import annotations
import socket
from shared.protocol import JOIN_GAME, CHAT, encode_message, make_message

HOST = "127.0.0.1"
PORT = 5050

def send_message(sock: socket.socket, message_type: str, data: dict) -> None:
    sock.sendall(encode_message(make_message(message_type, data)))

def main() -> None:
    username = input("Username: ").strip() or "player"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        send_message(sock, JOIN_GAME, {"username": username})
        while True:
            text = input("> ").strip()
            if text.lower() in {"quit", "exit"}:
                break
            send_message(sock, CHAT, {"message": text})
            print(sock.recv(4096).decode("utf-8").strip())

if __name__ == "__main__":
    main()
