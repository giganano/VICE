"""
Produces Fig. 6 of Johnson & Weinberg (2019), a 2-column by 1-row plot showing
the effect of different assumptions of the Sr CCSN yield on [Sr/Fe]-[Fe/H]
tracks and stellar [Sr/Fe] distributions.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys

def setup_axes():
	"""
	Sets up the 2x1 axis grid with the proper axis labels and ranges

	Returns
	=======
	axes :: list
		The axes objects themselves
	"""
	axes = visuals.subplots(1, 2, figsize = (14, 7))
	axes[1].set_yscale("log")
	axes[0].set_xlabel("[Fe/H]")
	axes[0].set_ylabel("[Sr/Fe]")
	axes[1].set_xlabel("[Sr/Fe]")
	axes[1].set_ylabel("Stellar Probability Density")
	axes[0].set_xlim([-2.2, 0.2])
	axes[0].set_ylim([-2.4, 0.4])
	axes[1].set_xlim([-1.4, 0.4])
	axes[1].set_ylim([0.05, 50])
	return axes


def plot_output(axes, name, color):
	"""
	Plots a VICE output on the output figure

	Parameters
	==========
	axes :: 1-D list
		The list of matplotlib axis objects to plot on
	name :: str
		The name of the VICE output
	color :: str
		The name of the color to plot in
	"""
	out = vice.output(name)
	axes[0].plot(out.history["[Fe/H]"], out.history["[Sr/Fe]"],
		c = visuals.colors()[color])
	bin_centers = list(map(lambda x, y: (x + y) / 2., out.mdf["bin_edge_left"],
		out.mdf["bin_edge_right"]))
	axes[1].plot(bin_centers, out.mdf["dn/d[sr/fe]"],
		c = visuals.colors()[color])


def plot_legend(ax):
	"""
	Draws the legend denoting the yield assumptions

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	"""
	lines = 4 * [None]
	colors = ["black", "deepskyblue", "lime", "crimson"]
	labels = [r"Constant $y_\text{Sr}^\text{CC}$",
		r"$y_\text{Sr}^\text{CC} \propto 1 - e^{-kZ}$",
		r"$y_\text{Sr}^\text{CC} \propto Z$",
		r"$y_\text{Sr}^\text{CC}$ = 0"]
	for i in range(4):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()["white"],
			label = labels[i])[0]
	leg = ax.legend(loc = visuals.mpl_loc()["upper left"], ncol = 1,
		bbox_to_anchor = (0.0, 0.99), frameon = False, handlelength = 0)
	for i in range(4):
		lines[i].remove()
		leg.get_texts()[i].set_color(colors[i])


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_output(axes, "../../simulations/default", "black")
	plot_output(axes, "../../simulations/yccsr_zero", "crimson")
	plot_output(axes, "../../simulations/yccsr_linear", "lime")
	plot_output(axes, "../../simulations/yccsr_1-exp", "deepskyblue")
	visuals.plot_track_points_intervals(axes[0],
		vice.history("../../simulations/default"), element = "Sr",
		reference = "Fe")
	plot_legend(axes[1])
	plt.tight_layout()
	visuals.yticklabel_formatter(axes[1])
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

