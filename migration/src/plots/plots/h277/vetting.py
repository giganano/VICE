r""" 
This script produces a heatmap of h277 star particles in the Rform-Tform plane 
to describe how we vet our sample of star particles. 
""" 

from ... import env 
from ..utils import named_colors 
from astropy.io import fits 
import matplotlib.pyplot as plt 
import numpy as np 


def main(stem): 
	ax = setup_axis() 
	plot_heatmap(ax) 
	plot_cuts(ax) 
	plt.tight_layout() 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.close() 


def get_histogram(): 
	h277dir = "../vice/toolkit/hydrodisk/data/h277/processor" 
	h277file = "%s/h277_particles_150Myr.fits" % (h277dir) 
	h277 = fits.open(h277file) 
	counts, xedges, yedges = np.histogram2d(h277[1].data["tform"], 
		h277[1].data["Rform"], bins = 100, range = [[0, 13.7], [0, 20]]) 
	counts = counts.T 
	return [counts, xedges, yedges] 


def plot_heatmap(ax): 
	counts, xedges, yedges = get_histogram() 
	ax.pcolormesh(xedges, yedges, counts, cmap = "Greys", vmin = 0, 
		vmax = 100) 


def plot_cuts(ax): 
	ax.plot(2 * [1.5], ax.get_ylim(), c = named_colors()["lime"], 
		linestyle = '--') 
	rgalcut = lambda tform: 1.4 * tform + 2 
	ax.plot(ax.get_xlim(), [rgalcut(i) for i in ax.get_xlim()], 
		c = named_colors()["lime"], linestyle = '--')  


def setup_axis(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xlabel(r"$T_\text{form}^\text{h277}$ [Gyr]") 
	ax.set_ylabel(r"$R_\text{form}^\text{h277}$ [kpc]") 
	ax.set_xlim([0, 13.7]) 
	ax.set_ylim([0, 20]) 
	ax.set_yticks([0, 5, 10, 15, 20]) 
	return ax 



