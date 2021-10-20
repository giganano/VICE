
import visuals
import matplotlib.pyplot as plt
import vice
import sys

def plot_sr_fe_tracks(ax):
	plot_track(ax, "../../simulations/sudden_5Gyr_5e9Msun", "sr", "crimson", '-')
	plot_track(ax, "../../simulations/sudden_5Gyr_5e9Msun", "fe", "black", ':')
	plot_track(ax, "../../simulations/sudden_5Gyr_5e9Msun_riaexp", "fe",
		"black", '--')
	plot_legend(ax)

def plot_track(ax, name, ref, color, linestyle):
	"""
	Plots [O/X]-[X/H] tracks on a matplotlib subplot

	Args:
	=====
	ax:				The name of the subplot
	name: 			The name of the VICE output
	ref: 			The symbol for the reference element
	color: 			The color of the line
	linestyle: 		The linestyle to use
	"""
	out = vice.output(name)
	ax.plot(out.history["[%s/h]" % (ref)], out.history["[o/%s]" % (ref)],
		c = visuals.colors()[color], linestyle = linestyle)

def plot_legend(ax):
	lines = 3 * [None]
	linestyles = ['-', ':', '--']
	colors = ["red", "black", "black"]
	labels = ["Sr", r"Fe; $R_\text{Ia}\propto t^{-1.1}$",
		r"Fe; $R_\text{Ia}\propto e^{-t/\tau_\text{Ia}}$"]
	for i in range(3):
		lines[i] = ax.plot([1, 2], [1, 2], c = visuals.colors()[colors[i]],
			linestyle = linestyles[i], label = labels[i])[0]
	leg = ax.legend(loc = visuals.mpl_loc()["lower left"], ncol = 1,
		bbox_to_anchor = (0.01, 0.01), frameon = False)
	for i in range(3):
		lines[i].remove()

if __name__ == "__main__":
	ax = visuals.subplots(1, 1)
	ax.set_xlabel("[X/H]")
	ax.set_ylabel("[O/X]")
	plot_sr_fe_tracks(ax)
	ax.set_xlim([-1.7, 0.1])
	ax.set_ylim([0., 0.6])
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()


