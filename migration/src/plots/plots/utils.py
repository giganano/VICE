
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter as fsf
import matplotlib.pyplot as plt


def xticklabel_formatter(ax):
	r"""
	Format the x-tick labels to '%g'

	Parameters
	----------
	ax : subplot
		The subplot to apply the formatting to.
	"""
	ax.xaxis.set_major_formatter(fsf("%g"))


def yticklabel_formatter(ax):
	r"""
	Format the y-tick labels to '%g'

	Parameters
	----------
	ax : subplot
		The subplot to apply the formatting to.
	"""
	ax.yaxis.set_major_formatter(fsf("%g"))


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


def markers():
	r"""
	Returns a dictionary of terms to matplotlib marker characters.

	Recognized markers:
		
		* point
		* pixel
		* circle
		* triangle_down
		* triangle_up
		* triangle_left
		* triangle_right
		* tri_down
		* tri_up
		* tri_left
		* tri_right
		* octagon
		* square
		* pentagon
		* plus_filled
		* star
		* hexagon1
		* hexagon2
		* plus
		* x
		* x_filled
		* diamond
		* thin_diamond
		* vline
		* hline
		* tickleft
		* tickright
		* tickup
		* tickdown
		* caretright
		* caretleft
		* caretup
		* caretdown
		* caretrightbase
		* caretleftbase
		* caretupbase
	"""
	return {"point":		".",
		"pixel":			",",
		"circle":			"o",
		"triangle_down":	"v",
		"circle":			"o",
		"triangle_down":	"V",
		"triangle_up":		"^",
		"triangle_left":	"<",
		"triangle_right":	">",
		"tri_down":			"1",
		"tri_up":			"2",
		"tri_left":			"3",
		"tri_right":		"4",
		"octagon":			"8",
		"square": 			"s",
		"pentagon":			"p",
		"plus_filled":		"P",
		"star":				"*",
		"hexagon1":			"h",
		"hexagon2":			"H",
		"plus":				"+",
		"x":				"x",
		"x_filled":			"X",
		"diamond":			"D",
		"thin_diamond":		"d",
		"vline":			"|",
		"hline":			"_",
		"tickleft":			"TICKLEFT",
		"tickright":		"TICKRIGHT",
		"tickup":			"TICKUP",
		"tickdown":			"TICKDOWN",
		"caretright":		"CARETRIGHT",
		"caretleft":		"CARETLEFT",
		"caretup":			"CARETUP",
		"caretdown":		"CARETDOWN",
		"caretrightbase":	"CARETRIGHTBASE",
		"caretleftbase":	"CARETLEFTBASE",
		"caretupbase":		"CARETUPBASE"
	}


def dummy_background_axes(axes):
	r"""
	Constructs a subplot in the background of a set of subplots with the
	corners aligned, but invisible tick labels.

	Parameters
	----------
	axes : 2-d list
		A 2-d list of subplots. First axis must be the row number of the
		subplot, with the zero'th element at the top of the figure. Second
		axis must be the column number of the subplot, with the zero'th
		element at the left of the figure.

	Returns
	-------
	dummy : subplot
		A matplotlib subplot whose corners are aligned with the grid of
		subplots passed, and will be drawn behind them.

	Raises
	------
	No exceptions are explicitly raised by this routine.
	"""
	dummy = plt.gcf().add_subplot(111, facecolor = "white", zorder = -100)
	posd = dummy.get_position()
	posd.x0 = axes[-1][0].get_position().x0
	posd.x1 = axes[-1][-1].get_position().x1
	posd.y0 = axes[-1][0].get_position().y0
	posd.y1 = axes[0][0].get_position().y1
	dummy.set_position(posd)
	plt.setp(dummy.get_xticklabels(), visible = False)
	plt.setp(dummy.get_yticklabels(), visible = False)
	return dummy

