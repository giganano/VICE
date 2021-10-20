
from __future__ import absolute_import
import os

try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False

if __VICE_SETUP__:

	__all__ = ["find_c_extensions"]
	from .._build_utils.c_extensions import _CFILES_

	def find_c_extensions(name):
		r"""
		Finds the paths to the C extensions required for the specified
		extension based on the _CFILES_ mapping in
		vice/_build_utils/c_extensions.py.

		Parameters
		----------
		name : str
			The name of the extension to compile.

		Returns
		-------
		exts : list
			A list of the relative paths to all C extensions.

		Notes
		-----
		If the extension does not have an entry in the _CFILES_ dictionary,
		VICE will compile the extension with ALL C files in it's C library,
		omitting those under a directory named "tests" if "tests" is not in the
		name of the extension.
		"""
		extensions = []
		if name in _CFILES_.keys():
			for item in _CFILES_[name]:
				if os.path.exists(item) and item.endswith(".c"):
					extensions.append(item)
				elif os.path.isdir(item):
					for i in os.listdir(item):
						if i.endswith(".c"): extensions.append("%s/%s" % (
							item, i))
				else:
					raise SystemError("""Internal Error. Invalid C Extension \
listing for extension %s: %s""" % (name, item))
		else:
			path = os.path.dirname(os.path.abspath(__file__))
			for root, dirs, files in os.walk(path):
				for i in files:
					if i.endswith(".c"):
						if "tests" in root and "tests" not in name:
							continue
						else:
							extensions.append(
								("%s/%s" % (root, i)).replace(os.getcwd(), '.')
							)
					else: pass
		
		return extensions

else:
	
	__all__ = [
		"callback",
		"imf",
		"io",
		"stats",
		"test",
		"utils"
	]
	from ..testing import moduletest
	from . import io
	from .tests import callback
	from .tests import imf
	from .tests import stats
	from .tests import utils

	@moduletest
	def test():
		r"""
		vice.src module test
		"""
		return ["vice.src",
			[
				callback.test(run = False),
				imf.test(run = False),
				io.test(run = False),
				stats.test(run = False),
				utils.test(run = False)
			]
		]

