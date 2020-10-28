
import argparse 
import src 
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
		help = "The migration model to assume. (Default: all)", 
		type = str, 
		default = "all") 

	parser.add_argument("--evolution", 
		help = "The evolutionary history to assume (Default: all)", 
		type = str, 
		default = "all") 

	parser.add_argument("--SFEmolecular", 
		help = "SFE timescale of molecular gas at the present day (Default: 2)", 
		type = float, 
		default = 2.0) 

	parser.add_argument("--SFEindex", 
		help = """Power-law index on molecular gas SFE timescale with \
simulation time. (Default: 0)""", 
		type = float, 
		default = 0.0) 

	parser.add_argument("--dt", 
		help = "Timestep size in Gyr. (Default: 0.01)", 
		type = float, 
		default = 0.01) 

	parser.add_argument("--nstars", 
		help = """Number of stellar populations per zone per timestep. \
(Default: 2)""", 
		type = int, 
		default = 2) 

	parser.add_argument("--outdir", 
		help = "The name of the output directory (Default: '.')", 
		type = str, 
		default = '.') 

	parser.add_argument("--elements", 
		help = """Elements to simulation the enrichment for separated by \
underscores. (Default: \"fe_o\")""", 
		type = str, 
		default = "fe_o") 

	parser.add_argument("--zonewidth", 
		help = "The width of each annulus in kpc. (Default: 0.1)", 
		type = float, 
		default = 0.1) 

	parser.add_argument("--Sigma_gCrit", 
		help = """The critical gas surface density, in Msun/kpc^2. \
(Default: 2.0e+07)""", 
		type = float, 
		default = 2.0e+07) 

	return parser 


def suite(args): 
	r""" 
	Get the simulation suite object. 

	Parameters 
	----------
	args : argparse.Namespace 
		The command line arguments parsed via argparse. 
	""" 
	if args.migration == "all": 
		migration = _MIGRATION_MODELS_ 
	else: 
		migration = [args.migration] 
	if args.evolution == "all": 
		evolution = _EVOLUTION_MODELS_ 
	else: 
		evolution = [args.evolution] 
	suite = src.simulations.suite(
		tau_star_mol = src.simulations.sfe(
			baseline = args.SFEmolecular, 
			index = args.SFEindex 
		), 
		star_particle_density = args.nstars, 
		timestep_size = args.dt, 
		elements = args.elements.split('_'), 
		zone_width = args.zonewidth, 
		Sigma_gCrit = args.Sigma_gCrit 
	) 
	for i in migration: 
		for j in evolution: 
			kwargs = dict(
				name = "%s/%s/%s" % (args.outdir, i, j), 
				spec = j 
			) 
			if i == "post-process": 
				kwargs["simple"] = True 
			else: 
				kwargs["migration_mode"] = i 
			suite.add_simulation(
				src.simulations.diskmodel.from_config(suite.config, **kwargs) 
			) 
	return suite 


if __name__ == "__main__": 
	parser = parse() 
	args = parser.parse_args() 
	suite(args).run(overwrite = args.force, pickle = False) 

