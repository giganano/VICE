r""" 
Produces a plot of the stellar [Fe/H] or [O/H] distributions in 3 different 
z-bins and for different galactocentric radii. 
""" 


from .. import env 
from ..utils import zheights 
from .utils import named_colors, mpl_loc 
import matplotlib.pyplot as plt 
import vice 

ZONE_WIDTH = 0.1 
BINS = [-2. + 0.02 * i for i in range(201)] 


def setup_axes(element): 
	fig = plt.figure(figsize = (7, 10)) 
	axes = 3 * [None] 
	for i in range(len(axes)): 
		axes[i] = fig.add_subplot(311 + i, facecolor = "white") 
		if i == len(axes) - 1: 
			axes[i].set_xlabel("[%s/H]" % (element.capitalize())) 
		else: 
			plt.setp(axes[i].get_xticklabels(), visible = False) 
		axes[i].set_xlim([-1.5, 0.7]) 
		axes[i].set_ylim([0, 5]) 
	axes[1].set_ylabel("PDF") 
	return axes 


def get_mdf(element, stars, min_rgal, max_rgal, min_absz, max_absz): 
	stars = stars.filter("zone_final", ">=", int(min_rgal / ZONE_WIDTH)) 
	stars = stars.filter("zone_final", "<=", int(max_rgal / ZONE_WIDTH) - 1) 
	stars = stars.filter("abszfinal", ">=", min_absz) 
	stars = stars.filter("abszfinal", "<=", max_absz) 
	stars = stars.filter("mass", ">", 0) 
	dist = (len(BINS) - 1) * [0.] 
	for i in range(len(dist)): 
		filtered_stars = stars.filter("[%s/h]" % (element), ">=", BINS[i]) 
		filtered_stars = filtered_stars.filter("[%s/h]" % (element), "<=", 
			BINS[i + 1]) 
		dist[i] = sum(filtered_stars["mass"]) 
	norm = sum(dist) * (BINS[1] - BINS[0]) 
	dist = [i / norm for i in dist] 
	print(sum(dist) * (BINS[1] - BINS[0])) 
	return dist 


def plot_mdf(ax, element, stars, min_rgal, max_rgal, min_absz, max_absz, color, 
	label = False): 
	centers = [(i + j) / 2. for i, j in zip(BINS[1:], BINS[:-1])] 
	mdf = get_mdf(element, stars, min_rgal, max_rgal, min_absz, max_absz) 
	kwargs = {
		"c": 	named_colors()[color] 
	} 
	if label: kwargs["label"] = r"$R_\text{gal}$ = %g - %g kpc" % (
		min_rgal, max_rgal) 
	ax.plot(centers, mdf, **kwargs) 


def main(element, output, stem): 
	axes = setup_axes(element) 
	output = vice.output(output) 
	output.stars["abszfinal"] = [abs(i) for i in zheights(
		output.name)[:output.stars.size[0]]] 
	radii = [3, 5, 7, 9, 11, 13, 15] 
	heights = [2.0, 1.0, 0.5, 0.0] 
	colors = ["black", "red", "gold", "green", "blue", "darkviolet"] 
	for i in range(len(heights) - 1): 
		axes[i].text(-0.5, 4, r"$\left|z\right|$ = %g - %g kpc" % (
			heights[i + 1], heights[i]), fontsize = 20) 
		for j in range(len(radii) - 1): 
			plot_mdf(axes[i], element, output.stars, radii[j], radii[j + 1], 
				heights[i + 1], heights[i], colors[j], label = i == 0) 
	leg = axes[0].legend(loc = mpl_loc("upper left"), ncol = 1, fontsize = 20, 
		frameon = False, bbox_to_anchor = (0.005, 0.99), handlelength = 0) 
	for i in range(len(radii) - 1): 
		leg.get_texts()[i].set_color(colors[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 

