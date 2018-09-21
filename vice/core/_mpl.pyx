
from __future__ import unicode_literals
try:
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	from matplotlib.ticker import AutoMinorLocator as _aml
except:
	pass

def set_frame(subplot):
	"""
	Args:
	-------------
	subplot: A matplotlib subplot instance

	Places tick-marks on all axes of the subplot, faces them inward, and 
	puts minor ticks between the major ticks.

	NOTE: If you're using this method with log-scale axes, it must be 
	called BEFORE switching to log-scale. E.g., the following code:

	1	import matplotlib.pyplot as plt
	2	fig = plt.figure()
	3	ax = fig.add_subplot(111, facecolor = 'white')
	4	ax.set_xscale('log')
	5	graphics.set_frame(ax)
	6	plt.savefig('foo.pdf')

	will throw an error not at line 5, but at line 6. plt.savefig() will 
	throw an ExceedsMaxTicks error. The code should be written:

	1	import matplotlib.pyplot as plt
	2	fig = plt.figure()
	3	ax = fig.add_subplot(111, facecolor = 'white')
	4	graphics.set_frame(ax)	
	5	ax.set_xscale('log')
	6	plt.savefig('foo.pdf')	
	"""	
	subplot.tick_params(direction = b"in", which = b"both")
	subplot.yaxis.set_ticks_position(b"both")
	subplot.xaxis.set_ticks_position(b"both")
	subplot.yaxis.set_minor_locator(_aml())
	subplot.xaxis.set_minor_locator(_aml())


def set_params():
	mpl.rcParams[b"axes.linewidth"] = 1
	mpl.rcParams[b"xtick.major.size"] = 4
	mpl.rcParams[b"xtick.major.width"] = 0.75
	mpl.rcParams[b"xtick.minor.size"] = 2
	mpl.rcParams[b"xtick.minor.width"] = 0.375
	mpl.rcParams[b"ytick.major.size"] = 4
	mpl.rcParams[b"ytick.major.width"] = 0.75
	mpl.rcParams[b"ytick.minor.size"] = 2.
	mpl.rcParams[b"ytick.minor.width"] = 0.375
	mpl.rcParams[b"axes.labelsize"] = 16
	mpl.rcParams[b"xtick.labelsize"] = 14
	mpl.rcParams[b"ytick.labelsize"] = 14



