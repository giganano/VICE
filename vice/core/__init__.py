r"""
VICE Core
=========
Provides all galactic chemical evolution simulations and dataframe features

.. warning:: The contents of this module are imported directly to vice.*. For
	example, the ``singlezone`` class should be accessed via ``vice.singlezone``
	rather than ``vice.core.singlezone``. Accessing the VICE core directly is
	discouraged.
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:
	__all__ = [
		"dataframe",
		"singlezone",
		"mirror",
		"mlr",
		"test"
	]

	import warnings
	from .singlezone import singlezone
	from .mirror import mirror
	from .mlr import mlr
	from . import multizone
	__all__.extend(multizone.__all__)
	from .multizone import *
	from .ssp import *
	from .dataframe import *
	from .dataframe._builtin_dataframes import *
	from .outputs import *
	__all__.extend(dataframe._builtin_dataframes.__all__)
	__all__.extend(outputs.__all__)
	__all__.extend(ssp.__all__)

	from ..testing import moduletest
	from .dataframe import test as test_dataframe
	from .multizone import test as test_multizone
	from .objects import test as test_objects
	from .outputs import test as test_outputs
	from .singlezone import test as test_singlezone
	from .ssp import test as test_ssp
	from . import tests

	@moduletest
	def test():
		return ["vice.core",
			[
				test_dataframe(run = False),
				test_multizone(run = False),
				test_objects(run = False),
				test_outputs(run = False),
				test_singlezone(run = False),
				test_ssp(run = False),
				tests.test(run = False)
			]
		]

else:
	pass
