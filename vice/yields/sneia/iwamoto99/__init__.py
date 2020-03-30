r"""
Iwamoto et al. (1999), ApJ, 124, 439 type Ia supernova (SN Ia) yields 

**Signature**: from vice.yields.sneia import iwamoto99 

Importing this module will automatically set the SN Ia yield settings for all 
elements to the IMF-averaged yields calculated with the Iwamoto et al. (1999) 
yield table under the W70 explosion model. This study is for Chandrasekhar 
Mass progenitors (1.4 :math:`M_\odot`). 

.. tip:: By importing this module, the user does not sacrifice the ability to 
	specify their yield settings directly. 

.. note:: This module is not imported with a simple "import vice" statement. 

Contents 
--------
set_params : <function> 
	Update the parameters with which the yields are calculated. 
""" 

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["set_params"] 
	from ...._globals import _RECOGNIZED_ELEMENTS_ 
	from .. import fractional as __fractional 
	from .. import settings as __settings 

	for i in _RECOGNIZED_ELEMENTS_: 
		__settings[i] = __fractional(i, study = "iwamoto99", model = "W70")  


	def set_params(**kwargs): 
		r"""
		Update the parameters with which the yields are calculated from the 
		Iwamoto et al. (1999) [1]_ data. 

		Parameters 
		----------
		kwargs : varying types
			Keyword arguments to pass to vice.yields.sneia.fractional. 

		Raises 
		------
		* TypeError 
			- Received a keyword argument "study". This will always be 
				"iwamoto99" when called from this module. 

		Other exceptions are raised by vice.yields.sneia.fractional. 

		Example Code 
		------------
		>>> from vice.yields.sneia import iwamoto99 
		>>> iwamoto99.set_params(n = 1.5e-03) 

		.. seealso:: vice.yields.sneia.fractional 
			vice.yields.sneia.single 

		.. [1] Iwamoto et al. (1999), ApJ, 124, 439 
		"""
		if "study" in kwargs.keys(): 
			raise TypeError("Got an unexpected keyword argument 'study'") 
		else: 
			# Override the default, which is for Seitenzahl et al. (2013) yields 
			if "model" not in kwargs.keys(): kwargs["model"] = "W70" 
			for i in _RECOGNIZED_ELEMENTS_: 
				__settings[i] = __fractional(i, study = "iwamoto99", **kwargs) 

else: 
	pass 

