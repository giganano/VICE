r"""
Plots the age-[X/Y] relation for a given model in various regions of the
galaxy.

This script produces Fig. 14 of Johnson et al. (2021).
"""

from ...._globals import ZONE_WIDTH, COLORMAP
from ... import env
from ...utils import (zheights, weighted_median, feuillet2019_data,
	filter_multioutput_stars)
from ..utils import (named_colors, mpl_loc, markers, xticklabel_formatter,
	dummy_background_axes)
import matplotlib.pyplot as plt
import vice

# x-axis limits for age in Gyr (note: log-scaled)
TIME_LIM = [0.2, 20]

# y-axis limits for [O/H]
OH_LIM = [-0.9, 0.7]

# y-axis limits for [Fe/H]
FEH_LIM = [-1.2, 0.7]

# bins in [O/Fe] for computing median ages
OFE_BINS = [-0.5 + 0.02 * i for i in range(51)]

# bins in [X/H] for computing median ages.
ONH_BINS = [-1. + 0.05 * i for i in range(41)]

# The bin-edges in radius defining the galactic regions the data will be
# presented in
RADII = [5, 7, 9, 11, 13]

# The bin-edges in disk midplane distance |z| defining the regions the data
# will be presented in, in reverse order.
HEIGHTS = [2.0, 1.0, 0.5, 0.0]


def main(element_x, element_y, output, stem):
	r"""
	Illustrate the age-[X/Y] relation in 12 galactic regions as predicted by a
	given VICE model in comparison to the measurements of Feuillet et al.
	(2019) [1]_.

	Parameters
	----------
	element_x : ``str``
		The element X in age-[X/Y] relation.
	element_y : ``str``
		The element Y in age-[X/Y] relation.
	output : ``str``
		The relative or absolute path to the VICE output whose predicted
		age-[X/Y] relation is to be visualized here.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.

	.. [1] Feuillet et al. (2019), MNRAS, 489, 1742
	"""
	axes = setup_axes(element_x, element_y)[:-1]
	output = vice.output(output)
	output.stars["abszfinal"] = [abs(i) for i in zheights(
		output.name)[:output.stars.size[0]]]
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			print([i, j])
			sc = plot_amr(axes[i][j], element_x, element_y, output, RADII[j],
				RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i])
			if i == 2 and j == 1:
				xvals, yvals = median_ages(axes[i][j], element_x, element_y,
					output, RADII[j], RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i])
			else:
				median_ages(axes[i][j], element_x, element_y, output, RADII[j],
					RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i],
					label = not i and not j)
			feuillet2019_amr(axes[i][j], element_x, element_y, RADII[j],
				RADII[j + 1], HEIGHTS[i + 1], HEIGHTS[i],
				label = i == 0 and j == 0)
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			axes[i][j].plot(xvals, yvals, c = named_colors()["black"])
	legend_kwargs = {
		"ncol": 		1,
		"frameon": 		False,
		"fontsize": 	20
	}
	if element_y.lower() == 'h':
		legend_kwargs["loc"] = mpl_loc("lower left")
		legend_kwargs["bbox_to_anchor"] = (0.01, 0.01)
	else:
		legend_kwargs["loc"] = mpl_loc("upper left")
		legend_kwargs["bbox_to_anchor"] = (0.01, 0.99)
	axes[0][0].legend(**legend_kwargs)
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95])
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical")
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10)
	cbar.set_ticks(range(2, 16, 2))
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, wspace = 0, bottom = 0.08, right = 0.91,
		left = 0.09)
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1,
		axes[-1][-1].get_position().y0,
		0.025,
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0
	])
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))
	plt.close()


def feuillet2019_amr(ax, element_x, element_y, min_rgal, max_rgal, min_absz,
	max_absz, label = False, **kwargs):
	r"""
	Plot the age-[X/Y] relation as reported by Feuillet et al. (2019) [1]_.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	element_x : ``str`` [case-insensitive]
		The element X in age-[X/Y] relation.
	element_y : ``str`` [case-insensitive]
		The element Y in age-[X/Y] relation.
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
	label : ``bool`` [default : False]
		Whether or not to produce a legend handle for the plotted points with
		error bars.
	kwargs : varying types
		Additional keyword arguments to pass to ``pyplot.errorbar``.

	.. [1] Feuillet et al. (2019), MNRAS, 489, 1742
	"""
	if element_y.lower() == 'h':
		subdir = "./data/age_%s/" % ({"o": "oh", "fe": "mh"}[element_x.lower()])
		filename = "%s/ELEM_GAUSS_AGE_%02d_%02d_%02d_%02d_%s_H.fits" % (
			subdir,
			min_rgal,
			max_rgal,
			10 * min_absz,
			10 * max_absz,
			{"o": "O", "fe": "M"}[element_x.lower()])
	else:
		subdir = "./data/age_alpha/"
		filename = "%s/ELEM_GAUSS_AGE_%02d_%02d_%02d_%02d_alpha.fits" % (
			subdir, min_rgal, max_rgal, 10 * min_absz, 10 * max_absz)
	age, abundance, age_disp, abundance_disp = feuillet2019_data(filename)
	kwargs["xerr"] 		= age_disp
	kwargs["yerr"] 		= abundance_disp
	kwargs["c"] 		= named_colors()["crimson"]
	kwargs["marker"] 	= markers()["triangle_up"]
	kwargs["linestyle"] = "None"
	if label: kwargs["label"] = "Feuillet et al. (2019)"
	ax.errorbar(age, abundance, **kwargs)


def plot_amr(ax, element_x, element_y, output, min_rgal, max_rgal, min_absz,
	max_absz):
	r"""
	Produce a scatter plot of the model predicted age-[X/Y] relation in a
	given galactic region.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	element_x : ``str`` [case-insensitive]
		The element X in age-[X/Y] relation.
	element_y : ``str`` [case-insensitive]
		The element Y in age-[X/Y] relation.
	output : ``vice.multioutput``
		The model predicted abundance data from the VICE output.
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

	Returns
	-------
	sc : ``matplotlib.collections.PathCollection``
		The scalar mappable with which the color bar can be drawn.
	"""
	stars = filter_multioutput_stars(output.stars,
		int(min_rgal / ZONE_WIDTH),
		int(max_rgal / ZONE_WIDTH) - 1,
		min_absz, max_absz)
	colors = [ZONE_WIDTH * (i + 0.5) for i in stars["zone_origin"]]
	return ax.scatter(stars["age"], stars["[%s/%s]" % (element_x, element_y)],
		c = colors, s = 0.1, cmap = plt.get_cmap(COLORMAP), vmin = 0, vmax = 15,
		rasterized = True)


def median_ages(ax, element_x, element_y, output, min_rgal, max_rgal,
	min_absz, max_absz, label = False, **kwargs):
	r"""
	Calculate and plot the median stellar ages in bins of [X/H] with error bars
	denoting the 16th and 84th percentiles of the age distribution in the
	respective bins.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	element_x : ``str`` [case-insensitive]
		The element X in age-[X/Y] relation.
	element_y : ``str`` [case-insensitive]
		The element Y in age-[X/Y] relation.
	output : ``vice.multioutput``
		The model predicted abundance data from the VICE output.
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
	label : ``bool`` [default : False]
		Whether or not to produce a legend handle for the median trend.
	kwargs : varying types
		Additional keyword arguments to pass to ``pyplot.errorbar``.
	"""
	stars = filter_multioutput_stars(output.stars,
		int(min_rgal / ZONE_WIDTH),
		int(max_rgal / ZONE_WIDTH) - 1,
		min_absz, max_absz)
	if element_y.lower() == 'h':
		bins = ONH_BINS[:]
	else:
		bins = OFE_BINS[:]
	ages = (len(bins) - 1) * [0.]
	lowers = (len(bins) - 1) * [0.]
	uppers = (len(bins) - 1) * [0.]
	for i in range(len(ages)):
		stars_ = stars.filter("[%s/%s]" % (element_x, element_y), ">=",
			bins[i])
		stars_ = stars_.filter("[%s/%s]" % (element_x, element_y), "<=",
			bins[i + 1])
		if len(stars_["age"]) > 20:
			masses = [a * (1 - vice.cumulative_return_fraction(b)) for a, b in
				zip(stars_["mass"], stars_["age"])]
			ages[i] = weighted_median(stars_["age"], masses)
			lowers[i] = weighted_median(stars_["age"], masses, stop = 0.16)
			uppers[i] = weighted_median(stars_["age"], masses, stop = 0.84)
		else:
			ages[i] = lowers[i] = uppers[i] = float("nan")
	xerr = [
		[ages[i] - lowers[i] for i in range(len(ages))],
		[uppers[i] - ages[i] for i in range(len(ages))]
	]
	kwargs["xerr"] 		= xerr
	kwargs["yerr"] 		= (bins[1] - bins[0]) / 2.
	kwargs["c"] 		= named_colors()["black"]
	kwargs["marker"] 	= markers()["square"]
	kwargs["linestyle"] = "None"
	kwargs = {
		"xerr": 		xerr,
		"yerr": 		(bins[1] - bins[0]) / 2.,
		"c": 			named_colors()["black"],
		"marker": 		markers()["square"],
		"linestyle": 	"None"
	}
	if label: kwargs["label"] = "Model"
	yvals = [(a + b) / 2. for a, b in zip(bins[1:], bins[:-1])]
	ax.errorbar(ages, yvals, **kwargs)
	return [ages, yvals]


def setup_axes(element_x, element_y, zlabels = True):
	r"""
	Setup the 4x3 grid of matplotlib subplots to plot on. Returns them as a
	2-D ``list``. Appends as the final element of the list a set of invisible
	dummy axes lying behind the ones being plotted on.

	Parameters
	----------
	element_x : ``str``
		The element X in the age-[X/Y] relation.
	element_y : ``str``
		The element Y in the age-[X/Y] relation.
	zlabels : ``bool`` [default : True]
		Whether or not to place text in the left-most column of panels labeling
		the heights |z| to which the row of panels corresponds.
	"""
	fig, axes = plt.subplots(ncols = 4, nrows = 3, figsize = (20, 15),
		sharex = True, facecolor = "white")
	axes = axes.tolist()
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(),
				visible = False)
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			if i == 0: axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
				RADII[j], RADII[j + 1]), fontsize = 25)
			axes[i][j].set_xlim(TIME_LIM)
			axes[i][j].set_xscale("log")
			xticklabel_formatter(axes[i][j])
			if element_y.lower() == 'h':
				axes[i][j].set_ylim(
					{"o": OH_LIM, "fe": FEH_LIM}[element_x.lower()])
			else:
				axes[i][j].set_ylim([-0.1, 0.5])
				if i:
					axes[i][j].set_yticks([-0.1, 0.0, 0.1, 0.2, 0.3, 0.4])
				else:
					axes[i][j].set_yticks([-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
		if zlabels:
			if element_y.lower() == 'h':
				axes[i][0].text({"o": 0.7, "fe": 0.6}[element_x.lower()],
					{"o": -0.5, "fe": -0.7}[element_x.lower()],
					r"$\left|z\right|$ = %g - %g kpc" % (
					HEIGHTS[i + 1], HEIGHTS[i]), fontsize = 20)
			else:
				axes[i][0].text(0.6, 0.32,
					r"$\left|z\right|$ = %g - %g kpc" % (HEIGHTS[i + 1],
						HEIGHTS[i]), fontsize = 20)
		else: pass

	# use dummy axes to draw the x-axis label in the middle and for colorbar
	dummy = dummy_background_axes(axes)
	dummy.set_xlabel("Age [Gyr]", labelpad = 30)
	dummy.set_ylabel("[%s/%s]" % (element_x.capitalize(),
		element_y.capitalize()), labelpad = 60)
	axes.append(dummy)

	return axes

