"""
Produces Fig. 7 of Johnson & Weinberg (2019), a 3-column by 2-row plot,
showing the 2- and 5-Gyr gas-driven (top row) and efficiency-driven (bottom
row) starburst models. The star formation and infall rates are plotted in
the left panel, the [Sr/Fe] tracks in the middle panels, and the normed
stellar [Sr/Fe] distributions in the right panels. The SFE timescale is
plotted beneath the SFR in the bottom row.
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
		axes[i][0].xaxis.set_ticks(list(range(0, 12, 2)))
		axes[i][0].set_xlim([-1, 11])
		axes[i][1].set_xlim([-1.7, 0.2])
		axes[i][1].set_ylim([-0.21, -0.04])
		axes[i][2].set_xlim([-0.21, -0.04])
		axes[i][2].set_ylim([0.2, 50])
	axes[0][1].yaxis.set_ticks([-0.2, -0.15, -0.1, -0.05])
	axes[1][1].yaxis.set_ticks([-0.2, -0.15, -0.1, -0.05, 0.0])
	axes[1][1].set_ylim([-0.21, 0.01])
	axes[1][2].set_xlim([-0.21, 0.01])
	axes[1].insert(1, visuals.append_subplot_below(axes[1][0]))
	axes[0][0].set_ylim([-1, 15])
	axes[1][0].set_ylim([-1, 7])
	axes[1][1].set_ylim([0.8, 2.2])
	visuals.set_labels_3axes(axes[0], "Sr")
	visuals.set_labels_4axes(axes[1], "Sr")
	return axes


def plot_gas_driven_models(axes):
	"""
	Plots the gas-driven starburst models in the top row of panels.

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axes
	"""
	visuals.plot_output_3axes(axes, "../../simulations/sudden_2Gyr_5e9Msun",
		"crimson", "Sr")
	visuals.plot_output_3axes(axes, "../../simulations/sudden_5Gyr_5e9Msun",
		"deepskyblue", "Sr")
	visuals.plot_output_3axes(axes, "../../simulations/default", "black",
		"Sr", second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[1],
		vice.history("../../simulations/default"), element = "Sr")


def plot_eff_driven_models(axes):
	"""
	Plots the efficiency-driven starburst models in the bottom row of panels.

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axes
	"""
	visuals.plot_output_4axes(axes, "../../simulations/SFEdriven_2Gyr",
		"crimson", "Sr")
	visuals.plot_output_4axes(axes, "../../simulations/SFEdriven_5Gyr",
		"deepskyblue", "Sr")
	visuals.plot_output_4axes(axes, "../../simulations/default", "black",
		"Sr", second_linestyle = ':')
	visuals.plot_track_points_intervals(axes[2],
		vice.history("../../simulations/default"), element = "Sr")


def main():
	"""
	Produces the figure and save it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_gas_driven_models(axes[0])
	plot_eff_driven_models(axes[1])
	visuals.legend(axes[0][1], ["black", "crimson", "deepskyblue"],
		["No Burst", "2 Gyr", "5 Gyr"])
	visuals.legend(axes[1][2], ["black", "crimson", "deepskyblue"],
		["No Burst", "2 Gyr", "5 Gyr"])
	visuals.sfr_ifr_legend(axes[0][0])
	for i in range(2):
		visuals.yticklabel_formatter(axes[i][-1])
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

