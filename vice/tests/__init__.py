"""
VICE Tests
==========
This module includes all of VICE's internal testing routines. The tests are
implemented in a tree strucutre - all tests can be ran via the test()
function, or alternatively, individual modules are imported here, and
their tests can also be ran, by calling their associated test() function
"""

from __future__ import absolute_import
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if not __VICE_SETUP__:

	__all__ = [
		"core",
		"elements",
		"toolkit",
		"milkyway",
		"src",
		"yields",
		"test"
	]

	from ..testing import moduletest
	from . import elements
	from .. import core
	from ..milkyway import test as milkyway_test
	from .. import src
	from .. import toolkit
	from .. import yields
	import warnings
	import sys
	import os
	if sys.version_info[:2] == (2, 7): input = raw_input

	@moduletest
	def test():
		r"""
		Runs VICE's unit tests

		.. note:: Calling this function will cause warning messages to get
			suppressed.
		"""
		if "test.vice" in os.listdir(os.getcwd()):
			answer = input("""\
This program will overwrite the VICE output at %s/test.vice. Proceed? \
(y | n) """ % (os.getcwd()))
			while answer.lower() not in ["yes", "y", "no", "n"]:
				answer = input("Please enter either 'y' or 'n': ")
			if answer.lower() in ["yes", "y"]:
				os.system("rm -rf %s/test.vice" % (os.getcwd()))
			else:
				raise RuntimeError("Cancelling tests, ignore this error.")
		else: pass
		
		header = "VICE Comprehensive Tests\n"
		for i in range(len(header) - 1):
			header += "="
		print("\033[091m%s\033[00m" % (header))
		print("This may take a few minutes.")
		warnings.filterwarnings("ignore")
		return ["",
			[
				core.test(run = False),
				elements.test(run = False),
				toolkit.test(run = False),
				milkyway_test(run = False),
				src.test(run = False),
				yields.test(run = False)
			]
		]

else:
	pass
