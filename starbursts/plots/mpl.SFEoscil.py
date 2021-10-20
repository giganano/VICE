
import visuals
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import vice
import sys
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":
	axes = visuals.subplots(1, 3, figsize = (21, 7))
	axes.insert(1, visuals.append_subplot_below(axes[0]))
	axes[0].xaxis.set_ticks([0, 2, 4, 6, 8, 10])
	axes[0].set_xlim([-1, 11])
	axes[0].set_ylim([2.1, 3.6])
	axes[1].set_ylim([1.3, 2.7])
	axes[2].set_xlim([-1.7, 0.2])
	axes[2].set_ylim([-0.1, 0.5])
	axes[3].set_xlim([-0.1, 0.5])
	axes[3].set_ylim([0.2, 50])
	visuals.set_labels_4axes(axes, "O")
	inset_xlim = [-0.26, -0.06]
	inset_ylim = [0.06, 0.16]
	visuals.draw_box(axes[2], inset_xlim, inset_ylim)
	inset = visuals.zoom_box(axes[2], inset_xlim, inset_ylim, zoom = 3.8)
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEoscil_amp0p2_per4", "crimson", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEoscil_amp0p4_per2", "blue", "O")
	visuals.plot_output_4axes(axes,
		"../../simulations/SFEoscil_amp0p2_per2", "black", "O")
	visuals.plot_inset(inset,
		"../../simulations/SFEoscil_amp0p2_per4", "crimson")
	visuals.plot_inset(inset,
		"../../simulations/SFEoscil_amp0p4_per2", "blue")
	visuals.plot_inset(inset,
		"../../simulations/SFEoscil_amp0p2_per2", "black")
	visuals.plot_inset(inset,
		"../../simulations/default", "black", linestyle = ':')
	visuals.plot_reference(axes)
	visuals.yticklabel_formatter(axes[-1])
	plt.tight_layout()
	plt.savefig(sys.argv[1])
	plt.clf()

