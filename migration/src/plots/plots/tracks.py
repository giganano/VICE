r""" 
This file produces plots of single-panel [O/Fe]-[Fe/H] track comparisons 
between two models. 
""" 

from .. import env 
from .utils import named_colors, mpl_loc, markers, yticklabel_formatter 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
# RADII = [3, 6, 9, 12, 15] 
# COLORS = ["red", "gold", "green", "blue", "darkviolet"] 
# PREFACTORS = [1, 1.5, 2.0, 2.5, 3.0]  
RADII = [3, 5, 7, 9, 11, 13, 15] 
COLORS = ["grey", "black", "red", "gold", "green", "blue", "darkviolet"] 
# PREFACTORS = [1., 1.5, 2.0, 2.5, 3.0, 3.5, 4.0] 
# PREFACTORS = [4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0] 
PREFACTORS = [55, 25, 10, 5, 3, 2.0, 1.0] 


def setup_axis(): 
	fig = plt.figure(figsize = (14, 7)) 
	axes = 2 * [None] 
	for i in range(len(axes)): 
		axes[i] = fig.add_subplot(121 + i, facecolor = "white") 
	axes[0].set_xlabel("[Fe/H]") 
	axes[0].set_ylabel("[O/Fe]") 
	axes[1].set_xlabel("Time [Gyr]") 
	axes[1].set_ylabel(r"$\propto \dot{N}_\text{Ia}$ [Gyr$^{-1}$]") 
	axes[0].set_xlim([-2.3, 0.8]) 
	axes[0].set_ylim([-0.1, 0.5]) 
	axes[0].set_xticks([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5]) 
	axes[1].set_xlim([-1, 14]) 
	axes[1].set_yscale("log") 
	axes[1].set_ylim([0.1, 100]) 
	yticklabel_formatter(axes[1]) 
	# axes[1].set_ylim([-0.2, 5.4]) 
	# axes[1].set_yticks(range(7)) 
	return axes 


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


def ia_rate_proxies(zone, prefactor = 1): 
	mir = vice.singlezone.from_output(zone) 
	proxies = (len(zone.history["time"]) - 1) * [0.] 
	for i in range(len(proxies)): 
		if zone.history["time"][i] > mir.delay: 
			proxies[i] = (
				zone.history["mass(fe)"][i + 1] - zone.history["mass(fe)"][i] 
			) / (
				zone.history["time"][i + 1] - zone.history["time"][i] 
			) 
			proxies[i] -= 1.e9 * (
				vice.yields.ccsne.settings["fe"] * zone.history["sfr"][i] 
			) 
			proxies[i] += zone.history["z(fe)"][i] * zone.history["sfr"][i] * (
				1 + mir.eta - 0.4) * 1.e9 
			proxies[i] /= zone.history["mass(fe)"][i] 
			proxies[i] *= prefactor 
			if proxies[i] < 0: proxies[i] = 0 
		else: pass 
	return proxies 


def plot_ia_rate_proxies(ax, output, linestyle = '-'): 
	for i in range(len(RADII)): 
		kwargs = {
			"c": 			COLORS[i], 
			"linestyle": 	linestyle 
		} 
		zone = int(RADII[i] / ZONE_WIDTH) 
		ax.plot(output.zones["zone%d" % (zone)].history["time"][:-1], 
			ia_rate_proxies(output.zones["zone%d" % (zone)], 
				prefactor = PREFACTORS[i]), **kwargs) 


def main(output1, output2, stem, times = [2, 4, 6, 8, 10, 12.7]): 
	axes = setup_axis() 
	out1 = vice.output(output1) 
	out2 = vice.output(output2) 
	plot_tracks(axes[0], out1, label = True) 
	plot_tracks(axes[0], out2, linestyle = ':') 
	plot_ticks(axes[0], out1, times, marker = markers()['x']) 
	plot_ticks(axes[0], out2, times, marker = markers()["point"]) 
	plot_ia_rate_proxies(axes[1], out1) 
	plot_ia_rate_proxies(axes[1], out2, linestyle = ':') 
	leg = axes[0].legend(loc = mpl_loc("lower left"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.01, 0.01), handlelength = 0, fontsize = 20) 
	for i in range(len(RADII)): 
		leg.get_texts()[i].set_color(COLORS[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

