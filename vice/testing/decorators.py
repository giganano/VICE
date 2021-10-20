r"""
**VICE Developer's Documentation**

This file implements the @unittest and @moduletest decorators for testing.
"""

from __future__ import absolute_import
__all__ = ["moduletest", "unittest"]
from .moduletest import _moduletest
from .unittest import _unittest
import functools
import inspect


def moduletest(function):
	r"""
	**VICE Developer's Documentation**

	Usage
	-----
	Place this decorator atop a function which returns the following objects:

	name : ``str``
		The name of the moduletest
	tests : ``list``
		A list containing the ``unittest`` objects and other ``moduletest``
		objects contained within the module test.

	.. tip:: The ``unittest`` and ``moduletest`` objects are simplest obtained
		by calling functions with the ``@unittest`` and ``@modultest``
		decorators applied.

	Example
	-------
	@moduletest
	def example():
		return ["example moduletest's name",
			[
				unittest_func_1(),
				unittest_func_2(),
				other_moduletest_1(),
				other_moduletest_2()
			]
		]

	In the above example, ``unittest_func_1()`` and ``unittest_func_2()`` have
	the ``@unittest`` decorator applied, while ``other_moduletest_1()`` and
	``other_moduletest_2()`` also have the ``@moduletest`` decorator applied.
	"""
	@functools.wraps(function)
	def wrapper(run = True, outfile = None):
		try:
			description, unittests = function()
		except TypeError:
			print(inspect.getfile(function))
			print(function)
			raise
		# Let the moduletest object do the error handling
		test = _moduletest(description)
		if unittests is None:
			test.new(skip_dummy(description))
		else:
			for i in unittests:
				test.new(i)
		if run:
			test.run(print_results = True, outfile = outfile)
		else:
			return test
	return wrapper


def unittest(function):
	r"""
	**VICE Developer's Documentation**

	A decorator which will construct a unittest automatically from a
	description and a function which runs the test

	Usage
	-----
	Place this decorator atop a function which returns the following objects:

	name : ``str``
		The name of the unit test.
	function : <function>
		A function to call which will run the unit test and return True if it
		passes, False if it fails, and None if it skips.

	Example
	-------
	@unittest
	def example():
		def test():
			result = True
			# Run the test, switching result to False if some condition is
			# not met.
			return result
		return ["example unit test", test]
	"""
	@functools.wraps(function)
	def wrapper(*args):
		"""
		Some unittests are for objects, and will require a call to self as the
		first argument
		"""
		# Let the unittest object do the error handling.
		description, testfunc = function(*args)
		return _unittest(description, testfunc)
	return wrapper


@unittest
def skip_dummy(description):
	r"""
	**VICE Developer's Documentation**

	Produces a skip message for an entire module test if the whole thing needs
	skipped.

	Parameters
	----------
	description : ``str``
		The name of module test.
	"""
	def test():
		return None
	return [description, test]

