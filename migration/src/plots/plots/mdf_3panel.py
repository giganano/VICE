r"""
This script produces 3-panel figures showing either the [Fe/H] or [O/H]
distributions in 3 bins in z for different galactocentric radii. Can be shown
in comparison to APOGEE DR16.
"""


from ..._globals import ZONE_WIDTH
from .. import env
from ..utils import zheights, filter_multioutput_stars
from .utils import named_colors, mpl_loc, markers, dummy_background_axes
from .metallicity_gradient import target_mode_abundance
import matplotlib.pyplot as plt
import numpy as np
import vice


def main(element, outputs, stem, radial_bins = [3, 5, 7, 9, 11, 13, 15],
	z_bins = [0.0, 0.5, 1.0, 2.0],
	labels = ["Inside-Out", "Late-Burst", "Outer-Burst"],
	# apogee = False,
	colors = ["black", "red", "gold", "green", "blue", "darkviolet"]):
	r"""
	For some element X, plot the metallicity distribution functions (MDFs) in
	[X/H] in different galactic regions as predicted by a given VICE model,
	with or without a comparison to the APOGEE data.

	Parameters
	----------
	element : ``str``
		The element X to plot the distributions in [X/H] for. Must be included
		in the model output.
	outputs : ``list`` [elements of type ``str``]
		A list of relative or absolute or absolute paths to the VICE outputs to
		predictions of.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	radial_bins : ``list`` [default : [3, 5, 7, 9, 11, 13, 15]]
		The bin-edges in galactocentric radius in kpc in which to compute the
		MDFs. Must be in ascending order.
	z_bins : ``list`` [default : [0.0, 0.5, 1.0, 2.0]]
		The bin-edges in height above/below the disk midplane in kpc in which
		to compute the MDFs. Must be in ascending order. Sign is neglected.
	labels : ``list`` [elements of type ``str``]
		[default : ["Inside-Out", "Late-Burst", "Outer-Burst"]]
		A descriptor to attach to each of the ``outputs`` to distinguish which
		panel belongs to which model visually.
	apogee : ``bool`` [default : False]
		Whether or not to plot the APOGEE data for comparison in another column
		of panels.
	colors : ``list`` [elements of type ``str``]
		[default : ["black", "red", "gold", "green", "blue", "darkviolet"]]
		The colors to use for each bin in radius. Must contain at least one
		the number of elements in ``radial_bins`` minus 1.

	The output figure will show each model as a column of panels, with a row
	for each bin in |z|, and bins in radius shown color-coded on the same panel.
	Points will be plotted at the top of the bottom row of panels corresopnding
	to what the mode abundance would be if it followed the Johnson et al.
	(2021) adopted form exactly.

	.. note:: The distributions will be normalized such that the area over
		their extent is equal to one.
	"""
	apogee = True # used to be keyword argument

	# finish setting up the subplots
	axes = setup_axes(element, ncols = len(outputs) + int(apogee),
		nrows = len(z_bins) - 1)
	if apogee: labels.append("APOGEE DR16")
	for i in range(len(axes[0])): axes[0][i].set_title(labels[i], fontsize = 25)
	z_bins = list(sorted(z_bins))[::-1] # reverse ordering -> high z at top
	for i in range(len(axes)): axes[i][-1].set_ylabel(
		r"$\left|z\right|$ = %g - %g" % (z_bins[i + 1], z_bins[i]))

	# read in the model-predicted data, calculate the plot distributions for
	# all models in all regions
	outputs = [vice.output(_) for _ in outputs]
	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
		i.name)[:i.stars.size[0]]]
	for i in range(len(axes[-1])):
		for j in range(len(radial_bins) - 1):
			axes[-1][i].scatter(target_mode_abundance(radial_bins[j]),
				{"o": 4.25, "fe": 3.4}[element.lower()],
				c = named_colors()[colors[j]],
				marker = markers()["point"], s = 40, zorder = 10)
	for i in range(len(z_bins) - 1):
		for j in range(len(outputs)):
			for k in range(len(radial_bins) - 1):
				plot_predicted_mdf(axes[i][j], element, outputs[j].stars,
					radial_bins[k], radial_bins[k + 1], z_bins[i + 1],
					z_bins[i], colors[k])
					# label = k in [2 * i, 2 * i + 1] and not j)
		if apogee:
			for k in range(len(radial_bins) - 1):
				plot_apogee_distributions(axes[i][-1], element, radial_bins[k],
					radial_bins[k + 1], z_bins[i + 1], z_bins[i], colors[k],
					label = not i)
		else: pass

	# plot the legends and save the figure
	# legend_kwargs = {
	# 	"loc": 				mpl_loc("upper left"),
	# 	"ncol": 			1,
	# 	"fontsize": 		20,
	# 	"frameon": 			False,
	# 	"bbox_to_anchor": 	(0.01, 0.99),
	# 	"handlelength": 	0
	# }
	# for i in range(len(z_bins) - 1):
	# 	leg = axes[i][0].legend(**legend_kwargs)
	# 	for j in range(len(leg.legendHandles)):
	# 		leg.get_texts()[j].set_color(colors[len(leg.legendHandles) * i + j])
	# 		leg.legendHandles[j].set_visible(False)
	legend_kwargs = {
		"loc": 				mpl_loc("upper right"),
		"ncol": 			1,
		"fontsize": 		18,
		"frameon": 			False,
		"bbox_to_anchor": 	(0.99, 0.99),
		"handlelength": 	0
	}
	axes[0][1].legend(**legend_kwargs)
	for i in range(len(radial_bins) - 1):
		leg.get_texts()[i].set_color(colors[i])
		leg.legendHandles[i].set_visible(False)
	plt.tight_layout()
	plt.subplots_adjust(wspace = 0, hspace = 0, bottom = 0.1, left = 0.08)
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))
	plt.close()


def plot_predicted_mdf(ax, element, stars, min_rgal, max_rgal, min_absz,
	max_absz, color, label = False):
	r"""
	Plot the metallicity distribution (MDF) for a given element in a given
	galactic region.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	element : ``str``
		The element X to plot the [X/H] distribution for. Must be included in
		the model output.
	stars : ``vice.core.dataframe._tracers.tracers``
		The VICE model-predicted stellar population data.
	min_rgal : ``float``
		The minimum galactocentric radius in kpc defining the region.
	max_rgal : ``float``
		The maximum galactocentric radius in kpc defining the region.
	min_absz : ``float``
		The minimum height above/below the disk midplane |z| in kpc defining
		the region.
	max_absz : ``float``
		The maximum height above/below the disk midplane |z| in kpc defining
		the region.
	color : ``str``
		The name of the color to plot the distribution in.
	label : ``bool`` [default : False]
		Whether or not to produce a legend handle for the plotted distribution.
	"""
	xvals, mdf = get_mdf(element, stars, min_rgal, max_rgal, min_absz, max_absz)
	kwargs = {"c": 	named_colors()[color]}
	if label: kwargs["label"] = r"%g - %g" % (min_rgal, max_rgal)
	ax.plot(xvals, mdf, **kwargs)


def plot_apogee_distributions(ax, element, min_rgal, max_rgal, min_absz,
	max_absz, color, label = False):
	r"""
	Plots the APOGEE DR16 distributions in a given galactic region for a
	specific element.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	element : ``str``
		The element X to plot the [X/H] distribution for. Must be included
		in the model output.
	min_rgal : ``float``
		The minimum galactocentric radius in kpc defining the region.
	max_rgal : ``float``
		The maximum galactocentric radius in kpc defining the region.
	min_absz : ``float``
		The minimum height above/below the disk midplane |z| in kpc defining
		the region.
	max_absz : ``float``
		The maximum height above/below the disk midplane |z| in kpc defining
		the region.
	color : ``str``
		The name of the color to plot the distribution in.
	"""
	xvals, mdf = get_mdf(element, apogee_data(), min_rgal, max_rgal, min_absz,
		max_absz)
	kwargs = {"c": named_colors()[color]}
	if label: kwargs["label"] = "%g - %g kpc" % (min_rgal, max_rgal)
	ax.plot(xvals, mdf, **kwargs)


def apogee_data():
	r"""
	Import the APOGEE DR16 data. Transfers the data into a ``vice.dataframe``
	object to make use of the ``get_mdf`` function in calculating the
	distribution.
	"""
	raw = np.genfromtxt("./data/dr16stars.dat")
	data = vice.dataframe({
		"[o/h]": 		[_[4] for _ in raw],
		"[fe/h]": 		[_[6] for _ in raw],
		"rgal": 		[_[11] for _ in raw],
		"abszfinal": 	[abs(_[12]) for _ in raw]
	})
	data["zone_final"] = [int(_ / ZONE_WIDTH) for _ in data["rgal"]]
	data["[o/fe]"] = [a - b for a, b in zip(data["[o/h]"], data["[fe/h]"])]
	data["mass"] = len(data["rgal"]) * [1.]
	data["age"] = len(data["rgal"]) * [0.]
	return data


def get_mdf(element, stars, min_rgal, max_rgal, min_absz, max_absz,
	window = 0.2):
	r"""
	Calculate the metallicity distribution function (MDF) for a given element
	in a given galactic region.

	Parameters
	----------
	element : ``str``
		The element X to calculate the [X/H] distribution for. Must be included
		in the model output.
	stars : ``vice.core.dataframe._tracers.tracers``
		The model predicted stellar population data.
	min_rgal : ``float``
		Minimum galactocentric radius in kpc defining the region.
	max_rgal : ``float``
		Maximum galactocentric radius in kpc defining the region.
	min_absz : ``float``
		The minimum height above/below the disk midplane |z| in kpc defining
		the region.
	max_absz : ``float``
		The maximum height above/below the disk midplane |z| in kpc defining
		the region.
	window : ``float`` [default : 0.2]
		The total width of the box-car smoothing "window" in calculating the
		distribution. Counts will be included around [X/H] +/- ``window / 2``.

	Returns
	-------
	xvals : ``list``
		The [X/H] values at which the distribution is measured.
	dist : ``list``
		The values of the MDF at that abundance. Normalized such that the
		integral over the extent of the distribution is equal to one.
	"""
	stars = filter_multioutput_stars(stars, int(min_rgal / ZONE_WIDTH),
		int(max_rgal / ZONE_WIDTH) - 1, min_absz, max_absz, min_mass = 0)
	xvals = [-1. + 0.01 * _ for _ in range(201)]
	dist = len(xvals) * [0.]
	for i in range(len(xvals)):
		filtered_stars = stars.filter("[%s/H]" % (element), ">=",
			xvals[i] - window / 2)
		filtered_stars = filtered_stars.filter("[%s/H]" % (element), "<=",
			xvals[i] + window / 2)
		dist[i] = sum([a * (1 - vice.cumulative_return_fraction(b)) for a, b
			in zip(filtered_stars["mass"], filtered_stars["age"])])
	norm = sum(dist) * (xvals[1] - xvals[0])
	dist = [_ / norm for _ in dist]
	return [xvals, dist]


def setup_axes(element, ncols = 1, nrows = 3):
	r"""
	Produce the 1x3 grid of subplots to plot the distributions on. Returns them
	as a ``list``.
	"""
	fig, axes = plt.subplots(ncols = ncols, nrows = nrows,
		figsize = (ncols * 5, 10), sharex = True, facecolor = "white")
	for i in range(nrows):
		for j in range(ncols):
			if i != nrows - 1: plt.setp(axes[i][j].get_xticklabels(),
				visible = False)
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			# axes[i][j].set_xlim([-0.7, 0.7])
			axes[i][j].set_xlim([{"o": -0.7, "fe": -0.9}[element.lower()], 0.7])
			axes[i][j].set_ylim([0, {"o": 4.5, "fe": 3.6}[element.lower()]])
			axes[i][j].set_xticks([-0.5, 0.0, 0.5])
			if j == ncols - 1: axes[i][j].yaxis.set_label_position("right")

	dummy = dummy_background_axes(axes)
	dummy.set_xlabel("[%s/H]" % (element.capitalize()), labelpad = 30)
	dummy.set_ylabel("PDF", labelpad = 15)

	return axes

