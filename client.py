
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    try:
        reader = client.makefile("r", encoding="utf-8")

        for message in reader:
            print(message.rstrip())

    except OSError:
        pass

    finally:
        print("\nDisconnected from chat server.")


def start_client():
    username = input("Enter your username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        client.sendall((username + "\n").encode("utf-8"))

        print("Connected to chat!")
        print("Type your message and press Enter.")
        print("Type /quit to leave.\n")

        receiver = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )
        receiver.start()

        while True:
            message = input()

            client.sendall((message + "\n").encode("utf-8"))

            if message == "/quit":
                break

    except ConnectionRefusedError:
        print("Cannot connect. Start server.py first.")

    except OSError as error:
        print("Connection error:", error)

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
