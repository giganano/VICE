r""" 
Produces a plot of the SFE timescale as a function of radius at various 
timestamps in the simulation. 
""" 

from .. import env 
from .utils import (named_colors, mpl_loc, dummy_background_axes, 
	yticklabel_formatter) 
from ..._globals import END_TIME, ZONE_WIDTH 
import matplotlib.pyplot as plt 
import vice 

RGAL_LIM = [-2, 17] 


def setup_axes(n_outputs): 
	fig, axes = plt.subplots(ncols = n_outputs, nrows = 1, 
		figsize = (n_outputs * 7, 7), sharey = True) 
	if n_outputs > 1: 
		axes = axes.tolist() 
	else: 
		axes = [axes] 
	for i in range(len(axes)): 
		if i: plt.setp(axes[i].get_yticklabels(), visible = False) 
		axes[i].set_xlim(RGAL_LIM) 
		axes[i].set_xticks([0, 5, 10, 15]) 
		# axes[i].set_ylim(TSTAR_LIM) 
		# axes[i].set_yticks(range(8)) 
		# axes[i].set_title(MODELS[i], fontsize = 25) 
	axes[0].set_ylabel(r"$\tau_\star$ [Gyr]") 

	dummy = dummy_background_axes([axes]) 
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 
	return axes 


def plot_sfe(ax, output, times, colors, label = False): 
	radii = [ZONE_WIDTH * i for i in range(int(15.5 / ZONE_WIDTH))] 
	zones = ["zone%d" % (i) for i in range(len(radii))] 
	for i in range(len(times)): 
		tau_star = len(radii) * [0.] 
		for j in range(len(tau_star)): 
			delta_t = [abs(k - times[i]) for k in 
				output.zones[zones[j]].history["time"]] 
			idx = delta_t.index(min(delta_t)) 
			tau_star[j] = 1.e-9 * (output.zones[zones[j]].history["mgas"][idx] 
				/ output.zones[zones[j]].history["sfr"][idx]) 
		kwargs = {
			"c": 		named_colors()[colors[i]] 
		} 
		if label: kwargs["label"] = "%g Gyr" % (times[i]) 
		ax.plot(radii, tau_star, **kwargs) 



def main(outputs, stem, 
	labels = ["Constant", "Inside-Out", "Late-Burst", "Outer-Burst"], 
	times = [2, 4, 6, 8, 10, END_TIME], 
	colors = ["red", "gold", "green", "blue", "darkviolet", "black"], 
	ylim = [0.5, 20], yticks = [1, 10]): 

	axes = setup_axes(len(outputs)) 
	for i in range(len(axes)): 
		axes[i].set_yscale("log") 
		axes[i].set_ylim(ylim) 
		axes[i].set_yticks(yticks) 
		yticklabel_formatter(axes[i]) 
		if labels is not None: axes[i].set_title(labels[i], fontsize = 25) 
	outputs = [vice.output(_) for _ in outputs] 
	for i in range(len(outputs)): plot_sfe(axes[i], outputs[i], 
		times, colors, label = not i) 
	leg = axes[0].legend(loc = mpl_loc("upper left"), ncol = 1, 
		frameon = False, bbox_to_anchor = (0.01, 0.99), handlelength = 0, 
		# fontsize = 20, labelspacing = 0.2) 
		fontsize = 20) 
	for i in range(len(times)): 
		leg.get_texts()[i].set_color(colors[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(wspace = 0, bottom = 0.2) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

