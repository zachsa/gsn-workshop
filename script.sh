#!/bin/bash

mkdir -p output

while IFS= read -r url; do
  filename=$(basename "$url")
  curl -o "output/$filename" "$url"
done < files.txt