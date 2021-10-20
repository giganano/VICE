"""
Produces Fig. 1 of Johnson & Weinberg (2019), a 3-column by 3-row plot,
showing the fiducial starburst models in [O/Fe]. The top row shows the
2- and 5-Gyr sudden onset gas-driven models, the middle row the 5-Gyr gas
driven models varying the timescale of accretion, and the bottom row the
2- and 5-Gyr efficiency-driven models. The SFE timescale is plotted beneath
the SFR in the bottom row.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys
import warnings
warnings.filterwarnings("ignore")


def setup_axes():
	"""
	Sets up the 3x3 axis grid with the proper axis labels and ranges

	Returns
	=======
	axes :: list
		The axes, indexable via axes[row number][column number]
	"""
	axes = visuals.subplots(3, 3, figsize = (21, 21))
	for i in range(3):
		axes[i][0].xaxis.set_ticks([0, 2, 4, 6, 8, 10])
		axes[i][0].set_xlim([-1, 11])
		axes[i][1].set_xlim([-1.7, 0.2])
		axes[i][1].set_ylim([0., 0.5])
		axes[i][2].set_xlim([0., 0.5])
		axes[i][2].set_ylim([0.2, 30])
	axes[2].insert(1, visuals.append_subplot_below(axes[2][0]))
	visuals.set_labels_3axes(axes[0], "O")
	visuals.set_labels_3axes(axes[1], "O")
	visuals.set_labels_4axes(axes[2], "O")
	axes[0][0].set_ylim([-1, 15])
	axes[1][0].set_ylim([-1, 21])
	axes[2][0].set_ylim([-1, 7])
	axes[2][1].set_ylim([0.8, 2.2])
	return axes


def plot_gas_driven_sudden_onset_models(axes):
	"""
	Plots the 2- and 5-Gyr sudden onset gas-driven starburst models in the top
	row.

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axes to plot on
	"""
	visuals.plot_output_3axes(axes, "../../simulations/sudden_2Gyr_5e9Msun",
		"crimson", "O")
	visuals.plot_output_3axes(axes, "../../simulations/sudden_5Gyr_5e9Msun",
		"deepskyblue", "O")
	visuals.plot_output_3axes(axes, "../../simulations/default", "black",
		"O", second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[1],
		vice.history("../../simulations/default"))


def plot_gas_driven_prolonged_models(axes):
	"""
	Plots the 5-Gyr gas driven models with varying accretion timescales.

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axes to plot on
	"""
	visuals.plot_output_3axes(axes,
		"../../simulations/prolonged_5Gyr_5e9Msun_0p5Gyr", "crimson", "O")
	visuals.plot_output_3axes(axes,
		"../../simulations/prolonged_5Gyr_5e9Msun_1p0Gyr", "deepskyblue", "O")
	visuals.plot_output_3axes(axes, "../../simulations/sudden_5Gyr_5e9Msun",
		"black", "O", second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[1],
		vice.history("../../simulations/sudden_5Gyr_5e9Msun"))


def plot_eff_driven_models(axes):
	"""
	Plots the 2- and 5-Gyr efficiency-driven starburst models

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axes to plot on
	"""
	visuals.plot_output_4axes(axes, "../../simulations/SFEdriven_2Gyr",
		"crimson", "O" )
	visuals.plot_output_4axes(axes, "../../simulations/SFEdriven_5Gyr",
		"deepskyblue", "O")
	visuals.plot_output_4axes(axes, "../../simulations/default", "black",
		"O", second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[2],
		vice.history("../../simulations/default"))


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_gas_driven_sudden_onset_models(axes[0])
	plot_gas_driven_prolonged_models(axes[1])
	plot_eff_driven_models(axes[2])
	visuals.legend(axes[0][1], ["black", "crimson", "deepskyblue"],
		["No Burst", "2 Gyr", "5 Gyr"])
	visuals.legend(axes[1][1], ["black", "crimson", "deepskyblue"],
		["Sudden", "0.5 Gyr", "1 Gyr"])
	visuals.legend(axes[2][2], ["black", "crimson", "deepskyblue"],
		["No Burst", "2 Gyr", "5 Gyr"])
	visuals.sfr_ifr_legend(axes[0][0])
	visuals.sfr_ifr_legend(axes[1][0])
	for i in range(len(axes)):
		visuals.yticklabel_formatter(axes[i][-1])
	plt.tight_layout()
	plt.subplots_adjust(right = 0.985)
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

