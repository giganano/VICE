r""" 
Sukhbold et al. (2016), ApJ, 821, 38 core collapse supernova yields 

**Signature**: from vice.yields.ccsne import S16 

Importing this module will automatically set the CCSN yield settings for all 
elements to the IMF-averaged yields calculated with the Sukhbold et al. (2016) 
yield table for [M/H] = 0 stars. This will adopt an upper mass limit of 
120 :math:`M_\odot`. 

.. tip:: By importing this module, the user does not sacrifice the ability to 
	specify their yield settings directly. 

.. note:: This module is not imported with a simple ``import vice`` statement. 

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

	__all__ = ["set_params", "test"]  
	from ...._globals import _RECOGNIZED_ELEMENTS_ 
	from .. import fractional as __fractional 
	from .. import settings as __settings 
	from .tests import test 

	def set_params(**kwargs): 
		r""" 
		Update the parameters with which the yields are calculated from the 
		Sukhbold et al. (2016) [1]_ data. 

		**Signature**: vice.yields.ccsne.S16.set_params(\*\*kwargs) 

		Parameters 
		----------
		kwargs : varying types 
			Keyword arguments to pass to vice.yields.ccsne.fractional. 

		Raises 
		------
		* TypeError 
			-	Recieved a keyword argument "study". This will always be 
				"S16/W18" when called from this module. 

		Other exceptions are raised by vice.yields.ccsne.fractional. 

		Example Code 
		------------
		>>> import vice 
		>>> from vice.yields.ccsne import S16 
		>>> S16.set_params(m_lower = 0.3, m_upper = 45, IMF = "salpeter") 

		.. seealso:: vice.yields.ccsne.fractional 

		.. [1] Sukhbold et al. (2016), ApJ, 821, 38 
		""" 
		if "study" in kwargs.keys(): 
			raise TypeError("Got an unexpected keyword argument: 'study'") 
		else: 
			for i in _RECOGNIZED_ELEMENTS_: 
				__settings[i] = __fractional(i, study = "S16/W18", **kwargs)[0] 

	set_params(m_upper = 120) 

else: 
	pass 

