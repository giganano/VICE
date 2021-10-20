r"""
Produces a scatterplot of 10,000 randomly selected model-predicted stellar
populations in [O/Fe]-[Fe/H] space for 15 galactic regions color-coded by
galactocentric radius of birth.

This script produces Fig. 7 of Johnson et al. (2021).
"""

from ..._globals import ZONE_WIDTH, COLORMAP
from .. import env
from ..utils import zheights, filter_multioutput_stars
from .utils import named_colors, dummy_background_axes
import matplotlib.pyplot as plt
import numpy as np
import vice

# The bin edges in radius in kpc defining galactic regions
RADII = [3, 5, 7, 9, 11, 13, 15]

# The bin edges in height above/below the midplane in kpc defining
# galactic regions
HEIGHTS = [0.0, 0.5, 1.0, 2.0]

# x-axis limits for [Fe/H]
FEH_LIM = [-1.3, 0.8]

# y-axis limits for [O/Fe]
OFE_LIM = [-0.1, 0.5]

# positions of ticks on the x-axis for [Fe/H]
FEH_TICKS = [-1, -0.5, 0, 0.5]


def main(output, comparison, stem, colormap = "winter", N = 10000):
	r"""
	Produce a 15-panel figure showing a scatter plot of randomly sampled
	stellar populations in [O/Fe]-[Fe/H] space color-coded by birth radius for
	different present-day galactic regions.

	Parameters
	----------
	output : ``str``
		The relative or absolute path to the VICE output whose predicted
		[O/Fe]-[Fe/H] distribution is to be visualized.
	comparison : ``str``
		The relative or absolute path to the VICE output whose predicted
		gas-phase track for the solar circle (R = 8 kpc) will be plotted as a
		reference in all panels.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	colormap : ``str`` [default : "winter"]
		The colormap to use in color-coding stellar populations by their
		birth radius.
	N : ``int`` [default : 10,000]
		The number of stellar populations to sample in each galactic region.
	"""
	axes = setup_axes()
	dummy = axes[-1]
	axes = axes[:-1]
	outputs = [vice.output(_) for _ in [output, comparison]]
	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
		i.name)[:i.stars.size[0]]]
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			sc = scatterplot_subsample(axes[i][j],
				filter_multioutput_stars(outputs[0].stars,
					int(RADII[j] / ZONE_WIDTH),
					int(RADII[j + 1] / ZONE_WIDTH) - 1,
					HEIGHTS[-2 - i], HEIGHTS[-1 - i], min_mass = 0),
				colormap = colormap, N = N)
			plot_solar_annulus_track(axes[i][j], outputs[1])
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95])
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical")
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10)
	cbar.set_ticks(range(2, 16, 2))
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, wspace = 0, bottom = 0.08, left = 0.06,
		right = 0.93)
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1,
		axes[-1][-1].get_position().y0,
		0.025,
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0
	])
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))
	plt.close()


def scatterplot_subsample(ax, stars, colormap = "winter", N = 10000):
	r"""
	Randomly draw some number of stellar populations from the abundances
	predicted by VICE and plot them in [O/Fe]-[Fe/H] space.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	stars : ``vice.core.dataframe.tracers._tracers``
		The model predicted stellar populations from the VICE output. Assumed
		to already be filtered for a specific galactic region.
	colormap : ``str`` [default : "winter"]
		The colormap to use in color-coding by birth radius.
	N : ``int`` [default : 1e5]
		The number of stellar populations to sample.

	Returns
	-------
	sc : ``matplotlib.collections.PathCollection``
		The scalar mappable with which to construct a colorbar for the figure.

	.. note:: The probability that a stellar population is sampled by this
		algorithm is proportional to its present-day mass.
	"""
	np.random.seed(seed = 0)
	masses = [a * (1 - vice.cumulative_return_fraction(b)) for a, b in zip(
		stars["mass"], stars["age"])]
	mass_fracs = [_ / sum(masses) for _ in masses]
	indeces = np.random.choice(list(range(len(masses))), p = mass_fracs,
		size = N)
	birth_radii = [(stars["zone_origin"][_] + 0.5) * ZONE_WIDTH for _ in indeces]
	kwargs = {
		"c": 			birth_radii,
		"s": 			0.1,
		"rasterized": 	True,
		"cmap": 		plt.get_cmap(COLORMAP),
		"vmin": 		0,
		"vmax": 		15
	}
	return ax.scatter(
		[stars["[Fe/H]"][_] for _ in indeces],
		[stars["[O/Fe]"][_] for _ in indeces],
		**kwargs)


def plot_solar_annulus_track(ax, output):
	r"""
	Plots the track for the solar circle (R = 8 kpc) as a reference on a given
	subplot.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	output : ``vice.multioutput``
		The abundances predicted by VICE for the given model.
	"""
	zone = output.zones["zone%d" % (int(8 / ZONE_WIDTH))]
	ax.plot(zone.history["[Fe/H]"], zone.history["[O/Fe]"],
		c = named_colors()["black"])


def setup_axes():
	r"""
	Setup the 5x3 panel figure of matplotlib subplots to plot on.
	"""
	fig, axes = plt.subplots(ncols = 5, nrows = 3, figsize = (25, 15),
		sharex = True, facecolor = "white")
	axes = axes.tolist()
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(),
				visible = False)
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			axes[i][j].set_xlim(FEH_LIM)
			axes[i][j].set_xticks(FEH_TICKS)
			axes[i][j].set_ylim(OFE_LIM)
			if i:
				axes[i][j].set_yticks([-0.1 + 0.1 * _ for _ in range(6)])
			else:
				axes[i][j].set_yticks([-0.1 + 0.1 * _ for _ in range(7)])
				axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
					RADII[j], RADII[j + 1]), fontsize = 25)
			if j == 2: axes[i][j].text(-0.3, 0.4,
				r"$\left|z\right|$ = %g - %g" % (HEIGHTS[-2 - i],
					HEIGHTS[-1 - i]), fontsize = 25)


	dummy = dummy_background_axes(axes)
	dummy.set_xlabel("[Fe/H]", labelpad = 30)
	dummy.set_ylabel("[O/Fe]", labelpad = 60)
	axes.append(dummy)

	return axes

