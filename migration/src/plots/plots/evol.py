r""" 
Produces a plot of the densities of infall, star formation, and gas as a 
function of simulation time for all models. 
""" 

from .. import env 
from .utils import named_colors, mpl_loc, yticklabel_formatter 
import matplotlib.pyplot as plt 
import math as m 
import vice 

ZONE_WIDTH = 0.1 
# SFR_LIM = [3e-5, 0.3] 
SFR_LIM = [1.1e-4, 0.3] 
# IFR_LIM = [3e-4, 3] 
IFR_LIM = [2.e-3, 0.3] 
# GAS_LIM = [3e5, 3e9] 
GAS_LIM = [3.e6, 3.e8] 
TIME_LIM = [-1, 14] 
RADII = [3, 5, 7, 9, 11, 13, 15] 
COLORS = ["grey", "black", "red", "gold", "green", "blue", "darkviolet"] 
MODELS = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"] 


def setup_axes(): 
	fig = plt.figure(figsize = (20, 15)) 
	fig, axes = plt.subplots(ncols = 4, nrows = 3, figsize = (20, 15)) 
	ylabels = [ 
		r"$\dot{\Sigma}_\star$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]", 
		r"$\dot{\Sigma}_\text{in}$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]", 
		r"$\Sigma_\text{gas}$ [M$_\odot$ kpc$^{-2}$]" 
	] 
	for i in range(len(axes)): 
		for j in range(len(axes[i])): 
			axes[i][j].set_yscale("log") 
			axes[i][j].set_xlim(TIME_LIM) 
			axes[i][j].set_ylim([SFR_LIM, IFR_LIM, GAS_LIM][i]) 
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(), 
				visible = False) 
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			if i == 0: axes[i][j].set_title(MODELS[j], fontsize = 25) 
		axes[i][0].set_ylabel(ylabels[i]) 
		if i != len(axes) - 1: yticklabel_formatter(axes[i][0]) 

	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[-1][0].get_position().x0 
	posd.x1 = axes[-1][-1].get_position().x1 
	posd.y0 = axes[-1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("Time [Gyr]", labelpad = 30) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	return axes 


def plot_evolution(axes, output, label = False): 
	zones = ["zone%d" % (int(i / ZONE_WIDTH)) for i in RADII] 
	for i in range(len(zones)): 
		kwargs = {"c": named_colors()[COLORS[i]]} 
		if label: kwargs["label"] = "%g kpc" % (RADII[i]) 
		sigma_sfr = [j / (m.pi * ((RADII[i] + ZONE_WIDTH)**2 - RADII[i]**2)) 
			for j in output.zones[zones[i]].history["sfr"]] 
		sigma_ifr = [j / (m.pi * ((RADII[i] + ZONE_WIDTH)**2 - RADII[i]**2)) 
			for j in output.zones[zones[i]].history["ifr"]] 
		sigma_gas = [j / (m.pi * ((RADII[i] + ZONE_WIDTH)**2 - RADII[i]**2)) 
			for j in output.zones[zones[i]].history["mgas"]] 
		axes[0].plot(output.zones[zones[i]].history["time"], sigma_sfr, 
			**kwargs) 
		axes[1].plot(output.zones[zones[i]].history["time"], sigma_ifr, 
			**kwargs) 
		axes[2].plot(output.zones[zones[i]].history["time"], sigma_gas, 
			**kwargs) 


def main(static, insideout, lateburst, outerburst, stem): 
	axes = setup_axes() 
	plot_evolution([row[0] for row in axes], vice.output(static), label = True) 
	plot_evolution([row[1] for row in axes], vice.output(insideout)) 
	plot_evolution([row[2] for row in axes], vice.output(lateburst)) 
	plot_evolution([row[3] for row in axes], vice.output(outerburst)) 
	leg = axes[1][0].legend(loc = mpl_loc("upper center"), ncol = 4, 
		frameon = False, bbox_to_anchor = (0.5, 0.99), handlelength = 0, 
		columnspacing = 0.8, fontsize = 20) 
	for i in range(len(RADII)): 
		leg.get_texts()[i].set_color(COLORS[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.08) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

