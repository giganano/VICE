r"""
This script produces a plot of the age-[O/H] and age-[Fe/H] relations in the
solar annulus predicted by the simulations and in comparison to the
Feuillet et al. (2019) data.
"""

from ... import env
from ...utils import zheights, weighted_median, feuillet2019_data
from ..utils import named_colors, mpl_loc, markers, xticklabel_formatter
from .galactic_regions import plot_amr, median_ages, feuillet2019_amr
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import vice


def main(output, stem):
	r"""
	Produce a figure comparing the model-predicted age-[O/H] and age-[Fe/H]
	relations in the solar annulus as predicted by VICE in comparison to the
	relations reported by Feuillet et al. (2018, 2019) [1]_ [2]_.

	Parameters
	----------
	output : ``str``
		The relative or absolute path to the VICE output containing the
		model predicted data.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.

	.. [1] Feuillet et al. (2018), MNRAS, 477, 2326
	.. [2] Feuillet et al. (2019), MNRAS, 489, 1742
	"""
	ax1, ax2 = setup_axes()
	output = vice.output(output)
	output.stars["abszfinal"] = [abs(_) for _ in zheights(
		output.name)[:output.stars.size[0]]]
	min_radius = 7
	max_radius = 9
	min_z = 0
	max_z = 0.5

	# majority of plotting and calculations done by these functions in
	# galactic_regions.py
	plot_amr(ax1, "O", "H", output, min_radius, max_radius, min_z, max_z)
	sc = plot_amr(ax2, "Fe", "H", output, min_radius, max_radius, min_z, max_z)
	median_ages(ax1, "O", "H", output, min_radius, max_radius, min_z, max_z,
		zorder = 2)
	median_ages(ax2, "Fe", "H", output, min_radius, max_radius, min_z, max_z,
		label = True, zorder = 2)
	feuillet2019_amr(ax1, "O", "H", min_radius, max_radius, min_z, max_z,
		zorder = 2)
	feuillet2019_amr(ax2, "Fe", "H", min_radius, max_radius, min_z, max_z,
		label = True, zorder = 2)
	feuillet2018_amr(ax1, 'o')
	feuillet2018_amr(ax2, 'fe', label = True)

	# legend and colorbar formatting
	kwargs = {
		"ncol": 			1,
		"frameon": 			False,
		"fontsize": 		20,
		"loc": 				mpl_loc("lower left"),
		"bbox_to_anchor": 	(0.01, 0.01)
	}
	handles, labels = ax2.get_legend_handles_labels()
	handles = [handles[1], handles[2], handles[0]]
	labels = [labels[1], labels[2], labels[0]]
	ax2.legend(handles, labels, **kwargs)
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95])
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical")
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10)
	cbar.set_ticks(range(2, 16, 2))
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, right = 0.8)
	cbar_ax.set_position([
		ax2.get_position().x1,
		ax2.get_position().y0,
		0.05,
		ax1.get_position().y1 - ax2.get_position().y0
	])
	plt.savefig("%s.pdf" % (stem))
	plt.savefig("%s.png" % (stem))
	plt.close()


def feuillet2018_amr(ax, element, label = True):
	r"""
	Plot the age-[X/H] relation for the solar annulus reported by Feuillet et
	al. (2018) [1]_.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	element : ``str``
		The chemical element X in age-[X/H].
	label : ``bool`` [default : True]
		Whether or not to produce a legend handle for the plotted line.

	.. [1] Feuillet et al. (2018), MNRAS, 477, 2326
	"""
	raw = np.genfromtxt("./data/feuillet2018/age_%s.dat" % ({
		"o": 	"oh",
		"fe": 	"mh"
		}[element.lower()])).tolist()
	lowers = [_[0] for _ in raw]
	uppers = [_[1] for _ in raw]
	abundance = [(a + b) / 2 for a, b in zip(lowers, uppers)]
	age = [10**(_[2] - 9) for _ in raw] # -9 yr -> Gyr
	outline = pe.withStroke(linewidth = 4, foreground = "white")
	kwargs = {
		"c": 				named_colors()["darkred"],
		"path_effects": 	[outline],
		"zorder": 			1
	}
	if label: kwargs["label"] = "Feuillet et al. (2018)"
	ax.plot(age, abundance, **kwargs)


def setup_axes():
	r"""
	Setup the two matplotlib subplots to illustrate the age-[O/H] and
	age-[Fe/H] relations on. Return them as a ``list``.
	"""
	fig = plt.figure(figsize = (7, 12), facecolor = "white")
	ax2 = fig.add_subplot(212)
	ax1 = fig.add_subplot(211, sharex = ax2)
	ax2.set_xscale("log")
	ax2.set_xlim([0.4, 20])
	ax1.set_ylim([-0.8, 0.6])
	ax2.set_ylim([-1.4, 0.6])
	ax1.set_yticks([-0.5, 0.0, 0.5])
	ax2.set_yticks([-1.0, -0.5, 0.0, 0.5])
	plt.setp(ax1.get_xticklabels(), visible = False)
	xticklabel_formatter(ax2)
	ax2.set_xlabel("Age [Gyr]")
	ax2.set_ylabel("[Fe/H]")
	ax1.set_ylabel("[O/H]")
	return [ax1, ax2]

