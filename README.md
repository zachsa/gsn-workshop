# gsn-workshop
HTTP is the language of the web - a formally defined protocol for exchanging web pages, files and other information across dispersed IT infrastructure. This workshop - "How do these tools work and why" - discusses HTTP in the context of accessing 3rd party data programmatically using Python and similar tools, and how to ask ChatGPT to generate such code for you (but doesn't touch on whether that's a good idea or not).


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [HTTP and the TCP/IP internet stack](#http-and-the-tcpip-internet-stack)
- [cURL-based download workflow](#curl-based-download-workflow)
    - [Now download each of these in turn](#now-download-each-of-these-in-turn)
  - [requests](#requests)
  - [Concurrent requests](#concurrent-requests)
  - [Rate-limited concurrent requests](#rate-limited-concurrent-requests)
  - [Async file IO and atomicity](#async-file-io-and-atomicity)
- [Dependency management](#dependency-management)
- [Serverless website deployment (GitHub Pages)](#serverless-website-deployment-github-pages)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# HTTP and the TCP/IP internet stack
`cURL` (Client for URLs) is an HTTP client for POSIX systems. Most Linux OSes have this installed by default. In addition, the following software is required for this workshop:

- Python v3.10.6 (similar versions will probably work fine)
- `jq`, a lightweight JSON processor (`sudo apt update && sudo apt install jq -y`)

# cURL-based download workflow
**_(1) Get a file listing_**
> Give me a cURL command that makes a request to https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307, specifying the HTTP header "Accept: Application/json", and make the result (which is JSON) readable
>
>Format the cURL command over multiple lines to make it easier to read.

```sh
curl \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
    | jq
```

**_(2) Let's only look at the tier3 files_**
>That command outputs an array of objects, each of which looks something like this:
>
> {
  "parent": "/somisana/algoa-bay/5-day-forecast",
  "path": "/somisana/algoa-bay/5-day-forecast/202307/20230712-hourly-avg-t3.nc",
  "v": 1,
  "entry": "20230712-hourly-avg-t3.nc",
  "isFile": true,
  "isDirectory": false,
  "size": 1054370784
}
>
>Extend the command to filter the output to only include objects where the entry ends with the string "-t3.nc", and output the "path" value of each object, prefixed with the base URL, to a line in a file called "files.txt"

```sh
curl \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
    | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za\(.path)"' \
      > files.txt
```

**_(3) Now download the list of files to output/*-t3.nc_**
>Extend that command so that the output is used as input to another cURL command that downloads each file to output/ (which should be created if it doesn't exist or recreated if it does):

```sh
mkdir -p output && rm -rf output/* \
&& curl \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
  | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za\(.path)"' \
  | while read url; do curl -o output/$(basename "$url") "$url"; done
```

**_(3.1) Speed up the process by downloading the files concurrently_**
>Adjust that command to download the files concurrently

```sh
mkdir -p output && rm -rf output/* \
&& curl \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
  | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za\(.path)"' \
  | while read url; do (curl -o output/$(basename "$url") "$url" &); done; wait
```

**_(3.2) Limit the number of concurrent downloads_**
>Limit the number of concurrent downloads to be 4 at a time:

```sh
mkdir -p output && rm -rf output/* \
&& curl \
  -X GET \
  -H "Accept: Application/json" \
  https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 \
  | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za\(.path)"' \
  | xargs -n 1 -P 4 -I {} bash -c 'curl -o output/$(basename "{}") "{}"'
```

### Now download each of these in turn

> Now give me a shell script that will loop over the files.txt lines, and download each to "output/"


## [requests](https://pypi.org/project/requests/)

## Concurrent requests

## Rate-limited concurrent requests

## Async file IO and atomicity

# Dependency management
GitHub / GitLab, and other platforms provide free/shared task executors in the form of ephemeral virtual machines. These products are a natural fit for running Python code programmatically / on a scheduled basis as part of automated workflows, provided that works best when Python scripts are packages in such a way as to be portable. This requires that dependencies are managed explicitly - good practice even without the requirement of portable deployments, as (in my opinion) this leads to better-structured code.
 
# Serverless website deployment ([GitHub Pages](https://pages.github.com/))
Discuss what a website is in the context of HTML, and what that means in terms of the ability to quickly setup websites.