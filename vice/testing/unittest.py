r"""
**VICE Developer's Documentation**

This file implements an object used for unit testing. The decorators.py file
implements the decorator @unittest, which can be attached to a function that
returns a name of the unit test (a string) and another function which will be
called to determine the status of the test.
"""

from __future__ import absolute_import
__all__ = ["_unittest"]
from .._globals import _VERSION_ERROR_
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

# "Passed" and "Failed" as green and red strings, respectively
_PASSED_MESSAGE_ = "\033[92mPassed\033[00m"
_FAILED_MESSAGE_ = "\033[91mFailed\033[00m"
_SKIPPED_MESSAGE_ = "\033[94mSkipped\033[00m"


class _unittest:

	r"""
	**VICE Developer's Documentation**

	The base class used for unit testing in VICE. Simply print the unit test
	or type-cast it to a string and the success, failure, or skipped message
	will be determined and included with the string/output.

	**Signature**: unittest(name, function)

	Attributes & Parameters
	-----------------------
	name : ``str``
		The name of the unit test.
	function : <function>
		A function to call which will determine the status of the unit test.
		Must return True if the unit test passes, False if it fails, and None
		if it skips.

	Functions
	---------
	run : instance method
		Run the function which executes the unit test. ``self.run()`` is
		equivalent to ``self.function()``.
	"""

	def __init__(self, name, function):
		self.name = name
		self.function = function

	def __repr__(self):
		return "%s :: %s" % (self.name,
			{
				True: 		_PASSED_MESSAGE_,
				False: 		_FAILED_MESSAGE_,
				None: 		_SKIPPED_MESSAGE_
			}[self.run()])

	def __str__(self):
		return self.__repr__()

	@property
	def name(self):
		r"""
		**VICE Developer's Documentation**

		Type : ``str``

		The name of the test.
		"""
		return self._name

	@name.setter
	def name(self, value):
		if isinstance(value, strcomp):
			self._name = value
		else:
			raise TypeError("""Unit test attribute 'name' must be of type \
str. Got: %s""" % (type(value)))

	@property
	def function(self):
		r"""
		**VICE Developer's Documentation**

		Type : <function>

		The function to call to conduct the unit test. This must return True
		if the test passes, False if it fails, and None if it skips.
		"""
		return self._function

	@function.setter
	def function(self, value):
		if callable(value):
			self._function = value
		else:
			raise TypeError("Unit test function must be a callable object.")

	def run(self):
		r"""
		**VICE Developer's Documentation**

		Run this unit test.
		"""
		return self.function()

