"""
Produces Fig. 2 of Johnson & Weinberg (2019), a 3-column by 2-row plot showing
the effect of outflow smoothing time on the 5-Gyr gas- and efficiency-driven
starburst models. Infall and star formation histories with SFE timescales are
shown in the left-hand panels, [O/Fe]-[Fe/H] tracks in the middle panels, and
stellar [O/Fe] distributions in the right-hand panels.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys
import warnings
warnings.filterwarnings("ignore")


def setup_axes():
	"""
	Sets up the 3x2 axis grid with the proper axis labels and ranges

	Returns
	=======
	axes :: list
		The axes, indexable via axes[row number][column number]
	"""
	axes = visuals.subplots(2, 3, figsize = (21, 14))
	for i in range(2):
		axes[i][0].xaxis.set_ticks([0, 2, 4, 6, 8, 10])
		axes[i][0].set_xlim([-1, 11])
		axes[i][1].set_xlim([-1.7, 0.2])
		axes[i][1].set_ylim([-0.1, 0.5])
		axes[i][2].set_xlim([-0.1, 0.5])
		axes[i][2].set_ylim([0.2, 50])
	axes[0][1].set_ylim([0.0, 0.5])
	axes[0][2].set_xlim([0.0, 0.5])
	axes[1].insert(1, visuals.append_subplot_below(axes[1][0]))
	axes[0][0].set_ylim([-1, 15])
	axes[1][0].set_ylim([-1, 7])
	axes[1][1].set_ylim([0.8, 2.2])
	visuals.set_labels_3axes(axes[0], "O")
	visuals.set_labels_4axes(axes[1], "O")
	return axes


def plot_gas_driven_models(axes):
	"""
	Plots the gas-driven starburst models on a set of axes

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axis objects to plot on
	"""
	visuals.plot_output_3axes(axes,
		"../../simulations/sudden_5Gyr_5e9Msun_ts0p5", "crimson", "O")
	visuals.plot_output_3axes(axes,
		"../../simulations/sudden_5Gyr_5e9Msun_ts1p0", "deepskyblue", "O")
	visuals.plot_output_3axes(axes,
		"../../simulations/sudden_5Gyr_5e9Msun", "black", "O",
		second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[1],
		vice.history("../../simulations/sudden_5Gyr_5e9Msun"))


def plot_eff_driven_models(axes):
	"""
	Plots the efficiency-driven starburst models on a set of axes

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axis objects to plot on
	"""
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEdriven_5Gyr_ts0p5", "crimson", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEdriven_5Gyr_ts1p0", "deepskyblue", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEdriven_5Gyr", "black", "O",
		second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[2],
		vice.history("../../simulations/SFEdriven_5Gyr"))


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_gas_driven_models(axes[0])
	plot_eff_driven_models(axes[1])
	visuals.sfr_ifr_legend(axes[0][0])
	visuals.legend(axes[0][-1], ["black", "crimson", "deepskyblue"],
		[r"$\tau_\text{s}$ = 0", r"$\tau_\text{s}$ = 0.5 Gyr",
		r"$\tau_\text{s}$ = 1 Gyr"],
		loc = "upper right", bbox_to_anchor = (0.99, 0.99))
	for i in range(2):
		visuals.yticklabel_formatter(axes[i][-1])
	plt.tight_layout()
	plt.subplots_adjust(right = 0.985)
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

