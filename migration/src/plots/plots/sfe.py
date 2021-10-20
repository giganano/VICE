r"""
Produces a plot of the SFE timescale as a function of galactocentric radius at
various timestamps for a set of VICE models.

This script produces Fig. 5 of Johnson et al. (2021).
"""

from ..._globals import END_TIME, ZONE_WIDTH, MAX_SF_RADIUS
from .. import env
from .utils import (named_colors, mpl_loc, dummy_background_axes,
	yticklabel_formatter)
import matplotlib.pyplot as plt
import vice

# x-axis limits for galactocentric radius in kpc.
RGAL_LIM = [-2, 17]


def main(outputs, stem,
	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"],
	times = [2, 4, 6, 8, 10, END_TIME],
	colors = ["red", "gold", "green", "blue", "darkviolet", "black"],
	ylim = [0.5, 20], yticks = [1, 10]):

	r"""
	Produce a plot of the SFE timescale :math:`\tau_\star` as a function of
	galactocentric radius at various timestamps for a set of VICE models.

	Parameters
	----------
	outputs : ``list`` [elements of type ``str``]
		The relative or absolute paths to the VICE outputs whose predicted SFE
		timescales are to be visualized here. They will be plotted in the
		order they appear in this list.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	labels : array-like [elements of type ``str``] or ``None``
		[default : ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"]]
		Short descriptors for each of the models to be plotted. Must contain
		at least as many elements as ``outputs``. If ``None``, no labels will
		be included.
	times : array-like [elements of type ``float``]
		[default : [2, 4, 6, 8, 10, 13.2]]
		The time-stamps at which to plot the SFE timescale as a function of
		radius.
	colors : array-like [elements of type ``str``]
		[default : ["red", "gold", "green", "blue", "darkviolet", "black"]]
		The colors in which to plot the SFE timescales. Must contain at least
		as many elements as ``outputs``.
	ylim : array-like [default : [0.5, 20]]
		y-axis limits for :math:`\tau_\star` in Gyr. Note that this function
		will use a log-scaled y-axis.
	yticks : array-like [default : [1, 10]]
		The values to place major ticks on the y-axis at.
	"""

	axes = setup_axes(len(outputs))
	for i in range(len(axes)):
		axes[i].set_yscale("log")
		axes[i].set_ylim(ylim)
		axes[i].set_yticks(yticks)
		yticklabel_formatter(axes[i])
		if labels is not None: axes[i].set_title(labels[i], fontsize = 25)
	outputs = [vice.output(_) for _ in outputs]
	for i in range(len(outputs)): plot_sfe(axes[i], outputs[i],
		times, colors, label = not i)
	leg = axes[0].legend(loc = mpl_loc("upper left"), ncol = 1,
		frameon = False, bbox_to_anchor = (0.01, 0.99), handlelength = 0,
		# fontsize = 20, labelspacing = 0.2)
		fontsize = 20)
	for i in range(len(times)):
		leg.get_texts()[i].set_color(colors[i])
		leg.legendHandles[i].set_visible(False)
	plt.tight_layout()
	plt.subplots_adjust(wspace = 0, bottom = 0.2)
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))


def plot_sfe(ax, output, times, colors, label = False):
	r"""
	Plot the SFE timescales as a function of galactocentric radius at various
	timestamps for a given model.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on
	output : ``vice.multioutput``
		The predicted abundance data from the VICE output.
	times : array-like [elements of type ``float``]
		The times in Gyr at which to plot the SFE timescale.
	colors : array-like [elements of type ``str``]
		The names of the colors to plot the SFE timescales in.
	label : ``bool`` [default : False]
		Whether or not to attach legend handles to the plotted lines.
	"""
	radii = [ZONE_WIDTH * i for i in range(int(MAX_SF_RADIUS / ZONE_WIDTH))]
	zones = ["zone%d" % (i) for i in range(len(radii))]
	for i in range(len(times)):
		# store the SFE timescale at each radius in here
		tau_star = len(radii) * [0.]
		for j in range(len(tau_star)):
			# pull the exact timestamp based on the one closest to the one
			# the user specified
			delta_t = [abs(k - times[i]) for k in
				output.zones[zones[j]].history["time"]]
			idx = delta_t.index(min(delta_t))
			# conversion factor goes from yr -> Gyr
			tau_star[j] = 1.e-9 * (output.zones[zones[j]].history["mgas"][idx]
				/ output.zones[zones[j]].history["sfr"][idx])
		kwargs = {"c": named_colors()[colors[i]]}
		if label: kwargs["label"] = "%g Gyr" % (times[i])
		ax.plot(radii, tau_star, **kwargs)


def setup_axes(n_outputs):
	r"""
	Setup the Nx1 array of matplotlib subplots. Return them as a ``list``.
	"""
	fig, axes = plt.subplots(ncols = n_outputs, nrows = 1,
		figsize = (n_outputs * 7, 7), sharey = True, facecolor = "white")
	if n_outputs > 1:
		axes = axes.tolist()
	else:
		axes = [axes]
	for i in range(len(axes)):
		if i: plt.setp(axes[i].get_yticklabels(), visible = False)
		axes[i].set_xlim(RGAL_LIM)
		axes[i].set_xticks([0, 5, 10, 15])
	axes[0].set_ylabel(r"$\tau_\star$ [Gyr]")

	dummy = dummy_background_axes([axes])
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30)
	plt.setp(dummy.get_xticklabels(), visible = False)
	plt.setp(dummy.get_yticklabels(), visible = False)
	return axes

