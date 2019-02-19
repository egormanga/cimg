#!/usr/bin/python3
# Python console image view library

import os, sys, requests
from PIL import Image
from utils import *; logstart('cimg')

def ascii(img, size, chars='█', *, padding=0, padchar=' ', bgcolor=None, double_vres=False, resample=0): # ░▒▓█
	"""
	img: PIL Image, Image.open arg or URL as str.
	size: (w, h) int tuple or single int to use as length of one or both sides of output.
	chars='█': multiple chars (i.e. '░▒▓█') to use as b/w palette or single (i.e. '█') for RGB (ANSI-escape) mode.
	padding=0: prefix every line with N `padchar`s.
	padchar=' ': character to use as left-padding.
	double_vres=False: double the vertical size and use bg color as the bottom pixel for half-block chars (i.e. '▀').
	resample=0: Image.resize() resampling mode.
	"""
	img = openimg(img)
	if (double_vres and chars == '█'): chars = '▀'
	color = len(chars) == 1
	if (type(size) == float): size = int(size)
	if (type(size) == int): size = (size,)
	if (len(size) == 1): size = tuple(map(int, (size[0], min(img.size)/(max(img.size)/size[0]))))
	if (double_vres): size = (size[0], size[1]*2)
	if (bgcolor):
		img_o, img = img.convert('RGBA'), Image.new('RGB', img.size, color=bgcolor)
		img.paste(img_o, mask=img_o)
	if (color): img = img.convert('RGBA')
	else: img = img.convert('L')
	img = img.resize(size, resample)
	px = img.load()
	padchar *= padding
	r = str()
	for y in range(0, size[1], 1+double_vres):
		r += padchar
		for x in range(size[0]):
			if (color):
				if (not px[x,y][3] or double_vres and not px[x,y+1][3]): r += ' '; continue # TODO FIXME
				r += '\033[38;2;'+';'.join(map(str, px[x,y][:3]))+'m'+'\033[48;2;'+';'.join(map(str, px[x,y][:3]))+'m'
				if (double_vres and y+1 < size[1]): r += '\033[48;2;'+';'.join(map(str, px[x,y+1][:3]))+'m'
				r += chars+'\033[0m'
			else: r += chars[px[x,y]*len(chars)//256]
		if (y+1+double_vres < size[1]): r += '\n'
	return r

def pixel(img, char='●'): return '\033[1;38;2;'+';'.join(map(str, openimg(img).resize((1, 1)).convert('RGB').load()[0,0]))+'m'+char+'\033[0m'

def openimg(img):
	if (Image.isImageType(img)): return img
	try: return Image.open(img)
	except Exception:
		try: return Image.open(requests.get(img, stream=True).raw)
		except Exception: ex = True
		if (ex): raise

def main():
	known_args = {i.dest for i in argparser._actions} # a hack, yep. TODO: do not hack
	argparser.add_argument('img', metavar='<path | url>')
	argparser.add_argument('-size', metavar='<maxSide | WxH>', default=-1)
	argparser.add_argument('-padding', metavar='N', type=int)
	argparser.add_argument('-padchar')
	argparser.add_argument('-bgcolor', metavar='color')
	argparser.add_argument('-resample', metavar='mode')
	argparser.add_argument('--ascii', action='store_true')
	cargs = argparser.parse_args()

	kwargs = dict(filter(operator.itemgetter(1), S(cargs.__dict__).translate({'double_vres': 'ascii'}, strict=False)(*({i.dest for i in argparser._actions}-known_args)).items()))
	size = Sstr(kwargs['size']).bool(minus_one=False)
	kwargs['size'] = tuple(map(int, kwargs['size'].split('x'))) if (size) else os.get_terminal_size()
	if ('resample' in kwargs): kwargs['resample'] = getattr(Image, kwargs['resample'].upper())
	if (not size): sys.stderr.write('\033c')
	sys.stdout.write(ascii(**kwargs)); sys.stdout.flush()
	if (size): sys.stderr.write('\n'); return
	try: sys.stdin.read(1)
	except: pass
	sys.stderr.write('\033c')
	sys.stderr.flush()

if (__name__ == '__main__'): logstarted(); main()
else: logimported()

# by Sdore, 2018
