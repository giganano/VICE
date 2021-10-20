"""
Produces the 2-panel figure showing the cumulative return fraction and the
main sequence mass fraction for VICE's science documentation.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import vice
vice.mlr.setting = "hpt2000"

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"
mpl.rcParams["errorbar.capsize"] = 5
mpl.rcParams["axes.linewidth"] = 2
mpl.rcParams["xtick.major.size"] = 16
mpl.rcParams["xtick.major.width"] = 2
mpl.rcParams["xtick.minor.size"] = 8
mpl.rcParams["xtick.minor.width"] = 1
mpl.rcParams["ytick.major.size"] = 16
mpl.rcParams["ytick.major.width"] = 2
mpl.rcParams["ytick.minor.size"] = 8
mpl.rcParams["ytick.minor.width"] = 1
mpl.rcParams["axes.labelsize"] = 30
mpl.rcParams["xtick.labelsize"] = 25
mpl.rcParams["ytick.labelsize"] = 25
mpl.rcParams["legend.fontsize"] = 30
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["ytick.right"] = True
mpl.rcParams["xtick.top"] = True
mpl.rcParams["xtick.minor.visible"] = True
mpl.rcParams["ytick.minor.visible"] = True


def setup_axis(which = "r"):
	"""
	Sets up a subplot with the correct label
	"""
	plt.clf()
	fig = plt.figure(figsize = (5, 5))
	ax1 = fig.add_subplot(111, facecolor = "white")
	ax1.set_ylabel("%s(t)" % (which.lower()))
	ax1.set_xlabel("Age [Gyr]")
	ax1.set_xlim([-1, 11])
	if which.lower() == "r":
		ax1.set_ylim([0.0, 0.5])
	elif which.lower() == "h":
		ax1.set_ylim([0.4, 1.0])
	else:
		raise ValueError("Must be either r or h. Got: %s" % (which))
	ax1.xaxis.set_ticks([0, 2, 4, 6, 8, 10])
	return ax1


def plot_r(ax, IMF, color):
	"""
	Plot the cumulative return fraction

	ax :: the subplot to plot on
	IMF :: the assumed stellar initial mass function
	color :: a string denoting the color to plot in
	"""
	times = np.linspace(0, 10, 1001)
	ax.plot(times,
		[vice.cumulative_return_fraction(i, IMF = IMF) for i in times],
		c = mpl.colors.get_named_colors_mapping()[color])


def plot_h(ax, IMF, color):
	"""
	Plot the main sequence mass fraction

	ax :: the subplot to plot on
	IMF :: the assumed stellar initial mass function
	color :: a string denoting the color to plot in
	"""
	times = np.linspace(0, 10, 1001)
	ax.plot(times,
		[vice.main_sequence_mass_fraction(i, IMF = IMF) for i in times],
		c = mpl.colors.get_named_colors_mapping()[color])
	# ax.plot(ax.get_xlim(),
	# 	2 * [vice.main_sequence_mass_fraction(10 * 8**-3.5, IMF = IMF)],
	# 	c = mpl.colors.get_named_colors_mapping()[color],
	# 	linestyle = ':')


def legend(ax, IMFs, colors, loc = 4):
	"""
	Produce the legend

	ax :: the subplot to put the legend on
	IMFs :: the assmed stellar initial mass functions
	colors :: the colors each IMF is plotted in
	"""
	lines = len(IMFs) * [None]
	for i in range(len(lines)):
		lines[i] = ax.plot([1, 2], [1, 2], label = IMFs[i],
			c = mpl.colors.get_named_colors_mapping()["white"])[0]
	leg = ax.legend(loc = loc, ncol = 1, frameon = False,
		handlelength = 0)
	for i in range(len(lines)):
		lines[i].remove()
		leg.get_texts()[i].set_color(colors[i])


if __name__ == "__main__":
	ax1 = setup_axis(which = "r")
	plot_r(ax1, "Salpeter", "blue")
	plot_r(ax1, "Kroupa", "crimson")
	legend(ax1, ["Kroupa", "Salpeter"], ["crimson", "blue"], loc = 4)
	plt.tight_layout()
	plt.savefig("r.pdf")
	plt.savefig("r.png")
	plt.clf()

	ax2 = setup_axis(which = "h")
	plot_h(ax2, "Salpeter", "blue")
	plot_h(ax2, "Kroupa", "crimson")
	legend(ax2, ["Kroupa", "Salpeter"], ["crimson", "blue"], loc = 1)
	plt.tight_layout()
	plt.savefig("h.pdf")
	plt.savefig("h.png")
	plt.clf()
