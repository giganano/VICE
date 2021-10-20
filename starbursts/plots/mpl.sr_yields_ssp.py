"""
Produces Fig. 5 of Johnson & Weinberg (2019), a 3-column by 1-row plot
showing the Sr yields from AGB stars and the enrichment behavior from single
stellar populations.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import math as m
import vice
import sys

# set initial yield parameters
vice.yields.ccsne.settings["sr"] = lambda z: 3.5e-8 * (z / 0.014)
vice.yields.ccsne.settings["fe"] = 0.0012
vice.yields.sneia.settings["sr"] = 0.0
vice.yields.sneia.settings["fe"] = 0.0017

# colors to plot in
_COLORS_ = ["black", "purple", "blue", "cyan", "green", "gold", "orange",
		"orangered", "red", "maroon"]

# adopted solar metallicity
_Z_SOLAR_ = 0.014

def setup_axes():
	"""
	Sets up the 3x1 axis grid with the proper axis labels and ranges

	Returns
	=======
	axes :: list
		The axes objects themselves
	"""
	axes = visuals.subplots(1, 3, figsize = (21, 7))
	axes[0].set_xlabel(r"Stellar Mass [$M_\odot$]")
	axes[0].set_ylabel(r"Sr Fractional Yield [$\times10^{-7}$]")
	axes[1].set_xlabel(r"$\log_{10}(Z/Z_\odot)$")
	axes[1].set_ylabel(r"$M_\text{Sr}/M_*\ [\times10^{-8}]$")
	axes[2].set_xlabel("Time [Gyr]")
	axes[2].set_ylabel(r"$M_\text{x}/M_\text{x,final}$")
	axes[2].set_xscale("log")
	axes[0].set_ylim([-0.5, 8.5])
	axes[0].set_xlim([0.8, 6.8])
	axes[0].xaxis.set_ticks(range(1, 7))
	axes[1].set_xlim([-4.2, 0.2])
	axes[1].set_ylim([-1, 11])
	axes[2].set_xlim([0.011, 15])
	axes[2].set_ylim([0.36, 1.04])
	return axes


def plot_sr_AGB_yields(ax):
	"""
	Plots the Cristallo et al. (2011) yields at each metallicity as a function
	of mass.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	"""
	y, m, z = vice.yields.agb.grid("sr") # Cristallo et al. (2011) yields
	for i in range(len(z)):
		# Offset by factor of 10^7 in this panel
		plot_AGB_yields_fixed_Z(ax, m, [1.e7 * j[i] for j in y], _COLORS_[i])
	plot_AGB_legend(ax, z)


def plot_AGB_yields_fixed_Z(ax, m, y, color):
	"""
	Plots AGB star yields as a function of mass on a given subplot

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	m :: list
		The stellar masses
	y :: list
		The fractional yields
	color :: str
		The name of the color to plot the yields in
	"""
	ax.scatter(m, y, c = visuals.colors()[color],
		marker = visuals.markers()["circle"])
	ax.plot(m, y, c = visuals.colors()[color])


def plot_AGB_legend(ax, z):
	"""
	Draws the legend for the AGB yields on the subplot

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	z :: list
		The metallicities
	"""
	lines = len(z) * [None]
	for i in range(len(z)):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()["white"],
			label = "Z = %g" % (z[i]))[0]
	leg = ax.legend(loc = visuals.mpl_loc()["upper right"], ncol = 1,
		bbox_to_anchor = (0.99, 0.99), frameon = False, handlelength = 0)
	for i in range(len(z)):
		lines[i].remove()
		leg.get_texts()[i].set_color(_COLORS_[i])


def plot_fractional_ssp_yields_sr_fe(ax):
	"""
	Plot the fractional yields of Sr and Fe from single stellar populations as
	a function of time.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	"""
	y, m, z = vice.yields.agb.grid("sr")
	for i in [2, 4, 6, 8]:
		plot_fractional_ssp_yield(ax, "sr", _COLORS_[i], '-', z[i], "plaw")
	plot_fractional_ssp_yield(ax, "fe", "black", ':', 0.014, "plaw")
	plot_fractional_ssp_yield(ax, "fe", "black", "--", 0.014, "exp")
	plot_ssp_legend(ax)


def plot_fractional_ssp_yield(ax, element, color, linestyle, z, ria):
	"""
	Plot the fractional single stellar population yield for a given element
	and metallicity of the stellar population.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	element :: str
		The element to plot the enrichment of
	color :: str
		The name of the color to plot in
	linestyle :: str
		The matplotlib linestyle to use
	z :: real number
		The metallicity of the stellar population
	ria :: real number
		The SN Ia DTD to adopt
	"""
	mass, times = vice.single_stellar_population(element, Z = z, RIa = ria)
	final = mass[-1]
	fractional = [i/final for i in mass]
	ax.plot(times, fractional, c = visuals.colors()[color],
		linestyle = linestyle)


def plot_yield_against_metallicity(ax, element, color, linestyle):
	"""
	Plots the late-time fractional yield of a given element against
	metallicity.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	element :: str
		The element to plot the yield of
	color :: str
		The name of the color to plot in
	linestyle :: str
		The linestyle to adopt
	"""
	MonH = [-4. + 0.01 * i for i in range(401)]
	fractional = len(MonH) * [0.]
	for i in range(len(fractional)):
		mass, times = vice.single_stellar_population(element,
			Z = _Z_SOLAR_ * 10**MonH[i])
		fractional[i] = 1.e8 * mass[-1] / 1.e6
	ax.plot(MonH, fractional, c = visuals.colors()[color],
		linestyle = linestyle)


def plot_ssp_legend(ax):
	"""
	Draws the labels for the SN Ia DTD

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	"""
	lines = 2 * [None]
	labels = [r"$R_\text{Ia}\propto t^{-1.1}$",
		r"$R_\text{Ia}\propto e^{-t/\tau_\text{Ia}}$"]
	for i in range(2):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()["black"],
			label = labels[i], linestyle = [':', '--'][i])[0]
	leg = ax.legend(loc = visuals.mpl_loc()["upper left"], ncol = 1,
		bbox_to_anchor = (0.01, 0.99), frameon = False)
	for i in range(2):
		lines[i].remove()


def plot_vs_metallicity_legend(ax):
	"""
	Plots the legend on the late-time panel denoting the form of the adopted
	CCSN yield of Sr

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	"""
	lines = 4 * [None]
	labels = [r"$y_\text{Sr}^\text{CC} = 0$",
		r"Constant $y_\text{Sr}^\text{CC}$",
		r"$y_\text{Sr}^\text{CC} \propto Z$",
		r"$y_\text{Sr}^\text{CC} \propto 1 - e^{-kZ}$"]
	colors = ["black", "crimson", "lime", "deepskyblue"]
	for i in range(len(lines)):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()["white"],
			label = labels[i])[0]
	leg = ax.legend(loc = visuals.mpl_loc()["upper left"], ncol = 1,
		bbox_to_anchor = (0.02, 0.98), frameon = False, handlelength = 0)
	for i in range(len(lines)):
		lines[i].remove()
		leg.get_texts()[i].set_color(colors[i])


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_sr_AGB_yields(axes[0])
	plot_fractional_ssp_yields_sr_fe(axes[2])
	vice.yields.ccsne.settings["sr"] = 0.0
	plot_yield_against_metallicity(axes[1], "Sr", "black", '-')
	vice.yields.ccsne.settings["sr"] = 3.5e-08
	plot_yield_against_metallicity(axes[1], "Sr", "crimson", '-')
	vice.yields.ccsne.settings["sr"] = lambda z: 3.5e-8 * (z / 0.014)
	plot_yield_against_metallicity(axes[1], "Sr", "lime", '-')
	vice.yields.ccsne.settings["sr"] = lambda z: 1.e-7 * (1 - m.exp(
		-10 * (z / 0.014)))
	plot_yield_against_metallicity(axes[1], "Sr", "deepskyblue", '-')
	vice.yields.ccsne.settings["sr"] = 3.5e-8
	plot_vs_metallicity_legend(axes[1])
	plt.tight_layout()
	visuals.xticklabel_formatter(axes[2])
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

