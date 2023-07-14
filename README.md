# gsn-workshop
HTTP is the language of the web - a formally defined protocol for exchanging web pages, files and other information across dispersed IT infrastructure. This workshop - "How do these tools work and why" - discusses HTTP in the context of accessing 3rd party data programmatically using Python and similar tools, and how to ask ChatGPT to generate such code for you (but doesn't touch on whether that's a good idea or not).


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [HTTP and the TCP/IP internet stack](#http-and-the-tcpip-internet-stack)
- [Downloading files](#downloading-files)
  - [cURL](#curl)
  - [requests](#requests)
  - [Concurrent requests](#concurrent-requests)
  - [Rate-limited concurrent requests](#rate-limited-concurrent-requests)
  - [Async file IO and atomicity](#async-file-io-and-atomicity)
- [Dependency management](#dependency-management)
- [Serverless website deployment (GitHub Pages)](#serverless-website-deployment-github-pages)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



# HTTP and the TCP/IP internet stack

# Downloading files

## cURL

### Look at the raw output
> Give me a cURL command that makes a request to https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307, specifying the HTTP header "Accept: Application/json", and make the result (which is JSON) readable:


### Get a list of tier3 files 

```
Give me a cURL command that makes a request to https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307, specifying the HTTP header "Accept: Application/json". The result is an array of objects, each of which looks something like this:

{
    "parent": "/somisana/algoa-bay/5-day-forecast",
    "path": "/somisana/algoa-bay/5-day-forecast/202307/20230714-hourly-avg-t3.nc",
    "v": 1,
    "entry": "20230714-hourly-avg-t3.nc",
    "isFile": true,
    "isDirectory": false,
    "size": 1054370784
}

Filter out objects where the "entry" key, which is a filename, ends with "*-t3.nc". Output a list of files using the "path" key prefixed with "https://mnemosyne.somisana.ac.za" to "files.txt". The "path" key includes the filename, which shouldn't be repeated.

curl -H "Accept: application/json" https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307 | jq -r '.[] | select(.entry | endswith("-t3.nc")) | "https://mnemosyne.somisana.ac.za" + .path' > files.txt

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