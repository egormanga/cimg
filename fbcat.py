#!/usr/bin/python3
# Write image to framebuffer

from utils import *
from . import *

@export
def fbwrite(fb, img, size):
	img = openimg(img)
	img.thumbnail(size)

	scr = Image.new('RGB', size)
	scr.paste(img, (abs(img.size[0]-size[0])//2, 0))
	data = scr.tobytes()

	with open(fb, 'wb', buffering=-1) as fb: #2**31-1)
		for i in range(len(data)//3):
			fb.write(bytes(data[i:i+4:-1]) + b'\0')

@apmain
@aparg('fb', metavar='<fb>')
@aparg('res', metavar='<res>')
@aparg('img', metavar='<img>')
def main(cargs):
	fbwrite(cargs.fb, cargs.img, tuple(map(int, cargs.res.split('x'))))

if (__name__ == '__main__'): exit(main())

# by Sdore, 2018-22
#   www.sdore.me
