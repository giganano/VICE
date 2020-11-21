r""" 
Produces a plot of the stellar [Fe/H] or [O/H] distributions in 3 different 
z-bins and for different galactocentric radii. 
""" 


from .. import env 
from ..utils import zheights 
from .utils import named_colors, mpl_loc, markers 
import matplotlib.pyplot as plt 
import numpy as np 
import vice 

ZONE_WIDTH = 0.1 
BINS = [-2. + 0.02 * i for i in range(201)] 


# def setup_axes(element): 
# 	fig = plt.figure(figsize = (7, 10)) 
# 	axes = 3 * [None] 
# 	for i in range(len(axes)): 
# 		axes[i] = fig.add_subplot(311 + i, facecolor = "white") 
# 		if i == len(axes) - 1: 
# 			axes[i].set_xlabel("[%s/H]" % (element.capitalize())) 
# 		else: 
# 			plt.setp(axes[i].get_xticklabels(), visible = False) 
# 		axes[i].set_xlim([-1.5, 0.7]) 
# 		axes[i].set_ylim([0, 5]) 
# 	axes[1].set_ylabel("PDF") 
# 	return axes 

def setup_axes(element, ncols = 1, nrows = 3): 
	fig, axes = plt.subplots(ncols = ncols, nrows = nrows, 
		figsize = (ncols * 5, 10), sharex = True) 
	for i in range(nrows):  
		for j in range(ncols): 
			if i != nrows - 1: plt.setp(axes[i][j].get_xticklabels(), 
				visible = False) 
			if j != 0: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			# axes[i][j].set_xlim([-0.7, 0.7]) 
			axes[i][j].set_xlim([{"o": -0.7, "fe": -0.9}[element.lower()], 0.7]) 
			axes[i][j].set_ylim([0, {"o": 4.5, "fe": 3.6}[element.lower()]]) 
			axes[i][j].set_xticks([-0.5, 0.0, 0.5]) 
			if j == ncols - 1: axes[i][j].yaxis.set_label_position("right") 

	dummy = fig.add_subplot(111, facecolor = "white", zorder = -1) 
	posd = dummy.get_position() 
	posd.x0 = axes[-1][0].get_position().x0 
	posd.x1 = axes[-1][-1].get_position().x1 
	posd.y0 = axes[-1][0].get_position().y0 
	posd.y1 = axes[0][0].get_position().y1 
	dummy.set_position(posd) 
	dummy.set_xlabel("[%s/H]" % (element.capitalize()), labelpad = 30) 
	dummy.set_ylabel("PDF", labelpad = 15) 
	plt.setp(dummy.get_xticklabels(), visible = False) 
	plt.setp(dummy.get_yticklabels(), visible = False) 

	return axes 


def get_mdf(element, stars, min_rgal, max_rgal, min_absz, max_absz, 
	window = 0.2): 
	stars = stars.filter("zone_final", ">=", int(min_rgal / ZONE_WIDTH)) 
	stars = stars.filter("zone_final", "<=", int(max_rgal / ZONE_WIDTH) - 1) 
	stars = stars.filter("abszfinal", ">=", min_absz) 
	stars = stars.filter("abszfinal", "<=", max_absz) 
	stars = stars.filter("mass", ">", 0) 
	xvals = [-1. + 0.01 * _ for _ in range(201)] 
	dist = len(xvals) * [0.] 
	for i in range(len(xvals)): 
		filtered_stars = stars.filter("[%s/H]" % (element), ">=", 
			xvals[i] - window / 2) 
		filtered_stars = filtered_stars.filter("[%s/H]" % (element), "<=", 
			xvals[i] + window / 2) 
		# dist[i] = sum(filtered_stars["mass"]) 
		dist[i] = sum([a * (1 - vice.cumulative_return_fraction(b)) for a, b 
			in zip(filtered_stars["mass"], filtered_stars["age"])]) 
	norm = sum(dist) * (xvals[1] - xvals[0])  
	dist = [_ / norm for _ in dist] 
	return [xvals, dist] 

	# dist = (len(BINS) - 1) * [0.] 
	# for i in range(len(dist)): 
	# 	filtered_stars = stars.filter("[%s/h]" % (element), ">=", BINS[i]) 
	# 	filtered_stars = filtered_stars.filter("[%s/h]" % (element), "<=", 
	# 		BINS[i + 1]) 
	# 	dist[i] = sum(filtered_stars["mass"]) 
	# norm = sum(dist) * (BINS[1] - BINS[0]) 
	# dist = [i / norm for i in dist] 
	# return dist 


def plot_mdf(ax, element, stars, min_rgal, max_rgal, min_absz, max_absz, color, 
	label = False): 
	# centers = [(i + j) / 2. for i, j in zip(BINS[1:], BINS[:-1])] 
	xvals, mdf = get_mdf(element, stars, min_rgal, max_rgal, min_absz, max_absz) 
	kwargs = {
		"c": 	named_colors()[color] 
	} 
	if label: kwargs["label"] = r"%g - %g" % (min_rgal, max_rgal) 
	ax.plot(xvals, mdf, **kwargs) 


def target_mode_abundance(radius): 
	return -0.08 * (radius - 4) + 0.3 


# def main(element, output, stem): 
# 	axes = setup_axes(element) 
# 	output = vice.output(output) 
# 	output.stars["abszfinal"] = [abs(i) for i in zheights(
# 		output.name)[:output.stars.size[0]]] 
# 	radii = [3, 5, 7, 9, 11, 13, 15] 
# 	heights = [2.0, 1.0, 0.5, 0.0] 
# 	colors = ["black", "red", "gold", "green", "blue", "darkviolet"] 
# 	for i in range(len(heights) - 1): 
# 		axes[i].text(-0.5, 4, r"$\left|z\right|$ = %g - %g kpc" % (
# 			heights[i + 1], heights[i]), fontsize = 20) 
# 		for j in range(len(radii) - 1): 
# 			plot_mdf(axes[i], element, output.stars, radii[j], radii[j + 1], 
# 				heights[i + 1], heights[i], colors[j], label = i == 0) 
# 	leg = axes[0].legend(loc = mpl_loc("upper left"), ncol = 1, fontsize = 20, 
# 		frameon = False, bbox_to_anchor = (0.005, 0.99), handlelength = 0) 
# 	for i in range(len(radii) - 1): 
# 		leg.get_texts()[i].set_color(colors[i]) 
# 		leg.legendHandles[i].set_visible(False) 
# 	plt.tight_layout() 
# 	plt.subplots_adjust(hspace = 0) 
# 	plt.savefig("%s.png" % (stem)) 
# 	plt.savefig("%s.pdf" % (stem)) 
# 	plt.close() 

def apogee_data(): 
	raw = np.genfromtxt("./data/dr16stars.dat") 
	data = vice.dataframe({
		"[o/h]": 		[_[4] for _ in raw], 
		"[fe/h]": 		[_[6] for _ in raw], 
		"rgal": 		[_[11] for _ in raw], 
		"abszfinal": 	[abs(_[12]) for _ in raw] 
	}) 
	data["zone_final"] = [int(_ / ZONE_WIDTH) for _ in data["rgal"]] 
	data["[o/fe]"] = [a - b for a, b in zip(data["[o/h]"], data["[fe/h]"])] 
	data["mass"] = len(data["rgal"]) * [1.] 
	data["age"] = len(data["rgal"]) * [0.] 
	return data 


def plot_apogee_distributions(ax, element, min_rgal, max_rgal, min_absz, 
	max_absz, color): 
	xvals, mdf = get_mdf(element, apogee_data(), min_rgal, max_rgal, min_absz, 
		max_absz) 
	kwargs = {"c": named_colors()[color]} 
	ax.plot(xvals, mdf, **kwargs) 


def main(element, outputs, stem, radial_bins = [3, 5, 7, 9, 11, 13, 15], 
	z_bins = [0.0, 0.5, 1.0, 2.0], 
	labels = ["Inside-Out", "Late-Burst", "Outer-Burst"], 
	apogee = False): 
	axes = setup_axes(element, ncols = len(outputs) + int(apogee), 
		nrows = len(z_bins) - 1) 
	if apogee: labels.append("APOGEE DR16") 
	for i in range(len(axes[0])): axes[0][i].set_title(labels[i], fontsize = 25) 
	z_bins = list(sorted(z_bins))[::-1] # reverse ordering -> high z at top 
	for i in range(len(axes)): axes[i][-1].set_ylabel(
		r"$\left|z\right|$ = %g - %g" % (z_bins[i + 1], z_bins[i])) 
	outputs = [vice.output(_) for _ in outputs] 
	colors = ["black", "red", "gold", "green", "blue", "darkviolet"] 
	for i in outputs: i.stars["abszfinal"] = [abs(_) for _ in zheights(
		i.name)[:i.stars.size[0]]] 
	for i in range(len(axes[-1])): 
		for j in range(len(radial_bins) - 1): 
			axes[-1][i].scatter(target_mode_abundance(radial_bins[j]), 
				{"o": 4.25, "fe": 3.4}[element.lower()], 
				c = named_colors()[colors[j]], 
				marker = markers()["point"], s = 40, zorder = 10) 
	for i in range(len(z_bins) - 1): 
		for j in range(len(outputs)): 
			for k in range(len(radial_bins) - 1): 
				plot_mdf(axes[i][j], element, outputs[j].stars, radial_bins[k], 
					radial_bins[k + 1], z_bins[i + 1], z_bins[i], colors[k], 
					label = k in [2 * i, 2 * i + 1] and not j) 
				# if apogee: plot_apogee_distributions(axes[i][j], element, 
				# 	radial_bins[k], radial_bins[k + 1], z_bins[i + 1], z_bins[i], 
				# 	colors[k]) 
				# if i == len(z_bins) - 2: axes[i][j].scatter(
				# 	target_mode_abundance(radial_bins[k]), 
				# 	{"o": 4.25, "fe": 3.4}[element.lower()], 
				# 	c = named_colors()[colors[k]], 
				# 	marker = markers()["point"], s = 40, zorder = 10) 
		if apogee: 
			for k in range(len(radial_bins) - 1): 
				plot_apogee_distributions(axes[i][-1], element, radial_bins[k], 
					radial_bins[k + 1], z_bins[i + 1], z_bins[i], colors[k]) 
		else: pass 
	legend_kwargs = {
		"loc": 				mpl_loc("upper left"), 
		"ncol": 			1, 
		"fontsize": 		20, 
		"frameon": 			False, 
		"bbox_to_anchor": 	(0.01, 0.99), 
		"handlelength": 	0 
	}
	for i in range(len(z_bins) - 1): 
		leg = axes[i][0].legend(**legend_kwargs) 
		for j in range(len(leg.legendHandles)): 
			leg.get_texts()[j].set_color(colors[len(leg.legendHandles) * i + j])  
			leg.legendHandles[j].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(wspace = 0, hspace = 0, bottom = 0.1, left = 0.08) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 


