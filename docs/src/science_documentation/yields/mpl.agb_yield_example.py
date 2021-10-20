r"""
This script produces a figure showing an example table of AGB star yields
using barium as the representative element.
This figure is used to justify why VICE enforces non-negative yields for
progenitor masses below 1.5 :math:`M_\odot`.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
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

_ZVALS_ = [0.0001, 0.003, 0.008, 0.014]
_COLORS_ = ["blue", "lime", "crimson", "black"]
_LOGPREFACTOR_ = 7

def main():
	ax = setup_axis()
	y, m, z = vice.yields.agb.grid("ba", study = "cristallo11")
	for i in range(len(_ZVALS_)):
		idx = z.index(_ZVALS_[i])
		yields = [10**_LOGPREFACTOR_ * y[_][idx] for _ in range(len(y))]
		kwargs = {"c": mpl.colors.get_named_colors_mapping()[_COLORS_[i]]}
		ax.plot(m, yields, **kwargs)
		kwargs["marker"] = 'o'
		kwargs['s'] = 50
		kwargs["label"] = "Z = %g" % (_ZVALS_[i])
		ax.scatter(m, yields, **kwargs)

	leg = ax.legend(loc = 1, ncol = 1, frameon = False, handlelength = 0,
		bbox_to_anchor = (0.99, 0.99), fontsize = 20)
	for i in range(len(_ZVALS_)):
		leg.get_texts()[i].set_color(_COLORS_[i])
		leg.legendHandles[i].set_visible(False)

	plt.tight_layout()
	for ext in ["pdf", "png"]: plt.savefig("agb_yield_example.%s" % (ext))


def setup_axis():
	r"""
	Setup a matplotlib subplot to plot on.
	"""
	fig = plt.figure(figsize = (5, 5), facecolor = "white")
	ax = fig.add_subplot(111)
	ax.set_xlabel(r"$M_\text{ZAMS}$ [$M_\odot$]")
	ax.set_ylabel(r"$y_\text{Ba}^\text{AGB}$ [$\times10^{-%d}$]" % (
		_LOGPREFACTOR_))
	ax.set_xlim([0.5, 6.5])
	ax.set_ylim([-0.2, 3])
	return ax


if __name__ == "__main__": main()

