r"""
Plots the surface density gradient as a function of galactocentric radius for a
given VICE output.

This script produces Fig. 6 of Johnson et al. (2021).
"""

from ..._globals import ZONE_WIDTH
from .. import env
import matplotlib.pyplot as plt
from .utils import named_colors, mpl_loc, markers
import math as m
import vice


def main(output, stem):
	r"""
	Plot the surface density of gas and stars as a function of galactocentric
	radius as predicted by a VICE model in comparison to that reported for the
	Milky Way by Bland-Hawthorn & Gerhard (2016) [1]_.

	Parameters
	----------
	output : ``str``
		The relative or absolute path to the VICE output whose gradient is to
		be visualized here.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.

	Notes
	-----
	This figure will assume a normalization to the Bland-Hawthorn & Gerhard
	(2016) consistent with a total stellar mass of ~6.08e+10 solar masses,
	consistent with the value reported by Licquia & Newman (2015) [2]_ for the
	total stellar mass of the Milky Way.

	Galactocentric radii will be plotted in units of kiloparces, and surface
	densities will be plotted in units of solar masses per square kiloparsec.

	.. [1] Bland-Hawthorn & Gerhard (2016), ARA&A, 54, 529
	.. [2] Licquia & Newman (2015), ApJ, 806, 96
	"""
	ax = setup_axis()
	surface_densities(ax, vice.multioutput(output))
	plt.tight_layout()
	plt.subplots_adjust(right = 0.99)
	plt.savefig("%s.pdf" % (stem))
	plt.savefig("%s.png" % (stem))


def surface_densities(ax, output):
	r"""
	Calculate and plot the surface densities as a function of radius for the
	given output.

	Parameters
	----------
	ax : ``axes``
		The matplotlib subplot to plot on.
	output : ``vice.multioutput``
		The model-predicted data from the VICE output.
	"""
	# gas and stellar densities known exactly from masses in output and the
	# area of each annulus.
	zones = ["zone%d" % (i) for i in range(int(20. / ZONE_WIDTH))]
	annuli = [ZONE_WIDTH * i for i in range(len(zones) + 1)]
	radii = len(zones) * [0.]
	stars = len(zones) * [0.]
	gas = len(zones) * [0.]
	for i in range(len(zones)):
		area = m.pi * (annuli[i + 1]**2 - annuli[i]**2)
		radii[i] = (annuli[i] + annuli[i + 1]) / 2.
		stars[i] = output.zones[zones[i]].history["mstar"][-1] / area
		if radii[i] <= 15.5:
			gas[i] = output.zones[zones[i]].history["mgas"][-1] / area
		else:
			gas[i] = float("nan")
	ax.plot(radii, [target_gradient(i) for i in radii],
		c = named_colors()["black"],
		# label = r"B-H \& G (2016)")
		label = "Stars (Milky Way)")
	ax.plot(radii, [thin_disk(i) for i in radii],
		c = named_colors()["black"], linestyle = ':')
	ax.plot(radii, [thick_disk(i) for i in radii],
		c = named_colors()["black"], linestyle = ':')
	# ax.plot(radii, stars, c = named_colors()["red"], label = "Stars")
	ax.plot(radii, stars, c = named_colors()["red"], label = "Stars (Model)")
	# ax.plot(radii, gas, c = named_colors()["blue"], label = "Gas")
	ax.plot(radii, gas, c = named_colors()["blue"], label = "Gas (Model)")

	# plot the legend, and right-align the text. By default, it's left-aligned
	# and it just doesn't look as nice for this figure.
	leg = ax.legend(loc = mpl_loc("upper right"), ncol = 1, frameon = False,
		bbox_to_anchor = (0.95, 0.99), handlelength = 0)
	# renderer = plt.gcf().canvas.get_renderer()
	# widths = [i.get_window_extent(renderer).width for i in leg.get_texts()]
	# shift = max(widths) - min(widths)
	for i in range(3):
		leg.get_texts()[i].set_color(["black", "red", "blue"][i])
		leg.legendHandles[i].set_visible(False)
		# leg.get_texts()[i].set_ha("right")
		# leg.get_texts()[i].set_position((shift, 0))
	

def target_gradient(radius):
	r"""
	The stellar surface density gradient of the Milky Way as reported by
	Bland-Hawthorn & Gerhard (2016) [1]_.

	Parameters
	----------
	radius : ``float``
		Galactocentric radius in kpc.

	Returns
	-------
	sigma : ``float``
		The total surface density of thin and thick disk stars in solar masses
		per square kiloparsec at that radius.

	Notes
	-----
	This function assumes a normalization of the gradient consistent with a
	total stellar mass of ~6.08e+10 solar masses, as reported by Licquia &
	Newman (2015) [2]_.

	.. [1] Bland-Hawthorn & Gerhard (2016), ARA&A, 54, 529
	.. [2] Licquia & Newman (2015), ApJ, 806, 96
	"""
	return thin_disk(radius) + thick_disk(radius)


def thin_disk(radius):
	r"""
	The surface density of thin disk stars in the Milky Way as reported by
	Bland-Hawthorn & Gerhard (2016) [1]_.

	Parameters
	----------
	radius : ``float``
		Galactocentric radius in kpc.

	Returns
	-------
	sigma : ``float``
		The surface density of thin disk stars only in solar masses per square
		kiloparsec at that radius.

	Notes
	-----
	This function assumes a normalization of the gradient consistent with a
	total stellar mass of ~6.08e+10 solar masses (counting the thick disk
	component), as reported by Licquia & Newman (2015) [2]_.

	.. [1] Bland-Hawthorn & Gerhard (2016), ARA&A, 56, 529
	.. [2] Licquia & Newman (2015), ApJ, 806, 96
	"""
	# sigma_0 = 1311e6
	sigma_0 = 1115e6
	rs = 2.5
	return sigma_0 * m.exp(-radius / rs)


def thick_disk(radius):
	r"""
	The surface density of thick disk stars in the Milky Way as reported by
	Bland-Hawthorn & Gerhard (2016) [1]_.

	Parameters
	----------
	radius : ``float``
		Galactocentric radius in kpc.

	Returns
	-------
	sigma : ``float``
		The surface density of thick disk stars only in solar masses per square
		kiloparsec at that radius.

	Notes
	-----
	This function assumes a normalization of the gradient consistent with a
	total stellar mass of ~6.08e+10 solar masses (counting the thick disk
	component), as reported by Licquia & Newman (2015) [2]_.

	.. [1] Bland-Hawthorn & Gerhard (2016), ARA&A, 56, 529
	.. [2] Licquia & Newman (2015), ApJ, 806, 96
	"""
	# sigma_0 = 353e6
	sigma_0 = 300e6
	rs = 2.0
	return sigma_0 * m.exp(-radius / rs)


def setup_axis():
	r"""
	Set up the matplotlib subplot to plot on. Return it as itself after
	formatting.
	"""
	fig = plt.figure(figsize = (7, 7), facecolor = "white")
	ax = fig.add_subplot(111)
	ax.set_xlabel(r"$R_\text{gal}$ [kpc]")
	ax.set_ylabel(r"$\Sigma$ [M$_\odot$ kpc$^{-2}$]")
	ax.set_yscale("log")
	ax.set_xlim([-2, 22])
	ax.set_ylim([1e5, 1e10])
	minorticks = []
	for i in range(5, 10):
		for j in range(2, 10):
			minorticks.append(j * 10**i)
	ax.yaxis.set_ticks([1e5, 1e6, 1e7, 1e8, 1e9, 1e10])
	ax.yaxis.set_ticks(minorticks, minor = True)
	ax.xaxis.set_ticks(range(0, 25, 5))
	return ax

