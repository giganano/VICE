""" 
Visualization Tools 
=================== 
""" 

from __future__ import absolute_import 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	import vice 
except (ModuleNotFoundError, ImportError): 
	raise RuntimeError("VICE not found.") 
try: 
	import matplotlib as mpl 
except (ModuleNotFoundError, ImportError): 
	raise ModuleNotFoundError("Matplotlib not found.")  
if int(mpl.__version__[0]) < 2: 
	raise RuntimeError(""""Matplotlib version >= 2.0.0 required. Current \
version: %s""" % (mpl.__version__)) 
else: 
	pass 
import matplotlib.pyplot as plt 
import sys 
import os 


