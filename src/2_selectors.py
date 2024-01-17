import selectors
import socket

selector = selectors.DefaultSelector()

HOST = "0.0.0.0"
PORT = 6000


def run_server() -> None:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()

    selector.register(               # async event
        fileobj=server_sock,
        events=selectors.EVENT_READ,
        data=accept_connection,
    )


def accept_connection(server_sock):
    client_sock, address = server_sock.accept()

    print(f"Connection from: {address}")

    selector.register(               # async event
        fileobj=client_sock,
        events=selectors.EVENT_READ,
        data=accept_message,
    )


def accept_message(client_sock):
    data = client_sock.recv(1024)
    if data:
        print(data)
    else:
        selector.unregister(client_sock)
        client_sock.close()


def send_message(client_sock):
    client_sock.send('hello')


def event_loop():
    while True:
        events = selector.select()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == "__main__":
    run_server()
    event_loop()
