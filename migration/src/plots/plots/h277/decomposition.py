r""" 
This script produces a plot of the birth/final radii distributions of h277 
star particles in bins of their birth/final radii and age. 
""" 

from ... import env 
from ..utils import named_colors, mpl_loc, dummy_background_axes 
from vice.toolkit.hydrodisk import hydrodiskstars 
from ...._globals import END_TIME 
import matplotlib.pyplot as plt 
import numpy as np 


def main(stem): 
	axes = setup_axes() 
	h277 = hydrodiskstars([0.1 * _ for _ in range(201)], N = 1e10) 
	h277.analog_data["age"] = [END_TIME - _ for _ in h277.analog_data["tform"]] 
	age_bins = [[0, 2], [2, 4], [4, 6], [6, 8], [8, 10]] 
	# age_bins = [[0, 0.4], [0.4, 0.8], [0.8, 1.2], [1.2, 1.6], [1.6, 2.0]] 
	rbins = [[5, 7], [7, 9], [9, 11], [11, 13]] 
	colors = ["darkviolet", "blue", "green", "gold", "red"] 
	for i in range(len(axes[0])): 
		if rbins[i][1] >= 11: 
			text_radius = 0 
		else: 
			text_radius = 12 
		axes[0][i].text(text_radius, 0.3, 
			r"$R_\text{Birth}$ = %d - %d" % (rbins[i][0], rbins[i][1]), 
			fontsize = 20) 
		axes[1][i].text(text_radius, 0.34, 
			r"$R_\text{Final}$ = %d - %d" % (rbins[i][0], rbins[i][1]), 
			fontsize = 20) 
		for j in range(len(age_bins)): 
			plot_subsample(axes[1][i], h277, rbins[i][0], rbins[i][1], 
				age_bins[j][0], age_bins[j][1], color = colors[j]) 
			plot_subsample(axes[0][i], h277, rbins[i][0], rbins[i][1], 
				age_bins[j][0], age_bins[j][1], cut = "rform", plot = "rfinal", 
				color = colors[j], label = not i) 
		axes[0][i].plot(2 * [rbins[i][0]], axes[0][i].get_ylim(), 
			c = named_colors()["black"], linestyle = ':') 
		axes[0][i].plot(2 * [rbins[i][1]], axes[0][i].get_ylim(), 
			c = named_colors()["black"], linestyle = ':') 
		axes[1][i].plot(2 * [rbins[i][0]], axes[1][i].get_ylim(), 
			c = named_colors()["black"], linestyle = ':') 
		axes[1][i].plot(2 * [rbins[i][1]], axes[1][i].get_ylim(), 
			c = named_colors()["black"], linestyle = ':') 
	leg = axes[0][0].legend(loc = mpl_loc("lower right"), ncol = 1, 
		frameon = False, bbox_to_anchor = (0.99, 0.01), handlelength = 0) 
	for i in range(len(age_bins)): 
		leg.get_texts()[i].set_color(colors[i]) 
		leg.legendHandles[i].set_visible(False) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, wspace = 0, left = 0.05, bottom = 0.1) 
	plt.savefig("%s.png" % (stem)) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.close() 


def plot_subsample(ax, h277, min_rgal, max_rgal, min_age, max_age, 
	cut = "rfinal", plot = "rform", color = "black", label = False): 
	stars = subsample(h277, min_rgal, max_rgal, min_age, max_age, which = cut) 
	print(len(stars["id"])) 
	xvals, pdf = calculate_pdf(stars, which = plot) 
	kwargs = {"c": named_colors()[color]} 
	if label: kwargs["label"] = "%g - %g Gyr" % (min_age, max_age) 
	ax.plot(xvals, pdf, **kwargs) 


def subsample(h277, min_rgal, max_rgal, min_age, max_age, which = "rfinal"): 
	return h277.analog_data.filter(
		which, ">=", min_rgal 
	).filter( 
		which, "<=", max_rgal 
	).filter(
		"age", ">=", min_age 
	).filter(
		"age", "<=", max_age 
	) 


def calculate_pdf(stars, which = "rform", window = 0.5): 
	xvals = [0.02 * i for i in range(1001)] 
	if len(stars["id"]) < 0.8 * len(xvals): 
		return [float("nan"), float("nan")] 
	elif len(stars["id"]) < 3 * len(xvals): 
		window *= 2 
	else: pass 
	dist = len(xvals) * [0.] 
	for i in range(len(xvals)): 
		test = [xvals[i] - window / 2 <= stars[which][_] <= 
			xvals[i] + window / 2 for _ in range(len(stars[which]))] 
		dist[i] = sum(test) 
	norm = sum(dist) * (xvals[1] - xvals[0]) 
	dist = [_ / norm for _ in dist] 
	return xvals, dist 
	# dist, bins = np.histogram(stars[which], range = [0, 20], bins = 200, 
	# 	density = True)  
	# xvals = [(a + b) / 2. for a, b in zip(bins[1:], bins[:-1])] 
	# return [xvals, dist] 


def setup_axes(): 
	fig = plt.figure(figsize = (20, 10)) 
	axes = 2 * [None] 
	for i in range(len(axes)): 
		axes[i] = 4 * [None] 
		for j in range(len(axes[i])): 
			axes[i][j] = fig.add_subplot(241 + 4 * i + j, facecolor = "white") 
			if i != len(axes) - 1: plt.setp(axes[i][j].get_xticklabels(), 
				visible = False) 
			if j: plt.setp(axes[i][j].get_yticklabels(), visible = False) 
			axes[i][j].set_xlim([-2, 22]) 
			if i: 
				axes[i][j].set_ylim([0, 0.399]) 
			else: 
				axes[i][j].set_ylim([0, 0.36]) 
			# axes[i][j].set_ylim([0, 0.5]) 
			axes[i][j].set_xticks([0, 5, 10, 15, 20])
	dummy = dummy_background_axes(axes) 
	dummy.set_xlabel(r"$R_\text{gal}$ [kpc]", labelpad = 30) 
	dummy.set_ylabel("PDF", labelpad = 30) 
	return axes 

