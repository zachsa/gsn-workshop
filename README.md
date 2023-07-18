# gsn-workshop
HTTP is the language of the web - a formally defined protocol for exchanging web pages, files and other information across dispersed IT infrastructure. This workshop - "How do these tools work and why" - discusses HTTP in the context of accessing 3rd party data programmatically using Python and similar tools, and how to ask ChatGPT to generate such code for you (but doesn't touch on whether that's a good idea or not).


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Initial setup](#initial-setup)
- [HTTP and the TCP/IP internet stack](#http-and-the-tcpip-internet-stack)
  - [The OSI model](#the-osi-model)
    - [A simple Python web server (HTML over HTTP)](#a-simple-python-web-server-html-over-http)
  - [The TCP/IP model](#the-tcpip-model)
    - [A simple Python TCP server](#a-simple-python-tcp-server)
  - [What content is available via HTTP?](#what-content-is-available-via-http)
- [HTTP](#http)
  - [The `cURL` HTTP client](#the-curl-http-client)
  - [A Python HTTP client](#a-python-http-client)
- [Dependency management](#dependency-management)
- [Serverless website deployment (GitHub Pages)](#serverless-website-deployment-github-pages)
  - [Let's generate some data](#lets-generate-some-data)
  - [A quick website](#a-quick-website)
  - [Deploy it!](#deploy-it)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Resources
- **_[The SAEON Data Portal](https://catalogue.saeon.ac.za)_**: Search and download SAEON's curated datasets
- **_[Mnemosyne](https://mnemosyne.saeon.ac.za)_**: HTTP file server

# Initial setup
This tutorial assumes `cURL` and `Python 3.10.6` (other versions will likely work) is available on your PC. In addition, please install the following
```sh
sudo apt update

# Install jq, a JSON wrangler
sudo apt install jq -y

# Install Python libs
pip install requests
pip install aiohttp
```

# HTTP and the TCP/IP internet stack
I was taught to think of web development in terms of layers, with each layer an abstraction over various parts of the software and physical components of web-related infrastructure. Basically, it's nice to think in terms of models to represent how information is transferred between computers.

## The OSI model

```txt
          OSI MODEL                       PYTHON/NODE.JS APPLICATION PERSPECTIVE
          ---------                       ------------------------------------
7 | Application Layer      <----->   Python/Node.js APIs (HTTP, HTTPS, FTP etc)
6 | Presentation Layer     <----->   Data Format (JSON, XML etc)
5 | Session Layer          <----->   State Management, Connection Handling
-------------------------------------------------------
4 | Transport Layer        <----->   Managed by OS (TCP, UDP)
3 | Network Layer          <----->   Managed by OS (IP, ICMP etc)
2 | Data Link Layer        <----->   Managed by OS / Hardware
1 | Physical Layer         <----->   Managed by Hardware (Ethernet, Wi-Fi)
```

### A simple Python web server (HTML over HTTP)
[scripts/osi.py](scripts/osi.py)
```Python
import http.server
import socketserver

# Application Layer: Python's built-in http.server provides high-level API for HTTP
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Presentation Layer: The data sent and received by the server is formatted as HTTP (a text-based protocol)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Hello World!", "utf-8"))  # We are responding with simple text message

# Transport Layer: Python's built-in socketserver provides the TCPServer class to handle TCP connections
with socketserver.TCPServer(("localhost", 8000), MyHttpRequestHandler) as httpd:
    # Session Layer: serve_forever starts the server and keeps the connection open
    print("serving at port", 8000)
    httpd.serve_forever()

# Network, Data Link, and Physical Layers are handled by the operating system and network hardware
# The Python program just sends and receives data as streams of bytes, without worrying about lower level details
```

## The TCP/IP model
More specific to a typical website, which is implemented using the TCP transport protocol, there is the `TCP/IP model`:

```txt
TCP/IP MODEL                    PYTHON/NODE.JS APPLICATION PERSPECTIVE
-------------                   ------------------------------------
Application Layer   <----->    Python/Node.js APIs (HTTP, HTTPS, FTP etc)
Transport Layer     <----->    Managed by OS (TCP, UDP)
Internet Layer      <----->    Managed by OS (IP)
Network Interface   <----->    Managed by OS / Hardware (Ethernet, Wi-Fi)
```

### A simple Python TCP server
[scripts/tcp_ip.py](scripts/tcp_ip.py)
```Python
import socket

# Application Layer: Python's built-in socket module provides a high-level API for TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Network Interface Layer: Bind the socket to a specific network interface and port
server_address = ('localhost', 12345)
print('Starting up server on {} port {}'.format(*server_address))
server_socket.bind(server_address)

# Transport Layer: Listen for incoming connections (TCP provides reliable, ordered and error-checked delivery of a stream of bytes)
server_socket.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()

    try:
        print('Connection from', client_address)

        # Application Layer: Receive and send data over the connection
        while True:
            data = client_socket.recv(16)
            print('Received {!r}'.format(data))
            if data:
                print('Sending data back to the client...')
                client_socket.sendall(data)
            else:
                print('No more data from', client_address)
                break

    finally:
        # Clean up the connection
        client_socket.close()

# Internet Layer: The details of routing data across the network are handled by the OS and are abstracted away by the socket API
```

This example, unlike the server above, does not include the HTTP application layer. As such going to http://localhost:1234 will not work as browsers and other HTTP clients are tools for navigating **_content/resources_** such as served over application layer protocols (`http(s)`/`WebSockets`/`WebRTC`), and don't directly handle how that content is transferred. And that is the context of this tutorial - **_consuming content over HTTP_**.

## What content is available via HTTP?
`WebRTC`/`Websockets` are the basis for realtime communication / video conferencing / chat applications (i.e. WhatsApp). In terms of downloading files, the HTTP(S) protocol is dominant (actually... FTP and other protocols are also applicable here but I don't know much about these). Here are some of the types of content accessed/transferred over HTTP:

- HTML Documents
- CSS Stylesheets
- JavaScript Files
- Images
- Videos and Audio
- API Requests: including REST, GraphQL, ODATA, SOAP, and other formats
- Form data (like a contact or login form)
- Many other Media and Files (hundreds or thousands of different types of files and formats)

# HTTP
Let's ask an HTTP file server for a file listing (using the address https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307):

```txt
+------------------------------------------------------+
| Dear File Server,                                    |
|                                                      |
| I would like to request the file list from your      |
| server located at:                                   |
|                                                      |
|    mnemosyne.somisana.ac.za                          |
|                                                      |
| The specific file I'm interested in is available at: |
|                                                      |
|    /somisana/algoa-bay/5-day-forecast/202307         |
|                                                      |
| I kindly request you to provide the file to me.      |
|                                                      |
| Please ensure the response is in JSON format.        |
|                                                      |
| Thank you!                                           |
+------------------------------------------------------+
```

And slightly more technical:

```txt
+-------------------------------------------------------+
| Dear File Server.                                     |
|                                                       |
| I want to "GET" your file list from the Host          |
|    mnemosyne.somisana.ac.za                           |
| At the path:                                          |
|   /somisana/algoa-bay/5-day-forecast/202307 HTTP/1.1| |
|                                                       |
| Not the following!                                    |
|   User-Agent: Mozilla/5.0                             |
|   Accept-Language: en-US,en;q=0.9                     |
|   Accept: application/json                            |
|                                                       |
| LETTER CONTENT (BODY)                                 |
| ... You shouldn't need more information than above    |
+-------------------------------------------------------+
```

And actually in HTTP speak (the left column is byte offset):

```txt
+-------------------------------------------------------+
| POSTMARK (START LINE)                                 |
| GET /somisana/algoa-bay/5-day-forecast/202307 HTTP/1.1|
| Host: mnemosyne.somisana.ac.za                        |
|                                                       |
| ENVELOPE (HEADERS)                                    |
| User-Agent: Mozilla/5.0                               |
| Accept-Language: en-US,en;q=0.9                       |
| Accept: application/json                              |
|                                                       |
| LETTER CONTENT (BODY)                                 |
|                                                       |
|                                                       |
+-------------------------------------------------------+
```

## The `cURL` HTTP client
This command via `cURL` looks like this (piped to `jq` to prettify the output):

**_(1) Get a file listing_**

```sh
# PROMPT
# Give me a cURL command that makes a request to https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307, specifying the HTTP header "Accept: Application/json", and make the result (which is JSON) readable. Format the cURL command over multiple lines to make it easier to read using jq.

# CMD
curl \
  --silent \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
    | jq
```

**_(2) Let's only look at the tier3 files_**
```sh
# PROMPT
#That command outputs an array of objects, each of which looks something like this: {"parent": "/somisana/algoa-bay/5-day-forecast", "path": "/somisana/algoa-bay/5-day-forecast/202307/20230712-hourly-avg-t3.nc", "v": 1, "entry": "20230712-hourly-avg-t3.nc", "isFile": true, "isDirectory": false, "size": 1054370784}. Extend the command to filter the output to only include objects where the entry ends with the string "-t3.nc", and output the "path" value of each object, prefixed with the hostname of the request

curl \
  --silent \
  -X GET \
  -H "Accept: application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
    | jq -r '.[] | select(.entry | endswith("-t3.nc")) | .path' \
    | sed "s|^|https://mnemosyne.somisana.ac.za|"
```

**_(3) Now download the list of files to output/*-t3.nc_**
```sh
# PROMPT
# Extend that command so that the output is used as input to another cURL command that downloads each file to a directory called "output/" (which should be created if it doesn't exist or recreated if it does)

# CMD
mkdir -p output && rm -rf output/* \
&& curl \
  --silent \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
  | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za\(.path)"' \
  | while read url; do curl --progress-bar -o output/$(basename "$url") "$url"; done
```

**_(4) Speed up the process by downloading the files concurrently_**
```sh
# PROMPT
# Adjust that command to download the files concurrently 

mkdir -p output && rm -rf output/* \
&& curl \
  --silent \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
  | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za\(.path)"' \
  | xargs -P 10 -I {} sh -c 'curl --silent -o output/$(basename {}) {}'
```

But... the logging is poor in this case (I added the `--silent` flag to suppress it) and it's actually necessary to queue downloads. And while I'm sure that there is some bash command configuration that allows for this, I think it's time to move to a scripting environment such as Python/Node.js/Ruby/C#/Java/Go/Rust/Erlang/C/or any one of a very large number of options.

## A Python HTTP client
As a base, let's convert the previous `cURL` command for retrieving a file listing into a Python script. Here is the prompt:

> Convert this curl command into a Python function: curl --silent -X GET -H "Accept: application/json" https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 | jq -r '.[] | select(.entry | endswith("-t3.nc")) | .path' | sed "s|^|https://mnemosyne.somisana.ac.za|"

ChatGPT suggests a reasonable function (in my case at least), that I've called [`get_filepaths`](/scripts/get_filepaths.py). To execute it, you first need to install the requests library:

```sh
python scripts/get_filepaths.py
```

The [requests](https://pypi.org/project/requests/) library is not part of the std lib, but is a fairly popular HTTP client for Python.

**_(1) Download each file synchronously_**
The easiest way to download files in Python is one at a time! Let's ask ChatGPT to give us a function that does that. Here is the prompt:

> In Python, given an array of URLs (that point to files), give me a function that will download each file to output/ (use the filename in the URL). First delete and recreate the output/ directory when running the function.

Execute [scripts/synchronous_download.py](/scripts/synchronous_download.py) with the command:

```sh
python scripts/synchronous_download.py
```

**_(2) Download files concurrently_**
Downloading several large files one at a time is quite slow - we can greatly improve this by working concurrently. Here is the prompt:

> Adjust the following script to download all the files asynchronously using asyncio and aiohttp:
> (and then copy/paste the contents of [/scripts/synchronous_download.py](/scripts/synchronous_download.py))

Execute [scripts/async_download.py](/scripts/async_download.py) with the command:

```sh
python scripts/async_download.py
```

**_(3) Add queuing to configure max-concurrent requests_**
Downloading files concurrently is fast, but trying to download too many files at once will not work for a variety of reasons. Many data providers (such as NOAA) rate-limit by IP and if you exceed that you get blocked and can no longer download data. Let's avoid that; here is the prompt:

> Adjust the following script to implement queuing using the asyncio library:
> (and copy/paste the contents of [/scripts/async_download.py](/scripts/async_download.py))

Execute [scripts/async_with_queue.py](/scripts/async_with_queue.py) with the command:

```sh
python scripts/async_with_queue.py
```

And that's that!

# Dependency management
GitHub / GitLab, and other platforms provide free/shared task executors in the form of ephemeral virtual machines. These products are a natural fit for running Python code programmatically / on a scheduled basis as part of automated workflows, provided that works best when Python scripts are packages in such a way as to be portable. This requires that dependencies are managed explicitly - good practice even without the requirement of portable deployments, as (in my opinion) this leads to better-structured code.
 
# Serverless website deployment ([GitHub Pages](https://pages.github.com/))

## Let's generate some data
Let's get some data from one of the downloads to display in a website chart.

## A quick website


## Deploy it!


