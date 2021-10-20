r"""
Plots the age-metallicity relation (AMR) within the disk in for a set of
four models.
"""

from ... import env
from ...utils import zheights, weighted_median, feuillet2019_data
from ..utils import (named_colors, mpl_loc, markers, xticklabel_formatter,
	dummy_background_axes)
from .galactic_regions import (plot_amr, median_ages, feuillet2019_amr, OH_LIM,
	FEH_LIM, TIME_LIM)
import matplotlib.pyplot as plt
import vice


def main(element, outputs, stem, radii = [[5, 7], [7, 9], [9, 11], [11, 13]],
	feuillet2019 = True,
	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"],
	**subplots_adjust_kwargs):

	r"""
	Produce a plot comparing the age-[X/H] relation predicted by a set of
	models in various galactic regions.

	Parameters
	----------
	element : ``str``
		The element X in age-[X/H] relation.
	outputs : array-like [elements of type ``str``]
		The relative or absolute paths to the VICE outputs whose predicted
		age-[X/H] relations are to be visualized.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	radii : ``list`` [elements are two-component ``list``s storing ``float``s]
		[default : [[5, 7], [7, 9], [9, 11], [11, 13]]]
		The ranges in radius defining the galactic regions to visualize the
		age-[X/H] relation within.
	feuillet2019 : ``bool`` [default : True]
		Whether or not to include the measurements of Feuillet et al. (2019)
		[1]_ as a comparison.
	labels : ``list`` [elements of type ``str``]
		Short descriptors distinguishing which model is which in the
		visualization. Models will be plotted in the order in which they appear
		in the ``outputs`` array.
	subplots_adjust_kwargs : varying types
		Additional keywords to pass to ``pyplot.subplots_adjust``.


	.. [1] Feuillet et al. (2019), MNRAS, 489, 1742
	"""

	axes = setup_axes(element, nrows = len(outputs), radii = radii,
		labels = labels)
	outputs = [vice.output(_) for _ in outputs]
	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
			i.name)[:i.stars.size[0]]]
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			# majority of the plotting and calculations done by these
			# functions in galactic_regions.py
			print([i, j])
			sc = plot_amr(axes[i][j], element, 'h', outputs[i], radii[j][0],
				radii[j][1], 0.0, 0.5)
			median_ages(axes[i][j], element, 'h', outputs[i], radii[j][0],
				radii[j][1], 0.0, 0.5, label = not i and not j and feuillet2019)
			if feuillet2019: feuillet2019_amr(axes[i][j], element, 'h',
				radii[j][0], radii[j][1], 0.0, 0.5,
				label = not i and not j)
	
	# legend, colorbar, and subplots formatting
	if feuillet2019:
		legend_kwargs = {
			"ncol": 			1,
			"frameon": 			False,
			"fontsize": 		20,
			"loc": 				mpl_loc("lower left"),
			"bbox_to_anchor": 	(0.01, 0.01)
		}
		axes[0][0].legend(**legend_kwargs)
	else: pass
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95])
	cbar = plt.colorbar(sc, cax = cbar_ax, orientation = "vertical")
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10)
	cbar.set_ticks(range(2, 16, 2))
	plt.tight_layout()
	default_adjustments = {
		"hspace": 		0,
		"wspace": 		0,
		"left": 		0.09,
		"right": 		0.91
	}
	for i in subplots_adjust_kwargs.keys():
		default_adjustments[i] = subplots_adjust_kwargs[i]
	plt.subplots_adjust(**default_adjustments)
	cbar_ax.set_position([
		axes[-1][-1].get_position().x1,
		axes[-1][-1].get_position().y0,
		0.025,
		axes[0][-1].get_position().y1 - axes[-1][-1].get_position().y0
	])
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))


def setup_axes(element, nrows = 4, radii = [[5, 7], [7, 9], [9, 11], [11, 13]],
	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"]):

	r"""
	Setup the array of matplotlib subplot objects. If there is only one row
	of panels, return them as a 1-D ``list``, and as a 2-D ``list`` in the
	event of multiple rows of panels.
	"""

	fig, axes = plt.subplots(ncols = len(radii), nrows = nrows,
		figsize = (len(radii) * 5, nrows * 5), sharex = True,
		facecolor = "white")
	axes = axes.tolist()
	if nrows == 1: axes = [axes]
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(),
				visible = False)
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			if i == 0: axes[i][j].set_title(r"$R_\text{gal}$ = %g - %g kpc" % (
				radii[j][0], radii[j][1]), fontsize = 25)
			axes[i][j].set_xlim(TIME_LIM)
			axes[i][j].set_xscale("log")
			xticklabel_formatter(axes[i][j])
			axes[i][j].set_ylim({"o": OH_LIM, "fe": FEH_LIM}[element.lower()])
			if labels is not None and j == len(axes[i]) - 1: axes[i][j].text(
				0.5, 0.4, labels[i], fontsize = 20)

	dummy = dummy_background_axes(axes)
	dummy.set_xlabel("Age [Gyr]", labelpad = 30)
	dummy.set_ylabel("[%s/H]" % (element.capitalize()), labelpad = 60)
	plt.setp(dummy.get_xticklabels(), visible = False)
	plt.setp(dummy.get_yticklabels(), visible = False)

	return axes

