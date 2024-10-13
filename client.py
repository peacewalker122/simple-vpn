import socket
import random


# Prime number and generator used for Diffie-Hellman
p = 23  # A prime number
g = 5  # A primitive root modulo p


def dh_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 8080))

    # Receive server's public key
    server_public = int(client_socket.recv(1024).decode())
    print(f"Received server public key: {server_public}")

    # Client's private key
    client_private = random.randint(1, p - 1)
    print(f"Client private key: {client_private}")

    # Client computes public key to send to server
    client_public = pow(g, client_private, p)
    print(f"Client public key: {client_public}")

    # Send public key to server
    client_socket.send(str(client_public).encode())

    # Compute shared secret key
    shared_secret = pow(server_public, client_private, p)
    print(f"Shared secret key (Client): {shared_secret}")

    client_socket.close()


if __name__ == "__main__":
    dh_client()
