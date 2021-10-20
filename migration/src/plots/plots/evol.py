r"""
Produces a plot of the densities of infall, star formation, and gas as a
function of simulation time for all models.
"""

from .. import env
from .utils import (named_colors, mpl_loc, yticklabel_formatter,
	dummy_background_axes)
from ..._globals import ZONE_WIDTH
import matplotlib.pyplot as plt
import math as m
import vice

# y-axis limits for SFR in Msun yr^-1 kpc^-2
SFR_LIM = [1.1e-4, 0.3]

# y-axis limit for infall rate in Msun yr^-1 kpc^-2
IFR_LIM = [2.e-3, 0.3]

# y-axis limit for gas surface density in Msun kpc^-2
GAS_LIM = [3.e6, 3.e8]

# x-axis limits for time in Gyr
TIME_LIM = [-1, 13]

# Galactocentric radii in kpc to plot the three quantities for.
RADII = [3, 5, 7, 9, 11, 13, 15]

# Colors to show each annulus's evolution in.
COLORS = ["grey", "black", "red", "gold", "green", "blue", "darkviolet"]

# Model names
MODELS = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"]


def main(static, insideout, lateburst, outerburst, stem):
	r"""
	Plot the surface densities of star formation, infall, and gas as functions
	of time for the four SFH models described in Johnson et al. (2021).

	Parameters
	----------
	static : ``str``
		The relative path to the VICE output with a constant SFH.
	insideout : ``str``
		The relative path to the VICE output with an inside-out SFH.
	lateburst : ``str``
		The relative path to the VICE output with a late-burst SFH.
	outerburst : ``str``
		The relative path to the VICE output with an outer-burst SFH.
	stem : ``str``
		The relative or absolute path to the output image, with no extension.
		This function will save the figure in both PDF and PNG formats.
	"""
	axes = setup_axes()
	plot_evolution([row[0] for row in axes], vice.output(static), label = True)
	plot_evolution([row[1] for row in axes], vice.output(insideout))
	plot_evolution([row[2] for row in axes], vice.output(lateburst))
	plot_evolution([row[3] for row in axes], vice.output(outerburst))
	leg = axes[1][0].legend(loc = mpl_loc("upper center"), ncol = 4,
		frameon = False, bbox_to_anchor = (0.5, 0.99), handlelength = 0,
		columnspacing = 0.8, fontsize = 20)
	for i in range(len(RADII)):
		leg.get_texts()[i].set_color(COLORS[i])
		leg.legendHandles[i].set_visible(False)
	plt.tight_layout()
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.08)
	plt.savefig("%s.png" % (stem))
	plt.savefig("%s.pdf" % (stem))


def plot_evolution(axes, output, label = False):
	r"""
	Plot each of the three quantities as functions of simulation time for
	a given model.

	Parameters
	----------
	axes : ``list``
		The list of matplotlib subplots to plot on. The star formation history
		will be plotted on the 0th element; the infall history on the 1st
		element, and the gas density on the 2nd element.
	output : ``vice.multioutput``
		The VICE output containing the model predicted data.
	label : ``bool`` [default : False]
		Whether or not to place a legend handle for the plotted curve.
	"""
	zones = ["zone%d" % (int(i / ZONE_WIDTH)) for i in RADII]
	for i in range(len(zones)):
		kwargs = {"c": named_colors()[COLORS[i]]}
		if label: kwargs["label"] = "%g kpc" % (RADII[i])
		sigma_sfr = [j / (m.pi * ((RADII[i] + ZONE_WIDTH)**2 - RADII[i]**2))
			for j in output.zones[zones[i]].history["sfr"]]
		sigma_ifr = [j / (m.pi * ((RADII[i] + ZONE_WIDTH)**2 - RADII[i]**2))
			for j in output.zones[zones[i]].history["ifr"]]
		sigma_gas = [j / (m.pi * ((RADII[i] + ZONE_WIDTH)**2 - RADII[i]**2))
			for j in output.zones[zones[i]].history["mgas"]]
		axes[0].plot(output.zones[zones[i]].history["time"], sigma_sfr,
			**kwargs)
		axes[1].plot(output.zones[zones[i]].history["time"], sigma_ifr,
			**kwargs)
		axes[2].plot(output.zones[zones[i]].history["time"], sigma_gas,
			**kwargs)


def setup_axes():
	r"""
	Setup the 3x4 axes to plot :math:`\dot{\Sigma}_\star`,
	:math:`\dot{\Sigma}_\text{in}`, and :math:`\Sigma_\text{gas}` as functions
	of time for all models. Returns them as a 3x4 list.
	"""
	fig, axes = plt.subplots(ncols = 4, nrows = 3, figsize = (20, 15),
		facecolor = "white")
	ylabels = [
		r"$\dot{\Sigma}_\star$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]",
		r"$\dot{\Sigma}_\text{in}$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]",
		r"$\Sigma_\text{gas}$ [M$_\odot$ kpc$^{-2}$]"
	]
	for i in range(len(axes)):
		for j in range(len(axes[i])):
			axes[i][j].set_yscale("log")
			axes[i][j].set_xlim(TIME_LIM)
			axes[i][j].set_ylim([SFR_LIM, IFR_LIM, GAS_LIM][i])
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(),
				visible = False)
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False)
			if i == 0: axes[i][j].set_title(MODELS[j], fontsize = 25)
		axes[i][0].set_ylabel(ylabels[i])
		if i != len(axes) - 1: yticklabel_formatter(axes[i][0])

	dummy = dummy_background_axes(axes)
	dummy.set_xlabel("Time [Gyr]")

	return axes

