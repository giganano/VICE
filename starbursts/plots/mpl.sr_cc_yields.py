"""
Produces Fig. 4 of Johnson & Weinberg (2019), a 1-panel plot showing the
IMF-averaged Sr yields from CCSNe as a funtion of total metallicity and
rotational velocity.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import math as m
import vice
import sys
import warnings
warnings.filterwarnings("ignore")

# The keywords accepted by VICE denoting the studies to plot yields from
_STUDIES_ = ["LC18", "CL04"]

# The rotational velocities of stars probed by a given study
_VROT_ = {
	"LC18":		[0, 150, 300],
	"CL04":		[0],
}

# The overall metallicities [M/H] probed by a given study
_MH_ = {
	"LC18":		[-3, -2, -1, 0],
	"CL04":		[-4, -2, -1, -0.37, 0.15],
}

# The colors to plot a given study in
_COLORS_ = {
	"LC18":		"blue",
	"CL04":		"crimson"
}

# The markers to use for each rotational velocity
_MARKERS_ = {
	0:		"circle",
	150:	"triangle_up",
	300:	"star"
}

# The full names of each study given the keyword
_NAMES_ = {
	"LC18":		"Limongi \& Chieffi (2018)",
	"CL04": 	"Chieffi \& Limongi (2004)"
}


def plot_all_yields(ax, element):
	"""
	Plots all yields for a given element on the axis given the studies and
	rotational velocities to determine yields from

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	element :: str
		The element to plot the yield of
	"""
	for i in _STUDIES_:
		for j in _MH_[i]:
			for k in _VROT_[i]:
				plot_yield(ax, element, i, j, k, _MARKERS_[k], _COLORS_[i])
	plot_legend(ax)


def plot_yield(ax, element, study, MH, vrot, marker, color):
	"""
	Plots a single IMF-averaged CCSN yield of Sr on the axis

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	element :: str
		The element to plot the yield of
	study :: str
		The study to adopt the yields from
	MH :: real number
		The value of [M/H] to calculate the yield for
	vrot :: real number
		The rotational velocity of the stars in km/s
	marker :: str
		The name of the marker to plot the point in
	color :: str
		The name of the color to plot the yield in
	"""
	y = vice.yields.ccsne.fractional(element, study = study, MoverH = MH,
		rotation = vrot)[0]
	ax.scatter(MH, y, c = visuals.colors()[color],
		marker = visuals.markers()[marker], s = 100)


def plot_functional(ax, func):
	"""
	Plots the yield as a function of metallicity on the axis

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	func :: <function>
		The function to plot on the axis
	"""
	small, big = ax.get_xlim()
	xvals = [small + (big - small) / 1000 * i for i in range(1000)]
	ax.plot(xvals, list(map(func, xvals)), linestyle = ':',
		c = visuals.colors()["black"])


def plot_legend(ax):
	"""
	Draws the legend on the axis

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	"""

	# First label the studies ...
	lines = len(_STUDIES_) * [None]
	for i in range(len(lines)):
		lines[i] = ax.plot([-1, -2], [1.e-8, 1.e-6],
			c = visuals.colors()["white"], label = _NAMES_[_STUDIES_[i]])[0]
	leg = ax.legend(loc = visuals.mpl_loc()["lower right"], ncol = 1,
		bbox_to_anchor = (0.99, 0.01), frameon = False, handlelength = 0,
		fontsize = 18)
	for i in range(len(lines)):
		lines[i].remove()
		leg.get_texts()[i].set_color(_COLORS_[_STUDIES_[i]])
	ax.add_artist(leg)

	# ... then label the rotational velocities
	points = 3 * [None]
	for i in range(len(points)):
		points[i] = ax.scatter([-1, -2], [1.e-8, 1.e-6],
			c = visuals.colors()["black"], s = 50,
			marker = visuals.markers()[_MARKERS_[[0, 150, 300][i]]],
			label = r"$v_\text{rot}$ = %g km s$^{-1}$" % ([0, 150, 300][i])
		)
	ax.legend(loc = visuals.mpl_loc()["upper left"], ncol = 1,
		bbox_to_anchor = (0.01, 0.99), frameon = False, fontsize = 18,
		handlelength = 1)
	for i in range(len(points)):
		points[i].remove()


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	ax = visuals.subplots(1, 1)
	ax.set_xlabel(r"$\log_{10}(Z/Z_\odot)$")
	ax.set_ylabel(r"$y_\text{Sr}^\text{CC}$")
	ax.set_yscale("log")
	ax.set_xlim([-4.4, 0.6])
	ax.set_ylim([3.e-13, 3.e-6])
	plot_all_yields(ax, "sr")
	plot_functional(ax, lambda x: 3.5e-8 * 10**x)
	plot_functional(ax, lambda x: 1.e-7 * (1 - m.exp(-10**(x + 1))))
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()



