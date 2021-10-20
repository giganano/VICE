"""
Subroutines for working with matplotlib that help produce the Johnson &
Weinberg (2019) starburst plots.
"""

try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	import matplotlib as mpl
except ModuleNotFoundError:
	raise ModuleNotFoundError("""Producing the Johnson & Weinberg (2019) \
plots requires matplotlib version >= 2.0.0""")
if int(mpl.__version__[0]) < 2:
	raise RuntimeError("""Producing the Johnson & Weinberg (2019) \
plots requires matplotlib version >= 2.0.0. Got: %s""" % (mpl.__version__))
else:
	pass
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes as zia
try:
	import vice
except ModuleNotFoundError:
	raise ModuleNotFoundError("Could not import VICE.")

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = [r"\usepackage{amsmath}"]
mpl.rcParams["errorbar.capsize"] = 5
mpl.rcParams["axes.linewidth"] = 2
mpl.rcParams["xtick.major.size"] = 16
mpl.rcParams["xtick.major.width"] = 2
mpl.rcParams["xtick.minor.size"] = 8
mpl.rcParams["xtick.minor.width"] = 1
mpl.rcParams["ytick.major.size"] = 16
mpl.rcParams["ytick.major.width"] = 2
mpl.rcParams["ytick.minor.size"] = 8
mpl.rcParams["ytick.minor.width"] = 1
mpl.rcParams["axes.labelsize"] = 30
mpl.rcParams["xtick.labelsize"] = 25
mpl.rcParams["ytick.labelsize"] = 25
mpl.rcParams["legend.fontsize"] = 25
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["ytick.right"] = True
mpl.rcParams["xtick.top"] = True
mpl.rcParams["xtick.minor.visible"] = True
mpl.rcParams["ytick.minor.visible"] = True


def subplots(nrows, ncols, figsize = (7, 7)):
	"""
	Generate subplots with a certain number of rows and columns

	Parameters
	==========
	nrows :: int
		The number of rows of subplots
	ncols :: int
		The number of columns of subplots
	figsize :: tuple
		The (width, height) of the figure

	Returns
	=======
	An MxN list of containing the matplotlib subplots
	"""
	fig, axes = plt.subplots(nrows = nrows, ncols = ncols,
		figsize = figsize)
	try:
		return axes.tolist()
	except:
		return axes


def colors():
	"""
	Returns
	=======
	A dictionary of color names to matplotlib colors
	"""
	return mpl.colors.get_named_colors_mapping()


def mpl_loc():
	"""
	Return
	======
	loc :: dict
		keys :: location descriptors (type str)
		fields :: integer that matplotlib recognizes

	Recognized keys
	===============
		"best"
		"upper right"
		"upper left"
		"lower left"
		"lower right"
		"right"
		"center left"
		"center right"
		"lower center"
		"upper center"
		"center"

	Example
	=======
	The following line of code will place the legend in the upper right corner:
	>>> subplot.legend(loc = visuals.mpl_loc()["upper right"])
	"""
	return {
		"best":				0,
		"upper right":		1,
		"upper left":		2,
		"lower left":		3,
		"lower right":		4,
		"right":			5,
		"center left":		6,
		"center right":		7,
		"lower center":		8,
		"upper center":		9,
		"center":			10
	}


def markers():
	"""
	Returns
	=======
	A dictionary of terms to matplotlib marker characters.

	Recognized markers
	==================
	point
	pixel
	circle
	triangle_down
	triangle_up
	triangle_left
	triangle_right
	tri_down
	tri_up
	tri_left
	tri_right
	octagon
	square
	pentagon
	plus_filled
	star
	hexagon1
	hexagon2
	plus
	x
	x_filled
	diamond
	thin_diamond
	vline
	hline
	tickleft
	tickright
	tickup
	tickdown
	caretright
	caretleft
	caretup
	caretdown
	caretrightbase
	caretleftbase
	caretupbase

	Example:
	This line of code will produce the scatter plot in red stars:
	plt.plot(range(10), range(10, 20), '%c%c' % (
		visuals.colors()['red'],
		visuals.markers()['star']
	))
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


def hide_xticklabels(ax):
	"""
	Hide x-axis tick labels

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to hide labels on
	"""
	plt.setp(ax.get_xticklabels(), visible = False)
	plt.setp(ax.get_xminorticklabels(), visible = False)


def hide_yticklabels(ax):
	"""
	Hide y-axis tick labels

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to hide labels on
	"""
	plt.setp(ax.get_yticklabels(), visible = False)
	plt.setp(ax.get_yminorticklabels(), visible = False)


def append_subplot_below(ax):
	"""
	Add a subplot to the bottom of an existing set of axes

	Parameters
	==========
	ax :: subplot
		The matplotlib subplot object to put axes on the bottom of

	Returns
	=======
	new :: subplot
		The appended axis object
	"""
	return make_axes_locatable(ax).append_axes("bottom", 2.5, pad = 0,
		sharex = ax)


def draw_box(ax, xlim, ylim):
	"""
	Draws a box in solid black lines on the subplot bounding the specified
	x and y limits

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to draw the box on
	xlim :: list
		The x limits of the box
	ylim :: list
		The y limits of the box
	"""
	ax.plot(2 * [xlim[0]], ylim, c = colors()["black"])
	ax.plot(2 * [xlim[1]], ylim, c = colors()["black"])
	ax.plot(xlim, 2 * [ylim[0]], c = colors()["black"])
	ax.plot(xlim, 2 * [ylim[1]], c = colors()["black"])


def zoom_box(ax, xlim, ylim, zoom = 2, loc = "lower left",
	borderpad = 1):
	"""
	Puts a zoomed inset axis on the associated x and y limits with the
	specified zoom scale on a matplotlib subplot.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the zoomed axes on
	xlim :: list
		The desired x limits of the inset
	ylim :: list
		The desired y limits of the inset
	zoom :: real number
		The zoom scale of the inset
	loc :: str
		The location string to pass to mpl_loc
	borderpad :: real number
		The borderpad argument to pass to matplotlib.zoomed_inset_axes
	"""
	axins = zia(ax, zoom, loc = mpl_loc()[loc], borderpad = borderpad)
	axins.set_xlim(xlim)
	axins.set_ylim(ylim)
	hide_xticklabels(axins)
	hide_yticklabels(axins)
	return axins


def xticklabel_formatter(ax):
	"""
	Changes the matplotlib ticker format on the x-axis to %g

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to format the ticks on
	"""
	ax.xaxis.set_major_formatter(FormatStrFormatter("%g"))


def yticklabel_formatter(ax):
	"""
	Changes the matplotlib ticker format on the y-axis to %g

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to format the ticks on
	"""
	ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))


def plot_output_3axes(axes, name, color, element, second_linestyle = '-'):
	"""
	Plots the star formation rate and infall rate on axes[0], [X/Fe]-[Fe/H]
	tracks on axes[1], and the dN/d[X/Fe] MDF on axes[2].

	Parameters
	==========
	axes :: list
		A 3-element list of matplotlib subplots
	name :: str
		The name of the VICE output to plot
	color :: str
		The name of the color to pass to matplotlib's named colors mapping
	element :: str
		The symbol for the element X
	second_linestyle :: str [default :: '-']
		The linestyle to use in the middle and right-hand panels
	"""
	out = vice.output(name)
	axes[0].plot(out.history["time"], out.history["sfr"], c = colors()[color])
	axes[0].plot(out.history["time"], out.history["ifr"], c = colors()[color],
		linestyle = '--')
	axes[1].plot(out.history["[Fe/H]"], out.history["[%s/Fe]" % (element)],
		c = colors()[color],
		linestyle = second_linestyle)
	axes[2].plot(list(map(lambda x, y: (x + y) / 2., out.mdf["bin_edge_left"],
		out.mdf["bin_edge_right"])), out.mdf["dN/d[%s/Fe]" % (element)],
		c = colors()[color],
		linestyle = second_linestyle)


def plot_output_4axes(axes, name, color, element, second_linestyle = '-'):
	"""
	Plots the star formation rate and infall rate on axes[0], SFE timescale
	on axes[1], [X/Fe]-[Fe/H] tracks on axes[1], and the dN/d[X/Fe] MDF on
	axes[2].

	Parameters
	==========
	axes :: list
		A 4-element list of matplotlib subplots
	name :: str
		The name of the VICE output to plot
	color :: str
		The name of the color to pass to matplotlib's named colors mapping
	element :: str
		The symbol for the element X
	second_linestyle :: str [default :: '-']
		the linestyle to use in the middle and right-hand panels
	"""
	out = vice.output(name)
	axes[0].plot(out.history["time"], out.history["sfr"], c = colors()[color])
	axes[1].plot(out.history["time"],
		list(map(lambda x, y: 1.e-9 * x / y, out.history["mgas"],
			out.history["sfr"])),
		c = colors()[color])
	axes[2].plot(out.history["[Fe/H]"], out.history["[%s/Fe]" % (element)],
		c = colors()[color],
		linestyle = second_linestyle)
	axes[3].plot(list(map(lambda x, y: (x + y) / 2., out.mdf["bin_edge_left"],
		out.mdf["bin_edge_right"])), out.mdf["dN/d[%s/Fe]" % (element)],
		c = colors()[color],
		linestyle = second_linestyle)


def set_labels_3axes(axes, element):
	"""
	Sets the x- and y- axis labels to their appropriate values for a
	3-panel plot as in Johnson & Weinberg (2019).

	Parameters
	==========
	axes :: list
		A 3-element list of matplotlib subplot objects
	element :: str
		The symbol for the element plotted against iron
	"""
	axes[0].set_xlabel("Time [Gyr]")
	axes[0].set_ylabel(r"$\dot{M}$ [M$_\odot$ yr$^{-1}$]")
	axes[1].set_xlabel("[Fe/H]")
	axes[1].set_ylabel("[%s/Fe]" % (element))
	axes[2].set_xlabel("[%s/Fe]" % (element))
	axes[2].set_ylabel("Stellar Probability Density")
	axes[2].set_yscale("log")


def set_labels_4axes(axes, element):
	"""
	Sets the x- and y- axis labels to their appropriat values for a 3-panel
	plot with split first panel as in Johnson & Weinberg (2019).

	Parameters
	==========
	axes :: list
		A 4-element list of matplotlib subplots objects
	element :: str
		The symbol for the element plotted against iron
	"""
	axes[0].set_ylabel(r"$\dot{M}_*$ [M$_\odot$ yr$^{-1}$]")
	axes[1].set_xlabel("Time [Gyr]")
	axes[1].set_ylabel(r"$\tau_*$ [Gyr]")
	axes[2].set_xlabel("[Fe/H]")
	axes[2].set_ylabel("[%s/Fe]" % (element))
	axes[3].set_xlabel("[%s/Fe]" % (element))
	axes[3].set_ylabel("Stellar Probability Density")
	axes[3].set_yscale("log")


def sfr_ifr_legend(ax, ncol = 1):
	"""
	Draw a legend noting that infall rates are plotted as dashed lines while
	star formation rates are plotted as solid lines on a given subplot

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	ncol :: int
		The desired number of columns in the legend
	"""
	lines = 2 * [None]
	labels = [r"$\dot{M}_\text{in}$", r"$\dot{M}_*$"]
	linestyles = ['--', '-']
	for i in range(2):
		lines[i] = ax.plot([1, 2], [1, 2], c = colors()["black"],
			linestyle = linestyles[i], label = labels[i])[0]
	ax.legend(loc = mpl_loc()["upper right"], ncol = ncol, frameon = False,
		bbox_to_anchor = (0.99, 0.99))
	for i in range(2):
		lines[i].remove()


def legend(ax, c, labels, loc = "lower left", bbox_to_anchor = (0.01, 0.01)):
	"""
	Draw a legend on a subplot given labels and colors of those labels

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	c :: list
		The list of colors to use in the legend
	labels :: list
		The labels for the legend
	loc :: str [default :: "lower left"]
		A descriptor of where to put the legend
	bbox_to_anchor :: tuple
		The (x, y) relative axis positions denoting where to put the legend
		on ax

	Raises
	======
	AssertionError ::
		::	c and labels are not of the same length
	"""
	assert len(c) == len(labels)
	lines = len(c) * [None]
	for i in range(len(lines)):
		lines[i] = ax.plot([1, 2], [1, 2], c = colors()["white"],
			label = labels[i])[0]
	leg = ax.legend(loc = mpl_loc()[loc], ncol = 1,
		bbox_to_anchor = bbox_to_anchor, frameon = False, handlelength = 0)
	for i in range(len(lines)):
		lines[i].remove()
		leg.get_texts()[i].set_color(c[i])


def plot_inset(inset, name, color, **kwargs):
	"""
	Plots [O/Fe]-[Fe/H] tracks on a set of inset axes

	Parameters
	==========
	inset :: subplot
		The matplotlib axis object to plot the tracks on
	name :: str
		The name of the VICE output
	color :: str
		The color to plot the output in
	kwargs :: varying types
		Other keyword arguments to pass to inset.plot
	"""
	out = vice.output(name)
	inset.plot(out.history["[Fe/H]"], out.history["[O/Fe]"],
		c = colors()[color], **kwargs)


def plot_reference(axes):
	"""
	Plots the [O/Fe]-[Fe/H] tracks and the stellar [O/Fe] distribution on the
	proper set of axes

	Parameters
	==========
	axes :: list
		The list of matplotlib axis objects to plot on
	"""
	out = vice.output("../../simulations/default")
	axes[-2].plot(out.history["[Fe/H]"], out.history["[O/Fe]"],
		c = colors()["black"], linestyle = ':')
	bins = list(map(lambda x, y: (x + y) / 2., out.mdf["bin_edge_left"],
		out.mdf["bin_edge_right"]))
	axes[-1].plot(bins, out.mdf["dN/d[O/Fe]"], c = colors()["black"],
		linestyle = ':')


def plot_track_points_intervals(ax, hist, element = "O", reference = "Fe"):
	"""
	Put points at 1 Gyr intervals on an [O/Fe]-[Fe/H] track.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	hist :: vice.history
		The VICE history object containing the time-evolution of the
		simulation
	"""
	for i in range(len(hist["time"])):
		if hist["time"][i] % 1 == 0:
			ax.scatter(hist["[%s/H]" % (reference)][i], hist["[%s/%s]" % (
				element, reference)][i], s = 10, c = colors()["black"])
		else: continue
