
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter as fsf
import numpy as np

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

OUTPUTS = ["timer_5.out", "timer_10.out", "timer_15.out", "timer_20.out",
	"timer_25.out"]
COLORS = ["red", "gold", "green", "blue", "purple"]
N = [5, 10, 15, 20, 25]

def setup_subplot():
	"""
	Setup a matplotlib subplot to plot on
	"""
	plt.clf()
	fig = plt.figure(figsize = (10, 10))
	ax = fig.add_subplot(111, facecolor = "white")
	ax.set_xlabel(r"$\Delta t$ [Gyr]")
	ax.set_ylabel(r"$\texttt{VICE}$ Integration Time [seconds]")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.tick_params(axis = 'x', which = 'both', pad = 10)
	return ax

def draw(name, ax, color, nelem):
	"""
	Plot execution time vs timestep size for a given number of elements

	name :: the name of the output file
	ax :: the subplot to plot on
	color :: the color to plot in
	nelem :: the number of elements in the simulation
	"""
	output = np.genfromtxt(name)
	x = [i[0] for i in output]
	y = [i[1] for i in output]
	ax.plot(x, y, c = mpl.colors.get_named_colors_mapping()[color])
	x = np.linspace(1.e-4, 1.e-1, 1000)
	fit = best_fit(nelem)
	ax.plot(x, list(map(fit, x)),
		c = mpl.colors.get_named_colors_mapping()[color], linestyle = ':')

def legend(ax):
	"""
	Put the legend on the axis

	ax :: the subplot
	"""
	lines = len(OUTPUTS) * [None]
	for i in range(len(lines)):
		lines[i] = ax.plot([0.001, 0.01], [1, 2],
			c = mpl.colors.get_named_colors_mapping()["white"],
			label = "%d elements" % (N[i]))[0]
	leg = ax.legend(loc = 3, ncol = 1, frameon = False,
		bbox_to_anchor = (0.02, 0.02), handlelength = 0)
	for i in range(len(lines)):
		lines[i].remove()
		leg.get_texts()[i].set_color(COLORS[i])
	ax.add_artist(leg)
	dummy = ax.plot([0.001, 0.01], [1, 2],
		c = mpl.colors.get_named_colors_mapping()["black"], linestyle = ':',
		label = r"$N\Delta t^{-2}$ expected fit")[0]
	ax.legend(loc = 1, ncol = 1, frameon = False,
		bbox_to_anchor = (0.98, 0.98))
	dummy.remove()

def best_fit(nelem):
	"""
	Obtain the expected fit for a given number of elements
	"""
	return lambda t: 4.2 * nelem * (1.e-3 / t)**2

if __name__ == "__main__":
	ax = setup_subplot()
	for i in range(len(N)):
		draw(OUTPUTS[i], ax, COLORS[i], N[i])
	legend(ax)
	ax.text(0.01, 300, "T = 10 Gyr", fontsize = 25,
		color = mpl.colors.get_named_colors_mapping()["black"])
	ax.set_xlim([3.3e-4, 0.06])
	ax.set_ylim([0.025, 1500])
	ax.xaxis.set_major_formatter(fsf("%g"))
	ax.yaxis.set_major_formatter(fsf("%g"))
	plt.tight_layout()
	plt.savefig("timer.pdf")
	plt.savefig("timer.png")
	plt.clf()



