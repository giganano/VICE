r"""
This script produces a plot of the birth/final radii distributions of h277
star particles in bins of their birth/final radii and age.
"""

from .. import env
from .utils import named_colors, mpl_loc, dummy_background_axes
from vice.toolkit.hydrodisk import hydrodiskstars
from ..._globals import END_TIME
import matplotlib.pyplot as plt
import numpy as np


def main(stem, age_bins = [[0, 2], [2, 4], [4, 6], [6, 8], [8, 10]],
	radial_bins = [[5, 7], [7, 9], [9, 11], [11, 13]],
	colors = ["darkviolet", "blue", "green", "gold", "red"]):
	r"""
	Create a figure showing the distributions of birth and final radii in
	bins of age for ``h277`` star particles (see Johnson et al. 2021 paper).

	Parameters
	----------
	stem : ``str``
		The full or relative path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	age_bins : ``list`` [elements are 2-element ``list``s storing ``float``s]
		[default : [[0, 2], [2, 4], [4, 6], [6, 8], [8, 10]]]
		The bin-edges in star particle ages in Gyr.
	radial_bins : ``list`` [elements are 2-element ``list``s storing ``float``s]
		[default : [[5, 7], [7, 9], [9, 11], [11, 13]]]
		The bin-edges in birth or final radius in kpc. This is required because
		distribution will be plotted for final radius in bins of birth radius,
		and vice versa. Must contain at least as many elements as ``age_bins``.
	colors : ``list`` [elements of type ``str``]
		The colors to plot these distributions in. Must contain at least as
		many elements as ``age_bins``.
	"""
	axes = setup_axes(n_columns = len(radial_bins))
	h277 = hydrodiskstars([0.1 * _ for _ in range(201)], N = 3102519)
	h277.decomp_filter([1, 2])
	h277.analog_data["age"] = [END_TIME - _ for _ in h277.analog_data["tform"]]
	for i in range(len(axes[0])):
		# note the radial bin both in text and vertical black dotted lines
		if radial_bins[i][1] >= 11:
			text_radius = 0
		else:
			text_radius = 12
		axes[0][i].text(text_radius, 0.3,
			r"$R_\text{Birth}$ = %d - %d" % (radial_bins[i][0],
				radial_bins[i][1]), fontsize = 20)
		axes[1][i].text(text_radius, 0.34,
			r"$R_\text{Final}$ = %d - %d" % (radial_bins[i][0],
				radial_bins[i][1]), fontsize = 20)
		axes[0][i].plot(2 * [radial_bins[i][0]], axes[0][i].get_ylim(),
			c = named_colors()["black"], linestyle = ':')
		axes[0][i].plot(2 * [radial_bins[i][1]], axes[0][i].get_ylim(),
			c = named_colors()["black"], linestyle = ':')
		axes[1][i].plot(2 * [radial_bins[i][0]], axes[1][i].get_ylim(),
			c = named_colors()["black"], linestyle = ':')
		axes[1][i].plot(2 * [radial_bins[i][1]], axes[1][i].get_ylim(),
			c = named_colors()["black"], linestyle = ':')

		# plotting the distributions
		for j in range(len(age_bins)):
			plot_subsample(axes[1][i], h277, radial_bins[i][0],
				radial_bins[i][1], age_bins[j][0], age_bins[j][1],
				color = colors[j])
			plot_subsample(axes[0][i], h277, radial_bins[i][0],
				radial_bins[i][1], age_bins[j][0], age_bins[j][1],
				cut = "rform", plot = "rfinal", color = colors[j],
				label = not i)

	# legend formatting
	leg = axes[0][0].legend(loc = mpl_loc("lower right"), ncol = 1,
		frameon = False, bbox_to_anchor = (0.99, 0.01), handlelength = 0)
	for i in range(len(age_bins)):
		leg.get_texts()[i].set_color(colors[i])
		leg.legendHandles[i].set_visible(False)
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.05, bottom = 0.1)
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))
	plt.close()


def plot_subsample(ax, h277, min_rgal, max_rgal, min_age, max_age,
	cut = "rfinal", plot = "rform", color = "black", label = False):
	r"""
	Calculate and plot the distribution of either birth or final radius in a
	bin of the other and age.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	h277 : ``vice.toolkit.hydrodisk.hydrodiskstars.hydrodiskstars``
		The VICE hydrodiskstars object containing the ``h277`` star particle
		data.
	min_rgal : ``float``
		Minimum galactocentric radius in kpc defining a bin edge.
	max_rgal : ``float``
		Maximum galactocentric radius in kpc defining a bin edge.
	min_age : ``float``
		Minimum stellar age in Gyr defining a bin edge.
	max_age : ``float``
		Maximum stellar age in Gyr defining a bin edge.
	cut : ``str`` [either "rfinal" or "rform"] [default : "rfinal"]
		A string denoting whether the binning is in either formation ("rform")
		or final ("rfinal") radius.
	plot : ``str`` [either "rfinal" or "rform"] [default : "rform"]
		A string denoting whether the distribution being plotted is in either
		formation ("rform") or final ("rfinal") radius.
	color : ``str`` [default : "black"]
		The color to plot the distribution in.
	label : ``bool`` [default : False]
		Whether or not to attach a legend-handle to the plotted line.
	"""
	stars = subsample(h277, min_rgal, max_rgal, min_age, max_age, which = cut)
	print(len(stars["id"]))
	xvals, pdf = calculate_pdf(stars, which = plot)
	kwargs = {"c": named_colors()[color]}
	if label: kwargs["label"] = "%g - %g Gyr" % (min_age, max_age)
	ax.plot(xvals, pdf, **kwargs)


def subsample(h277, min_rgal, max_rgal, min_age, max_age, which = "rfinal"):
	r"""
	Subsample the ``h277`` analog star particle data.

	Parameters
	----------
	h277 : ``vice.toolkit.hydrodisk.hydrodiskstars.hydrodiskstars``
		The VICE hydrodiskstars object containing the ``h277`` star particle
		data.
	min_rgal : ``float``
		Minimum galactocentric radius in kpc defining a bin edge.
	max_rgal : ``float``
		Maximum galactocentric radius in kpc defining a bin edge.
	min_age : ``float``
		Minimum stellar age in Gyr defining a bin edge.
	max_age : ``float``
		Maximum stellar age in Gyr defining a bin edge.
	which : ``str`` [either "rfinal" or "rform"] [default : "rfinal"]
		Denotes whether the filter is trained on formation ("rform") or final
		("rfinal") radii.
	"""
	return h277.analog_data.filter(
		which, ">=", min_rgal
	).filter(
		which, "<=", max_rgal
	).filter(
		"age", ">=", min_age
	).filter(
		"age", "<=", max_age
	)


def calculate_pdf(stars, which = "rform", window = 0.5):
	r"""
	Calculates the radius distribution of some subsample of ``h277`` star
	particles.

	Parameters
	----------
	stars : ``vice.dataframe``
		The subsampled star particle data from ``h277``.
	which : ``str`` [either "rform" or "rfinal"] [default : "rform"]
		Denotes whether or not the distribution is being plotted in formation
		("rform") or final ("rfinal") radius.
	window : ``float`` [default : 0.5]
		The full width of the box-car smoothing window. Stars will contribute
		to counts at some radius r if they're within r +/- ``window / 2``.

	.. note:: The distribution is normalized such that the integral over its
		extent is equal to one.
	"""
	xvals = [0.02 * i for i in range(1001)]
	if len(stars["id"]) < 0.8 * len(xvals):
		return [float("nan"), float("nan")]
	elif len(stars["id"]) < 3 * len(xvals):
		window *= 2
	else: pass
	dist = len(xvals) * [0.]
	for i in range(len(xvals)):
		test = [xvals[i] - window / 2 <= stars[which][_] <=
			xvals[i] + window / 2 for _ in range(len(stars[which]))]
		dist[i] = sum(test)
	norm = sum(dist) * (xvals[1] - xvals[0])
	dist = [_ / norm for _ in dist]
	return xvals, dist


def setup_axes(n_columns = 4):
	r"""
	Setup the Nx2 array of matplotlib subplots to plot the distributions on.
	Return them as a 2-D ``list``.
	"""
	assert isinstance(n_columns, int), "Internal Error."
	fig, axes = plt.subplots(figsize = (5 * n_columns, 10), facecolor = "white",
		nrows = 2, ncols = n_columns)
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(),
				visible = False)
			if j: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			axes[i][j].set_xlim([-2, 22])
			if i:
				axes[i][j].set_ylim([0, 0.399])
			else:
				axes[i][j].set_ylim([0, 0.36])
			axes[i][j].set_xticks([0, 5, 10, 15, 20])
	dummy = dummy_background_axes(axes)
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30)
	# dummy.set_ylabel("PDF", labelpad = 30)
	axes[0][0].set_ylabel(r"PDF($R_\text{Final}|R_\text{Birth}$)")
	axes[1][0].set_ylabel(r"PDF($R_\text{Birth}|R_\text{Final}$)")
	return axes

