
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from . import output
	from .history import test_history
	from .mdf import test_mdf
	from .stars import test_stars
	from .multioutput import test_multioutput

	@moduletest
	def test():
		r"""
		vice.outputs moduletest
		"""
		return ["vice.core.outputs",
			[
				output.test(run = False),
				test_history(),
				test_mdf(),
				test_stars(),
				test_multioutput()
			]
		]

else:
	pass

