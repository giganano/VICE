r""" 
Plots the surface density gradient of a set of simulation outputs as a 
function of galactocentric radius in kpc. 
""" 

from .. import env 
import matplotlib.pyplot as plt 
from .utils import named_colors, mpl_loc, markers 
import math as m 
import vice 

ZONE_WIDTH = 0.1 


def setup_axis(): 
	fig = plt.figure(figsize = (5, 5)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel(r"$R_\text{gal}$ [kpc]") 
	ax.set_ylabel(r"$\Sigma$ [M$_\odot$ kpc$^{-2}$]") 
	ax.set_yscale("log") 
	ax.set_xlim([-2, 22]) 
	ax.set_ylim([1e5, 1e10]) 
	minorticks = [] 
	for i in range(5, 10): 
		for j in range(2, 10): 
			minorticks.append(j * 10**i) 
	ax.yaxis.set_ticks([1e5, 1e6, 1e7, 1e8, 1e9, 1e10]) 
	ax.yaxis.set_ticks(minorticks, minor = True) 
	ax.xaxis.set_ticks(range(0, 25, 5)) 
	return ax 


def surface_densities(ax, output): 
	zones = ["zone%d" % (i) for i in range(int(20. / ZONE_WIDTH))] 
	annuli = [ZONE_WIDTH * i for i in range(len(zones) + 1)] 
	radii = len(zones) * [0.] 
	stars = len(zones) * [0.] 
	gas = len(zones) * [0.] 
	for i in range(len(zones)): 
		area = m.pi * (annuli[i + 1]**2 - annuli[i]**2) 
		radii[i] = (annuli[i] + annuli[i + 1]) / 2. 
		stars[i] = output.zones[zones[i]].history["mstar"][-1] / area 
		if radii[i] <= 15.5: 
			gas[i] = output.zones[zones[i]].history["mgas"][-1] / area 
		else: 
			gas[i] = float("nan") 
	ax.plot(radii, [target_gradient(i) for i in radii], 
		c = named_colors()["black"], 
		label = r"B-H \& G (2016)") 
	ax.plot(radii, [thin_disk(i) for i in radii], 
		c = named_colors()["black"], linestyle = ':') 
	ax.plot(radii, [thick_disk(i) for i in radii], 
		c = named_colors()["black"], linestyle = ':') 
	ax.plot(radii, stars, c = named_colors()["red"], label = "Stars") 
	ax.plot(radii, gas, c = named_colors()["blue"], label = "Gas") 
	leg = ax.legend(loc = mpl_loc("upper right"), ncol = 1, frameon = False, 
		bbox_to_anchor = (0.95, 0.99), handlelength = 0) 
	renderer = plt.gcf().canvas.get_renderer() 
	widths = [i.get_window_extent(renderer).width for i in leg.get_texts()] 
	shift = max(widths) - min(widths) 
	for i in range(3): 
		leg.get_texts()[i].set_color(["black", "red", "blue"][i]) 
		leg.legendHandles[i].set_visible(False) 
		leg.get_texts()[i].set_ha("right") 
		leg.get_texts()[i].set_position((shift, 0)) 
	

def target_gradient(radius): 
	# sigma_thin_0 = 986e6 
	# sigma_thick_0 = 266e6 
	# rs_thin = 2.5 
	# rs_thick = 2.0 
	# return sigma_thin_0 * m.exp(-radius / rs_thin) + sigma_thick_0 * m.exp(
	# 	-radius / rs_thick) 
	return thin_disk(radius) + thick_disk(radius) 


def thin_disk(radius): 
	sigma_0 = 986e6 
	rs = 2.5 
	return sigma_0 * m.exp(-radius / rs) 


def thick_disk(radius): 
	sigma_0 = 266e6 
	rs = 2.0 
	return sigma_0 * m.exp(-radius / rs) 


def main(output, stem): 
	ax = setup_axis() 
	surface_densities(ax, vice.multioutput(output)) 
	plt.tight_layout() 
	plt.subplots_adjust(right = 0.99)
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 


