import os
import fcntl
import struct
import subprocess
import select

# Constants
TUNSETIFF = 0x400454CA
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

try:
    # Open TUN device file
    tun = open("/dev/net/tun", "r+b", buffering=0)
except FileNotFoundError:
    print("Error: /dev/net/tun not found. Please ensure the TUN module is loaded.")
    exit(1)

# Prepare ioctl request
ifr = struct.pack("16sH", b"tun0", IFF_TUN | IFF_NO_PI)

try:
    # Configure TUN interface
    fcntl.ioctl(tun, TUNSETIFF, ifr)
except OSError as e:
    print(f"Error configuring TUN interface: {e}")
    exit(1)

# Get interface name
ifname = struct.unpack("16sH", ifr)[0].strip(b"\x00").decode("utf-8")

print(f"TUN interface {ifname} created")

# Configure IP address for the interface
subprocess.run(["ip", "addr", "add", "10.0.0.1/24", "dev", ifname])
subprocess.run(["ip", "link", "set", "dev", ifname, "up"])

print(f"Configured {ifname} with IP 10.0.0.1/24")

# Simple packet handling loop
while True:
    ready, _, _ = select.select([tun], [], [], 1)
    if ready:
        packet = os.read(tun.fileno(), 2048)
        print(f"Received packet: {packet.hex()}")
        # For demonstration, we're just echoing the packet back
        os.write(tun.fileno(), packet)
