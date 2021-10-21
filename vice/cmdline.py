r"""
Runs a singlezone simulation from the command line. Alternatively, open the
documentation or the QuickStartTutorial.
"""

from __future__ import print_function
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	import vice
except (ImportError, ModuleNotFoundError):
	raise ModuleNotFoundError("""\
VICE not found. Source code and installation instructions can be found at \
<https://pypi.org/project/vice>.""")
import urllib.request
import math as m
import argparse
import sys
import os


def parse():
	"""
	Parse the command line arguments using argparse.ArgumentParser
	"""
	"""
	The description of each argument in the arguement parser fulfill the
	purpose of any comment blocks that would be present in this function.
	"""
	parser = argparse.ArgumentParser(
		description = """\
Run a simulation of a simple one-zone model and/or access VICE's \
documentation. """,
		epilog = """\
The functionality available on the command line is severely limited compared \
to the full python capabilities of VICE. In python, the user can specify \
their own functions of time to describe evolutionary parameters, construct \
their own stellar IMF, change their nucleosynthetic yield settings, and run \
multiple zones linked via gas and stellar migration. From the command line, \
users are restricted to smooth evolutionary histories, the built-in stellar \
IMFs, their default nucleosynthetic yields, and only one zone. For details on \
the implementation of VICE, see the associated documentation at \
<https://vice-astro.readthedocs.io>.\
""")

	parser.add_argument("-t", "--tutorial",
		help = """Download and launch VICE's QuickStartTutorial, a jupyter \
notebook intended to familiarize new users with the ins and outs of VICE.""",
		action = "store_true")

	parser.add_argument("-d", "--docs",
		help = "Open documentation in default web browser",
		action = "store_true")

	parser.add_argument("-f", "--force",
		help = "Force overwrite existing VICE outputs of the same name",
		action = "store_true")

	parser.add_argument("-r", "--recognized",
		help = "Print elements recognized by VICE",
		action = "store_true")

	parser.add_argument("-v", "--verbose",
		help = "Run the simulation in verbose mode",
		action = "store_true")

	parser.add_argument("-V", "--version",
		help = "Print the current version of VICE.",
		action = "store_true")

	parser.add_argument("-s", "--schmidt",
		help = """\
Implement star formation efficiency driven by the Kennicutt-Schmidt Law (i.e. \
SFE ~ Mgas^n)""",
		action = "store_true")

	parser.add_argument("--timedep",
		help = """\
The time dependence of the evolutionary model. Either 'constant', 'exp' \
(exponential decay), or 'linexp' (linear-exponential) (Default: constant)""",
		type = str,
		default = "constant")

	parser.add_argument("--mode",
		help = """\
The specification of the evolutionary model. Either 'ifr' for a specified \
infall rate, 'sfr' for a specified star formation rate, or 'gas' for a \
specified gas supply. The time evolution of this parameter is set by the \
argument --timedep (Default: ifr)""",
		type = str,
		default = "ifr")

	parser.add_argument("--name",
		help = "The name of the output (Default: \"onezonemodel\")",
		type = str,
		default = "onezonemodel")

	parser.add_argument("--normalization",
		help = """\
A fiducial value for the infall rate, gas supply, or star formation rate in \
Msun [yr^-1] (Default: 9.1). In the case of a constant time dependence, this \
will be the value of the constant itself. For exponential and \
linear-exponential time dependencies, this sets the prefactor.""",
		type = float,
		default = 9.1)

	parser.add_argument("--timescale",
		help = """\
The e-folding timescale of the infall rate, gas supply, or star formation \
rate in Gyr (Default: 4.0)""",
		type = float,
		default = 4.)

	parser.add_argument("--elements",
		help = """\
Elements to simulate the enrichment for separated by underscores \
(Default: \"fe_sr_o\")""",
		type = str,
		default = "fe_sr_o")

	parser.add_argument("--IMF",
		help = """The stellar initial mass function to assume (Default: \
\"kroupa\")""",
		type = str,
		default = "kroupa")

	parser.add_argument("--eta",
		help = """\
The mass loading factor (ratio of outflow to star formation rates) \
(Default: 2.5)""",
		type = float,
		default = 2.5)

	parser.add_argument("--enhancement",
		help = """The ratio of outflow to gas-phase metallicities (Default: \
1.0)""",
		type = float,
		default = 1.0)

	parser.add_argument("--delay",
		help = """Minimum delay time for type Ia supernovae in Gyr (Default: \
0.15)""",
		type = float,
		default = 0.15)

	parser.add_argument("--RIa",
		help = """\
The delay-time distribution for SNe Ia to adopt ('exp' or 'plaw') (Default: \
\"plaw\")""",
		type = str,
		default = "plaw")

	parser.add_argument("--Mg0",
		help = """\
The gas supply at time 0 in Msun (only relevant for infall histories) \
(Default: 6.0e9)""",
		type = float,
		default = 6.0e9)

	parser.add_argument("--smoothing",
		help = "The outflow smoothing timescale in Gyr (Default: 0)",
		type = float,
		default = 0)

	parser.add_argument("--tau_ia",
		help = """\
The e-folding timescale for SNe Ia in Gyr (only relevant for --ria=\"exp\") \
(Default: 1.5)""",
		type = float,
		default = 1.5)

	parser.add_argument("--tau_star",
		help = "Gas supply per unit star formation rate in Gyr (Default: 2)",
		type = float,
		default = 2.)

	parser.add_argument("--dt",
		help = "The timestep size in Gyr (Default: 0.01)",
		type = float,
		default = 0.01)

	parser.add_argument("--recycling",
		help = """\
The recycling fraction (continuous if a negative number) (Default: -1)""",
		type = float,
		default = -1)

	parser.add_argument("--MgSchmidt",
		help = """\
The normalization of the gas supply in Msun when implementing \
Kennicutt-Schmidt Law star formation efficiency (Default: 6.0e9)""",
		type = float,
		default = 6.0e9)

	parser.add_argument("--schmidt_index",
		help = """\
The power law index on Kennicutt-Schidt Law star formation efficiency \
(Default: 0.5)""",
		type = float,
		default = 0.5)

	parser.add_argument("--postMS",
		help = """\
The ratio of stellar post main sequence lifetimes to their main sequence \
lifetimes. (Default: 0.1)""",
		type = float,
		default = 0.1)

	parser.add_argument("--end",
		help = "The end time of the simulation in Gyr (Default: 10)",
		type = float,
		default = 10.)

	return parser


def print_help_message(parser):
	r"""
	Prints the help message if necessary

	Parameters
	----------
	parser : argparse.ArgumentParser
		The command line-argument parser object.

	Returns
	-------
	proceed : bool
		True if this program should continue with a simulation.
	"""
	if len(sys.argv) == 1:
		parser.print_usage()
		print("""
help: vice -h
      vice --help

To run VICE over the default parameters here, adding '-f' will achieve this, \
overwriting an existing onezonemodel.vice output in the current working \
directory.\

""")
		return False
	else:
		return True


def print_version(args):
	r"""
	Prints the VICE version number if necessary

	Parameters
	----------
	args : argparse.Namespace
		The command line arguments parsed via argparse.

	Returns
	-------
	proceed : bool
		True if this program should continue with a simulation.
	"""
	if args.version: print("VICE %s" % (vice.__version__))
	if "-V" in sys.argv: sys.argv.remove("-V")
	if "--version" in sys.argv: sys.argv.remove("--version")
	return len(sys.argv) > 1


def launch_tutorial(args):
	r"""
	Launches VICE's QuickStartTutorial jupyter notebook on GitHub.

	Parameters
	----------
	args : argparse.Namespace
		The command line arguments parsed via argparse.

	Returns
	-------
	proceed : bool
		True if this program should continue with a simulation.
	"""
	if args.tutorial:
		if download_tutorial():
			os.system("jupyter notebook %s/QuickStartTutorial.ipynb" % (
				vice.__path__[0]))
		else:
			# if it doesn't exist, it's because it couldn't get downloaded.
			# A previous version may still be there.
			raise RuntimeError("""\
Could not download VICE QuickStartTutorial jupyter notebook. \
Please check your internet connection and try again.""")
		if "-t" in sys.argv: sys.argv.remove("-t")
		if "--tutorial" in sys.argv: sys.argv.remove("--tutorial")
	else:
		pass
	return len(sys.argv) > 1


def download_tutorial():
	r"""
	Downloads VICE's tutorial into its installed directory if it isn't
	already present.

	Returns
	-------
	True if the jupyter notebook exists within VICE's install directory, False
	otherwise.
	"""
	filename = "%s/QuickStartTutorial.ipynb" % (vice.__path__[0])
	url = "https://raw.githubusercontent.com/giganano/VICE/main/examples"
	url += "/QuickStartTutorial.ipynb"
	try:
		urllib.request.urlretrieve(url, filename)
	except:
		pass
	return os.path.exists(filename)


def open_documentation(args):
	r"""
	Opens VICE's documentation in the default web browser if prompted

	Parameters
	----------
	args : argparse.Namespace
		The command line arguments parsed via argparse.

	Returns
	-------
	proceed : bool
		True if this program should continue with a simulation.
	"""
	if args.docs:
		import webbrowser
		url = "https://vice-astro.readthedocs.io"
		webbrowser.open(url)
		if "-d" in sys.argv: sys.argv.remove("-d")
		if "--docs" in sys.argv: sys.argv.remove("--docs")
	else:
		pass
	return len(sys.argv) > 1


def print_recognized_elements(args):
	r"""
	Prints the recognized elements if necessary

	Parameters
	----------
	args : argparse.Namespace
		The command line arguments parsed via argparse.

	Returns
	-------
	proceed : bool
		True if this program should continue with a simulation.
	"""
	if args.recognized: print(vice._globals._RECOGNIZED_ELEMENTS_)
	if "-r" in sys.argv: sys.argv.remove("-r")
	if "--recognized" in sys.argv: sys.argv.remove("--recognized")
	return len(sys.argv) > 1


def run_simulation(args):
	r"""
	Runs the simulation according to the arguments passed on the command line.
	
	Parameters
	----------
	args : argparse.Namespace
		The command line arguments parsed via argparse.
	"""

	# Stitch together the evolutionary function of time
	if args.timedep == "constant":
		function = lambda t: args.normalization
	elif args.timedep == "exp":
		function = lambda t: args.normalization * m.exp(-t / args.timescale)
	elif args.timedep == "linexp":
		function = lambda t: args.normalization * t * m.exp(-t / args.timescale)
	else:
		raise ValueError("Unrecognized time dependence: %s" % (args.timedep))

	# keyword args to vice.singlezone
	params = dict(
		name = args.name,
		func = function,
		mode = args.mode,
		elements = [i.lower() for i in args.elements.split('_')],
		IMF = args.IMF,
		eta = args.eta,
		enhancement = args.enhancement,
		delay = args.delay,
		RIa = args.RIa,
		Mg0 = args.Mg0,
		smoothing = args.smoothing,
		tau_ia = args.tau_ia,
		tau_star = args.tau_star,
		dt = args.dt,
		verbose = args.verbose,
		recycling = "continuous" if args.recycling < 0 else args.recycling,
		schmidt = args.schmidt,
		MgSchmidt = args.MgSchmidt,
		schmidt_index = args.schmidt_index,
		postMS = args.postMS
	)

	outtimes = [i * args.dt for i in range(int(args.end / args.dt) + 1)]
	vice.singlezone(**params).run(outtimes, overwrite = args.force)


def main():
	r"""
	Print the help message, print the recognized elements, and/or run a
	simulation based on the command line arguments
	"""
	parser = parse()
	if print_help_message(parser):
		args = parser.parse_args()
		if print_version(args):
			if launch_tutorial(args):
				if open_documentation(args):
					if print_recognized_elements(args):
						run_simulation(args)
					else: pass
				else: pass
			else: pass
		else: pass
	else: pass
	parser.exit()


if __name__ == "__main__":
	main()

