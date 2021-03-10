r"""
Nucleosynthetic Yield Tools 

Each sub-package stores built-in yield tables and user-presets for each 
element from each enrichment channel. 

**Signature**: vice.yields 

Contains 
--------
agb : <module> 
	Yields from asymptotic giant branch stars 
ccsne : <module> 
	Yields from core collapse supernovae 
sneia : <module> 
	Yields from type Ia supernovae 
presets : <module> 
	Yield settings presets 
test : <function> 
	Run the tests on this package 

Notes 
-----
The yield tables built into VICE include a treatment for only two radioactive 
isotopes. The mass of nickel-56 in all cases is added to the iron-56 yield, and 
the mass of aluminum-26 is added to the magnesium-26 yield always. VICE does 
not include a treatment for other radioactive isotopes; equations are evaluated 
and tables returned couting only the total mass yield of stable isotopes. In 
the case of other elements with a significant nucleosynthetic contribution from 
radioactive decay products, the values returned from the functions in this 
module should be interpreted as lower bounds rather than estimates of the true 
yield. 
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
		r""" 
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

