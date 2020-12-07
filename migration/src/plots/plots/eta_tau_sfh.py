r""" 
This script creates a plot of the mass-loading factor eta and the star 
formation e-folding timescale as functions of Galactocentric radius. 
""" 

from .. import env 
from ...simulations.models.insideout import insideout 
from .utils import named_colors 
import matplotlib.pyplot as plt 
import math as m 
import vice 


def main(stem): 
	ax1, ax2 = setup_axes() 
	plot_eta(ax1) 
	plot_tau_sfh(ax2) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 


def plot_eta(ax): 
	rgal = [0.01 * _ for _ in range(1551)] 
	eta = [vice.milkyway.default_mass_loading(_) for _ in rgal] 
	ax.plot(rgal, eta, c = named_colors()["black"]) 
	ax.plot(2 * [8.], ax.get_ylim(), c = named_colors()["crimson"], 
		linestyle = ':') 
	ax.plot(ax.get_xlim(), 2 * [vice.milkyway.default_mass_loading(8.)], 
		c = named_colors()["crimson"], linestyle = ':') 


def plot_tau_sfh(ax): 
	rgal = [0.01 * _ for _ in range(1551)] 
	tau = [insideout.timescale(_) for _ in rgal] 
	ax.plot(rgal, tau, c = named_colors()["black"]) 
	ax.plot(2 * [8.], ax.get_ylim(), c = named_colors()["crimson"], 
		linestyle = ':') 
	ax.plot(ax.get_xlim(), 2 * [insideout.timescale(8.)], 
		c = named_colors()["crimson"], linestyle = ':') 


def setup_axes(): 
	fig = plt.figure(figsize = (5, 10)) 
	ax1 = fig.add_subplot(211, facecolor = "white") 
	ax2 = fig.add_subplot(212, facecolor = "white") 
	ax1.set_ylabel(r"$\eta \equiv \dot{M}_\text{out} / \dot{M}_\star$") 
	ax2.set_ylabel(r"$\tau_\text{sfh}$ [Gyr]") 
	ax2.set_xlabel(r"$R_\text{gal}$ [kpc]") 
	plt.setp(ax1.get_xticklabels(), visible = False) 
	for i in [ax1, ax2]: 
		i.set_xlim([-2, 17]) 
		i.set_xticks([0, 5, 10, 15]) 
	ax1.set_ylim([-1, 11]) 
	ax2.set_ylim([0, 50]) 
	return [ax1, ax2] 

