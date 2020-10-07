
import matplotlib as mpl 


def named_colors(): 
	r""" 
	Returns 
	-------
	colors : dict 
		A dictionary of color names to matplotlib colors 

	Notes 
	-----
	This function simply wraps matplotlib.colors.get_named_colors_mapping() 
	""" 
	return mpl.colors.get_named_colors_mapping() 


def mpl_loc(label): 
	r""" 
	Parameters 
	----------
	label : str 
		A descriptive location of a point in box 

		Recognized inputs: 

			- "best" 
			- "upper right" 
			- "upper left" 
			- "lower left" 
			- "lower right" 
			- "right" 
			- "center left" 
			- "center right" 
			- "lower center" 
			- "upper center" 
			- "center" 

	Returns 
	-------
	index : int 
		The matplotlib integer index denoting the location within the box 
	""" 
	indeces = {
		"best": 0,
		"upper right": 1,
		"upper left": 2,
		"lower left": 3,
		"lower right": 4,
		"right": 5,
		"center left": 6,
		"center right": 7,
		"lower center": 8,
		"upper center": 9,
		"center": 10
	} 

	if label.lower() in indeces.keys(): 
		return indeces[label.lower()] 
	else: 
		raise ValueError("Unrecognized location string: %s" % (label)) 

