r""" 
This script produces a plot of our star formation law to ensure that it 
resembles the observed KS-relation. 
""" 

from src.simulations.sfe import sfe 
from src.plots import env 
from src.plots.plots.utils import named_colors, markers 
import matplotlib.pyplot as plt 
import numpy as np 
import math as m 


def setup_axes(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xscale("log") 
	ax.set_yscale("log") 
	ax.set_xlabel(r"$\Sigma_\text{gas}$ [M$_\odot$ kpc$^{-2}$]") 
	ax.set_ylabel(r"$\dot{\Sigma}_\star$ [M$_\odot$ kpc$^{-2}$ yr$^{-1}$]") 
	return ax 


def plot_relation(ax): 
	area = m.pi * (8.1**2 - 8**2) 
	relation = sfe(area) 
	sfrs = np.logspace(-5, 0, 1001).tolist() 
	Sigma_sfrs = [_ / area for _ in sfrs] 
	tau_stars = [relation(12.2, _) for _ in sfrs] 
	Sigma_gases = [1.e9 * a * b for a, b in zip(Sigma_sfrs, tau_stars)] 
	ax.plot(Sigma_gases, Sigma_sfrs, c = named_colors()["black"]) 


def krumholz_points(ax): 
	xvals = [10**6.15, 10**6.75, 10**7.3, 10**8.3] 
	yvals = [1.e-5, 1.e-4, 1.e-2, 1.e-1] 
	ax.scatter(xvals, yvals, c = named_colors()["blue"], 
		marker = markers()["star"]) 


if __name__ == "__main__": 
	ax = setup_axes() 
	plot_relation(ax) 
	krumholz_points(ax) 
	plt.tight_layout() 
	plt.savefig("sfe_test.png") 
	plt.savefig("sfe_test.pdf") 
	plt.close() 

