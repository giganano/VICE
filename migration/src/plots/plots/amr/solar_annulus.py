r""" 
This script produces a plot of the age-[O/H] and age-[Fe/H] relations in the 
solar annulus predicted by the simulations and in comparison to the 
Feuillet et al. (2019) data. 
""" 

from ... import env 
from ...utils import zheights, weighted_median, feuillet2019_data 
from ..utils import named_colors, mpl_loc, markers, xticklabel_formatter 
from .galactic_regions import plot_amr, median_ages, feuillet2019_amr 
import matplotlib.patheffects as pe 
import matplotlib.pyplot as plt 
import numpy as np 
import vice 

def setup_axes(): 
	fig = plt.figure(figsize = (7, 12)) 
	ax2 = fig.add_subplot(212, facecolor = "white") 
	ax1 = fig.add_subplot(211, facecolor = "white", sharex = ax2) 
	ax2.set_xscale("log") 
	ax2.set_xlim([0.4, 20]) 
	ax1.set_ylim([-0.8, 0.6]) 
	ax2.set_ylim([-1.4, 0.6]) 
	ax1.set_yticks([-0.5, 0.0, 0.5]) 
	ax2.set_yticks([-1.0, -0.5, 0.0, 0.5]) 
	plt.setp(ax1.get_xticklabels(), visible = False) 
	xticklabel_formatter(ax2) 
	ax2.set_xlabel("Age [Gyr]") 
	ax2.set_ylabel("[Fe/H]") 
	ax1.set_ylabel("[O/H]") 
	return [ax1, ax2] 


def feuillet2018_amr(ax, element, label = True): 
	raw = np.genfromtxt("./data/feuillet2018/age_%s.dat" % ({
		"o": 	"oh", 
		"fe": 	"mh" 
		}[element.lower()])).tolist() 
	lowers = [_[0] for _ in raw] 
	uppers = [_[1] for _ in raw] 
	abundance = [(a + b) / 2 for a, b in zip(lowers, uppers)] 
	age = [10**(_[2] - 9) for _ in raw] # -9 yr -> Gyr 
	outline = pe.withStroke(linewidth = 4, foreground = "white") 
	kwargs = {
		"c": 				named_colors()["darkred"], 
		"path_effects": 	[outline], 
		"zorder": 			1 
	} 
	if label: kwargs["label"] = "Feuillet et al. (2018)" 
	ax.plot(age, abundance, **kwargs) 


def main(output, stem): 
	ax1, ax2 = setup_axes() 
	output = vice.output(output) 
	output.stars["abszfinal"] = [abs(_) for _ in zheights(
		output.name)[:output.stars.size[0]]] 
	plot_amr(ax1, "O", "H", output, 7, 9, 0, 0.5) 
	sc = plot_amr(ax2, "Fe", "H", output, 7, 9, 0, 0.5) 
	median_ages(ax1, "O", "H", output, 7, 9, 0, 0.5, zorder = 2) 
	median_ages(ax2, "Fe", "H", output, 7, 9, 0, 0.5, label = True, zorder = 2) 
	feuillet2019_amr(ax1, "O", "H", 7, 9, 0, 0.5, zorder = 2) 
	feuillet2019_amr(ax2, "Fe", "H", 7, 9, 0, 0.5, label = True, zorder = 2) 
	feuillet2018_amr(ax1, 'o') 
	feuillet2018_amr(ax2, 'fe', label = True) 
	kwargs = {
		"ncol": 			1, 
		"frameon": 			False, 
		"fontsize": 		20, 
		"loc": 				mpl_loc("lower left"), 
		"bbox_to_anchor": 	(0.01, 0.01) 
	} 
	# ax2.legend(**kwargs) 
	handles, labels = ax2.get_legend_handles_labels() 
	handles = [handles[1], handles[2], handles[0]] 
	labels = [labels[1], labels[2], labels[0]] 
	ax2.legend(handles, labels, **kwargs) 
	cbar_ax = plt.gcf().add_axes([0.92, 0.05, 0.02, 0.95]) 
	cbar = plt.colorbar(sc, cax = cbar_ax, pad = 0.0, orientation = "vertical") 
	cbar.set_label(r"$R_\text{gal}$ of birth [kpc]", labelpad = 10) 
	cbar.set_ticks(range(2, 16, 2)) 
	plt.tight_layout() 
	plt.subplots_adjust(hspace = 0, right = 0.8) 
	cbar_ax.set_position([
		ax2.get_position().x1, 
		ax2.get_position().y0, 
		0.05, 
		ax1.get_position().y1 - ax2.get_position().y0 
	]) 
	plt.savefig("%s.pdf" % (stem)) 
	plt.savefig("%s.png" % (stem)) 
	plt.close() 

