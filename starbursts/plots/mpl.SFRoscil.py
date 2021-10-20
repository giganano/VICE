
import visuals
import matplotlib.pyplot as plt
import vice
import sys
import warnings
warnings.filterwarnings("ignore")

def plot_output_3axes(axes, name, color):
	"""
	Overrides the visuals.plot_output_3axes function to omit time = 0 for the
	infall rate. VICE does not know the infall rate at time = 0 when ran in
	star formation mode.
	"""
	out = vice.output(name)
	axes[0].plot(out.history["time"][1:], out.history["ifr"][1:],
		c = visuals.colors()[color], linestyle = '--')
	axes[0].plot(out.history["time"], out.history["sfr"],
		c = visuals.colors()[color], linestyle = '-')
	axes[1].plot(out.history["[Fe/H]"], out.history["[O/Fe]"],
		c = visuals.colors()[color])
	axes[2].plot(list(map(lambda x, y: (x + y) / 2., out.mdf["bin_edge_left"],
		out.mdf["bin_edge_right"])), out.mdf["dn/d[O/Fe]"],
		c = visuals.colors()[color])

if __name__ == "__main__":
	axes = visuals.subplots(1, 3, figsize = (21, 7))
	axes[0].xaxis.set_ticks([0, 2, 4, 6, 8, 10])
	axes[0].yaxis.set_ticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
	axes[0].set_xlim([-1, 11])
	axes[0].set_ylim([-1, 17])
	axes[1].set_xlim([-1.7, 0.2])
	axes[1].set_ylim([-0.1, 0.5])
	axes[2].set_xlim([-0.1, 0.5])
	axes[2].set_ylim([0.2, 50])
	visuals.set_labels_3axes(axes, "O")
	inset_xlim = [-0.26, -0.06]
	inset_ylim = [0.06, 0.16]
	visuals.draw_box(axes[1], inset_xlim, inset_ylim)
	inset = visuals.zoom_box(axes[1], inset_xlim, inset_ylim, zoom = 3.8)
	plot_output_3axes(axes, "../../simulations/SFRoscil_amp0p3_per4",
		"crimson")
	plot_output_3axes(axes, "../../simulations/SFRoscil_amp0p6_per2",
		"blue")
	plot_output_3axes(axes, "../../simulations/SFRoscil_amp0p3_per2",
		"black")
	visuals.plot_inset(inset, "../../simulations/SFRoscil_amp0p3_per4",
		"crimson")
	visuals.plot_inset(inset, "../../simulations/SFRoscil_amp0p6_per2",
		"blue")
	visuals.plot_inset(inset, "../../simulations/SFRoscil_amp0p3_per2",
		"black")
	visuals.plot_inset(inset, "../../simulations/default", "black",
		linestyle = ":")
	visuals.plot_reference(axes)
	visuals.yticklabel_formatter(axes[-1])
	visuals.sfr_ifr_legend(axes[0], ncol = 2)
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()











