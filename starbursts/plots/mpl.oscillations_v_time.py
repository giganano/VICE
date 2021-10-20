"""
Produces Fig. 10 of Johnson & Weinberg (2019), a 3-column by 1-row plot
showing the oscillations in [Fe/H] and [O/Fe] with time of the 20% 2-Gyr
period models.
"""

import visuals # visuals.py -> matplotlib subroutines in this directory
import matplotlib.pyplot as plt
import vice
import sys

# The min and max [Fe/H] to determine the [O/Fe] abundance within
_FEH_MIN_ = -0.3
_FEH_MAX_ = -0.2

def setup_axes():
	"""
	Sets up the 3x1 axis grid with the proper axis labels and ranges

	Returns
	=======
	axes :: list
		The axes objects themselves
	"""
	axes = visuals.subplots(1, 3, figsize = (21, 7))
	xlabels = ["Time [Gyr]", "Time [Gyr]", "[O/Fe]"]
	ylabels = ["[Fe/H]", "[O/Fe]", "Stellar Probability Density"]
	xlim = [[-1, 11], [-1, 11], [0.08, 0.22]]
	ylim = [[-0.42, -0.08], [0, 0.5], [3, 300]]
	for i in range(3):
		axes[i].set_xlabel(xlabels[i])
		axes[i].set_ylabel(ylabels[i])
		axes[i].set_xlim(xlim[i])
		axes[i].set_ylim(ylim[i])
	for i in range(2):
		axes[i].xaxis.set_ticks(range(0, 12, 2))
	axes[2].set_yscale("log")
	return axes


def get_bin_number(bins, val):
	"""
	Gets the bin number of a value in a binspace

	Parameters
	==========
	bins :: list
		The bin edges
	val :: real number
		The value to get the bin number for

	Returns
	=======
	The bin number of the test value. -1 if it is not within the binspace
	"""
	for i in range(len(bins) - 1):
		if bins[i] <= val <= bins[i + 1]: return i
	return -1


def get_ofe_pdf(out):
	"""
	Determine the [O/Fe] PDF for a given VICE output in the range of [Fe/H]
	specified.

	Parameters
	==========
	out :: vice.output
		The VICE output object containing the simulation results
	"""
	# bins = np.linspace(0, 0.3, 201)
	bins = [0.001 * i for i in range(301)]
	pdf = (len(bins) - 1) * [0.]
	for i in range(len(out.history["time"])):
		if _FEH_MIN_ <= out.history["[Fe/H]"][i] <= _FEH_MAX_:
			x = get_bin_number(bins, out.history["[O/Fe]"][i])
			if x != -1: pdf[x] += out.history["sfr"][i]
	s = 0
	for i in range(len(pdf)):
		s += pdf[i] * (bins[i + 1] - bins[i])
	for i in range(len(pdf)):
		pdf[i] /= s
	return [bins, pdf]


def plot_pdf(ax, output, color):
	"""
	Plot the [O/Fe] PDF in the specified [Fe/H] bin

	Parameters
	==========
	ax :: subplot
		The matplotlib axis object to plot on
	output :: vice.output
		The VICE output object containing the simulation results
	color :: str
		The color to plot in
	"""
	bins, pdf = get_ofe_pdf(output)
	centers = list(map(lambda x, y: (x + y) / 2., bins[1:], bins[:-1]))
	ax.plot(centers, pdf, c = visuals.colors()[color])


def plot_oscillatory(axes, output, color):
	"""
	Plot the oscillations in [O/Fe] and [Fe/H] against time

	Parameters
	==========
	axes :: list
		The list of matplotlib axis objects to plot on
	output :: vice.output
		The VICE output object containing the simulation results
	color :: str
		The name of the color to plot in

	"""
	axes[0].plot(output.history["time"], output.history["[Fe/H]"],
		c = visuals.colors()[color])
	axes[1].plot(output.history["time"], output.history["[O/Fe]"],
		c = visuals.colors()[color])


def legend(ax):
	"""
	Draws the legend denoting the oscillatory infall and efficiency models

	Parameters
	==========
	ax :: subplot
		The matplotlib subplot to put the legend on
	"""
	visuals.legend(ax, ["crimson", "deepskyblue"],
		[r"oscillatory $\dot{M}_\text{in}$", r"oscillatory $\tau_*$"],
		loc = "upper right", bbox_to_anchor = (0.99, 0.99))   	


def main():
	"""
	Produces the figure and saves it as a PDF.
	"""
	plt.clf()
	axes = setup_axes()
	plot_oscillatory(axes,
		vice.output("../../simulations/SFRoscil_amp0p3_per2"),
		"crimson")
	plot_oscillatory(axes,
		vice.output("../../simulations/SFEoscil_amp0p2_per2"),
		"deepskyblue")
	plot_pdf(axes[-1],
		vice.output("../../simulations/SFRoscil_amp0p3_per2"),
		"crimson")
	plot_pdf(axes[-1],
		vice.output("../../simulations/SFEoscil_amp0p2_per2"),
		"deepskyblue")
	axes[2].text(0.14, 150, r"%g $\leq$ [Fe/H] $\leq$ %g" % (_FEH_MIN_,
		_FEH_MAX_), fontsize = 25)
	legend(axes[1])
	plt.tight_layout()
	visuals.yticklabel_formatter(axes[2])
	plt.savefig(sys.argv[1])
	plt.clf()


if __name__ == "__main__":
	main()

