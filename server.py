import socket
import random
import secrets


import socket
import random

# Prime number and generator used for Diffie-Hellman
p = 23  # A prime number
g = 5  # A primitive root modulo p


def hkdf(shared_key: int) -> str:
    return secrets.token_hex(32)


def dh_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8080))
    server_socket.listen(1)
    print("Server is listening for connections...")

    conn, addr = server_socket.accept()
    print(f"Connection from: {addr}")

    # Server's private key
    server_private = random.randint(1, p - 1)
    print(f"Server private key: {server_private}")

    # Server computes public key to send to client
    server_public = pow(g, server_private, p)
    print(f"Server public key: {server_public}")

    # Send public key to client
    conn.send(str(server_public).encode())

    # Receive client's public key
    client_public = int(conn.recv(1024).decode())
    print(f"Received client public key: {client_public}")

    # Compute shared secret key
    shared_secret = pow(client_public, server_private, p)
    print(f"Shared secret key (Server): {shared_secret}")

    conn.close()
    server_socket.close()


if __name__ == "__main__":
    print(f"Server started at: {socket.gethostbyname(socket.gethostname())}")
    dh_server()
