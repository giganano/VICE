"""
Produces Fig. 11 of Johnson & Weinberg (2019), a 2-column by 2-row plot
showing the slow burst models. Star formation histories are shown in the top
left, [O/Fe]-[Fe/H] tracks in the top right, [O/Fe] and [Fe/H] against time
in the bottom left, and [O/Fe] against time in the bottom right.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys
import warnings
warnings.filterwarnings("ignore")


def setup_axes():
	"""
	Sets up the 2x2 axis grid with the proper axis labels and ranges and the
	associated insets

	Returns
	=======
	axes :: list
		The axes, indexable via axes[row number][column number]
	insets :: list
		The insets, indexable via insets[row number]
	"""
	axes = visuals.subplots(2, 2, figsize = (14, 14))
	xlabels = [["Time [Gyr]", "[Fe/H]"], ["Time [Gyr]", "Time [Gyr]"]]
	ylabels = [[r"$\dot{M}_*$ [M$_\odot$ yr$^{-1}$]", "[O/Fe]"],
		["[X/H]", "[O/Fe]"]]
	xlims = [[[-1, 16], [-1.7, 0.2]], [[-1, 16], [-1, 16]]]
	ylims = [[[-1, 13], [0.0, 0.5]], [[-0.34, 0.14], [-0.1, 0.5]]]
	for i in range(2):
		for j in range(2):
			axes[i][j].set_xlabel(xlabels[i][j])
			axes[i][j].set_ylabel(ylabels[i][j])
			axes[i][j].set_xlim(xlims[i][j])
			axes[i][j].set_ylim(ylims[i][j])
	axes[1][0].yaxis.set_ticks([-0.3, -0.2, -0.1, 0.0, 0.1])
	return axes


def plot_history(axes, name, color, linestyle = '-'):
	"""
	Plots the relevant information for a given history on the 2x2 axis grid

	Parameters
	==========
	axes :: list
		The 2x2 list of matplotlib axis objects to plot on
	name :: str
		The name of the model to plot
	color :: str
		The name of the color to use in plotting the model
	"""
	hist = vice.history(name)
	# axes[0][0].plot(hist["time"], hist["ifr"], linestyle = '--',
	# 	c = visuals.colors()[color])
	axes[0][0].plot(hist["time"], hist["sfr"], c = visuals.colors()[color],
		linestyle = linestyle)
	if linestyle == '-':
		axes[0][1].plot(hist["[Fe/H]"], hist["[O/Fe]"],
			c = visuals.colors()[color], linestyle = linestyle)
		axes[1][0].plot(hist["time"], hist["[O/H]"], linestyle = '--',
			c = visuals.colors()[color])
		axes[1][0].plot(hist["time"], hist["[Fe/H]"], linestyle = '-',
			c = visuals.colors()[color])
	else:
		axes[1][0].plot(hist["time"], hist["[O/H]"], linestyle = linestyle,
			c = visuals.colors()[color])
		axes[1][0].plot(hist["time"], hist["[Fe/H]"], linestyle = linestyle,
			c = visuals.colors()[color])
	axes[1][1].plot(hist["time"], hist["[O/Fe]"], c = visuals.colors()[color],
		linestyle = linestyle)


def draw_ofe_legend(ax):
	"""
	Draws the legend differentiating between oxygen and iron in the plot of
	[X/H] against time.

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to put the legend on
	"""
	lines = 2 * [None]
	for i in range(2):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()["black"],
			label = ["O", "Fe"][i], linestyle = ['--', '-'][i])[0]
	ax.legend(loc = visuals.mpl_loc()["upper left"], frameon = False,
		bbox_to_anchor = (0.01, 0.99))
	for i in range(2):
		lines[i].remove()


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_history(axes, "../../simulations/episodic_infall", "black",
		linestyle = ':')
	plot_history(axes, "../../simulations/constant", "black",
		linestyle = ':')
	plot_history(axes, "../../simulations/slowburst_episodic_infall",
		"crimson")
	plot_history(axes, "../../simulations/slowburst_constant", "deepskyblue")
	draw_ofe_legend(axes[1][0])
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

