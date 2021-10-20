
from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = ["test"]
	from ....testing import moduletest
	from .from_output import test_from_output
	from . import mig_matrix_row
	from . import mig_matrix
	from . import mig_specs
	from . import zone_array
	from . import _multizone
	from ....src.multizone.tests import test as src_test

	@moduletest
	def test():
		r"""
		vice.multizone module test
		"""
		return ["vice.multizone",
			[
				test_from_output(),
				mig_matrix_row.test(run = False),
				mig_matrix.test(run = False),
				mig_specs.test(run = False),
				zone_array.test(run = False),
				_multizone.test(run = False),
				src_test(run = False)
			]
		]

else:
	pass
