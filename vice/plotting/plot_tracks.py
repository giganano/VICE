""" 
Plot Tracks 
=========== 
This file implements the core routines of the plotTracks function 
""" 

from __future__ import absolute_import 
# try: 
# 	ModuleNotFoundError 
# except NameError: 
# 	ModuleNotFoundError = ImportError 
# try: 
# 	import matplotlib as mpl 
# except (ModuleNotFoundError, ImportError): 
# 	raise ModuleNotFoundError("Matplotlib not found.") 
# if int(mpl.__version__[0]) < 2: 
# 	raise RuntimeError("Matplotlib version >= 2.0.0 is required.") 
# else: 
# 	pass 
from . import _rcparams 
from .utils.mplutils import square_subplot 
from .utils.mplutils import named_colors
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import sys 
import os 
import vice 
from vice._globals import _RECOGNIZED_ELEMENTS_ 
from vice._globals import _VERSION_ERROR_ 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
SIZE = 7

def plot_single_track_set(imgname, outputs, colors, reference, secondary): 
	""" 
	Plot the tracks for the given outputs 

	Parameters 
	========== 
	outputs :: list 
		The VICE output objects containing the data to be plotted 
	colors :: list 
		A list of strings containing the colors to use for each output 
	reference :: str 
		The symbol for the reference element 
	secondary :: str 
		The symbol for the secondary element 
	""" 
	assert isinstance(imgname, strcomp) 
	assert isinstance(outputs, list) 
	assert isinstance(colors, list) 
	assert len(outputs) == len(colors) 
	assert isinstance(reference, strcomp) 
	assert isinstance(secondary, strcomp) 
	plt.clf() 
	ax = square_subplot(
		SIZE, 
		xlabel = "[%s/H]" % (reference), 
		ylabel = "[%s/%s]" % (secondary, reference)
	) 
	for i in range(len(outputs)): 
		ax.plot(outputs[i].history["[%s/H]" % (reference)], 
			outputs[i].history["[%s/%s]" % (secondary, reference)], 
			c = named_colors()[colors[i]]) 
	plt.savefig(imgname) 
	plt.clf() 

def plot_all_tracks(names, colors, left = None, right = None, bottom = None, 
	top = None): 
	if len(names) = len(colors): 
		outputs = [vice.output(i) for i in names] 
	else: 
		raise ValueError("Array-length mismatch. Names: %d. Colors: %d" % (
			len(names), len(colors))) 
	for i in range(1, len(names)): 
		if outputs[i].elements != outputs[0].elements: raise ValueError("""\
All outputs must have simulated the same elements.""") 
	if os.path.exists("tracks"): os.system("rm -rf tracks") 
	os.system("mkdir tracks") 
	os.chdir("tracks") 
	for i in range(len(outputs[0].elements)): 
		os.system("mkdir %s" % (outputs[0].elements[i])) 
		os.chdir("%s" % (outputs[0].elements[i])) 
		for j in range(len(outputs[0].elements)): 
			if i == j: 
				continue 
			else: 
				plot_single_track_set("%s.pdf" % (outputs[0].elements[j]), 
					outputs, colors, outputs[0].elements[i], 
					outputs[0].elements[j]) 
		os.chdir("..") 
	os.chdir("..") 



