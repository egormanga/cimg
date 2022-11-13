#!/usr/bin/env python3
# Python console image view library

from PIL import Image
from utils.nolog import *

export(Image)

@export
def showimg(img, size, chars='█', *, padding=0, padchar=' ', bgcolor=None, double_vres=False, resample=0): # ░▒▓█
	""" Render an Image.
	Parameters:
		img: PIL Image, Image.open arg or URL as str.
		size: (w, h) int tuple or single int to use as length of one or both sides of output.
		chars='█': multiple chars (e.g. '░▒▓█') to use as b/w palette or single (e.g. '█') for RGB (ANSI-escape) mode.
		padding=0: prefix every line with N `padchar`s.
		padchar=' ': character to use as left-padding.
		double_vres=False: double the vertical size and use bg color as the bottom pixel for half-block chars (e.g. '▀').
		resample=0: Image.resize() resampling mode.
	"""
	img = openimg(img)
	if (double_vres):
		if (chars == '█'): chars = '▀'
		else: double_vres = False
	color = (len(chars) == 1)
	if (type(size) == float): size = int(size)
	if (type(size) == int): size = (size,)
	if (len(size) == 1): size = tuple(map(int, (size[0], min(img.size)/(max(img.size)/size[0]))))
	if (double_vres): size = (size[0], size[1]*2)
	if (bgcolor):
		img_o, img = img.convert('RGBA'), Image.new('RGB', img.size, color=bgcolor)
		img.paste(img_o, mask=img_o)
	img = img.convert('RGBA' if (color) else 'L').resize(size, resample)
	px = img.load()
	padchar *= padding
	r = str()
	for y in range(0, size[1], 1+double_vres):
		r += padchar
		for x in range(size[0]):
			if (color):
				if (not px[x,y][3] or double_vres and not px[x,y+1][3]): r += ' '; continue # TODO FIXME
				r += '\033[38;2;'+';'.join(map(str, px[x,y][:3]))+'m'
				if (double_vres and y+1 < size[1]): r += '\033[48;2;'+';'.join(map(str, px[x,y+1][:3]))+'m'
				else: r += '\033[48;2;'+';'.join(map(str, px[x,y][:3]))+'m'
				r += chars+'\033[0m'
			else: r += chars[px[x,y]*len(chars)//256]
		if (y+1+double_vres < size[1]): r += '\n'
	return r

@export
def pixel_color(img): return openimg(img).resize((1, 1)).convert('RGB').load()[0,0]

@export
def pixel(img, char='●'): return '\033[1;38;2;'+';'.join(map(str, pixel_color(img)))+'m'+char+'\033[0m'

@export
def openimg(img):
	if (Image.isImageType(img)): return img
	try: return Image.open(open(img.split('file://', maxsplit=1)[-1], 'rb') if (isinstance(img, str)) else img)
	except Exception:
		import requests
		try: return Image.open(requests.get(img, stream=True).raw)
		except Exception: ex = True
		if (ex): raise

# by Sdore, 2020-22
#   www.sdore.me
