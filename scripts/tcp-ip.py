# TCP/IP MODEL                    PYTHON/NODE.JS APPLICATION PERSPECTIVE
# -------------                   ------------------------------------
# Application Layer   <----->    Python/Node.js APIs (HTTP, HTTPS, FTP etc)
# Transport Layer     <----->    Managed by OS (TCP, UDP)
# Internet Layer      <----->    Managed by OS (IP)
# Network Interface   <----->    Managed by OS / Hardware (Ethernet, Wi-Fi)

import socket

# Application Layer: Python's built-in socket module provides a high-level API for TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Network Interface Layer: Bind the socket to a specific network interface and port
server_address = ("localhost", 12345)
print("Starting up server on {} port {}".format(*server_address))
server_socket.bind(server_address)

# Transport Layer: Listen for incoming connections (TCP provides reliable, ordered and error-checked delivery of a stream of bytes)
server_socket.listen(1)

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()

    try:
        print("Connection from", client_address)

        # Application Layer: Receive and send data over the connection
        while True:
            data = client_socket.recv(16)
            print("Received {!r}".format(data))
            if data:
                print("Sending data back to the client...")
                client_socket.sendall(data)
            else:
                print("No more data from", client_address)
                break

    finally:
        # Clean up the connection
        client_socket.close()

# Internet Layer: The details of routing data across the network are handled by the OS and are abstracted away by the socket API
