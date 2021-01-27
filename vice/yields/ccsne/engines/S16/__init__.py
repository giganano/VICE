r""" 
Core collapse supernova explosion engines: explodability as a function of 
progenitor mass in solar masses as reported by the Sukhbold et al. (2016) [1]_ 
models. 

**Signature**: from vice.yields.ccsne.engines import S16 

.. tip:: Instances of the ``engine`` class can be passed the keyword argument 
	``explodability`` to ``vice.yields.ccsne.fractional`` to calculate 
	IMF-averaged yields assuming a particular black hole landscape. The impact 
	of these assumptions is explored in Griffith et al. (2021, in prep) [2]_. 

Contents 
--------
W18 : ``engine`` 
	An engine characterized by the W18 explosion model. 

.. [1] Sukhbold et al. (2016), ApJ, 821, 38 
.. [2] Griffith et al. (2021), in prep 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["W18", "test"]  
	# from .N20 import N20 
	from .W18 import W18 
	from .tests import test 

	# Instances of derived classes rather than derived classes themselves 
	# N20 = N20() 
	W18 = W18() 

else: pass 

