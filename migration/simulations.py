
import argparse 
import src 
from src.simulations.mass_loading import strong_mass_loading 
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

	parser.add_argument("--Sigma_gCrit", 
		help = """The critical gas surface density, in Msun/kpc^2. \
(Default: 2.0e+07)""", 
		type = float, 
		default = 2.0e+07) 

	parser.add_argument("--mass_loading", 
		help = """The mass-loading prescription. Either 'standard' or \
'strong'. (Default: "strong")""", 
		type = str, 
		default = "strong") 

	return parser 


def suite(args): 
	r""" 
	Get the simulation suite object. 

	Parameters 
	----------
	args : argparse.Namespace 
		The command line arguments parsed via argparse. 
	""" 
	# if args.migration == "all": 
	# 	migration = _MIGRATION_MODELS_ 
	# else: 
	# 	migration = [args.migration] 
	# if args.evolution == "all": 
	# 	evolution = _EVOLUTION_MODELS_ 
	# else: 
	# 	evolution = [args.evolution] 
	suite = src.simulations.suite(
		tau_star_mol = src.simulations.sfe(
			baseline = args.SFEmolecular, 
			index = args.SFEindex 
		), 
		star_particle_density = args.nstars, 
		timestep_size = args.dt, 
		elements = args.elements.split('_'), 
		zone_width = args.zonewidth, 
		Sigma_gCrit = args.Sigma_gCrit, 
		mass_loading = {
			"standard": 		milkyway.default_mass_loading, 
			"strong": 			strong_mass_loading 
		}[args.mass_loading] 
	) 
	kwargs = dict(
		name = args.name, 
		spec = args.evolution 
	) 
	if args.migration == "post-process": 
		kwargs["simple"] = True 
	else: 
		kwargs["migration_mode"] = args.migration 
	suite.add_simulation(
		src.simulations.diskmodel.from_config(suite.config, **kwargs) 
	) 
	return suite 
	# for i in migration: 
	# 	for j in evolution: 
	# 		kwargs = dict(
	# 			name = "%s/%s/%s" % (args.outdir, i, j), 
	# 			spec = j 
	# 		) 
	# 		if i == "post-process": 
	# 			kwargs["simple"] = True 
	# 		else: 
	# 			kwargs["migration_mode"] = i 
	# 		suite.add_simulation(
	# 			src.simulations.diskmodel.from_config(suite.config, **kwargs) 
	# 		) 
	# return suite 


if __name__ == "__main__": 
	parser = parse() 
	args = parser.parse_args() 
	suite(args).run(overwrite = args.force, pickle = False) 

