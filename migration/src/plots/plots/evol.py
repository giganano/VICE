
from ..core import doublewide 
from ...simulations.config import config 
import matplotlib.pyplot as plt 
from matplotlib.ticker import FormatStrFormatter as fsf 
import math as m 
import vice 

CMAP = "plasma" 
XLIM = [-1, 14] 

def setup_axes(): 
	r""" 
	Sets up the 3x1 matplotlib axes to plot on 
	""" 
	fig = doublewide(nrows = 2) 
	fig = plt.figure(figsize = (10, 10)) 
	axes = 2 * [None] 
	ylabels = [ 
		[ 
		r"$\propto\dot{\Sigma}_\text{in}$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]", 
		r"$\propto\dot{\Sigma}_\star$ [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]" 
		], [
		r"$\propto\Sigma_\text{gas}$ [M$_\odot$ kpc$^{-2}$]", 
		r"$\tau_\star \equiv \Sigma_\text{gas}/\dot{\Sigma}_\star$ [Gyr]" 
		]
	] 
	for i in range(len(axes)): 
		axes[i] = 2 * [None] 
		for j in range(len(axes[i])): 
			axes[i][j] = fig.add_subplot(221 + len(axes) * i + j, 
				facecolor = "white")  
			axes[i][j].set_xlabel("Time [Gyr]") 
			axes[i][j].set_ylabel(ylabels[i][j]) 
			axes[i][j].set_xlim(XLIM) 
	axes[1][1].set_yscale("log") 
	axes[1][1].yaxis.set_major_formatter(fsf("%g")) 
	return fig, axes 


def plot_quantities(axes, out): 
	r""" 
	Plot the four quantities at each radius against time on the proper axes. 

	Parameters 
	----------
	axes : list 
		The 2x2 axes to plot on 
	out : vice.multioutput 
		The multioutput object from the VICE simulation. 
	""" 
	sigma_ifr_prefactor = 10 
	sigma_sfr_prefactor = 100 
	sigma_gas_prefactor = 1.e-8 
	cmap = plt.get_cmap(CMAP) 
	centers = list(map(lambda x, y: (x + y) / 2, 
		config.radial_bins[1:], config.radial_bins[:-1])) 
	bin_indeces = list(filter(lambda i: centers[i] <= 15.5, 
		range(len(centers)))) 
	for i in bin_indeces: 
		sigma_ifr = out.zones["zone%d" % (i)].history.size[0] * [0.] 
		sigma_sfr = out.zones["zone%d" % (i)].history.size[0] * [0.] 
		sigma_gas = out.zones["zone%d" % (i)].history.size[0] * [0.] 
		tau_star = out.zones["zone%d" % (i)].history.size[0] * [0.] 
		area = m.pi * (config.radial_bins[i + 1]**2 - config.radial_bins[i]**2) 
		for j in range(out.zones["zone%d" % (i)].history.size[0]): 
			sigma_ifr[j] = out.zones["zone%d" % (i)].history["ifr"][j] / area 
			sigma_sfr[j] = out.zones["zone%d" % (i)].history["sfr"][j] / area 
			sigma_gas[j] = out.zones["zone%d" % (i)].history["mgas"][j] / area 
			if sigma_sfr[j]: 
				tau_star[j] = sigma_gas[j] / sigma_sfr[j] * 1.e-9 
			else: 
				tau_star[j] = float("inf") 
			sigma_ifr[j] *= sigma_ifr_prefactor 
			sigma_sfr[j] *= sigma_sfr_prefactor 
			sigma_gas[j] *= sigma_gas_prefactor 

		kwargs = {
			"c": 	cmap(config.zone_width * (i + 0.5) / 15.5) 
		} 
		axes[0][0].plot(out.zones["zone%d" % (i)].history["time"], sigma_ifr, 
			**kwargs) 
		axes[0][1].plot(out.zones["zone%d" % (i)].history["time"], sigma_sfr, 
			**kwargs) 
		axes[1][0].plot(out.zones["zone%d" % (i)].history["time"], sigma_gas, 
			**kwargs) 
		axes[1][1].plot(out.zones["zone%d" % (i)].history["time"], tau_star, 
			**kwargs) 


def main(name): 
	r""" 
	For a given simulation, produce the figure showing the surface density of 
	gas and infall and star formation rates along with the SFE timescale as 
	functions of simulation time in Gyr. 

	Parameters 
	----------
	name : str 
		The name of the VICE output to plot on the figure 
	""" 
	plt.clf() 
	fig, axes = setup_axes() 
	plot_quantities(axes, vice.multioutput(name)) 
	plt.tight_layout() 
	cbar_ax = fig.add_axes([0.92, 0.02, 0.05, 0.95]) 
	sm = plt.cm.ScalarMappable(cmap = plt.get_cmap(CMAP), 
		norm = plt.Normalize(vmin = 0, vmax = 15.5)) 
	cbar = plt.colorbar(sm, cax = cbar_ax) 
	cbar.set_label(r"$R_\text{gal}$ [kpc]") 
	axes[1][1].set_ylim([0.5, 30]) 
	axes[0][0].set_ylim([-1, 6]) 
	plt.subplots_adjust(right = 0.88) 
	cbar_ax.set_position([
		axes[0][1].get_position().x1, 
		axes[1][1].get_position().y0, 
		0.03, 
		axes[0][1].get_position().y1 - axes[1][1].get_position().y0
	]) 
	plt.savefig("%s_evol.pdf" % (name)) 
	plt.savefig("%s_evol.png" % (name)) 
	plt.clf() 

