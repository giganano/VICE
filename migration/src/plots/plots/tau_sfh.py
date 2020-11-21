r""" 
Produces a plot of the star formation timescales in Gyr as a function of 
galactocentric radius in kpc. 
""" 

from .. import env 
from ...simulations.models.insideout import insideout 
from .utils import named_colors 
import matplotlib.pyplot as plt 
import math as m 


def setup_axis(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel(r"$R_\text{gal}$ [kpc]") 
	ax.set_ylabel(r"$\tau_\text{sfh}$ [Gyr]") 
	ax.set_xlim([-1, 16]) 
	ax.set_ylim([0, 50])
	return ax 


# def fit(radius): 
# 	return 6. * m.exp(radius / 7.) 


def main(stem): 
	ax = setup_axis() 
	rgal = [0.01 * i for i in range(1551)] 
	tau = [insideout.timescale(i) for i in rgal] 
	ax.plot(rgal, tau, c = named_colors()["black"]) 
	# rgal = [0.01 * i for i in range(1551)]
	# ax.plot(rgal, [insideout.timescale(_) for _ in rgal], 
	# 	c = named_colors()["blue"], 
	# 	linestyle = '--') 
	ax.plot(2 * [8.], ax.get_ylim(), c = named_colors()["crimson"], 
		linestyle = ':') 
	ax.plot(ax.get_xlim(), 2 * [insideout.timescale(8.)], 
		c = named_colors()["crimson"], linestyle = ':') 
	plt.tight_layout() 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.close() 


