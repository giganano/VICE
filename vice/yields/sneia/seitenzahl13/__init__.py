r"""
Seitenzahl et al. (2013), MNRAS, 429, 1156 typa Ia supernova (SN Ia) yields 

**Signature**: from vice.yields.sneia import seitenzahl13 

Importing this module will automatically set the SN Ia yield settings for all 
elements to the IMF-averaged yields calculated with the Seitenzahl et al. 
(2013) yield table under the N1 explosion model. This study is for delayed 
detonation explosion models of Chandrasekhar mass progenitors 
(1.4 :math:`M_\odot`). 

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
		Seitenzahl et al. (2013) [1]_ data. 

		**Signature**: vice.yields.sneia.seitenzahl13(\*\*kwargs) 

		Parameters 
		---------- 
		kwargs : varying types 
			Keyword arguments to pass to vice.yields.sneia.fractional.  

		Raises 
		------
		* TypeError 
			- 	Received a keyword argument "study". This will always be 
				"seitenzahl13" when called from this module. 

		Other exceptions are raised by vice.yields.sneia.fractional.  

		.. seealso:: vice.yields.sneia.fractional 

		Example Code 
		------------
		>>> from vice.yields.sneia import seitenzahl13 
		>>> seitenzahl13.set_params(n = 1.5e-03) 

		.. seealso:: 
			- vice.yields.sneia.fractional 
			- vice.yields.sneia.single 

		.. [1] Seitenzahl et al. (2013), ApJ, 124, 439 
		"""
		if "study" in kwargs.keys(): 
			raise TypeError("Got an unexpected keyword argument 'study'") 
		else: 
			for i in _RECOGNIZED_ELEMENTS_: 
				__settings[i] = __fractional(i, study = "seitenzahl13", 
					**kwargs) 

	set_params() 

else: 
	pass 
