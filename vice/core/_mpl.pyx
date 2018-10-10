"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

from __future__ import unicode_literals
import sys
if sys.version_info[0] == 3:
	from builtins import str
else:
	pass
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
	subplot.tick_params(direction = "in", which = "both")
	subplot.yaxis.set_ticks_position("both")
	subplot.xaxis.set_ticks_position("both")
	subplot.yaxis.set_minor_locator(_aml())
	subplot.xaxis.set_minor_locator(_aml())


def set_params():
	mpl.rcParams["axes.linewidth"] = 1
	mpl.rcParams["xtick.major.size"] = 4
	mpl.rcParams["xtick.major.width"] = 0.75
	mpl.rcParams["xtick.minor.size"] = 2
	mpl.rcParams["xtick.minor.width"] = 0.375
	mpl.rcParams["ytick.major.size"] = 4
	mpl.rcParams["ytick.major.width"] = 0.75
	mpl.rcParams["ytick.minor.size"] = 2.
	mpl.rcParams["ytick.minor.width"] = 0.375
	mpl.rcParams["axes.labelsize"] = 16
	mpl.rcParams["xtick.labelsize"] = 14
	mpl.rcParams["ytick.labelsize"] = 14



