"""
Produces Fig. 8 of Johnson & Weinberg (2019), a 3-column by 1-row plot
showing [Sr/O]-[O/H] tracks of the smooth (left), gas-driven (middle), and
efficiency-driven (right) 5-Gyr starburst models.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import math as m
import vice
import sys
import warnings
warnings.filterwarnings("ignore")

def setup_axes():
	"""
	Sets up the 3x1 axis grid with the proper axis labels and ranges

	Returns
	=======
	axes :: list
		The axes objects themselves
	"""
	axes = visuals.subplots(1, 3, figsize = (21, 7))
	for i in range(3):
		axes[i].set_xlim([-1.6, 0.1])
	plt.subplots_adjust(top = 0.9, bottom = 0.15, right = 0.97, left = 0.08)
	# line up the middle- and right-hand panels
	pos1 = axes[1].get_position()
	pos2 = axes[2].get_position()
	pos1.x0 += pos2.x0 - pos1.x1
	pos1.x1 = pos2.x0
	axes[1].set_position(pos1)
	axes[0].set_xlabel("[O/H]")
	axes[0].set_ylabel("[Sr/O]")
	axes[1].set_ylabel("[Sr/O]")
	visuals.hide_yticklabels(axes[2])
	# use dummy axes to put x-axis label between the middle and right panels
	dummy = plt.gcf().add_subplot(122, facecolor = "white", zorder = -1)
	posd = dummy.get_position()
	posd.x0 = pos1.x0
	dummy.set_position(posd)
	dummy.set_xlabel("[O/H]", labelpad = 30)
	visuals.hide_xticklabels(dummy)
	visuals.hide_yticklabels(dummy)
	axes[0].set_ylim([-2.7, 0.2])
	for i in axes[1:]:
		i.set_xlim([-0.65, 0.1])
		i.set_ylim([-0.8, 0.2])
	return axes


def plot_track(ax, name, color):
	"""
	Plots a single [Sr/O]-[O/H] track

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	name :: str
		The name of the VICE output
	color :: str
		The name of the color to plot in
	"""
	output = vice.output(name)
	ax.plot(output.history["[O/H]"], output.history["[Sr/O]"],
		c = visuals.colors()[color])


def legend(ax):
	"""
	Draws the legend differentiating between the yield models

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the yield on
	"""
	lines = 3 * [None]
	colors = ["black", "deepskyblue", "crimson"]
	labels = [r"Constant $y_\text{Sr}^\text{CC}$",
		r"$y_\text{Sr}^\text{CC} \propto 1-e^{-kZ}$",
		r"$y_\text{Sr}^\text{CC} \propto Z$"]
	for i in range(3):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()["white"],
			label = labels[i])[0]
	leg = ax.legend(loc = visuals.mpl_loc()["lower right"], ncol = 1,
		bbox_to_anchor = (0.98, 0.02), frameon = False, handlelength = 0)
	for i in range(3):
		lines[i].remove()
		leg.get_texts()[i].set_color(colors[i])


def label(ax, text):
	"""
	Labels an axis with a given starburst model indicator

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the label on
	text :: str
		The label itself
	"""
	ax.text(-0.6, 0.05, text, fontsize = 25)


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_track(axes[0], "../../simulations/default", "black")
	plot_track(axes[0], "../../simulations/yccsr_linear", "crimson")
	plot_track(axes[0], "../../simulations/yccsr_1-exp", "deepskyblue")
	plot_track(axes[1], "../../simulations/sudden_5Gyr_5e9Msun", "black")
	plot_track(axes[1], "../../simulations/yccsr_linear_sudden_5Gyr_5e9Msun",
		"crimson")
	plot_track(axes[1], "../../simulations/yccsr_1-exp_sudden_5Gyr_5e9Msun",
		"deepskyblue")
	plot_track(axes[2], "../../simulations/SFEdriven_5Gyr", "black")
	plot_track(axes[2], "../../simulations/yccsr_linear_SFEdriven_5Gyr",
		"crimson")
	plot_track(axes[2], "../../simulations/yccsr_1-exp_SFEdriven_5Gyr",
		"deepskyblue")
	visuals.plot_track_points_intervals(axes[0],
		vice.history("../../simulations/default"), element = "Sr",
		reference = "O")
	visuals.plot_track_points_intervals(axes[1],
		vice.history("../../simulations/sudden_5Gyr_5e9Msun"), element = "Sr",
		reference = "O")
	visuals.plot_track_points_intervals(axes[2],
		vice.history("../../simulations/SFEdriven_5Gyr"), element = "Sr",
		reference = "O")
	legend(axes[0])
	label(axes[1], "Gas-Driven")
	label(axes[2], "Efficiency-Driven")
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

