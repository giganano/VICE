"""
This file handles testing of the pickled_object and jar classes implemented in
vice/core/pickles.py
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...testing import moduletest
from ...testing import unittest
from ..pickles import pickled_object
from ..pickles import jar
import pickle
import os


@moduletest
def test():
	"""
	Run the tests on this module
	"""
	test1 = pickled_object_tester("test", name = "test", default = None)
	test2 = jar_tester({
		"a": 		3,
		"b": 		"string",
		"c": 		list(range(10))
	}, name = "test", default = None)
	return ["vice.core.pickles",
		[
			test1.test_save(),
			test1.test_from_pickle(),
			test2.test_close(),
			test2.test_open()
		]
	]


class jar_tester(jar):

	"""
	A class designed to test the jar class.
	"""
	def __init__(self, objects, name = "objects", default = None):
		super().__init__(objects, name = name, default = default)


	@unittest
	def test_close(self):
		"""
		Tests the close() function of the jar class
		"""
		def test():
			"""
			Returns True on success and False on failure
			"""
			try:
				self.close()
			except:
				os.system("rm -rf %s" % (self._name))
				return False

			x = True
			for i in self._objects.keys():
				if os.path.exists("%s/%s.obj" % (self._name, i)):
					if (pickle.load(open("%s/%s.obj" % (self._name, i), "rb"))
						== self._objects[i]):
						continue
					else:
						x = False
						break
				else:
					x = False
					break

			os.system("rm -rf %s" % (self._name))
			return x

		return ["vice.core.pickles.jar.close", test]


	@unittest
	def test_open(self):
		"""
		Tests the open() function of the jar class
		"""
		def test():
			"""
			Returns True on success and False on failure
			"""
			test_ = {
				"a": 		3,
				"b": 		"string",
				"c": 		list(range(10))
			}

			if os.path.exists(self._name): os.system("rm -rf %s" % (self._name))
			os.system("mkdir %s" % (self._name))
			for i in test_.keys():
				pickle.dump(test_[i], open("%s/%s.obj" % (self._name, i), "wb"))

			try:
				copy = self.open(self._name)
				assert copy == test_
			except:
				return False
			finally:
				os.system("rm -rf %s" % (self._name))

			return True

		return ["vice.core.pickles.jar.open", test]


class pickled_object_tester(pickled_object):

	"""
	A class designed to test the pickled_object class.
	"""

	def __init__(self, obj, name = "object", default = None):
		super().__init__(obj, name = name, default = default)


	@unittest
	def test_save(self):
		"""
		Test the save function of the pickled_object class.
		"""
		def test():
			"""
			Returns True on success, False on failure
			"""
			filename = "%s.obj" % (self._name)
			try:
				self.save()
				assert pickle.load(open(filename, "rb")) == self._obj
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			self._obj = 3
			try:
				self.save()
				assert pickle.load(open(filename, "rb")) == 3
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			self._obj = "string"
			try:
				self.save()
				assert pickle.load(open(filename, "rb")) == "string"
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			self._obj = list(range(10))
			try:
				self.save()
				assert pickle.load(open(filename, "rb")) == list(range(10))
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			return True

		return ["vice.core.pickles.pickled_object.save", test]


	@unittest
	def test_from_pickle(self):
		"""
		Test the from_pickle function of the pickled_object class.
		"""
		def test():
			"""
			Returns True on success, False on failure
			"""
			filename = "%s.obj" % (self._name)
			pickle.dump(3, open(filename, "wb"))
			try:
				assert self.from_pickle(filename) == 3
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			pickle.dump("string", open(filename, "wb"))
			try:
				assert self.from_pickle(filename) == "string"
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			pickle.dump(list(range(10)), open(filename, "wb"))
			try:
				assert self.from_pickle(filename) == list(range(10))
			except:
				return False
			finally:
				os.system("rm -f %s" % (filename))

			return True

		return ["vice.core.pickles.pickled_object.from_pickle", test]

