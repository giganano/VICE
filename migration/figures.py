r"""
This script produces the figures in Johnson et al. (2021).

Run ``python figures.py --help`` for more info.
"""

import argparse
import src
import os


# The functions that must be called to produce each figure
_FUNCTIONS_ = {
	"fig1": 	src.plots.h277_decomposition,
	"fig2": 	src.plots.migration,
	"fig3": 	src.plots.eta_tau_sfh,
	"fig4": 	src.plots.evol,
	"fig5": 	src.plots.sfe,
	"fig6": 	src.plots.surface_density_gradient,
	"fig7": 	src.plots.ofe_feh_densitymap,
	"fig8": 	src.plots.tracks,
	"fig9": 	src.plots.metallicity_gradient,
	"fig10": 	src.plots.mdf_3panel,
	"fig11": 	src.plots.mdf_3panel,
	"fig12": 	src.plots.ofe_mdfs,
	"fig13a": 	src.plots.age_ofe,
	"fig13b": 	src.plots.age_ofe,
	"fig14": 	src.plots.amr.galactic_regions,
	"fig15": 	src.plots.amr.comparison,
	"fig16": 	src.plots.amr.solar_annulus,
	"fig17": 	src.plots.amr.comparison,
	"fig18": 	src.plots.amr.comparison
}


# The arguments that must be passed to each function.
_ARGS_ = {
	"fig1": 	["./figures/fig1"],
	"fig2": 	["./figures/fig2"],
	"fig3": 	["./figures/fig3"],
	"fig4": 	["./outputs/diffusion/static",
					"./outputs/diffusion/insideout",
					"./outputs/diffusion/lateburst",
					"./outputs/diffusion/outerburst",
					"./figures/fig4"],
	"fig5": 	[["./outputs/diffusion/insideout"],
					"./figures/fig5"],
	"fig6": 	["./outputs/diffusion/insideout",
					"./figures/fig6"],
	"fig7": 	["./outputs/diffusion/insideout",
					"./outputs/post-process/insideout",
					"./figures/fig7"],
	"fig8": 	["./outputs/diffusion/insideout",
					"./outputs/post-process/insideout",
					"./figures/fig8"],
	"fig9": 	["./outputs/diffusion/static",
					"./outputs/diffusion/insideout",
					"./outputs/diffusion/lateburst",
					"./outputs/diffusion/outerburst",
					"./figures/fig9"],
	"fig10": 	["Fe",
					["./outputs/diffusion/insideout"],
					"./figures/fig10"],
	"fig11": 	["O",
					["./outputs/diffusion/insideout"],
					"./figures/fig11"],
	"fig12": 	["./outputs/diffusion/insideout",
					"./figures/fig12"],
	"fig13a": 	["./outputs/post-process/insideout",
					"./outputs/diffusion/insideout",
					"./outputs/sudden/insideout",
					"./outputs/linear/insideout",
					"./figures/fig13a"],
	"fig13b": 	["./outputs/diffusion/static",
					"./outputs/diffusion/insideout",
					"./outputs/diffusion/lateburst",
					"./outputs/diffusion/outerburst",
					"./figures/fig13b"],
	"fig14": 	["O", "Fe",
					"./outputs/diffusion/insideout",
					"./figures/fig14"],
	"fig15": 	["O",
					["./outputs/diffusion/static"],
					"./figures/fig15"],
	"fig16": 	["./outputs/diffusion/insideout",
					"./figures/fig16"],
	"fig17": 	["Fe",
					["./outputs/diffusion/insideout",
					"./outputs/diffusion/lateburst"],
					"./figures/fig17"],
	"fig18": 	["O",
					["./outputs/diffusion/insideout",
					"./outputs/diffusion/lateburst",
					"./outputs/diffusion/outerburst"],
					"./figures/fig18"]
}


# The keyword arguments that must be passed to each function.
_KWARGS_ = {
	"fig1": 	{},
	"fig2": 	{},
	"fig3": 	{},
	"fig4": 	{},
	"fig5": 	{"labels": None},
	"fig6": 	{},
	"fig7": 	{},
	"fig8": 	{},
	"fig9": 	{},
	"fig10": 	{"labels": ["Inside-Out"]},
	"fig11": 	{"labels": ["Inside-Out"]},
	"fig12": 	{},
	"fig13a": 	{"names": [["Post-Process", "Diffusion"], ["Sudden", "Linear"]]},
	"fig13b": 	{},
	"fig14": 	{},
	"fig15": 	{"feuillet2019": False, "radii": [[7, 9], [11, 13]],
					"labels": None, "left": 0.15, "right": 0.85, "bottom": 0.18},
	"fig16": 	{},
	"fig17": 	{"labels": ["Inside-Out", "Late-Burst"]},
	"fig18": 	{"labels": ["Inside-Out", "Late-Burst", "Outer-Burst"]}
}


def parse():
	r"""
	Parse the command line arguments using argparse.ArgumentParser
	"""
	parser = argparse.ArgumentParser(
		description = "Produce the figures in Johnson et al. (2021).")

	for i in range(1, 19):
		if i == 13:
			for j in ["a", "b"]:
				parser.add_argument("--fig%d%s" % (i, j),
					help = "Produce Fig. %d%s." % (
						i, j),
					action = "store_true")
		else:
			parser.add_argument("--fig%d" % (i),
				help = "Produce Fig. %d." % (i),
				action = "store_true")

	return parser


def produce_figure(key):
	r"""
	Produce a figure of Johnson et al. (2021).

	Parameters
	----------
	key : str
		"fig" followed by the number of the figure to produce.
	"""
	_FUNCTIONS_[key](*_ARGS_[key], **_KWARGS_[key])


def main():
	r"""
	Runs the script.
	"""
	# Put the user in this directory for the duration of the program
	src_path = os.path.dirname(os.path.abspath(__file__))
	old_path = os.getcwd()
	os.chdir(src_path)
	if not os.path.exists("figures") or (
		os.path.exists("figures") and not os.path.isdir("figures")):
			os.mkdir("figures")
	else: pass
	parser = parse()
	args = parser.parse_args()
	if args.fig1: produce_figure("fig1")
	if args.fig2: produce_figure("fig2")
	if args.fig3: produce_figure("fig3")
	if args.fig4: produce_figure("fig4")
	if args.fig5: produce_figure("fig5")
	if args.fig6: produce_figure("fig6")
	if args.fig7: produce_figure("fig7")
	if args.fig8: produce_figure("fig8")
	if args.fig9: produce_figure("fig9")
	if args.fig10: produce_figure("fig10")
	if args.fig11: produce_figure("fig11")
	if args.fig12: produce_figure("fig12")
	if args.fig13a: produce_figure("fig13a")
	if args.fig13b: produce_figure("fig13b")
	if args.fig14: produce_figure("fig14")
	if args.fig15: produce_figure("fig15")
	if args.fig16: produce_figure("fig16")
	if args.fig17: produce_figure("fig17")
	if args.fig18: produce_figure("fig18")
	os.chdir(old_path) # move them back to their old directory


if __name__ == "__main__": main()

