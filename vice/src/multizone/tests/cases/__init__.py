
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from .....testing import moduletest
	from ._generic import generic_test
	from ._no_migration import no_migration_test
	from ._separation import separation_test
	from .bifurcation import bifurcation_test

	@moduletest
	def test():
		r"""
		vice.core.multizone edge cases module test
		"""
		# Sometimes Linux leaves behind .nfs files in the various zoneN.vice
		# output sub-directories associated with each output. If this happens,
		# the bifurcation test fails to run because the output reader thinks
		# it needs to read in beyond the second zone given the presence of,
		# e.g., a zone2.vice output directory, even though only 2 zones
		# (zone0 and zone1) are used in that test. To prevent this from
		# happening, simply run the bifurcation test first.
		return ["vice.core.multizone edge cases",
			[
				bifurcation_test(run = False),
				generic_test(run = False),
				no_migration_test(run = False),
				separation_test(run = False),
			]
		]

else:
	pass
