r""" 
This file produces plots of single-panel [O/Fe]-[Fe/H] track comparisons 
between two models. 
""" 

from ... import env 
from ..utils import named_colors, mpl_loc, markers 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
RADII = [3, 5, 7, 9, 11, 13, 15] 
COLORS = ["grey", "black", "red", "gold", "green", "blue", "darkviolet"] 


def setup_axis(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel("[Fe/H]") 
	ax.set_ylabel("[O/Fe]") 
	ax.set_xlim([-1.8, 0.8]) 
	ax.set_ylim([-0.2, 0.5]) 
	ax.set_xticks([-1.5, -1.0, -0.5, 0.0, 0.5]) 
	return ax 


def plot_tracks(ax, output, linestyle = '-', label = False): 
	zones = [int(i / ZONE_WIDTH) for i in RADII] 
	for i in range(len(zones)): 
		kwargs = {
			"c": 			named_colors()[COLORS[i]], 
			"linestyle": 	linestyle 
		} 
		if label: kwargs["label"] = r"$R_\text{gal}$ = %g kpc" % (RADII[i]) 
		ax.plot(output.zones["zone%d" % (zones[i])].history["[Fe/H]"], 
			output.zones["zone%d" % (zones[i])].history["[O/Fe]"], 
			**kwargs) 


def plot_ticks(ax, output, times, **kwargs): 
	for i in range(len(RADII)): 
		zone = "zone%d" % (int(RADII[i] / ZONE_WIDTH)) 
		for j in range(len(times)): 
			delta_t = [abs(k - times[j]) for k in 
				output.zones[zone].history["time"]] 
			idx = delta_t.index(min(delta_t)) 
			ax.scatter(output.zones[zone].history["[Fe/H]"][idx], 
				output.zones[zone].history["[O/Fe]"][idx], 
				c = COLORS[i], **kwargs) 


def main(output1, output2, times, stem): 
	ax = setup_axis() 
	plot_tracks(ax, vice.output(output1), label = True) 
	plot_tracks(ax, vice.output(output2), linestyle = ':') 
	plot_ticks(ax, vice.output(output1), times, marker = markers()['x']) 
	plot_ticks(ax, vice.output(output2), times, marker = markers()["point"]) 
	leg = ax.legend(loc = mpl_loc("lower left"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.01, 0.01), handlelength = 0, fontsize = 20) 
	for i in range(len(RADII)): 
		leg.get_texts()[i].set_color(COLORS[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

