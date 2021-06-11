r""" 
Sukhbold et al. (2016), ApJ, 821, 38 W18 Engine with Forced Explosions 

**Signature**: from vice.yields.ccsne.S16 import W18F 

.. versionadded:: 1.2.0 

Importing this module will automatically set the CCSN yield settings for all 
elements to the IMF-averaged yields calculated with the Sukhbold et al. (2016) 
yield table under the W18F explosion engine for [M/H] = 0 stars. This will 
adopt an upper mass limit of 120 :math:`M_\odot`. 

For details on the nature of the forced explosion model, see discussion in 
Griffith et al. (2021) [1]_. 

.. tip:: By importing this module the user does not sacrifice the ability to 
	specify their yield settings directly. 

.. note:: This module is not imported with a simple ``import vice`` statement. 

.. note:: When this module is imported, the yields will be updated with a 
	maximum of 10^5 bins in quadrature to decrease computational overhead. For 
	some elements, the yield calculation may not converge. To rerun the yield 
	calculation with higher numerical precision, simply call ``set_params`` 
	with a new value for the keyword ``Nmax`` (see below). 

Contents 
--------
set_params : <function> 
	Update the parameters with which the yields are calculated. 

.. [1] Griffith et al. (2021), arxiv:2103.09837 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["set_params", "test"] 
	from ....._globals import _RECOGNIZED_ELEMENTS_ 
	from ... import fractional as __fractional 
	from ... import settings as __settings 
	from .tests import test 

	def set_params(**kwargs): 
		r""" 
		Update the parameters with which the yields are calculated from the 
		Sukhbold et al. (2016) [1]_ W18F explosion engine data. 

		**Signature**: vice.yields.ccsne.S16.W18F.set_params(\*\*kwargs) 

		Parameters 
		----------
		kwargs : varying types 
			Keyword arguments to pass to vice.yields.ccsne.fractional. 

		Raises 
		------
		* TypeError 
			- 	Received a keyword argument "study". This will always be 
				"S16/W18F" when called from this module. 

		Other exceptions are raised by vice.yields.ccsne.fractional. 

		Example Code 
		------------
		>>> import vice 
		>>> from vice.yields.ccsne.S16 import W18F 
		>>> W18F.set_params(m_lower = 0.3, m_upper = 45, IMF = "salpeter") 

		.. seealso:: vice.yields.ccsne.fractional 

		.. [1] Sukhbold et al. (2016), ApJ, 821, 38 
		""" 
		if "study" in kwargs.keys(): 
			raise TypeError("Got an unexpected keyword argument: 'study'") 
		else: 
			for i in _RECOGNIZED_ELEMENTS_: 
				__settings[i] = __fractional(i, study = "S16/W18F", **kwargs)[0] 

	set_params(m_upper = 120, Nmax = 1e5) 

else: 
	pass 

