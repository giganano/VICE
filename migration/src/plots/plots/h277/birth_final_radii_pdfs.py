r""" 
Produces a plot of PDFs of the birth and final radii of bulge, pseudobulge, 
thin disk, and thick disk stars from h277. 
""" 

from ... import env 
from ..utils import (named_colors, mpl_loc, dummy_background_axes, 
	yticklabel_formatter) 
from vice.toolkit.hydrodisk import hydrodiskstars 
import matplotlib.pyplot as plt 
import numpy as np 
import math as m 
# H277_STARS = hydrodiskstars([0.1 * _ for _ in range(201)], N = 1e10) 

DECOMP = {
	1: "thin", 
	2: "thick", 
	3: "bulge", 
	4: "pseudo" 
}
COLORS = {
	1: "crimson", 
	2: "blue", 
	3: "black", 
	4: "lime" 
}


def main(stem): 
	axes = setup_axes() 
	h277 = hydrodiskstars([0.1 * _ for _ in range(201)], N = 1e10) 
	for i in DECOMP.keys(): 
		kwargs = {
			"decomp": 	i, 
			"c": 		named_colors()[COLORS[i]] 
		}
		plot_pdf(axes[0], h277, **kwargs) 
		plot_pdf(axes[1], h277, which = "rfinal", label = "count", **kwargs) 
	kwargs = {
		"loc": 				mpl_loc("upper right"), 
		"ncol": 			2, 
		"frameon": 			False, 
		"bbox_to_anchor": 	(0.99, 0.99), 
		"handlelength": 	0, 
		"fontsize": 		23, 
		"handletextpad": 	-0.5 
	} 
	for i in range(len(axes)): 
		leg = axes[i].legend(**kwargs) 
		for j in range(len(DECOMP.keys())): 
			leg.get_texts()[j].set_color(COLORS[list(DECOMP.keys())[j]]) 
			leg.legendHandles[j].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(wspace = 0) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 


def plot_pdf(ax, h277, which = "rform", label = "decomp", decomp = 1, **kwargs): 
	subsample = h277.analog_data.filter("decomp", "==", decomp) 
	pdf, bins = np.histogram(subsample[which], range = [0, 20], bins = 500, 
		density = True) 
	centers = [(a + b) / 2. for a, b in zip(bins[1:], bins[:-1])] 
	if label == "decomp": 
		kwargs["label"] = DECOMP[decomp] 
	elif label == "count": 
		# kwargs["label"] = "%.2e" % (len(subsample["id"])) 
		n = len(subsample["id"]) 
		kwargs["label"] = r"%.2f$\times10^{%d}$" % (n / 10**int(m.log10(n)), 
			int(m.log10(n))) 
	else: 
		raise KeyError("Internal Error.") 
	ax.plot(centers, pdf, **kwargs) 


def setup_axes(): 
	fig = plt.figure(figsize = (10, 5)) 
	axes = [] 
	for i in range(2): 
		axes.append(fig.add_subplot(121 + i, facecolor = "white")) 
		# axes.append(fig.add_subplot(121 + i, facecolor = "white", 
		# 	sharey = axes[0] if i else None)) 
		if i: plt.setp(axes[i].get_yticklabels(), visible = False) 
		axes[i].set_xlim([-2, 22]) 
		axes[i].set_xticks([0, 5, 10, 15, 20]) 
		axes[i].set_yscale("log") 
		axes[i].set_ylim([3e-4, 3]) 
		axes[i].set_yticks([1e-3, 1e-2, 1e-1, 1]) 
		yticklabel_formatter(axes[i]) 
	axes[0].set_xlabel(r"Birth $R_\text{gal}$ [kpc]") 
	axes[1].set_xlabel(r"Final $R_\text{gal}$ [kpc]") 
	axes[0].set_ylabel("PDF") 
	# dummy = dummy_background_axes([axes]) 
	# dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30) 
	# dummy.set_ylabel("Probability Density", labelpad = 60) 
	return axes 

