"""
VICE Pickle Utility Functions
=============================

.. warning:: User access of these routines is discouraged.

Handles pickling of ``singlezone`` and ``multizone`` object attributes. These
objects themselves are not pickles, because there is always at least one
functional attribute. Encoding functional attributes requires dill_, a
*secondary* dependence of VICE which is an extension to ``pickle`` in the
python standard library. It is recommended that VICE user's install dill_ >=
0.2.0.

.. _dill: https://pypi.org/project/dill/
"""

from __future__ import absolute_import
from .._globals import _VERSION_ERROR_
import warnings
import pickle
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	"""
	Let dill masquerade as pickle, because dill.dump must be called when
	functional attributes are included.
	"""
	import dill as pickle
except (ModuleNotFoundError, ImportError):
	pass 	# working without dill


class jar:

	r"""
	A directory of pickled objects (i.e. a pickle jar). Serves as the engine
	for saving the attributes of singlezone and multizone objects after
	simulation and in reading them back in thereafter.

	.. warning:: User access of this class is discouraged.

	Parameters
	----------
	objects : ``dict``
		The attribute ``objects``, initialized via keyword argument.
	name : ``str`` [default : "objects"]
		The attribute ``name``, initialized via keyword argument.
	default : ``object`` [default : None]
		The value to assume in the case that an object can't be pickled.
		This will be the case if the object is a function and the user does
		not have dill_ installed.

	.. _dill: https://pypi.org/project/dill/

	Attributes
	----------
	objects : ``dict``
		The objects to pickle. The keys to this dictionary will serve as the
		names of these attributes.
	name : ``str`` [default : "objects"]
		The name of the directory to save pickles in.

	Functions
	---------
	- close : Save pickles
	- open [staticmethod] : Load pickles from a directory
	"""

	def __init__(self, objects, name = "objects", default = None):
		if isinstance(objects, dict):
			if all(map(lambda x: isinstance(x, strcomp), objects.keys())):
				self._objects = objects
			else:
				raise TypeError("All keys must be of type str.")
		else:
			raise TypeError("Must be of type dict. Got: %s" % (type(objects)))
		self.name = name
		self._default = default

	@property
	def objects(self):
		r"""
		Type : ``dict``

		.. warning:: User access of this attribute is discouraged.

		The objects to put in a pickle jar. The keys of this dictionary will
		be taken as the names of the objects.
		"""
		return self._objects

	@property
	def name(self):
		r"""
		Type : ``str``

		.. warning:: User access of this attribute is discouraged.

		The name of the directory to put a pickle jar in.
		"""
		return self._name

	@name.setter
	def name(self, value):
		if isinstance(value, strcomp):
			self._name = value
		else:
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(name)))

	def close(self):
		r"""
		Save all of the attributes of this class as pickles in a directory
		under the name <self.name> (i.e. "close the jar").

		.. warning:: User access of this function is discouraged.

		**Signature**: x.close()

		Parameters
		----------
		x : ``jar``
			An instance of this class
		"""
		if os.path.exists(self.name): os.system("rm -rf %s" % (self.name))
		os.system("mkdir %s" % (self.name))
		old_path = os.getcwd()
		os.chdir(self.name)
		for i in self.objects.keys():
			# dill will taken care of down the line
			pickled_object(self.objects[i], name = i,
				default = self._default).save()
		os.chdir(old_path)

	@staticmethod
	def open(dirname):
		r"""
		Obtain a dictionary of all of the values stored in a pickle jar
		(i.e. open the jar).

		.. warning:: User access of this function is discouraged.

		**Signature**: vice.core.pickles.jar.open(dirname)

		Parameters
		----------
		dirname : ``str``
			The name of the directory storing pickled objects. Only files with
			a ".obj" extension will be included.

		Returns
		-------
		objects : ``dict``
			All unpickled objects with a ".obj" extension inside the specified
			directory.

		Raises
		------
		* TypeError
			- dirname is not of type str
		* IOError
			- dirname does not exist, or is not a directory
			- No pickled objects found in that directory

		.. note:: Other errors may be raised by pickled_object.from_pickle.
		"""
		if isinstance(dirname, strcomp):
			if os.path.isdir(dirname):
				old_path = os.getcwd()
				os.chdir(dirname)
				pickles = list(filter(lambda x: x.endswith(".obj"),
					os.listdir('.')))
				if len(pickles) > 0:
					names = [i[:-4] for i in pickles]
					objects = [pickled_object.from_pickle(i) for i in pickles]
					os.chdir(old_path)
					return dict(zip(names, objects))
				else:
					os.chdir(old_path)
					raise IOError("No pickled objects found in directory: %s" % (
						dirname))
			else:
				raise IOError("Not a directory: %s" % (dirname))
		else:
			raise TypeError("Must be of type str. Got: %s" % (type(dirname)))


class pickled_object:

	r"""
	An object which is to be pickled. Along with ``jar``, this class serves
	as the engine for saving attributes of the ``singlezone`` and ``multizone``
	objects after simulation and in reading them back in thereafter.

	.. warning:: User access of this class is discouraged.

	Parameters
	----------
	obj : ``object``
		The attribute ``obj``, initialized via keyword argument.
	name : ``str`` [default : "object"]
		The attribute ``name``, initialized via keyword argument.
	default : ``object`` [default : None]
		The value to assume in the event that the object cannot be pickled.
		This will be the case if the object is a function and the user does
		not have dill_ installed.

	.. _dill: https://pypi.org/project/dill/

	Attributes
	----------
	obj : ``object``
		The object to pickle.
	name : ``str`` [default : "object"]
		The name of the object. A file will be created at <name>.obj
		containing the pickled object.

	Functions
	---------
	- save : Save the object
	- from_pickle [staticmethod] : Load an object from a pickle.
	"""

	def __init__(self, obj, name = "object", default = None):
		self._obj = obj
		self.name = name
		self._default = default

	@property
	def obj(self):
		r"""
		Type : any

		.. warning:: User access of this attribute is discouraged.

		The object to pickle.
		"""
		return self._obj

	@property
	def name(self):
		r"""
		Type : str

		.. warning:: User access of this attribute is discouraged.

		The name of the object. When saved, a file at <name>.obj will be
		created.
		"""
		return self._name

	@name.setter
	def name(self, value):
		if isinstance(value, strcomp):
			self._name = value
		else:
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(value)))

	def save(self):
		r"""
		Save the object in a pickle.

		.. warning:: User access of this function is discouraged.

		**Signature**: x.save()

		Parameters
		----------
		x : ``pickled_object``
			An instance of this class.

		Raises
		------
		* UserWarning
			- 	The object is callable, and the user does not have dill
				installed. In this case, the default value (usually None) will
				be saved instead.
			- 	The object is not callable, but could still not be pickled.
				In this case a None will be pickled regardless of the default.

		Notes
		-----
		This will remove any file previously located at <self.name>.obj
		"""
		if os.path.exists("%s.obj" % (self.name)):
			os.system("rm -f %s.obj" % (self.name))
		else: pass
		file = open("%s.obj" % (self.name), "wb")
		if callable(self.obj):
			if "dill" in sys.modules:
				try:
					pickle.dump(self.obj, file)
				except:
					warnings.warn("""\
Could not pickle function. The following attribute will not be saved with \
this output: %s""" % (self.name), UserWarning)
					pickle.dump(None, file)
			else:
				warnings.warn("""\
Encoding functions along with VICE outputs requires the package dill \
(installable via pip). The following attribute will not be saved with this \
output: %s""" % (self.name), UserWarning)
				try:
					pickle.dump(self._default, file)
				except:
					pickle.dump(None, file)
		else:
			try:
				pickle.dump(self.obj, file)
			except:
				warnings.warn("""Could not save object %s with this VICE \
output.""" % (self.name), UserWarning)
				pickle.dump(None, file)
		file.close()

	@staticmethod
	def from_pickle(filename):
		r"""
		Obtain an object from its pickled version.

		.. warning:: User access of this function is discouraged.

		**Signature**: vice.core.pickles.pickled_object.from_pickle(filename)

		Parameters
		----------
		filename : ``str``
			The full or relative path to the pickled object.

		Returns
		-------
		obj : ``object``
			The object pickled in the file. If the pickled object was a
			function and the user does not have dill_ installed, this will be
			None.

		.. _dill: https://pypi.org/project/dill

		Raises
		------
		* TypeError
			- ``filename`` is not of type str
		* FileNotFoundError
			- ``filename`` does not exist
		* IOError
			- Could not unpickle the file
		"""
		if isinstance(filename, strcomp):
			if os.path.exists(filename):
				try:
					file = open(filename, "rb")
					obj = pickle.load(file)
					file.close()
					return obj
					# return pickle.load(open(filename, "rb"))
				except:
					raise IOError("Could not unpickle file: %s" % (filename))
			else:
				raise FileNotFoundError("File does not exist: %s" % (filename))
		else:
			raise TypeError("Must be of type str. Got: %s" % (type(filename)))

