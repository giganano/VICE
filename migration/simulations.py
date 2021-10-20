r"""
This script runs the models in Johnson et al. (2021).

Run ``python simulations.py --help`` for more info.
"""

import argparse
import src
from vice import milkyway
import sys

_MIGRATION_MODELS_ = ["diffusion", "linear", "post-process", "sudden"]
_EVOLUTION_MODELS_ = ["static", "insideout", "lateburst", "outerburst"]

def parse():
	r"""
	Parse the command line arguments using argparse.ArgumentParser
	"""
	parser = argparse.ArgumentParser(
		description = "The parameters of the Milky Way models to run.")

	parser.add_argument("-f", "--force",
		help = "Force overwrite existing VICE outputs of the same name.",
		action = "store_true")

	parser.add_argument("--migration",
		help = "The migration model to assume. (Default: diffusion)",
		type = str,
		default = "diffusion")

	parser.add_argument("--evolution",
		help = "The evolutionary history to assume (Default: insideout)",
		type = str,
		default = "insideout")

	parser.add_argument("--dt",
		help = "Timestep size in Gyr. (Default: 0.01)",
		type = float,
		default = 0.01)

	parser.add_argument("--nstars",
		help = """Number of stellar populations per zone per timestep. \
(Default: 2)""",
		type = int,
		default = 2)

	parser.add_argument("--name",
		help = "The name of the output simulations (Default: 'milkway')",
		type = str,
		default = 'milkyway')

	parser.add_argument("--elements",
		help = """Elements to simulation the enrichment for separated by \
underscores. (Default: \"fe_o\")""",
		type = str,
		default = "fe_o")

	parser.add_argument("--zonewidth",
		help = "The width of each annulus in kpc. (Default: 0.1)",
		type = float,
		default = 0.1)

	return parser


def model(args):
	r"""
	Get the milkyway object corresponding to the desired simulation.

	Parameters
	----------
	args : argparse.Namespace
		The command line arguments parsed via argparse.
	"""
	config = src.simulations.config(
		timestep_size = args.dt,
		star_particle_density = args.nstars,
		zone_width = args.zonewidth,
		elements = args.elements.split('_')
	)
	kwargs = dict(
		name = args.name,
		spec = args.evolution
	)
	if args.migration == "post-process":
		kwargs["simple"] = True
	else:
		kwargs["migration_mode"] = args.migration
	return src.simulations.diskmodel.from_config(config, **kwargs)


def main():
	r"""
	Runs the script.
	"""
	parser = parse()
	args = parser.parse_args()
	model_ = model(args)
	model_.run([_ * model_.dt for _ in range(round(
		src._globals.END_TIME / model_.dt) + 1)],
		overwrite = args.force, pickle = False)


if __name__ == "__main__": main()

