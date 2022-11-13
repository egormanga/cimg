#!/bin/sh

SIZE=1920x1080

exec convert -resize "$SIZE" -background black -gravity center -extent "$SIZE" "$1" bgra:'/dev/fb0'
