"""
Produces Fig. A1 of Johnson & Weinberg (2020), a single axis plot showing the
abundance data of several dwarf galaxies taken from Kirby et al. (2010) in
comparison to a smooth and single-burst model simulated in VICE.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys
import warnings
warnings.filterwarnings("ignore")


_NAMES_ = {
	"Scl": 		"Sculptor",
	"LeoI": 	"Leo I",
	"Sex": 		"Sextans",
	"LeoII": 	"Leo II",
	"CVnI": 	"Canes Venatici I",
	"UMi": 		"Ursa Minor",
	"Dra": 		"Draco"
}

_COLORS_ = {
	"Scl": 		"crimson",
	"LeoI": 	"grey",
	"Sex": 		"lime",
	"LeoII": 	"deepskyblue",
	"CVnI": 	"darkviolet",
	"UMi": 		"black",
	"Dra": 		"gold"
}

_MARKERS_ = {
	"Scl": 		"circle",
	"LeoI": 	"square",
	"Sex": 		"star",
	"LeoII": 	"thin_diamond",
	"CVnI": 	"pentagon",
	"UMi": 		"hexagon2",
	"Dra": 		"triangle_up"
}

_SIZES_ = {
	"Scl": 		30,
	"LeoI": 	10,
	"Sex": 		80,
	"LeoII": 	30,
	"CVnI": 	60,
	"UMi": 		50,
	"Dra": 		40
}


def setup_axis():
	"""
	Sets up the axis with the proper labels and ranges

	Returns
	=======
	axis :: matplotlib subplot
		The axis to plot the data on
	"""
	fig = plt.figure(figsize = (10, 7))
	ax = fig.add_subplot(111, facecolor = "white")
	ax.set_xlabel("[Fe/H]")
	ax.set_ylabel("[Mg/Fe]")
	ax.set_xlim([-3.2, -0.4])
	ax.set_ylim([-0.9, 1.4])
	return ax


def read_data(filename = "../../data/kirby2010processed.dat"):
	"""
	Import the data from the associated file.

	Args
	====
	filename :: str [default :: ../data/kirby2010processed.dat]
		The path to the data file

	Returns
	=======
	An 2D-ascii list containing the data as it appears in the file
	"""
	data = 849 * [None]
	with open(filename, 'r') as f:
		f.readline() # header
		for i in range(len(data)):
			data[i] = f.readline().split()
			for j in range(2, len(data[i])):
				data[i][j] = float(data[i][j])
		f.close()
	return data


def plot_data(ax, data, dwarf):
	"""
	Plots an individual dwarf galaxy's abundance data on the subplot.

	Parameters
	==========
	ax :: matplotlib subplot
		The axis to plot the abundance data on
	data :: 2D-list
		The raw data itself
	dwarf :: str
		A key denoting which dwarf is being plotted. These appear in the first
		column of the argument data.
	"""
	FeH_column = 12
	MgFe_column = 14
	fltrd = list(filter(lambda x: x[0] == dwarf, data))
	kwargs = {
		"c": 				visuals.colors()[_COLORS_[dwarf]],
		"marker": 			visuals.markers()[_MARKERS_[dwarf]],
		"linestyle": 		"None",
		"label": 			_NAMES_[dwarf],
		"s": 				_SIZES_[dwarf]
	}
	if dwarf == "LeoI": kwargs["zorder"] = 0
	ax.scatter(
		[row[FeH_column] for row in fltrd],
		[row[MgFe_column] for row in fltrd],
		**kwargs
	)


def plot_representative_errorbar(ax, data, dwarf):
	"""
	Plots a representative error bar in the lower-left corner of the figure

	Parameters
	==========
	ax :: matplotlib subplot
		The axis object to put the errorbar on
	data :: 2D-list
		The raw data itself
	dwarf :: str
		The name of the dwarf to take the median errors from
	"""
	err_FeH_column = 13
	err_MgFe_column = 15
	fltrd = list(filter(lambda x: x[0] == dwarf, data))
	ax.errorbar(-2.8, -0.4,
		xerr = sorted([row[err_FeH_column] for row in fltrd])[len(fltrd) // 2],
		yerr = sorted([row[err_MgFe_column] for row in fltrd])[len(fltrd) // 2],
		ms = 0, color = visuals.colors()[_COLORS_[dwarf]])


def plot_vice_comparison(ax, name):
	"""
	Plots the [Mg/Fe]-[Fe/H] track of a given VICE model on the subplot.

	Parameters
	==========
	ax :: matplotlib subplot
		The axis to plot on
	name :: str
		The relative path to the VICE output
	"""
	out = vice.output(name)
	ax.plot(out.history["[fe/h]"], out.history["[mg/fe]"],
		c = visuals.colors()["black"],
		linestyle = '--')


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	ax = setup_axis()
	data = read_data()
	for i in _NAMES_.keys():
		plot_data(ax, data, i)
	plot_vice_comparison(ax, "../../simulations/kirby2010_smooth_enh1")
	plot_vice_comparison(ax, "../../simulations/kirby2010_smooth")
	plot_vice_comparison(ax, "../../simulations/kirby2010_burst")
	plot_representative_errorbar(ax, data, "UMi")
	ax.legend(loc = visuals.mpl_loc()["upper left"], ncol = 1, frameon = False,
		bbox_to_anchor = (1.02, 0.98), fontsize = 18)
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

