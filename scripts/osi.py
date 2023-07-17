# OSI MODEL                            PYTHON/NODE.JS APPLICATION PERSPECTIVE
# --------------------------------------------------------------------------------
# 7 | Application Layer      <----->   Python/Node.js APIs (HTTP, HTTPS, FTP etc)
# 6 | Presentation Layer     <----->   Data Format (JSON, XML etc)
# 5 | Session Layer          <----->   State Management, Connection Handling
# -------------------------------------------------------
# 4 | Transport Layer        <----->   Managed by OS (TCP, UDP)
# 3 | Network Layer          <----->   Managed by OS (IP, ICMP etc)
# 2 | Data Link Layer        <----->   Managed by OS / Hardware
# 1 | Physical Layer         <----->   Managed by Hardware (Ethernet, Wi-Fi)

import http.server
import socketserver

html = """
<html>
<body>
    <h1>Hello World!</h1>
    <p>This is a simple website</p>
</body>
</html>
"""


# Application Layer: Python's built-in http.server provides high-level API for HTTP
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Presentation Layer: The data sent and received by the server is formatted as HTTP (a text-based protocol)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Respond with a simple HTML document
        self.wfile.write(bytes(html, "utf-8"))


# Transport Layer: Python's built-in socketserver provides the TCPServer class to handle TCP connections
with socketserver.TCPServer(("localhost", 8000), MyHttpRequestHandler) as httpd:
    # Session Layer: serve_forever starts the server and keeps the connection open
    print("serving at port", 8000)
    httpd.serve_forever()

# Network, Data Link, and Physical Layers are handled by the operating system and network hardware
# The Python program just sends and receives data as streams of bytes, without worrying about lower level details
