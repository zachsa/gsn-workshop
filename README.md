# HTTP Party: A Quirky Adventure in Data Retrieval with cURL and Python
When it comes to accessing data over the web programmatically, most data providers, including those I've encountered while working at SAEON, serve their content over the HTTP protocol. HTTP, the language of the web, is a formally defined protocol for exchanging web pages, files, and other information across dispersed IT infrastructure.

In the workshop "HTTP Party: A Quirky Adventure in Data Retrieval with cURL and Python", HTTP is explained in the context of accessing third-party data programmatically using Python and similar tools. We explore how to effectively download files from HTTP file servers and provide guidance on leveraging HTTP to retrieve data.

Join us for a comprehensive (but quick!) walkthrough of HTTP, learn valuable techniques for programmatically accessing data, and explore the potential of leveraging tools like ChatGPT to generate code tailored to your needs. Whether you are a data enthusiast, developer, or researcher, this workshop equips you with practical knowledge and some useful code snippets as a future reference.


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Resources](#resources)
- [Initial setup](#initial-setup)
- [HTTP and the TCP/IP internet stack](#http-and-the-tcpip-internet-stack)
    - [The TCP/IP model](#the-tcpip-model)
- [HTTP clients](#http-clients)
  - [The `cURL` HTTP client](#the-curl-http-client)
  - [A Python HTTP client](#a-python-http-client)
- [Dependency management](#dependency-management)
  - [Containerization](#containerization)
- [And that's a wrap](#and-thats-a-wrap)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Resources
- **_[This tutorial](https://github.com/zachsa/gsn-workshop)_** You are welcome to save/fork this repository for future reference
- **_[The SAEON Data Portal](https://catalogue.saeon.ac.za)_** Search and download SAEON's curated datasets
- **_[Mnemosyne](https://mnemosyne.saeon.ac.za)_** HTTP file server

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
I was taught to think of web development in terms of layers, with each layer an abstraction over various parts of the software and physical components of web-related infrastructure. Basically, it's nice to think in terms of models to represent how information is transferred between computers. One such model is the Open Systems Interconnection (OSI) model:

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

Translating the abstract layers of models like the OSI model or the TCP/IP stack into concrete code can be challenging, given the conceptual nature of these layers and the less defined boundaries within actual code implementation. By annotating lines of code with comments that map to these theoretical layers, we can gain a clearer understanding of how a high-level language like Python fits into the OSI framework. Here's an example of a web server, generated by ChatGPT, that contextualizes Python's role within the OSI model:

```Python
# PROMPT
# Please provide a simple Python web server example using the built-in http.server and socketserver modules that illustrates which layers of the OSI model Python can interact with? Please include comments in the code that explain which OSI layer each part of the code corresponds to. The application layer protocol should be HTTP and respond with a simple "Hello world"

import http.server
import socketserver


# Layer 7 - Application Layer: Python's built-in http.server module provides a high-level API for HTTP
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Layer 6 - Presentation Layer: The data sent and received by the server is formatted as HTTP, a text-based protocol
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Sending the HTTP response body. The HTTP response itself is a part of the Application Layer,
        # but the content type of the response is related to the Presentation Layer.
        self.wfile.write(
            bytes("Hello World!", "utf-8")
        )  # We are responding with a simple text message


# Layer 4 - Transport Layer: Python's built-in socketserver module provides the TCPServer class to handle TCP connections
with socketserver.TCPServer(("localhost", 8000), MyHttpRequestHandler) as httpd:
    # Layer 5 - Session Layer: serve_forever starts the server and keeps the connection open, managing the session
    print("Serving at port", 8000)
    httpd.serve_forever()

# Layers 3, 2, 1 - Network, Data Link, and Physical Layers: These are handled by the operating system and network hardware.
# The Python program just sends and receives data as streams of bytes, without worrying about these lower-level details.
```

(Run this code by copy/pasting to a file called `scripts/http_server`, and executing with the command `python scripts/http_server.py`)

This may seem pretty amazing - that ChatGPT can generate this working HTTP server along with code comments. However... this server will process requests one at a time and not concurrently, so it's not suitable for deploying as an application - but the limitations would only become obvious when there is more than a single concurrent user. ChatGPT **_could have_** provided a production-ready web server that handles requests concurrently if you know to ask for it (in other words.. ChatGPT doesn't replace you, it augments you).

```Python
# PROMPT
# Please provide a simple Python web server example using the built-in http.server and socketserver modules that illustrates which layers of the OSI model Python can interact with? Please include comments in the code that explain which OSI layer each part of the code corresponds to. The application layer protocol should be HTTP and respond with a simple "Hello world". Use the aiohttp library to implement the web server so that requests are handled concurrently
from aiohttp import web


# Layer 7 - Application Layer: aiohttp provides high-level API for HTTP
async def handle(request):
    # Layer 6 - Presentation Layer: The data sent and received by the server is formatted as HTTP, a text-based protocol
    return web.Response(
        text="Hello World!"
    )  # We are responding with a simple text message


app = web.Application()
# The route we are setting up here corresponds to the Session Layer
# Layer 5 - Session Layer: setting up route and handling HTTP GET method.
app.router.add_get("/", handle)

# Layer 4 - Transport Layer: The TCP transport is handled by the web.run_app function.
web.run_app(app, host="localhost", port=8000)

# Layers 3, 2, 1 - Network, Data Link, and Physical Layers: These are handled by the operating system and network hardware.
# The Python program just sends and receives data as streams of bytes, without worrying about these lower-level details.
```

### The TCP/IP model
When it comes to a typical website, which commonly uses the TCP transport protocol, we often refer to the TCP/IP model. This model serves as a more specific and streamlined framework compared to the broader OSI model:

```txt
TCP/IP MODEL                    PYTHON/NODE.JS APPLICATION PERSPECTIVE
-------------                   ------------------------------------
Application Layer   <----->    Python/Node.js APIs (HTTP, HTTPS, FTP etc)
Transport Layer     <----->    Managed by OS (TCP, UDP)
Internet Layer      <----->    Managed by OS (IP)
Network Interface   <----->    Managed by OS / Hardware (Ethernet, Wi-Fi)
```

We can ask ChatGPT to re-annotate the above web server within the context of this model - the code is the same, but the comments are different. In addition, let's ask ChatGPT to serve files identified via the HTTP path in the request to completely recreate the context of a 'file server' that we are going to download files from:

```Python
# PROMPT
# Please provide a simple Python web server example that illustrates which layers of the TCP/IP model Python can interact with? Please include comments in the code that explain which layer each part of the code corresponds to. The application layer protocol should be HTTP and respond with a file download located at the path specified by a user request (please stream the file back, don't load it into memory). Use the aiohttp library to implement the web server so that requests are handled concurrently.

from aiohttp import web
import os

# TCP/IP model:
# Layer 4: Application Layer - HTTP
# Layer 3: Transport Layer - TCP
# Layer 2: Internet Layer - IP
# Layer 1: Link Layer - Network Interface

# This script specifically interacts with Layer 4 (HTTP Application Layer) and Layer 3 (TCP Transport Layer)


async def file_download(request):
    # Here's where we interact with the Application Layer (Layer 4). We're using HTTP protocol here to parse incoming request
    filepath = request.match_info.get("filepath", "")

    # Check if the file exists
    if not os.path.isfile(filepath):
        return web.Response(text="File not found", status=404)

    # Open the file in binary mode, this doesn't load the file into memory
    file_stream = web.FileResponse(path=filepath)

    # Set the Content-Disposition header to "attachment" which prompts the browser to download the file
    file_stream.headers[
        "Content-Disposition"
    ] = f'attachment; filename="{os.path.basename(filepath)}"'

    # Respond with the file stream, the TCP (Transport Layer - Layer 3) will handle transmitting the data packets
    return file_stream


app = web.Application()
# Routing to handle file download requests
app.router.add_route("GET", "/{filepath:.*}", file_download)

if __name__ == "__main__":
    # Run the web application
    # The underlying library would open a TCP socket (Layer 3) and listen for incoming connections
    web.run_app(app, port=8080)
```

This code implements a file server that delivers content over HTTP. The type of content that is served is varied (HTTP is flexible in this regard). For example, on a day-to-day basis most people consume the following content over HTTP:

- HTML Documents
- CSS Stylesheets
- JavaScript Files
- Images
- Videos and Audio
- API Requests: including REST, GraphQL, ODATA, SOAP, and other formats
- Form data (like a contact or login form)
- Many other Media and Files (hundreds or thousands of different types of files and formats)

**_From the perspective of a file server, downloading a NetCDF file or downloading a website for viewing in a browser is conceptually similar. In both cases, the server receives a request for a specific file and responds by providing the requested content to the client. The underlying process of serving the files remains consistent regardless of the file type or the intended use._**

In the context of this workshop, here is a prompt that will more or less generate an equivalent to the Mnemosyne file server where we will fetch all our data from:

> Please provide a simple Python web server to respond to HTTP requests with a file download (as an attachment) located at the path specified by a user request. please stream the file back, don't load it into memory. Use the aiohttp library to implement the web server so that requests are handled concurrently.

# HTTP clients
During a recent conversation with a colleague, I inquired about his experience with sending letters by post. After pondering for a moment, he reminisced about his youth and mentioned sending a letter to his first girlfriend (he is 31).

It is likely that the analogy of equating an HTTP request to sending a letter via post may become less relatable. Perhaps a "Posting Letters 101" course could become a prerequisite for comprehending the foundations of HTTP. However, for now, the majority can still resonate with and value the comforting structure of a conventional letter:

```txt
+--------------------------------------------------+
|                         Your Name                |
|                         Your Address Line 1      |
|                         Your Address Line 2      |
|                         City, State, Postal Code |
|                                                  |
|                                                  |
| Date: DD/MM/YYYY                                 |
|                                                  |
|                                                  |
| Recipient's Name                                 |
| Recipient's Address Line 1                       |
| Recipient's Address Line 2                       |
| City, State, Postal Code                         |
|                                                  |
|                                                  |
| Dear Recipient's Name,                           |
|                                                  |
| Content of the letter goes here.                 |
|                                                  |
|                                                  |
| Sincerely,                                       |
|                                                  |
| Your Name                                        |
+--------------------------------------------------+
```

The terminology used to describe HTTP request/responses draws parallels with sending letters, including references to HTTP envelopes. Inspired by this correspondence theme, let's imagine sending a letter to Mnemosyne, the Greek goddess of memory and file systems — a fitting name for a contemporary file server. In Greek mythology, Mnemosyne held immense knowledge and was associated with the preservation of memories.

With this in mind, let's compose a letter to Mnemosyne, requesting a listing of SAEON's July's ocean modelling data:

```txt
+------------------------------------------------------+
| Dear Mnemosyne,                                      |
|                                                      |
| I would like to request July ocean data from your    |
| server located at:                                   |
|                                                      |
|    mnemosyne.somisana.ac.za                          |
|                                                      |
| You should be able to find this data at the path     |
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

And slightly more http-like/technical:

```txt
+-------------------------------------------------------+
| Dear Mnemosyne.                                       |
|                                                       |
| I would like to GET July ocean data from your server  |
| located at:                                           |
|    mnemosyne.somisana.ac.za                           |
|                                                       |
| At the PATH:                                          |
|   /somisana/algoa-bay/5-day-forecast/202307           |
|                                                       |
| Not the following!                                    |
|   User-Agent: Mozilla/5.0                             |
|   Accept-Language: en-US,en;q=0.9                     |
|   Accept: application/json                            |
|                                                       |
| LETTER CONTENT (BODY)                                 |
| NULL                                                  |
+-------------------------------------------------------+
```

And actually in HTTP speak:

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
| NULL                                                  |
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
# That command outputs an array of objects, each of which looks something like this: {"parent": "/somisana/algoa-bay/5-day-forecast", "path": "/somisana/algoa-bay/5-day-forecast/202307/20230712-hourly-avg-t3.nc", "v": 1, "entry": "20230712-hourly-avg-t3.nc", "isFile": true, "isDirectory": false, "size": 1054370784}. Extend the command to filter the output to only include objects where the entry ends with the string "-t3.nc", and output the "path" value of each object, prefixed with the hostname of the request

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

However, the output (logging) in this case is terrible, and I had to resort to using the --silent flag in the download command (second `curl` command) to suppress it. Additionally, the need to queue downloads has become apparent. While it's possible that configuring a bash command could address these concerns, the resulting code may become increasingly convoluted and challenging to comprehend.

I think it's advantageous to transition to a scripting environment like Python, Node.js, Ruby, C#, Java, Go, Rust, Erlang, C, or any of the numerous options available. These languages offer robust scripting capabilities and a wide range of libraries and frameworks, making it easier to address complex tasks while maintaining code readability and maintainability.

## A Python HTTP client
As a base, let's convert the previous `cURL` command for retrieving a file listing into a Python script. Here is the prompt:

```txt
Convert this curl command into a Python function: curl --silent -X GET -H "Accept: application/json" https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 | jq -r '.[] | select(.entry | endswith("-t3.nc")) | .path' | sed "s|^|https://mnemosyne.somisana.ac.za|"
```

ChatGPT suggests a reasonable function (in my case at least), that I've called [`mnemosyne`](/scripts/mnemosyne.py). To execute it, you first need to install the requests library:

```sh
python scripts/mnemosyne.py
```

The [requests](https://pypi.org/project/requests/) library is not part of the std lib, but is a fairly popular HTTP client for Python.

**_(1) Download each file synchronously_**

The easiest way to download files in Python is one at a time! Let's ask ChatGPT to give us a function that does that. Here is the prompt:

```txt
In Python, given an array of URLs (that point to files), give me a function that will download each file to output/ (use the filename in the URL). First delete and recreate the output/ directory when running the function.
```

Execute [scripts/download_sync.py](/scripts/download_sync.py) with the command:

```sh
python scripts/download_sync.py
```

**_(2) Download files concurrently_**

Downloading several large files one at a time is quite slow - we can greatly improve this by working concurrently. Here is the prompt:


> Adjust the following script to download all the files asynchronously using asyncio and aiohttp:
> (and then copy/paste the contents of [/scripts/download_sync.py](/scripts/download_sync.py))

Execute [scripts/download_async.py](/scripts/download_async.py) with the command:

```sh
python scripts/download_async.py
```

**_(3) Add queuing to configure max-concurrent requests_**

Downloading files concurrently is fast, but trying to download too many files at once will not work for a variety of reasons. Many data providers (such as NOAA) rate-limit by IP and if you exceed that you get blocked and can no longer download data. Let's avoid that; here is the prompt:

> Adjust the following script to implement queuing using the asyncio library:
> (and copy/paste the contents of [/scripts/download_async.py](/scripts/download_async.py))

Execute [scripts/download_async_queue.py](/scripts/download_async_queue.py) with the command:

```sh
python scripts/download_async_queue.py
```

And that's that!

# Dependency management
GitHub / GitLab, and other platforms provide free/shared task executors in the form of ephemeral virtual machines. These products are a natural fit for running Python code programmatically / on a scheduled basis as part of automated workflows, provided that works best when Python scripts are packages in such a way as to be portable. This requires that dependencies are managed explicitly - good practice even without the requirement of portable deployments, as (in my opinion) this leads to better-structured code.

In this repository, you can generate a list of dependencies using `pip freeze`:

```sh
pip freeze > requirements.txt

# or some variation thereof. For example:
pipenv run pip freeze > requirements.txt
```

Commit this file to the git index so that it's accessible in deployment/execution environments in the future. Then, on the server that you would like to execute your program (for example [script.py](/script.py)), first install dependencies listed in `requirements.txt` and then execute the program:

```sh
pip install -r requirements.txt
python script.py
```

## Containerization
Most operating systems come with Python installed. If a Python script makes use of 3rd party libraries or binaries that need to be prior-installed on a server there are a number of approaches to manage environments (instead of just Python dependencies). My favourite is via containerization (Docker).

Dockerize (and run) [script.py](/script.py) with the following commands:

```sh
# First update requirements.txt

# Then build and run the Docker image
docker build -t gsn-tut .
docker run --rm --name gsn gsn-tut
```
 
# And that's a wrap
Let me know if there are any questions! If there is still time, some ideas for next steps:

- Publish a repository as a website using GitHub pages. Yet another take on the typical HTTP file-serving stack, GitHub provides a mechanism for turning into repository into a beautiful website using [GitHub Pages](https://pages.github.com/). In this case your README.md file will either be formatted as a website (as is the case of this tutorial - https://zachsa.github.io/gsn-workshop/), or you can serve your own HTML / CSS / JS. Note that you can even assign your own domain name to a GitHub pages site!
- We could generate a website with charts using ChatGPT (and GitHub pages)
- We could look more into containerization Docker - how Docker works, and how to include it in GitHub Actions workflows


