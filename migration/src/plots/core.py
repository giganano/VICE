r""" 
Core routines for producing the Johnson et al. (2021) figures 
""" 

__all__ = ["singlewide", "doublewide"] 
from . import env 
import matplotlib.pyplot as plt 

# The width of a single-column figure in inches 
_SINGLEWIDE_WIDTH_ = 5 


def singlewide(nrows = 1): 
	r""" 
	Produce a matplotlib figure to occupy only one column of the text. 

	Parameters 
	----------
	nrows : int [default : 1] 
		The number of rows of panels in the figure 

	Returns 
	-------
	fig : matplotlib.pyplot.figure 
		The figure object with the proper size 
	""" 
	return plt.figure(figsize = (_SINGLEWIDE_WIDTH_, 
		nrows * _SINGLEWIDE_WIDTH_)) 


def doublewide(nrows = 1): 
	r""" 
	Produce a matplotlib figure to occupy both columns of the text. 

	Parameters 
	----------
	nrows : int [default : 1] 
		The number of rows of panels in the figure 

	Returns 
	-------
	fig : matplotlib.pyplot.figure 
		The figure object with the proper size 
	""" 
	return plt.figure(figsize = (2 * _SINGLEWIDE_WIDTH_, 
		nrows * _SINGLEWIDE_WIDTH_)) 

