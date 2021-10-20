r"""
This script produces a 4x2 panel figure comparing the model-predicted radial
abundance gradients of four models in [O/H], [Fe/H], and [O/Fe].

In Johnson et al. (2021), this script produces Fig. 9.
"""

from ..._globals import ZONE_WIDTH
from .. import env
from ..utils import zheights
from .utils import named_colors, mpl_loc, markers, dummy_background_axes
import matplotlib.pyplot as plt
import vice

# The maximum radius of the VICE models in kpc
MAX_RADIUS = 20.0

# The maximum radius of star formation in the VICE models in kpc
# gas gradients will be plotted only to this radius.
MAX_SF_RADIUS = 15.5

# y-axis limits for [O/H] and [Fe/H]
XH_YLIM = [-0.9, 1.2]

# y-axis limits for [O/Fe]
OFE_YLIM = [-0.2, 0.5]

# x-axis limits for galactocentric radius in kpc
XLIM = [-2, 22]


def main(farleft, midleft, midright, farright, stem,
	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"]):
	r"""
	Produce a 4x2 panel figure showing the radial metallicity gradients in
	both stars and gas predicted by four VICE models.

	Parameters
	----------
	static : ``str``
		The relative or absolute path to the VICE output whose predicted
		gradient is to be plotted in the far-left panels.
	midleft : ``str``
		The relative or absolute path to the VICE output whose predicted
		gradient is to be plotted in the middle-left panels.
	midright : ``str``
		The relative or absolute path to the VICE output whose predicted
		gradient is to be plotted in the middle-right panels.
	farright: ``str``
		The relative or absolute path to the VICE output whose predicted
		gradient is to be plotted in the far-right panels.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	labels : ``list`` [elements of type ``str``]
		[default : ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-burst"]]
		A list of descriptors of the four models to be visualized.
	"""
	axes = setup_axes(labels = labels)
	outputs = [farleft, midleft, midright, farright]
	outputs = [vice.multioutput(_) for _ in outputs]
	# static = vice.multioutput(static)
	# insideout = vice.multioutput(insideout)
	# lateburst = vice.multioutput(lateburst)
	# outerburst = vice.multioutput(outerburst)
	for i in range(4):
		plot_stellar_metallicities(axes[0][i], axes[1][i], outputs[i],
			symbols_legend = not i)
		plot_gas_phase_metallicity(axes[0][i], axes[1][i], outputs[i],
			label = not i, symbols_legend = not i)
		plot_target_gradient(axes[0][i])

	# plot_stellar_metallicities(axes[0][0], axes[1][0], static)
	# plot_stellar_metallicities(axes[0][1], axes[1][1], insideout)
	# plot_stellar_metallicities(axes[0][2], axes[1][2], lateburst)
	# plot_stellar_metallicities(axes[0][3], axes[1][3], outerburst)
	# plot_gas_phase_metallicity(axes[0][0], axes[1][0], static, label = True)
	# plot_gas_phase_metallicity(axes[0][1], axes[1][1], insideout)
	# plot_gas_phase_metallicity(axes[0][2], axes[1][2], lateburst)
	# plot_gas_phase_metallicity(axes[0][3], axes[1][3], outerburst)
	# for i in range(4): plot_target_gradient(axes[0][i])

	leg = axes[0][0].legend(loc = mpl_loc("upper right"), frameon = False,
		ncol = 1, bbox_to_anchor = (0.99, 0.99), handlelength = 0)
	for i in range(2):
		leg.get_texts()[i].set_color(["blue", "red"][i])
		leg.legendHandles[i].set_visible(False)

	axes[1][0].legend(loc = mpl_loc("upper center"), frameon = False,
		ncol = 1, bbox_to_anchor = (0.50, 0.99), fontsize = 18)

	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))


def plot_gas_phase_metallicity(ax1, ax2, out, label = False,
	symbols_legend = False):
	r"""
	Plot the present-day gas-phase gradient in [O/H], [Fe/H], and [O/Fe]
	predicted by a given model.

	Parameters
	----------
	ax1 : ``axes``
		The matplotlib subplot to plot the [O/H] and [Fe/H] gradients on.
	ax2 : ``axes``
		The matplotlib subplot to plot the [O/Fe] gradients on.
	out : ``vice.multioutput``
		The output data from VICE's calculations containing the model-predicted
		abundances.
	label : ``bool`` [default : False]
		Whether or not to attach a legend handle to plotted lines.
	symbols_legend : ``bool`` [default : False]
		Whether or not to label the line in ax2 as corresponding to the
		present-day gas-phase abundances.
	"""
	zones = ["zone%d" % (i) for i in range(int(MAX_SF_RADIUS / ZONE_WIDTH))]
	O = [out.zones[i].history["[o/h]"][-1] for i in zones]
	Fe = [out.zones[i].history["[fe/h]"][-1] for i in zones]
	OFe = [out.zones[i].history["[o/fe]"][-1] for i in zones]
	radii = [ZONE_WIDTH * (i + 0.5) for i in range(len(zones))]
	if label:
		ax1.plot(radii, Fe, c = named_colors()["blue"], label = "Fe")
		ax1.plot(radii, O, c = named_colors()["red"], label = "O")
	else:
		ax1.plot(radii, Fe, c = named_colors()["blue"])
		ax1.plot(radii, O, c = named_colors()["red"])
	if symbols_legend:
		ax2.plot(radii, OFe, c = named_colors()["black"],
			label = "Gas (Present Day)")
	else:
		ax2.plot(radii, OFe, c = named_colors()["black"])


def plot_stellar_metallicities(ax1, ax2, multioutput, symbols_legend = False):
	r"""
	Plot the stellar metallicity gradients in [O/H], [Fe/H], and [O/Fe]
	predicted by a ``milkyway`` model.

	Parameters
	----------
	ax1 : ``axes``
		The matplotlib subplot to plot the [O/H] and [Fe/H] gradients on.
	ax2 : ``axes``
		The matplotlib subplot to plot the [O/Fe] gradient on.
	multioutput : ``vice.multioutput``
		The output data from VICE's calculations containing the model-predicted
		abundance distributions.
	symbols_legend : ``bool`` [default : False]	
		Whether or not to label the points and shaded region in ax2 as
		corresponding to the median stellar abundance and dispersion in the
		stars, respectively.
	"""
	zones = ["zone%d" % (i) for i in range(int(MAX_RADIUS / ZONE_WIDTH))]
	O = [median_stellar_metallicity(multioutput.zones[i],
		"dn/d[o/h]") for i in zones]
	O_disp = [stellar_dispersion(multioutput.zones[i],
		"dn/d[o/h]") for i in zones]
	Fe = [median_stellar_metallicity(multioutput.zones[i],
		"dn/d[fe/h]") for i in zones]
	Fe_disp = [stellar_dispersion(multioutput.zones[i],
		"dn/d[fe/h]") for i in zones]
	OFe = [median_stellar_metallicity(multioutput.zones[i],
		"dn/d[o/fe]") for i in zones]
	OFe_disp = [stellar_dispersion(multioutput.zones[i],
		"dn/d[o/fe]") for i in zones]
	radii = [ZONE_WIDTH * (i + 0.5) for i in range(
		len(multioutput.zones.keys()))]
	kwargs = {
		"s": 		50,
		"zorder": 	20,
		"marker": 	markers()["point"]
	}
	# ax1.scatter(radii, O, c = named_colors()["red"],
	# 	marker = markers()["point"], s = 20, zorder = 20)
	# ax1.scatter(radii, Fe, c = named_colors()["blue"],
	# 	marker = markers()["point"], s = 20, zorder = 20)
	# ax2.scatter(radii, OFe, c = named_colors()["black"],
	# 	marker = markers()["point"], s = 20, zorder = 20)
	ax1.scatter(radii, O, c = named_colors()["red"], **kwargs)
	ax1.scatter(radii, Fe, c = named_colors()["blue"], **kwargs)
	if symbols_legend: kwargs["label"] = "Stars (median)"
	ax2.scatter(radii, OFe, c = named_colors()["black"], **kwargs)
	kwargs = {
		"alpha": 		0.2,
		"zorder": 		0
	}
	# ax1.fill_between(radii, [row[0] for row in O_disp],
	# 	[row[1] for row in O_disp], alpha = 0.3, zorder = 0,
	# 	color = named_colors()["red"])
	# ax1.fill_between(radii, [row[0] for row in Fe_disp],
	# 	[row[1] for row in Fe_disp], alpha = 0.3, zorder = 0,
	# 	color = named_colors()["blue"])
	# ax2.fill_between(radii, [row[0] for row in OFe_disp],
	# 	[row[1] for row in OFe_disp], alpha = 0.3, zorder = 0,
	# 	color = named_colors()["black"])
	ax1.fill_between(radii, [row[0] for row in O_disp],
		[row[1] for row in O_disp], color = named_colors()["red"], **kwargs)
	ax1.fill_between(radii, [row[0] for row in Fe_disp],
		[row[1] for row in Fe_disp], color = named_colors()["blue"], **kwargs)
	if symbols_legend: kwargs["label"] = r"Stars (16\% - 84\%)"
	ax2.fill_between(radii, [row[0] for row in OFe_disp],
		[row[1] for row in OFe_disp], color = named_colors()["black"], **kwargs)


def median_stellar_metallicity(zone, mdf_key):
	r"""
	Determine the median abundance within a given annulus.

	Parameters
	----------
	zone : ``vice.output``
		The VICE output containing the model-predicted data for a given
		annulus.
	mdf_key : ``str``
		The key denoting which computed metallicity distribution function to
		calculate the 50th percentile of.

	Returns
	-------
	med : ``float``
		The median [X/Y] abundance in the given zone predicted by the model.

	Notes
	-----
	VICE MDFs are normalized such that the integral over their extent is equal
	to 1. This function takes advantage of this by computing the integral by
	hand and simply stopping when it reaches 0.5.
	"""
	s = 0
	for i in range(len(zone.mdf["bin_edge_left"])):
		s += zone.mdf[mdf_key][i] * (zone.mdf["bin_edge_right"][i] -
			zone.mdf["bin_edge_left"][i])
		if s >= 0.5: return (zone.mdf["bin_edge_left"][i] +
			zone.mdf["bin_edge_right"][i]) / 2.
	raise ArithmeticError("Median not found.")


def stellar_dispersion(zone, mdf_key):
	r"""
	Determine the 16th and 84th percentiles of a metallicity distribution
	function in a given annulus.

	Parameters
	----------
	zone : ``vice.output``
		The VICE output containing the model-predicted data for a given
		annulus.
	mdf_key : ``str``
		The key denoting which computed metallicity distribution function to
		calculate the 16th and 84th percentiles of.

	Returns
	-------
	low : ``float``
		The 16th percentile of the [X/Y] distribution in the given zone.
	high : ``float``
		The 84th percentile of the [X/Y] distribution in the given zones.

	Notes
	-----
	VICE MDFs are normalized such that the integral over their extent is equal
	to 1. This function takes advantage of this by computing the integral by
	hand and simply stopping when it gets to 0.16 and 0.84.
	"""
	s = 0
	low = 0
	high = 0
	for i in range(len(zone.mdf[mdf_key])):
		s += (zone.mdf["bin_edge_right"][i] -
			zone.mdf["bin_edge_left"][i]) * zone.mdf[mdf_key][i]
		if s >= 0.16 and low == 0:
			low = (zone.mdf["bin_edge_right"][i] +
				zone.mdf["bin_edge_left"][i]) / 2.
		if s >= 0.84:
			high = (zone.mdf["bin_edge_right"][i] +
				zone.mdf["bin_edge_left"][i]) / 2.
			break
	return [low, high]


def plot_target_gradient(ax):
	r"""
	Plot the adopted gradient relating mode([:math:`\alpha`/H]) and
	galactocentric radius as adopted in Johnson et al. (2021).

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	"""
	radii = [0.01 * _ for _ in range(1551)] # 0 to 15.5 in steps of 0.01
	grad = [target_mode_abundance(_) for _ in radii]
	ax.plot(radii, grad, c = named_colors()["black"], zorder = 100)


def target_mode_abundance(radius):
	r"""
	The adopted relation between mode([:math:`\alpha`/H]) and galactocentric
	radius in Johnson et al. (2021).

	Parameters
	----------
	radius : ``float``
		Galactocentric radius in kpc.

	Returns
	-------
	mode_alpha : ``float``
		The mode alpha abundance at that radius if it followed the Johnson et
		al. (2021) gradient exactly, defined by:

		.. math:: [$\alpha$/\text{H}] = -0.08 * (\frac{R}{\text{kpc}} - 4) + 0.3

		for a given galactocentric radius :math:`R`.
	"""
	return -0.08 * (radius - 4) + 0.3


def setup_axes(
	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"]):
	r"""
	Setup the 4x2 matplotlib axes to plot on.

	Parameters
	----------
	labels : ``list``
		A list of descriptors of each of the four models whose gradients this
		script will visualize.

	Returns
	-------
	axes : ``list``
		A 2x4-element ``list`` containing the rows of subplots on the first
		axis and the columns on the second.
	"""
	fig = plt.figure(figsize = (20, 10), facecolor = "white")
	axes = 2 * [None]
	for i in range(len(axes)):
		axes[i] = 4 * [None]
		for j in range(len(axes[i])):
			if j == 0:
				axes[i][j] = fig.add_subplot(241 + 4 * i + j)
			else:
				axes[i][j] = fig.add_subplot(241 + 4 * i + j,
					sharey = axes[i][0])
			if i == 0:
				plt.setp(axes[i][j].get_xticklabels(), visible = False)
				axes[i][j].text(5, 0.9, labels[j], fontsize = 25)
				axes[i][j].set_ylim(XH_YLIM)
			else:
				axes[i][j].set_ylim(OFE_YLIM)
			axes[i][j].set_xlim(XLIM)
			axes[i][j].xaxis.set_ticks([0.0, 5.0, 10.0, 15.0, 20.0])
			if j: plt.setp(axes[i][j].get_yticklabels(), visible = False)

	axes[0][0].set_ylabel("[X/H]")
	axes[1][0].set_ylabel("[O/Fe]")
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, wspace = 0, bottom = 0.12)
	dummy = dummy_background_axes(axes)
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30)
	return axes

