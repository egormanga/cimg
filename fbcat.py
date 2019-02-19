#!/usr/bin/python3
# Write image to framebuffer

import os, sys, requests
from cimg import *
from utils import *; logstart('fbcat')

def write(fb, img, size):
	fb = open(fb, 'wb', buffering=-1)#2**31-1)
	img = openimg(img)
	img.thumbnail(size)
	scr = Image.new('RGB', size)
	scr.paste(img, (abs(img.size[0]-size[0])//2, 0))
	data = scr.tobytes()
	for i in range(len(data)//3): fb.write(bytes(data[i:i+4:-1])+b'\0')

def main():
	argparser.add_argument('fb', metavar='<fb>')
	argparser.add_argument('res', metavar='<res>')
	argparser.add_argument('img', metavar='<img>')
	cargs = argparser.parse_args()
	write(cargs.fb, cargs.img, tuple(map(int, cargs.res.split('x'))))

if (__name__ == '__main__'): logstarted(); main()
else: logimported()
