r"""
Plots the distribution of [O/Fe] in bins of [Fe/H] within 15 different galactic
regions.

This script produces Fig. 12 of Johnson et al. (2021).
"""

from ..._globals import ZONE_WIDTH
from .. import env
import matplotlib.pyplot as plt
from ..utils import analogdata, filter_multioutput_stars
from .utils import named_colors, mpl_loc
import numpy as np
import vice

# x-axis limits for [O/Fe]
XLIM = [-0.05, 0.35]

# y-axis limits for PDF
YLIM = [0, 20]

# The bins in [Fe/H] to calculate the distribution within
FEH_BINS = [
	[-0.4, -0.2],
	[0.0, 0.2]
]

# The colors to plot the distributions in bins of [Fe/H] with
COLORS = [
	"blue",
	"crimson"
]

# The edges of the radial bins defining galactic region in kpc
RADII = [3, 5, 7, 9, 11, 13]

# the edges of the midplane distance bins defining galactic region in kpc.
Z = [2.0, 1.0, 0.5, 0.0]


def main(name, stem):
	r"""
	Plot the distributions of [O/Fe] in bins of [Fe/H] in 15 different galactic
	regions.

	Parameters
	----------
	name : ``str``
		The relative or absolute path to the VICE output whose predicted
		[O/Fe] distributions are to be visualized here.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.

	.. note:: The 15 regions are defined by bins in radius whose edges are
		3, 5, 7, 9, 11, and 13 kpc, and bins in height above/below the disk
		midplane whose edges are 0, 0.5, 1, and 2 kpc. In each panel, the
		distribution will be shown for [Fe/H] = -0.4 - -0.2 and 0 - 0.2.
	"""
	axes = setup_axes()
	out = vice.multioutput(name)
	analog_data = analogdata("%s_analogdata.out" % (name))
	out.stars["abszfinal"] = [abs(row[-1]) for row in
		analog_data[:out.stars.size[0]]]
	for i in range(3):
		for j in range(5):
			plot_observed_mdfs(axes[i][j], RADII[j], Z[i + 1])
			plot_mdfs(axes[i][j], out.stars, RADII[j], RADII[j + 1],
				Z[i + 1], Z[i], label = i == 0 and j == 4)
	leg = axes[0][4].legend(loc = mpl_loc("upper right"),
		ncol = 1, frameon = False, handlelength = 0, fontsize = 20)
	for i in range(len(leg.get_texts())):
		leg.get_texts()[i].set_color(COLORS[i])
		leg.legendHandles[i].set_visible(False)
	model_data_legend(axes[0][2])
	plt.tight_layout()
	plt.subplots_adjust(wspace = 0, hspace = 0)
	plt.savefig("%s.pdf" % (stem))
	plt.savefig("%s.png" % (stem))


def plot_mdfs(ax, stars, min_rgal, max_rgal, min_absz, max_absz, label = False):
	r"""
	Plot all MDFs for a given rgal - |z| bin

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	stars : ``vice.core.dataframe._tracers.tracers``
		The model-predicted stellar abundance data from the VICE output.
	min_rgal : ``float``
		Minimum galactocentric radius defining the region.
	max_rgal : ``float``
		Maximum galactocentric radius defining the region.
	min_absz : ``float``
		Minimum height above/below the disk midplane |z| in kpc defining the
		region.
	max_absz : ``float``
		Maximum height above/below the disk midplane |z| in kpc defining the
		region.
	label : ``bool`` [default : False]
		Whether or not to produce a legend handle for the plotted distributions.
	"""
	bins1 = [-0.1 + 0.04 * _ for _ in range(16)]
	bins2 = [-0.12 + 0.04 * _ for _ in range(17)]
	for i in range(len(FEH_BINS)):
		xvals, dist = get_pdf(stars, min_rgal, max_rgal, min_absz, max_absz,
			FEH_BINS[i][0], FEH_BINS[i][1], bins = bins1 if i else bins2)
		kwargs = {
			"c": 		named_colors()[COLORS[i]],
			"where": 	"mid"
		}
		if label: kwargs["label"] = r"%g $\leq$ [Fe/H] $\leq$ %g" % (
			FEH_BINS[i][0], FEH_BINS[i][1])
		ax.step(xvals, dist, **kwargs)


def plot_observed_mdfs(ax, min_rgal, min_absz):
	r"""
	Plot the [O/Fe] distributions in the same regions and for the same
	[Fe/H] bins as characterized by Vincenzo et al. (2021) [1]_.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	min_rgal : ``float``
		Minimum galactocentric radius in kpc defining the region.
	min_absz : ``float``
		Minimum height above/below the disk midplane |z| in kpc defining the
		region.

	.. note:: Although there are no parameters for maximum radius and maximum
		height |z| required, the distributions this function plots are for the
		same regions as in this script (provided it hasn't been modified).

	.. [1] Vincenzo et al. (2021), arxiv:2101.04488
	"""
	for i in range(len(FEH_BINS)):
		data = np.genfromtxt(
			"./data/ofe_mdfs/Rmin%.1f_hmin%.1f_FeHmin%.1f.dat" % (min_rgal,
				min_absz, FEH_BINS[i][0])).tolist()
		# convert distribution into PDF
		yvals = [row[-1] for row in data]
		xvals = [row[-2] for row in data]
		norm = sum([i * (xvals[1] - xvals[0]) for i in yvals])
		yvals = [i / norm for i in yvals]
		kwargs = {
			"c": 				named_colors()[COLORS[i]],
			"linestyle": 		':'
		}
		ax.plot(xvals, yvals, **kwargs)


def get_pdf(stars, min_rgal, max_rgal, min_absz, max_absz, min_FeH, max_FeH,
	bins = 10):
	r"""
	Calculate the [O/Fe] PDF in a given galactic region and bin of [Fe/H].

	Parameters
	----------
	stars : ``vice.core.dataframe._tracers.tracers``
		The model-predicted stellar abundance data from the VICE output.
	min_rgal : ``float``
		Minimum galactocentric radius in kpc defining the region.
	max_rgal : ``float``
		Maximum galactocentric radius in kpc defining the region.
	min_absz : ``float``
		Minimum height above/below the disk midplane |z| in kpc defining the
		region.
	max_absz : ``float``
		Maximum height above/below the disk midplane |z| in kpc defining the
		region.
	minFeH : ``float``
		Minimum [Fe/H] defining the metallicity bin.
	maxFeH : ``float``
		Maximum [Fe/h] defining the metallicity bin.
	bins : ``int`` or array-like [default : 10]
		Either the number of bins to use in computing the distribution
		(i.e. type ``int``) or the bins themselves (i.e. array-like).
	"""
	stars = filter_multioutput_stars(stars,
		int(min_rgal / ZONE_WIDTH),
		int(max_rgal / ZONE_WIDTH) - 1,
		min_absz, max_absz, min_mass = 0.0)
	stars = stars.filter(
		"[Fe/H]", ">=", min_FeH).filter(
		"[Fe/H]", "<=", max_FeH)
	print(len(stars["mass"]))
	dist, bins = np.histogram(stars["[O/Fe]"],
		bins = bins, weights = stars["mass"], density = True)
	xvals = [(a + b) / 2. for a, b in zip(bins[1:], bins[:-1])]
	return [xvals, dist]


def model_data_legend(ax):
	r"""
	Produce a legend with handles distinguishing between model and APOGEE data.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to put the legend on.
	"""
	# simply put a few dummy lines with the appropriate line-style and color
	model, = ax.plot([-10, -9], [-10, -9], linestyle = '-',
		c = named_colors()["black"], label = "Model")
	data, = ax.plot([-10, -9], [-10, -9], linestyle = ':',
		c = named_colors()["black"], label = "APOGEE")
	kwargs = {
		"loc": 			mpl_loc("upper center"),
		"ncol": 		1,
		"frameon": 		False,
		"fontsize": 	20
	}

	# then just draw the legend and remove the dummy lines.
	ax.legend(**kwargs)
	model.remove()
	data.remove()


def setup_axes():
	r"""
	Setup the 3x5 matplotlib axes to plot on. Return them as 2-D ``list``.
	"""
	fig, axes = plt.subplots(ncols = 5, nrows = 3, figsize = (20, 12),
		sharex = True, facecolor = "white")
	for i in range(3):
		for j in range(5):
			if i != 2: plt.setp(axes[i][j].get_xticklabels(), visible = False)
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			axes[i][j].set_xlim(XLIM)
			axes[i][j].set_ylim(YLIM)
			if i:
				axes[i][j].set_yticks([0, 5, 10, 15])
			else:
				axes[i][j].set_yticks([0, 5, 10, 15, 20])
				axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
					[3, 5, 7, 9, 11][j], [5, 7, 9, 11, 13][j]), fontsize = 25)
			axes[i][j].set_xticks([0.0, 0.1, 0.2, 0.3])
			if j == 0: axes[i][j].text(0.0, 16,
				r"$\left|z\right|$ = %g - %g kpc" % (
					[1, 0.5, 0][i], [2, 1, 0.5][i]),
				fontsize = 25)
	axes[2][2].set_xlabel("[O/Fe]")
	axes[1][0].set_ylabel("PDF")
	return axes

