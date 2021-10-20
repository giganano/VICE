
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from .....testing import moduletest
	from ._quiescence import tau_star_inf
	from ._max_age_ssp import single_max_age_ssp
	from ._zero_age_ssp import single_zero_age_ssp


	@moduletest
	def test():
		r"""
		vice.core.singlezone edge cases
		"""
		return ["vice.core.singlezone edge cases",
			[
				tau_star_inf(run = False),
				single_max_age_ssp(run = False),
				single_zero_age_ssp(run = False)
			]
		]

else:
	pass
