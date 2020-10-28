r""" 
Produces a plot of the SFE timescale as a function of radius at various 
timestamps in the simulation. 
""" 

from .. import env 
from .utils import named_colors, mpl_loc 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
MODELS = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"] 
TIMES = [2, 4, 6, 8, 10, 12.8] 
COLORS = ["red", "gold", "green", "blue", "darkviolet", "black"] 
RGAL_LIM = [-1, 16] 
TSTAR_LIM = [0, 7] 


def setup_axes(): 
	fig = plt.figure(figsize = (20, 5)) 
	axes = 4 * [None] 
	for i in range(len(axes)): 
		kwargs = {"facecolor": "white"} 
		if i != 0: kwargs["sharey"] = axes[0] 
		axes[i] = fig.add_subplot(141 + i, **kwargs) 
		if i != 0: plt.setp(axes[i].get_yticklabels(), visible = False) 
		axes[i].set_xlim(RGAL_LIM) 
		axes[i].set_ylim(TSTAR_LIM) 
		axes[i].set_yticks(range(8)) 
		axes[i].set_title(MODELS[i], fontsize = 25) 
	axes[0].set_ylabel(r"$\tau_\star$ [Gyr]") 

	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[0].get_position().x0 
	posd.x1 = axes[-1].get_position().x1 
	posd.y0 = axes[0].get_position().y0 
	posd.y1 = axes[0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	return axes 


def plot_sfe(ax, output, label = False): 
	radii = [ZONE_WIDTH * i for i in range(int(15.5 / ZONE_WIDTH))] 
	zones = ["zone%d" % (i) for i in range(len(radii))] 
	for i in range(len(TIMES)): 
		tau_star = len(radii) * [0.] 
		for j in range(len(tau_star)): 
			delta_t = [abs(k - TIMES[i]) for k in 
				output.zones[zones[j]].history["time"]] 
			idx = delta_t.index(min(delta_t)) 
			tau_star[j] = 1.e-9 * (output.zones[zones[j]].history["mgas"][idx] 
				/ output.zones[zones[j]].history["sfr"][idx]) 
		kwargs = {
			"c": 		named_colors()[COLORS[i]] 
		} 
		if label: kwargs["label"] = "%g Gyr" % (TIMES[i]) 
		ax.plot(radii, tau_star, **kwargs) 


def main(static, insideout, lateburst, outerburst, stem): 
	axes = setup_axes() 
	plot_sfe(axes[0], vice.output(static), label = True) 
	plot_sfe(axes[1], vice.output(insideout)) 
	plot_sfe(axes[2], vice.output(lateburst)) 
	plot_sfe(axes[3], vice.output(outerburst)) 
	leg = axes[0].legend(loc = mpl_loc("upper left"), ncol = 2, frameon = False, 
		bbox_to_anchor = (0.01, 0.99), handlelength = 0, fontsize = 20) 
	for i in range(len(TIMES)): 
		leg.get_texts()[i].set_color(COLORS[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(wspace = 0, bottom = 0.2) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

