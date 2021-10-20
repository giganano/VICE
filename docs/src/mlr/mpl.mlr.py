r"""
Produces a figure showing the lifetimes of stars as a function of zero age
main sequence mass according to the functional forms built into VICE.
"""


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter as fsf
import numpy as np
import vice

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"
mpl.rcParams["errorbar.capsize"] = 5
mpl.rcParams["axes.linewidth"] = 2
mpl.rcParams["xtick.major.size"] = 16
mpl.rcParams["xtick.major.width"] = 2
mpl.rcParams["xtick.minor.size"] = 8
mpl.rcParams["xtick.minor.width"] = 1
mpl.rcParams["ytick.major.size"] = 16
mpl.rcParams["ytick.major.width"] = 2
mpl.rcParams["ytick.minor.size"] = 8
mpl.rcParams["ytick.minor.width"] = 1
mpl.rcParams["axes.labelsize"] = 30
mpl.rcParams["xtick.labelsize"] = 25
mpl.rcParams["ytick.labelsize"] = 25
mpl.rcParams["legend.fontsize"] = 12
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["ytick.right"] = True
mpl.rcParams["xtick.top"] = True
mpl.rcParams["xtick.minor.visible"] = True
mpl.rcParams["ytick.minor.visible"] = True


_FORMS_ = {
	"larson1974": vice.mlr.larson1974,
	"mm1989": vice.mlr.mm1989,
	"pm1993": vice.mlr.pm1993,
	"ka1997": vice.mlr.ka1997,
	"hpt2000": vice.mlr.hpt2000,
	"vincenzo2016": vice.mlr.vincenzo2016,
	"powerlaw": vice.mlr.powerlaw
}

_LABELS_ = {
	"larson1974": "Larson (1974)",
	"mm1989": "Maeder \& Meynet (1989)",
	"pm1993": "Padovani \& Matteucci (1993)",
	"ka1997": "Kodama \& Arimoto (1997)",
	"hpt2000": "Hurley, Pols \& Tout (2000)",
	"vincenzo2016": "Vincenzo et al. (2016)",
	"powerlaw": r"$\tau \propto M^{-3.5}$"
}

_COLORS_ = {
	"larson1974": "black",
	"mm1989": "crimson",
	"pm1993": "gold",
	"ka1997": "green",
	"hpt2000": "blue",
	"vincenzo2016": "darkviolet",
	"powerlaw": "grey"
}


def main():
	r"""
	Produce the figure
	"""
	ax = setup_subplot()
	for form in _FORMS_.keys(): draw(ax, form)
	
	# highlight 1 Msun and 10 Gyr
	kwargs = {
		"c": mpl.colors.get_named_colors_mapping()["black"],
		"linestyle": ':'
	}
	ax.plot(2 * [1.], ax.get_ylim(), **kwargs)
	ax.plot(ax.get_xlim(), 2 * [10.], **kwargs)

	# Make the legend
	kwargs = {
		"loc": 9, # upper center
		"ncol": 1,
		"frameon": False,
		"bbox_to_anchor": (0.7, 0.96),
		"handlelength": 0,
	}
	leg = ax.legend(**kwargs)
	for i in range(len(_FORMS_.keys())):
		leg.get_texts()[i].set_color(_COLORS_[list(_FORMS_.keys())[i]])
		leg.legendHandles[i].set_visible(False)

	plt.tight_layout()
	for ext in ["pdf", "png"]: plt.savefig("mlr.%s" % (ext))


def draw(ax, form):
	r"""
	Plot a given mass-lifetime relation.

	Parameters
	----------
	ax : subplot
		The matplotlib axes to plot on
	form : str
		A string denoting which form to plot
	"""
	xvals = np.logspace(-1, 2, 1000)
	kwargs = {
		"c": mpl.colors.get_named_colors_mapping()[_COLORS_[form]],
		"label": _LABELS_[form]
	}
	yvals = [_FORMS_[form](_) for _ in xvals]
	ax.plot(xvals, yvals, **kwargs)


def setup_subplot():
	r"""
	Setup a matplotlib subplot to plot on
	"""
	plt.clf()
	fig = plt.figure(figsize = (6, 6), facecolor = "white")
	ax = fig.add_subplot(111)
	ax.set_xlabel(r"M$_\text{ZAMS}$ [M$_\odot$]")
	ax.set_ylabel(r"$\tau$ [Gyr]")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.xaxis.set_major_formatter(fsf("%g"))
	ax.yaxis.set_major_formatter(fsf("%g"))
	ax.set_xlim([0.07, 150])
	ax.set_ylim([1.e-3, 1.e+3])
	ax.set_xticks([0.1, 1, 10, 100])
	ax.set_yticks([10**_ for _ in range(-3, 4)])
	return ax


if __name__ == "__main__":
	main()

