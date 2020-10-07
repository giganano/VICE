r"""
Limongi & Chieffi (2018), ApJS, 237, 13 core collapse supernova (CCSN) yields 

**Signature**: from vice.yields.ccsne import LC18 

Importing this module will automatically set the CCSN yield settings for all 
elements to the IMF-averaged yields calculated with the Limongi & Chieffi 
(2018) yield table for [M/H] = 0 stars. This will adopt an upper mass limit of 
100 :math:`M_\odot`. 

.. tip:: By importing this module, the user does not sacrifice the ability to 
	specify their yield settings directly. 

.. note:: This module is not imported with a simple ``import vice`` statement. 

Contents 
--------
set_params : <function> 
	Update the parameters with which the yields are calculated 
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
		Limongi & Chieffi (2018) [1]_ data. 

		**Signature**: vice.yields.ccsne.LC18.set_params(\*\*kwargs) 

		Parameters 
		----------
		kwargs : varying types 
			Keyword arguments to pass to vice.yields.ccsne.fractional. 

		Raises 
		------
		* TypeError 
			- 	Received a keyword argument "study". This will always be "LC18" 
				when called from this module. 

		Other exceptions are raised by vice.yields.ccsne.fractional. 

		Example Code 
		------------
		>>> import vice 
		>>> from vice.yields.ccsne import LC18 
		>>> LC18.set_params(m_lower = 0.3, m_upper = 40, IMF = "salpeter") 

		.. seealso:: vice.yields.ccsne.fractional 

		.. [1] Limongi & Chieffi (2018), ApJS, 237, 17 
		"""
		if "study" in kwargs.keys(): 
			raise TypeError("Got an unexpected keyword argument: 'study'") 
		else: 
			for i in range(len(_RECOGNIZED_ELEMENTS_)): 
				__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(
					_RECOGNIZED_ELEMENTS_[i], study = "LC18", **kwargs)[0] 

	set_params() 

else: pass 

