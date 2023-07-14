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

## [requests](https://pypi.org/project/requests/)

## Concurrent requests

## Rate-limited concurrent requests

## Async file IO and atomicity

# Dependency management
GitHub / GitLab, and other platforms provide free/shared task executors in the form of ephemeral virtual machines. These products are a natural fit for running Python code programmatically / on a scheduled basis as part of automated workflows, provided that works best when Python scripts are packages in such a way as to be portable. This requires that dependencies are managed explicitly - good practice even without the requirement of portable deployments, as (in my opinion) this leads to better-structured code.
 
# Serverless website deployment ([GitHub Pages](https://pages.github.com/))
Discuss what a website is in the context of HTML, and what that means in terms of the ability to quickly setup websites.