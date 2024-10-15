import os
import fcntl
import struct
import subprocess
import select
import logging
import socket
import threading

# Constants
TUNSETIFF = 0x400454CA
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# Logger setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def configure_tun_interface(
    tun, ifname="tun0", ip_addr="10.0.0.1", netmask="255.255.255.0"
):
    # Prepare ioctl request to create the interface
    ifr = struct.pack("16sH", ifname.encode("utf-8"), IFF_TUN | IFF_NO_PI)
    try:
        fcntl.ioctl(tun, TUNSETIFF, ifr)
        logging.info(f"TUN interface {ifname} created")
    except OSError as e:
        logging.error(f"Error configuring TUN interface: {e}")
        exit(1)

    # Set IP address and bring interface up
    try:
        subprocess.run(
            ["ip", "addr", "add", f"{ip_addr}/24", "dev", ifname], check=True
        )
        subprocess.run(["ip", "link", "set", "dev", ifname, "up"], check=True)
        logging.info(f"Configured {ifname} with IP {ip_addr}/24")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to configure IP address or bring up {ifname}: {e}")
        exit(1)


def handle_packet(tun):
    while True:
        ready, _, _ = select.select([tun], [], [], 1)
        if ready:
            try:
                packet = os.read(tun.fileno(), 2048)
                logging.info(f"Received packet: {packet.hex()}")

                # Parse packet (for example, handle IP header)
                # For demonstration, we just echo the packet back
                os.write(tun.fileno(), packet)
                logging.info(f"Echoed packet back to the interface")
            except OSError as e:
                logging.error(f"Error handling packet: {e}")


def forward_packet_to_network(packet, dest_ip="8.8.8.8", dest_port=53):
    """
    Example function to forward packet to a real network (e.g., DNS query).
    This is a simple UDP example; you can extend this to TCP or other protocols.
    """
    try:
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(packet, (dest_ip, dest_port))
            logging.info(f"Forwarded packet to {dest_ip}:{dest_port}")
    except socket.error as e:
        logging.error(f"Failed to forward packet: {e}")


def start_tun_server(ifname="tun0", ip_addr="10.0.0.1"):
    # Open TUN device file
    try:
        tun = open("/dev/net/tun", "r+b", buffering=0)
    except FileNotFoundError:
        logging.error(
            "Error: /dev/net/tun not found. Please ensure the TUN module is loaded."
        )
        exit(1)

    # Configure TUN interface
    configure_tun_interface(tun, ifname, ip_addr)

    # Start packet handling thread
    packet_handler_thread = threading.Thread(target=handle_packet, args=(tun,))
    packet_handler_thread.start()

    # Wait for the thread to finish (it runs indefinitely)
    packet_handler_thread.join()


if __name__ == "__main__":
    # Example usage: you can configure the interface name and IP
    start_tun_server(ifname="tun0", ip_addr="10.0.0.1")
