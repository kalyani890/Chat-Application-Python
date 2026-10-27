
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

clients = {}
lock = threading.Lock()


def broadcast(message):
    with lock:
        connected_clients = list(clients.items())

    for client, username in connected_clients:
        try:
            client.sendall((message + "\n").encode("utf-8"))
        except OSError:
            pass


def handle_client(client, address):
    username = "Unknown"

    try:
        reader = client.makefile("r", encoding="utf-8")
        username = reader.readline().strip()

        if not username:
            return

        with lock:
            clients[client] = username

        print(f"{username} connected.")

        timestamp = datetime.now().strftime("%H:%M")
        broadcast(f"[{timestamp}] SERVER: {username} joined the chat.")

        for line in reader:
            message = line.strip()

            if message == "/quit":
                break

            if message:
                timestamp = datetime.now().strftime("%H:%M")
                chat_message = f"[{timestamp}] {username}: {message}"
                print(chat_message)
                broadcast(chat_message)

    except OSError as error:
        print("Connection error:", error)

    finally:
        with lock:
            clients.pop(client, None)

        timestamp = datetime.now().strftime("%H:%M")
        broadcast(f"[{timestamp}] SERVER: {username} left the chat.")

        print(f"{username} disconnected.")
        client.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen()

        print(f"Chat server running on {HOST}:{PORT}")
        print("Waiting for clients...")

        while True:
            client, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()
