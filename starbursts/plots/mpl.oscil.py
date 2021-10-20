"""
Produces Fig. 9 of Johnson & Weinberg (2019), a 3-column by 2-row plot showing
the oscillatory history models. Infall rates, star formation histories, and
SFE timescales are shown in the left hand panels, [O/Fe]-[Fe/H] tracks in the
middle panels, and normed stellar [O/Fe] distributions in the right hand
panels.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys
import warnings
warnings.filterwarnings("ignore")


def setup_axes():
	"""
	Sets up the 3x2 axis grid with the proper axis labels and ranges and the
	associated insets

	Returns
	=======
	axes :: list
		The axes, indexable via axes[row number][column number]
	insets :: list
		The insets, indexable via insets[row number]
	"""
	inset_xlim = [-0.26, -0.06]
	inset_ylim = [0.06, 0.16]
	axes = visuals.subplots(2, 3, figsize = (21, 14))
	insets = 2 * [None]
	for i in range(2):
		axes[i][0].xaxis.set_ticks(list(range(0, 12, 2)))
		axes[i][0].set_xlim([-1, 11])
		axes[i][0].set_ylim([-1, 17])
		axes[i][1].set_xlim([-1.7, 0.2])
		axes[i][1].set_ylim([0.0, 0.5])
		axes[i][2].set_xlim([0.0, 0.5])
		axes[i][2].set_ylim([0.2, 50])
		axes[i][2].set_yscale("log")
		visuals.draw_box(axes[i][1], inset_xlim, inset_ylim)
		insets[i] = visuals.zoom_box(axes[i][1], inset_xlim, inset_ylim,
			zoom = 3.5)
	axes[0].insert(1, visuals.append_subplot_below(axes[0][0]))
	visuals.set_labels_3axes(axes[1], "O")
	visuals.set_labels_4axes(axes[0], "O")
	axes[0][0].set_ylim([2.1, 3.7])
	axes[0][1].set_ylim([1.3, 2.7])
	axes[1][0].yaxis.set_ticks(list(range(0, 18, 2)))
	return axes, insets


def plot_oscillatory_infall_model(axes, inset):
	"""
	Plots the models in which the infall rate oscillates with time

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axis objects to plot on
	inset :: subplot
		The matplotlib axis to plot the tracks inset on
	"""
	visuals.plot_output_3axes(axes, "../../simulations/SFRoscil_amp0p3_per4",
		"crimson", "O")
	visuals.plot_output_3axes(axes, "../../simulations/SFRoscil_amp0p6_per2",
		"deepskyblue", "O")
	visuals.plot_output_3axes(axes, "../../simulations/SFRoscil_amp0p3_per2",
		"black", "O")
	visuals.plot_track_points_intervals(axes[1],
		vice.history("../../simulations/SFRoscil_amp0p3_per2"))
	# visuals.plot_output_3axes(axes, "../../simulations/slow", "lime", "O")
	visuals.plot_inset(inset, "../../simulations/SFRoscil_amp0p3_per4",
		"crimson")
	visuals.plot_inset(inset, "../../simulations/SFRoscil_amp0p6_per2",
		"deepskyblue")
	visuals.plot_inset(inset, "../../simulations/SFRoscil_amp0p3_per2",
		"black")
	visuals.plot_inset(inset, "../../simulations/default", "black",
		linestyle = ":")
	visuals.plot_track_points_intervals(inset,
		vice.history("../../simulations/SFRoscil_amp0p3_per2"))
	# visuals.plot_inset(inset, "../../simulations/slow", "lime")
	visuals.plot_reference(axes)
	visuals.sfr_ifr_legend(axes[0], ncol = 2)


def plot_oscillatory_eff_model(axes, inset):
	"""
	Plots the models in which the SFE timescale oscillates with time

	Parameters
	==========
	axes :: list
		The 1-D list of matplotlib axis objects to plot on
	inset :: subplot
		The matplotlib axis to plot the tracks inset on
	"""
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEoscil_amp0p2_per4", "crimson", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEoscil_amp0p4_per2", "deepskyblue", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEoscil_amp0p2_per2", "black", "O")
	visuals.plot_track_points_intervals(axes[2],
		vice.history("../../simulations/SFEoscil_amp0p2_per2"))
	# visuals.plot_output_4axes(axes,
		# "../../simulations/slow", "lime", "O")
	visuals.plot_inset(inset,
		"../../simulations/SFEoscil_amp0p2_per4", "crimson")
	visuals.plot_inset(inset,
		"../../simulations/SFEoscil_amp0p4_per2", "deepskyblue")
	visuals.plot_inset(inset,
		"../../simulations/SFEoscil_amp0p2_per2", "black")
	visuals.plot_inset(inset,
		"../../simulations/default", "black", linestyle = ':')
	visuals.plot_track_points_intervals(inset,
		vice.history("../../simulations/SFEoscil_amp0p2_per2"))
	# visuals.plot_inset(inset,
		# "../../simulations/slow", "lime")
	visuals.plot_reference(axes)


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes, insets = setup_axes()
	plot_oscillatory_infall_model(axes[1], insets[1])
	plot_oscillatory_eff_model(axes[0], insets[0])
	plt.tight_layout()
	plt.subplots_adjust(right = 0.985)
	for i in range(2):
		visuals.yticklabel_formatter(axes[i][-1])
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

