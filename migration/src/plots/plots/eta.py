r""" 
Produces a plot of the mass-loading factor :math:`\eta` as a function of 
galactocentric radius in kpc. 
""" 

from .. import env 
from .utils import named_colors 
import matplotlib.pyplot as plt 
import vice 


def setup_axis(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel(r"$R_\text{gal}$ [kpc]") 
	ax.set_ylabel(r"$\eta \equiv \dot{M}_\text{out}/\dot{M}_\star$") 
	ax.set_xlim([-1, 16]) 
	ax.set_ylim([0, 6]) 
	return ax 


def main(stem): 
	ax = setup_axis() 
	xvals = [0.01 * i for i in range(int(15.5 / 0.01))] 
	yvals = [vice.milkyway.default_mass_loading(i) for i in xvals] 
	ax.plot(xvals, yvals, c = named_colors()["black"]) 
	ax.plot(2 * [8.], ax.get_ylim(), c = named_colors()["red"], 
		linestyle = ':') 
	ax.plot(ax.get_xlim(), 2 * [vice.milkyway.default_mass_loading(8)], 
		c = named_colors()["red"], linestyle = ':') 
	plt.tight_layout() 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 

