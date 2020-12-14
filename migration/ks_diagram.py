r""" 
ARGV 
----
1) 		The name of the vice output 
2) 		The name of the output image (without extension) 
""" 


from src.plots import env 
from src.plots.plots.utils import named_colors, markers 
import matplotlib.pyplot as plt 
import math as m 
import vice 
import sys 


def setup_axis(): 
	fig = plt.figure(figsize = (7, 7)) 
	ax = fig.add_subplot(111, facecolor = "white") 
	ax.set_xscale("log") 
	ax.set_yscale("log") 
	ax.set_xlabel(r"$\Sigma_\text{gas}$ [M$\odot$ kpc$^{-2}$]") 
	ax.set_ylabel(r"$\dot{\Sigma}_\star$ [M$_\odot$ kpc$^{-2}$ yr$^{-1}$]") 
	ax.set_xlim([4.e5, 6.e8]) 
	ax.set_ylim([2.e-6, 0.4]) 
	return ax 


def plot_relation(ax, output): 
	cmap = plt.get_cmap("viridis") 
	annuli = [0.1 * _ for _ in range(201)] 
	for i in range(0, len(output.zones.keys()), 4): 
		zone = "zone%d" % (i) 
		area = m.pi * (annuli[i + 1]**2 - annuli[i]**2) 
		Sigma_sfr = [_ / area for _ in output.zones[zone].history["sfr"][1:]] 
		Sigma_gas = [_ / area for _ in output.zones[zone].history["mgas"][1:]] 
		ax.plot(Sigma_gas, Sigma_sfr, c = cmap(0.1 * (i + 0.5) / 15.5)) 


def krumholz_points(ax): 
	xvals = [10**6.15, 10**6.75, 10**7.3, 10**8.3] 
	yvals = [1.e-5, 1.e-4, 1.e-2, 1.e-1] 
	ax.scatter(xvals, yvals, c = named_colors()["crimson"], 
		marker = markers()["star"], s = 50) 


if __name__ == "__main__": 
	ax = setup_axis() 
	plot_relation(ax, vice.output(sys.argv[1])) 
	krumholz_points(ax) 
	plt.tight_layout() 
	plt.savefig("%s.pdf" % (sys.argv[2])) 
	plt.savefig("%s.png" % (sys.argv[2])) 
	plt.close() 

