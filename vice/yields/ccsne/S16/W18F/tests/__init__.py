
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ......testing import moduletest
	from . import set_params

	@moduletest
	def test():
		r"""
		Run the unit tests on this module.
		"""
		return ["vice.yields.ccsne.S16.W18F",
			[
				set_params.test()
			]
		]

else:
	pass
