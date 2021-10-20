"""
Produces Fig. 3 of Johnson & Weinberg (2019), a 3-column by 1-row plot
showing the effect of an outflow smoothing time on starburst model predictions.
The left panel shows the inflow and star formation rates with the SFE timescale
plotted beneath them, the [O/Fe]-[Fe/H] tracks in the middle panel, and the
stellar probability density in the right panel.
"""

import visuals
import matplotlib.pyplot as plt
import vice
import sys


def setup_axes():
	"""
	Sets up the 3x2 axis grid with the proper axis labels and ranges and the
	associated insets

	Returns
	=======
	axes :: list
		The axes, indexable via axes[row number][column number]
	"""
	axes = visuals.subplots(1, 3, figsize = (21, 7))
	axes.insert(1, visuals.append_subplot_below(axes[0]))
	visuals.set_labels_4axes(axes, "O")
	visuals.hide_xticklabels(axes[0])
	axes[0].set_ylim([-1, 16])
	axes[0].set_xlim([-1, 11])
	axes[1].set_ylim([1.3, 2.5])
	axes[2].set_xlim([-1.7, 0.1])
	axes[2].set_ylim([0., 0.5])
	axes[3].set_xlim([-0.1, 0.5])
	axes[3].set_ylim([0.15, 50])
	axes[1].yaxis.set_ticks([1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
	axes[1].xaxis.set_ticks(list(range(0, 12, 2)))
	return axes


def plot_ifr(ax, name, color):
	"""
	Plots the gas inflow rate on a given matplotlib subplot given the name of
	the VICE output

	Parameters
	==========
	ax :: subplot
		The matplotlib axis to plot the inflow rate on
	name :: str
		The name of the VICE output
	color :: str
		The name of the color to plot in
	"""
	out = vice.output(name)
	ax.plot(out.history["time"], out.history["ifr"], linestyle = '--',
		c = visuals.colors()[color])


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	visuals.plot_output_4axes(axes,
		"../../simulations/sudden_5Gyr_5e9Msun_schmidt", "crimson", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/sudden_5Gyr_5e9Msun_ts1p0_schmidt", "deepskyblue",
		"O")
	visuals.plot_output_4axes(axes, "../../simulations/sudden_5Gyr_5e9Msun",
		"black", "O", second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[2],
		vice.history("../../simulations/sudden_5Gyr_5e9Msun"))
	visuals.sfr_ifr_legend(axes[0])
	visuals.legend(axes[2], ["black", "crimson", "deepskyblue"],
		[r"$\tau_*\propto M_\text{g}^0$ \qquad$\tau_\text{s}$ = 0",
		r"$\tau_*\propto M_\text{g}^{-1/2}$\quad$\tau_\text{s}$ = 0",
		r"$\tau_*\propto M_\text{g}^{-1/2}$\quad$\tau_\text{s}$ = 1 Gyr"])
	plot_ifr(axes[0], "../../simulations/sudden_5Gyr_5e9Msun_schmidt",
		"crimson")
	plot_ifr(axes[0], "../../simulations/sudden_5Gyr_5e9Msun_ts1p0_schmidt",
		"deepskyblue")
	plot_ifr(axes[0], "../../simulations/sudden_5Gyr_5e9Msun",
		"black")
	plt.tight_layout()
	visuals.yticklabel_formatter(axes[3])
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

