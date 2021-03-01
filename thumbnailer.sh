#!/bin/bash

start=$SECONDS
f=$1
hash=$(echo -n "$1" | sha256sum | awk '{print $1}')
path="/root/pydirlist/pydirlist/static/.thumbnails/"

for s in 1600 720; do
   echo Reducing $f to ${s}x${s}
   convert "$f" -resize ${s}x${s} $path$hash-$s.jpg
   echo "$path$hash-$s.jpg"
done
for s in 150; do
   echo Reducing $f to ${s}x${s}
   convert "$f" -resize "${s}x${s}^" -gravity center -crop ${s}x${s}+0+0 +repage $path$hash-$s.jpg
   echo "$path$hash-$s.jpg"
done

echo Time: $((SECONDS-start))
