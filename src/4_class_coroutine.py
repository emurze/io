import enum
from select import select
import socket
from collections.abc import Generator

tasks: list[Generator] = []  # ready generators
to_read = {}
to_write = {}


class Operation(enum.Enum):
    READ: int = enum.auto()
    WRITE: int = enum.auto()
    ERRORS: int = enum.auto()


def run_server() -> Generator:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", 6000))
    server_sock.listen()

    while True:
        yield Operation.READ, server_sock
        client_sock, address = server_sock.accept()  # read
        print("Connected by", address)
        tasks.append(accept_message(client_sock))


def accept_message(client_sock) -> Generator:
    while True:
        yield Operation.READ, client_sock
        request = client_sock.recv(1024)  # read
        if request:
            print(request)
            response = b"Hello World!"
            yield Operation.WRITE, client_sock  # write
            client_sock.sendall(response)
        else:
            break

    client_sock.close()


def event_loop() -> None:
    while True:
        while any([tasks, to_read, to_write]):
            while tasks:
                task = tasks.pop(0)
                try:
                    operation, sock = next(task)
                    match operation:
                        case Operation.READ:
                            to_read[sock] = task
                        case Operation.WRITE:
                            to_write[sock] = task
                        case _:
                            raise SystemError
                except StopIteration:
                    pass

            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))



if __name__ == "__main__":
    tasks.append(run_server())
    event_loop()
