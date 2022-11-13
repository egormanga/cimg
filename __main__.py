#!/usr/bin/env python3

from utils import *
from . import *

def main():
	utils_args = {i.dest for i in argparser._actions} # a hack, yep. TODO: do not hack
	argparser.add_argument('img', metavar='<path | url>')
	argparser.add_argument('-size', metavar='<maxSide | WxH>', default=-1)
	argparser.add_argument('-padding', metavar='N', type=int)
	argparser.add_argument('-padchar', metavar='char')
	argparser.add_argument('-bgcolor', metavar='color')
	argparser.add_argument('-resample', metavar='mode')
	argparser.add_argument('--ascii', action='store_true')
	argparser.add_argument('--noansi', action='store_true')
	cargs = argparser.parse_args()

	kwargs = dict(filter(operator.itemgetter(1), S(cargs.__dict__).translate({'double_vres': 'ascii'}, strict=False)(*({i.dest for i in argparser._actions}-utils_args)).items()))
	size = Sstr(kwargs['size']).bool(minus_one=False)
	kwargs['size'] = tuple(map(int, kwargs['size'].split('x'))) if (size) else os.get_terminal_size()
	if ('resample' in kwargs): kwargs['resample'] = getattr(Image, kwargs['resample'].upper())
	if (kwargs.pop('noansi', False)): kwargs['chars'] = ' ░▒▓█'
	if (not size): sys.stderr.write('\033c')
	sys.stdout.write(showimg(**kwargs)); sys.stdout.flush()
	if (size): sys.stderr.write('\n'); return
	try: sys.stdin.read(1)
	except: pass
	sys.stderr.write('\033c')
	sys.stderr.flush()

if (__name__ == '__main__'): exit(main(), nolog=True)

# by Sdore, 2022
#  www.sdore.me
