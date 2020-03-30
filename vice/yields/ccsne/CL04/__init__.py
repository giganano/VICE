r"""
Chieffi & Limongi (2014), ApJ, 608, 405 core collapse supernova (CCSN) yields 

**Signature**: from vice.yields.ccsne import CL04 

Importing this module will automatically set the CCSN yield settings for all 
elements to the IMF-averaged yields calculated with the Chieffi & Limongi 
(2004) yield table for [M/H] = 0.15 stars. This will adopt an upper mass limit 
of 35 :math:`M_\odot`. 

.. tip:: By importing this module, the user does not sacrifice the ability to 
	specify their yield settings directly. 

.. note:: [M/H] = 0.15 corresponds to Z = 0.02 if the solar abundance is 
	Z = 0.014 (Asplund et al. 2009) [1]_. 

.. note:: This module is not imported with a simple "import vice" statement. 

Contents 
--------
set_params : <function> 
	Update the parameters with which the yields are calculated. 

.. [1] Asplund et al. (2009), ARA&A, 47, 481 
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
		__settings[i] = __fractional(i, study = "CL04", MoverH = 0.15, 
			m_upper = 35)[0] 

	def set_params(**kwargs): 
		r""" 
		Update the parameter with which the yields are calculated from the 
		Chieffi & limongi (2004) [1]_ data. 

		**Signature**: vice.yields.ccsne.CL04.set_params(\*\*kwargs) 

		Parameters 
		----------
		kwargs : varying types 
			Keyword arguments to pass to vice.yields.ccsne.fractional. 

		Raises 
		------
		* TypeError 
			 - Received a keyword argument "study". This will always be "CL04" 
				 when called from this module. 

		Other exceptions are raised by vice.yields.ccsne.fractional. 

		Example Code 
		------------
		>>> import vice 
		>>> from vice.yields.ccsne import CL04 
		>>> CL04.set_params(lower = 0.3, upper = 40, IMF = "salpeter") 

		.. seealso:: vice.yields.ccsne.fractional 

		.. [1] Chieffi & Limongi (2004), ApJ, 608, 405 
		""" 
		if "study" in kwargs.keys(): 
			raise TypeError("Got an unexpected keyword argument: 'study'") 
		else: 
			if "MoverH" not in kwargs.keys(): 
				# fractional will default to 0, override this 
				kwargs["MoverH"] = 0.15 
			else: 
				pass 
			for i in _RECOGNIZED_ELEMENTS_: 
				__settings[i] = __fractional(i, study = "CL04", **kwargs)[0] 

else: 
	pass 

