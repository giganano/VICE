r"""
Ensures runtime dependencies are satisfied for producing figures in Johnson et
al. (2021).

Dependencies:

	- matplotlib >= 2.0.0
	- NumPy >= 1.17.0
"""

try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError

# Enforce matplotlib >= 2.0.0 or else RuntimeError
try:
	import matplotlib as mpl
except (ModuleNotFoundError, ImportError):
	raise ModuleNotFoundError("Matplotlib not found.")
if tuple([int(i) for i in mpl.__version__.split('.')])[:2] < (2, 0):
	raise RuntimeError("""Matplotlib version >= 2.0.0 required for producing \
Johnson et al. (2021) figures. Current: %s""" % (mpl.__version__))
else: pass

# Enforce NumPy >= 1.17.0 or else RuntimeError
try:
	import numpy as np
except (ModuleNotFoundError, ImportError):
	raise ModuleNotFoundError("NumPy not found.")
if tuple([int(i) for i in np.__version__.split('.')])[:2] < (1, 17):
	raise RuntimeError("""NumPy version >= 1.17.0 required for producing \
Johnson et al. (2021) figures. Current: %s""" % (np.__version__))
else: pass


# by setting matplotlib rcParams here, all plots will be automatically
# formatted since this file will be imported everywhere to ensure dependencies
# are met anyway.
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
mpl.rcParams["legend.fontsize"] = 25
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["ytick.right"] = True
mpl.rcParams["xtick.top"] = True
mpl.rcParams["xtick.minor.visible"] = True
mpl.rcParams["ytick.minor.visible"] = True

