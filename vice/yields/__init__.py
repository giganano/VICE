r"""
Nucleosynthetic Yield Tools 
===========================
Each sub-package stores built-in yield tables and user-presets for each 
element from each enrichment channel. 

**Signature**: vice.yields 

Contains 
--------
agb : <package> 
	Yields from asymptotic giant branch stars 
ccsne : <package> 
	Yields from core collapse supernovae 
sneia : <package> 
	Yields from type Ia supernovae 
presets : <package> 
	Yield settings presets 
test : <function> 
	Run the tests on this package 
"""

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 

	__all__ = ["agb", "ccsne", "sneia", "presets", "test"] 
	from ..testing import moduletest 
	from . import agb 
	from . import ccsne 
	from . import sneia 
	from . import presets 
	from . import tests 

	@moduletest 
	def test(): 
		""" 
		Run the tests on this module 

		**Signature**: vice.yields.test() 
		""" 
		return ["vice.yields", 
			[
				agb.test(run = False), 
				ccsne.test(run = False), 
				sneia.test(run = False), 
				presets.test(run = False), 
				tests.test(run = False) 
			] 
		] 

else: 
	pass 

