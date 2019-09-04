""" 
Matplotlib rc Parameters 
======================== 
This file declares rc parameters in matplotlib for running VICE's 
visualization features. 
""" 

# try: 
# 	ModuleNotFoundError 
# except NameError: 
# 	ModuleNotFoundError = ImportError 
# try: 
# 	import matplotlib as mpl 
# except (ModuleNotFoundError, ImportError): 
# 	raise ModuleNotFoundError("Matplotlib not found.") 
import matplotlib as mpl 

mpl.rcParams["font.family"] = "serif"
mpl.rcParams["text.usetex"] = True 
mpl.rcParams["text.latex.preamble"] = [r"\usepackage{amsmath}"]
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
