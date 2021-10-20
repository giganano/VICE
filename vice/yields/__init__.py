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
All yields built into VICE reflect stable isotopes *only*. The built-in tables
reflect data which assume all important radioactive nuclides have fully
decayed. Further details can be found in the ``agb``, ``ccsne``, and ``sneia``
modules and in the journal publications in which the data were originally
published.
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

