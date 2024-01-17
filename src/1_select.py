import select
import socket

monitor_objects = []


def get_server_socket():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", 6000))
    server_sock.listen()
    return server_sock


def accept_message(client_sock) -> None:
    data = client_sock.recv(1024)
    if data:
        print(data)
    else:
        client_sock.close()


def accept_client(server_sock) -> None:
    client_sock, address = server_sock.accept()
    monitor_objects.append(client_sock)
    print(address)


def event_loop(server_sock):
    while True:
        read_data, _, _ = select.select(monitor_objects, [], [])

        for sock in read_data:
            if sock is server_sock:
                accept_client(sock)
            else:
                accept_message(sock)


if __name__ == "__main__":
    server_socket = get_server_socket()
    monitor_objects.append(server_socket)
    event_loop(server_socket)
