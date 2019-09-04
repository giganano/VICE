""" 
Matplotlib Utils 
================ 
This file implements utility functions for working with matplotlib. 
""" 

from __future__ import absolute_import 

__all__ = ["square_subplot", "named_colors"]  

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
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib.ticker import FormatStrFormatter as fsf 
from mpl_toolkits.axes_grid1 import make_axes_locatable 
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes as zia 
import numbers 
import sys 
import os 

def square_subplot(size, xlabel = "", ylabel = "", xlog = False, 
	ylog = False): 
	""" 
	Create a square subplot of a given size 

	Parameters 
	========== 
	size :: real number 
		The width and height of the subplot, in inches 
	xlabel :: str [default :: ""]  
		The x-axis label 
	ylabel :: str [default :: ""] 
		The y-axis label 
	xlog :: bool [default :: False] 
		Whether or not to use a log-scaled x-axis 
	ylog :: bool [default :: False] 
		Whether or not to use a log-scaled y-axis 

	Returns 
	======= 
	ax :: subplot 
		A matplotlib subplot object with the specified parameters 

	Raises 
	====== 
	All exceptions raised by matplotlib 
	""" 
	fig = plt.figure(figsize = (size, size)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel(xlabel) 
	ax.set_ylabel(ylabel) 
	if xlog: ax.set_xscale("log") 
	if ylog: ax.set_yscale("log") 
	return ax 

def named_colors(): 
	""" 
	Returns 
	======= 
	colors :: dict 
		The matplotlib named colors mapping dictionary 
	""" 
	return mpl.colors.get_named_colors_mapping() 


