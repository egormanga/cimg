#SIZE=1920x1080
SIZE=1376x768
convert -resize $SIZE -background black -gravity center -extent $SIZE $1 bgra:/dev/fb0
