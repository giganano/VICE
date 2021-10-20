r"""
The VICE dataframe
==================
Provides a means of storing and accessing data with both case-insensitive
strings and integers, allowing both indexing and calling.

Derived Classes:
	- agb_yield_settings
	- ccsn_yield_table
	- elemental_settings
	- channel_entrainment
	- evolutionary_settings
	- fromfile
	- history
	- noncustomizable
	- saved_yields
	- tracers
	- yield_settings

Built-in Instances:
	- atomic_number
	- primordial
	- solar_z
	- sources
	- stable_isotopes
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = [
		"agb_yield_settings",
		"base",
		"ccsn_yield_table",
		"channel_entrainment",
		"elemental_settings",
		"evolutionary_settings",
		"fromfile",
		"history",
		"noncustomizable",
		"saved_yields",
		"tracers",
		"yield_settings",
		"test"
	]

	from ...testing import moduletest
	from ._agb_yield_settings import agb_yield_settings
	from ._base import base
	from ._ccsn_yield_table import ccsn_yield_table
	from ._entrainment import channel_entrainment
	from ._elemental_settings import elemental_settings
	from ._evolutionary_settings import evolutionary_settings
	from ._fromfile import fromfile
	from ._history import history
	from ._noncustomizable import noncustomizable
	from ._saved_yields import saved_yields
	from ._tracers import tracers
	from ._yield_settings import yield_settings
	from ._builtin_dataframes import *
	from . import tests
	__all__.extend(_builtin_dataframes.__all__)

	@moduletest
	def test():
		r"""
		Run the tests on this module
		"""
		return ["vice.core.dataframe",
			[
				tests.test(run = False),
				_builtin_dataframes.test(run = False)
			]
		]

else:
	pass

