r"""
This script produces a 2x2 panel figures compairing four Age-[O/Fe] relations
in a given galactic regions predicted by different models.

In Johnson et al. (2021), this script produces Figs. 13a and 13b.
"""

from ..._globals import ZONE_WIDTH, COLORMAP
from .. import env
from ..utils import (zheights, weighted_median, filter_multioutput_stars,
	feuillet2019_data)
from .utils import (named_colors, mpl_loc, markers, xticklabel_formatter,
	dummy_background_axes)
from .amr.galactic_regions import feuillet2019_amr
from astropy.io import fits
import matplotlib.pyplot as plt
import vice

# y-axis limits for [O/Fe]
OFE_LIM = [-0.2, 0.5]

# x-axis limits for age in Gyr (note: log-scaled x-axis)
TIME_LIM = [0.4, 18]

# bins in [O/Fe] in which to measure mass-weighted median age
BINS = [-1. + 0.02 * i for i in range(101)]


def main(upperleft, upperright, lowerleft, lowerright, stem,
	min_rgal = 7, max_rgal = 9, min_absz = 0, max_absz = 0.5,
	names = [["Constant SFR", "Inside-Out"], ["Late-Burst", "Outer-Burst"]]):
	r"""
	Plot a 2x2 panel figure showing comparing the model-predicted age-[O/Fe]
	relations to the Feuillet et al. (2019) [1]_ measurements in a given
	galactic region.

	Parameters
	----------
	upperleft : ``str``
		The relative or absolute path to the VICE output whose predicted
		age-[O/Fe] relation is to go in the upper-left panel.
	upperright: ``str``
		The relative or absolute path to the VICE output whose predicted
		age-[O/Fe] relation is to go in the upper-right panel.
	lowerleft : ``str``
		The relative or absolute  path to the VICE output whose predicted
		age-[O/Fe] relation is to go in the lower-left panel.
	lowerright : ``str``
		The relative or absolute path to the VICE output whose predicted
		age-[O/Fe] relation is to go in the lower-right panel.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	min_rgal : ``float`` [default : 7.0]
		Minimum galactocentric radius in kpc.
	max_rgal : ``float`` [default : 9.0]
		Maximum galactocentric radius in kpc.
	min_absz : ``float`` [default : 0.0]
		Minimum height above/below the disk midplane |z| in kpc.
	max_absz : ``float`` [default : 0.5]
		Maximum height above/below the disk midplane |z| in kpc.
	names : 2x2 element ``list`` [elements of type ``str``]
		[default : [["Constant SFR", "Inside-Out"], ["Late-Burst",
		"Outer-Burst"]]]
		Short descriptors for each model to denote which is which on each
		panel.

	.. [1] Feuillet et al. (2019), MNRAS, 489, 1742
	"""
	global MIN_RGAL
	global MAX_RGAL
	global MIN_ABSZ
	global MAX_ABSZ
	global ZONE_MIN
	global ZONE_MAX
	MIN_RGAL = min_rgal
	MAX_RGAL = max_rgal
	MIN_ABSZ = min_absz
	MAX_ABSZ = max_absz
	ZONE_MIN = int(MIN_RGAL / ZONE_WIDTH)
	ZONE_MAX = int((MAX_RGAL - ZONE_WIDTH) / ZONE_WIDTH)
	axes = setup_axes()
	outputs = [
		[vice.output(upperleft), vice.output(upperright)],
		[vice.output(lowerleft), vice.output(lowerright)]
	]
	for i in range(2):
		for j in range(2):
			axes[i][j].text(1, 0.4, names[i][j], fontsize = 18)
			feuillet2019_amr(axes[i][j], "O", "Fe", min_rgal, max_rgal,
				min_absz, max_absz, label = not i and not j)
			outputs[i][j].stars["abszfinal"] = [abs(k) for k in zheights(
				outputs[i][j].name)[:outputs[i][j].stars.size[0]]]
			sc = plot_relation(axes[i][j], outputs[i][j],
				label = i == 0 and j == 0)
	axes[0][0].legend(loc = mpl_loc("upper left"), ncol = 1, frameon = False,
		bbox_to_anchor = (0.01, 0.87), handletextpad = 0.4, fontsize = 18)
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95])
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical")
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10)
	cbar.set_ticks(range(2, 16, 2))
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.15, bottom = 0.1,
		right = 0.85)
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1,
		axes[-1][-1].get_position().y0,
		0.05,
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0
	])
	plt.savefig("%s.pdf" % (stem))
	plt.savefig("%s.png" % (stem))


def plot_relation(ax, output, label = False):
	r"""
	Plot the model-predicted age-[O/Fe] relation.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	output : ``vice.multioutput``
		The output object containing the multizone output data.
	label : ``bool`` [default : False]
		Whether or not to put a legend label on the points.
	"""

	# First scatter plot all stellar populations in the background
	stars = filter_multioutput_stars(output.stars, ZONE_MIN, ZONE_MAX,
		MIN_ABSZ, MAX_ABSZ)
	colors = [ZONE_WIDTH * (i + 0.5) for i in stars["zone_origin"]]
	sc = ax.scatter(stars["age"], stars["[O/Fe]"], c = colors, s = 0.1,
		cmap = plt.get_cmap(COLORMAP), vmin = 0, vmax = 15, rasterized = True)

	# measure population-averaged trend
	ages = (len(BINS) - 1) * [0.]
	lowers = (len(BINS) - 1) * [0.]
	uppers = (len(BINS) - 1) * [0.]
	for i in range(len(ages)):
		stars_ = stars.filter("[O/Fe]", ">=", BINS[i])
		stars_ = stars_.filter("[O/Fe]", "<=", BINS[i + 1])
		if len(stars_["age"]) > 20:
			masses = [a * (1 - vice.cumulative_return_fraction(b)) for a, b in
				zip(stars_["mass"], stars_["age"])]
			ages[i] = weighted_median(stars_["age"], masses)
			lowers[i] = weighted_median(stars_["age"], masses, stop = 0.16)
			uppers[i] = weighted_median(stars_["age"], masses, stop = 0.84)
		else:
			ages[i] = lowers[i] = uppers[i] = float("nan")

	# plot black squares and error bars for trend in mass-weighted median
	xerr = [
		[ages[i] - lowers[i] for i in range(len(ages))],
		[uppers[i] - ages[i] for i in range(len(ages))]
	]
	kwargs = {
		"xerr": 		xerr,
		"yerr": 		(BINS[1] - BINS[0]) / 2.,
		"c": 			named_colors()["black"],
		"marker": 		markers()["square"],
		"linestyle": 	"None"
	}
	if label: kwargs["label"] = "Model"
	ax.errorbar(ages, [(a + b) / 2. for a, b in zip(BINS[1:], BINS[:-1])],
		**kwargs)
	return sc


def setup_axes():
	r"""
	Setup the 2x2 axes to plot the age-[O/Fe] relation on. Returns them as a
	2-D ``list``.
	"""
	fig = plt.figure(figsize = (10, 10), facecolor = "white")
	axes = 2 * [None]
	for i in range(2):
		axes[i] = 2 * [None]
		for j in range(2):
			axes[i][j] = fig.add_subplot(221 + 2 * i + j)
			axes[i][j].set_xscale("log")
			axes[i][j].set_xlim(TIME_LIM)
			axes[i][j].set_ylim(OFE_LIM)
			if i == 0:
				plt.setp(axes[i][j].get_xticklabels(), visible = False)
			else:
				xticklabel_formatter(axes[i][j])
			if j == 1: plt.setp(axes[i][j].get_yticklabels(), visible = False)

	dummy = dummy_background_axes(axes)
	dummy.set_xlabel("Age [Gyr]", labelpad = 30)
	dummy.set_ylabel("[O/Fe]", labelpad = 60)
	return axes

